"""② 힘장: GAFF2 원자 타입 + AM1-BCC 전하 → 결합 · 각 · 이면각 매개변수 → 강좌 JSON.

순서 (AmberTools · 모두 이 파일이 대신 실행하고 로그를 ws/ff/<이름>/ 에 남긴다)
  1. antechamber -at gaff2 -c bcc : 원자마다 GAFF2 타입 · sqm(AM1) 계산 뒤 BCC 보정 전하
  2. parmchk2 -s gaff2           : gaff2.dat 에 없는 결합 · 각 · 이면각 조합을 비슷한 타입에서 빌려 frcmod 로
  3. tleap                       : 타입 + gaff2.dat + frcmod → 모든 결합 · 각 · 이면각 · 비정규 이면각에 수치를 붙인 prmtop
  4. parmed                      : prmtop 을 읽어 강좌 JSON 으로 (LAMMPS 형식: harmonic · fourier · cvff)
넣는 것: ws/mol/<이름>.mol (①)        나오는 것: ws/ff/<이름>_gaff2.json
틀리기 쉬운 곳: 형식전하(-nc)를 틀리게 줌 · parmchk2 가 빌린 값(ATTN)을 그대로 믿음 · 단위 변환(이면각 위상 · 1-4 축소)
확인(자동): 전하 합 = 형식전하 · 타입 빠짐(DU) 0 · ATTN 개수 기록 · 결합 · 각 · 이면각 개수가 prmtop 과 같음
"""
import argparse, json, math, os, re, time
from collections import OrderedDict
from pathlib import Path
from .common import workspace, molecules, need, run, dump

TLEAP = """source leaprc.gaff2
loadamberparams {name}.frcmod
m = loadmol2 {name}.mol2
check m
saveamberparm m {name}.prmtop {name}.inpcrd
quit
"""


def amber_steps(name, ws, charge, nthreads=1):
    d = ws / "ff" / name; d.mkdir(parents=True, exist_ok=True)
    src = ws / "mol" / f"{name}.mol"
    if not src.exists():
        raise SystemExit(f"{src} 없음 · 먼저 ① 분자: python mdwf.py mol {name}")
    (d / f"{name}.mol").write_text(src.read_text())
    need("antechamber"); need("parmchk2"); need("tleap")
    env = dict(os.environ, OMP_NUM_THREADS=str(nthreads))
    t = {}
    t["antechamber_s"] = run(["antechamber", "-i", f"{name}.mol", "-fi", "mdl", "-o", f"{name}.mol2", "-fo", "mol2",
                              "-at", "gaff2", "-c", "bcc", "-nc", str(charge), "-rn", "MOL", "-pf", "y", "-dr", "no"],
                             d, d / "antechamber.log", env=env)
    t["parmchk2_s"] = run(["parmchk2", "-i", f"{name}.mol2", "-f", "mol2", "-o", f"{name}.frcmod", "-s", "gaff2"], d, d / "parmchk2.log")
    (d / "tleap.in").write_text(TLEAP.format(name=name))
    t["tleap_s"] = run(["tleap", "-f", "tleap.in"], d, d / "tleap.log")
    return d, t


def to_json(name, d, info):
    import parmed
    s = parmed.load_file(str(d / f"{name}.prmtop"), str(d / f"{name}.inpcrd"))
    atoms = []
    for a in s.atoms:
        atoms.append(OrderedDict(index=a.idx + 1, element=a.element_name, ff_type=a.type, charge=round(a.charge, 6),
                                 epsilon=round(a.epsilon, 6), sigma=round(a.sigma, 6),
                                 xyz=[round(a.xx, 4), round(a.xy, 4), round(a.xz, 4)]))
    # 반올림 찌꺼기: 전하 합을 형식전하에 정확히 맞춘다(차이를 원자 수로 나눠 고르게 · 크기 기록)
    q0 = sum(a["charge"] for a in atoms); fix = (info.get("formal_charge", 0) - q0) / len(atoms)
    for a in atoms: a["charge"] = round(a["charge"] + fix, 6)
    T = lambda *ix: "-".join(s.atoms[i].type for i in ix)

    def canon(ix):  # 같은 결합을 양쪽 방향으로 두 번 세지 않도록 타입 열을 정렬된 방향으로
        k1, k2 = T(*ix), T(*ix[::-1])
        return (ix, k1) if k1 <= k2 else (ix[::-1], k2)

    bonds, btypes = [], OrderedDict()
    for b in s.bonds:
        ix, key = canon((b.atom1.idx, b.atom2.idx)); prm = (round(b.type.k, 4), round(b.type.req, 4))
        tk = btypes.setdefault((key, prm), f"b{len(btypes) + 1}"); bonds.append([tk] + [i + 1 for i in ix])
    angles, atypes = [], OrderedDict()
    for g in s.angles:
        ix, key = canon((g.atom1.idx, g.atom2.idx, g.atom3.idx)); prm = (round(g.type.k, 4), round(g.type.theteq, 4))
        tk = atypes.setdefault((key, prm), f"a{len(atypes) + 1}"); angles.append([tk] + [i + 1 for i in ix])
    # 이면각: Amber 는 같은 네 원자에 항(n)이 여러 개 → LAMMPS fourier 한 줄(m 항)로 묶는다
    prop, impr = OrderedDict(), []
    for t in s.dihedrals:
        ix = (t.atom1.idx, t.atom2.idx, t.atom3.idx, t.atom4.idx)
        terms = [(round(x.phi_k, 5), int(round(x.per)), round(x.phase, 3)) for x in (t.type if isinstance(t.type, parmed.DihedralTypeList) else [t.type])]
        if t.improper:
            impr.append((ix, terms))
        else:
            ix2, _ = canon(ix); prop.setdefault(ix2, []).extend(terms)
    dihedrals, dtypes = [], OrderedDict()
    for ix, terms in prop.items():
        terms = sorted(set(terms), key=lambda x: x[1]); prm = tuple(terms)
        tk = dtypes.setdefault((T(*ix), prm), f"d{len(dtypes) + 1}"); dihedrals.append([tk] + [i + 1 for i in ix])
    impropers, itypes = [], OrderedDict()
    for ix, terms in impr:
        K, n, ph = terms[0]
        prm = (K, -1 if abs(ph - 180) < 1 else 1, n)          # Amber K[1+cos(nφ−γ)] → cvff K[1+d·cos(nφ)] · γ 180° → d = −1
        tk = itypes.setdefault((T(*ix), prm), f"i{len(itypes) + 1}"); impropers.append([tk] + [i + 1 for i in ix])
    ff = OrderedDict(
        schema="mdwf-ff-1", mol_id=name, ff_family="gaff2", charge_model="am1_bcc", generator="mdworkflow forcefield.py (antechamber · parmchk2 · tleap · parmed)",
        smiles=info.get("smiles"), formal_charge=info.get("formal_charge", 0), MW=info.get("MW"),
        charge_sum=round(sum(a["charge"] for a in atoms), 6), charge_residual_fixed=round(q0 - info.get("formal_charge", 0), 6), styles={"pair": "lj/cut/coul/long", "bond": "harmonic", "angle": "harmonic",
                                                                     "dihedral": "fourier", "improper": "cvff", "special_bonds": "amber", "mixing": "arithmetic"},
        atoms=atoms,
        bond_types=[{"id": v, "key": k[0], "k": k[1][0], "r0": k[1][1]} for k, v in btypes.items()],
        angle_types=[{"id": v, "key": k[0], "k": k[1][0], "theta0": k[1][1]} for k, v in atypes.items()],
        dihedral_types=[{"id": v, "key": k[0], "terms": [list(x) for x in k[1]]} for k, v in dtypes.items()],
        improper_types=[{"id": v, "key": k[0], "K": k[1][0], "d": k[1][1], "n": k[1][2]} for k, v in itypes.items()],
        bonds=bonds, angles=angles, dihedrals=dihedrals, impropers=impropers)
    return ff, s


def checks(ff, d, s):
    frc = (d / f"{ff['mol_id']}.frcmod").read_text(errors="replace")
    attn = len(re.findall(r"ATTN", frc))
    types = {a["ff_type"] for a in ff["atoms"]}
    c = OrderedDict(
        charge_sum_ok=abs(ff["charge_sum"] - ff["formal_charge"]) < 1e-3,
        no_dummy_type=not any(t.upper().startswith("DU") for t in types),
        attn_borrowed=attn,
        counts={"atoms": len(ff["atoms"]), "bonds": len(ff["bonds"]), "angles": len(ff["angles"]), "dihedrals": len(ff["dihedrals"]), "impropers": len(ff["impropers"])},
        prmtop_counts={"bonds": len(s.bonds), "angles": len(s.angles)},
    )
    c["pass"] = c["charge_sum_ok"] and c["no_dummy_type"] and c["counts"]["bonds"] == c["prmtop_counts"]["bonds"] and c["counts"]["angles"] == c["prmtop_counts"]["angles"]
    return c


def make(name, ws, nthreads=1):
    info_p = ws / "mol" / f"{name}.json"
    info = json.loads(info_p.read_text()) if info_p.exists() else {}
    d, t = amber_steps(name, ws, info.get("formal_charge", 0), nthreads)
    ff, s = to_json(name, d, info)
    ff["checks"] = checks(ff, d, s); ff["timing_s"] = {k: round(v, 1) for k, v in t.items()}
    dump(ff, ws / "ff" / f"{name}_gaff2.json")
    return ff


def main(argv=None):
    ap = argparse.ArgumentParser(description="GAFF2 · AM1-BCC 힘장 만들기 (MD 워크플로우 ②)")
    ap.add_argument("names", nargs="*", help="비우면 ws/mol 에 있는 분자 전체"); ap.add_argument("--ws")
    ap.add_argument("--threads", type=int, default=1, help="sqm 계산 스레드")
    a = ap.parse_args(argv); ws = workspace(a.ws)
    names = a.names or sorted(p.stem for p in (ws / "mol").glob("*.mol"))
    for n in names:
        ff = make(n, ws, a.threads); c = ff["checks"]
        print(f"{n:12s} 원자 {c['counts']['atoms']:4d} · 타입 {len({x['ff_type'] for x in ff['atoms']}):2d} · 전하 합 {ff['charge_sum']:+.4f} · "
              f"빌린 값(ATTN) {c['attn_borrowed']} · 이면각 {c['counts']['dihedrals']} · {'통과' if c['pass'] else '확인 필요'} · "
              f"AM1-BCC {ff['timing_s']['antechamber_s']} s")


if __name__ == "__main__":
    main()
