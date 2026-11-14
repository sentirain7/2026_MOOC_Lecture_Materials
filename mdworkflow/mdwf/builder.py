"""③ 셀: 조성(분자별 개수) → 초기 밀도로 상자 길이 역산 → Packmol 배치 → 품질 게이트 → LAMMPS data.

넣는 것: --comp 이름=개수,…  (또는 --sara S,A,R,As wt% → 12분자 개수 역산 · W11 과 같은 규칙)
나오는 것: ws/cells/<id>/system.data · packmol.inp · packmol.log · cell.json(조성 · 원자 수 · 상자 · 게이트)
틀리기 쉬운 곳: 초기 밀도를 너무 높게(Packmol 실패) · 분자마다 같은 타입 이름에 다른 수치(합칠 때 섞임) · 전하 합 ≠ 0
확인(자동): Packmol 'Success!' · 분자간 최소 거리 ≥ 0.9 × tolerance · 원자 수 일치 · 같은 타입 이름 = 같은 ε · σ · 전하 합 ≈ 0
"""
import argparse, json, math, shutil
from collections import OrderedDict
from pathlib import Path
import numpy as np
from .common import workspace, need, run, dump, NA, MASS, DATA

SARA = ("saturate", "aromatic", "resin", "asphaltene")


def load_ff(ws, name):
    p = ws / "ff" / f"{name}_gaff2.json"
    if not p.exists():
        raise SystemExit(f"{p.name} 없음 · 먼저 ② 힘장: python mdwf.py ff {name}")
    return json.loads(p.read_text())


def sara_to_counts(sara_wt, ws, total_atoms=3000, ref="AAA1"):
    """SARA wt%(합 100) → 12분자 개수. 분획 안의 분자 비율 = Li & Greenfield AAA-1 표 개수 비율 · 반올림 뒤 ±1 탐욕 조정."""
    comp = json.loads((DATA / "compositions_LG2014.json").read_text())[ref]["counts"]
    from .common import molecules
    lib = molecules(); ffs = {n: load_ff(ws, n) for n in comp}
    MW = {n: ffs[n]["MW"] or sum(MASS[a["element"]] for a in ffs[n]["atoms"]) for n in comp}
    nat = {n: len(ffs[n]["atoms"]) for n in comp}
    frac = {s: {n: c for n, c in comp.items() if lib[n]["sara"] == s} for s in SARA}
    tgt = dict(zip(SARA, [x / sum(sara_wt) for x in sara_wt]))

    def wt(cnt):
        tot = sum(cnt[n] * MW[n] for n in cnt); return {s: sum(cnt[n] * MW[n] for n in frac[s]) / tot for s in SARA}

    def counts(total_mass):
        cnt = {}
        for s, mem in frac.items():
            k = tgt[s] * total_mass / sum(r * MW[n] for n, r in mem.items())
            for n, r in mem.items(): cnt[n] = round(k * r)
            if tgt[s] > 0 and sum(cnt[n] for n in mem) == 0: cnt[max(mem, key=mem.get)] = 1
        err = lambda c: sum(abs(wt(c)[s] - tgt[s]) for s in SARA)
        for _ in range(300):
            best = (err(cnt), None)
            for n in sorted(cnt):
                for d in (1, -1):
                    if cnt[n] + d < 0: continue
                    c2 = dict(cnt); c2[n] += d
                    if sum(c2.values()) == 0: continue
                    e = err(c2)
                    if e < best[0] - 1e-12: best = (e, (n, d))
            if best[1] is None: break
            cnt[best[1][0]] += best[1][1]
        return cnt
    m = 2000.0; cnt = counts(m)
    while sum(cnt[n] * nat[n] for n in cnt) < total_atoms: m *= 1.05; cnt = counts(m)
    w = wt(cnt)
    return {n: c for n, c in cnt.items() if c > 0}, {s: round(w[s] * 100, 2) for s in SARA}


def packmol(ws, cell, comp, ffs, L, tol, seed, margin=1.0):
    need("packmol")
    lines = [f"tolerance {tol}", "filetype pdb", "output packed.pdb", f"seed {seed}", ""]
    for n, c in comp.items():
        pdb = cell / f"{n}.pdb"
        with open(pdb, "w") as f:
            for a in ffs[n]["atoms"]:
                x, y, z = a["xyz"]; el = a["element"]
                f.write(f"HETATM{a['index']:5d} {el + str(a['index'] % 1000):<4s} MOL A   1    {x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00          {el:>2s}\n")
            f.write("END\n")
        lines += [f"structure {n}.pdb", f"  number {c}", f"  inside box {margin} {margin} {margin} {L - margin:.3f} {L - margin:.3f} {L - margin:.3f}", "end structure", ""]
    (cell / "packmol.inp").write_text("\n".join(lines))
    try:
        run(["packmol"], cell, cell / "packmol.log", stdin=cell / "packmol.inp")
    except SystemExit:
        pass
    log = (cell / "packmol.log").read_text(errors="replace")
    xyz = []
    if (cell / "packed.pdb").exists():
        for l in (cell / "packed.pdb").read_text().splitlines():
            if l.startswith(("ATOM", "HETATM")): xyz.append((float(l[30:38]), float(l[38:46]), float(l[46:54])))
    return "Success!" in log, np.array(xyz)


def min_inter(xyz, molid, L):
    """분자간 최소 거리(주기 경계 포함) · 격자 칸으로 나눠 가까운 쌍만 본다."""
    from scipy.spatial import cKDTree
    t = cKDTree(np.mod(xyz, L), boxsize=L)
    pairs = t.query_pairs(4.0, output_type="ndarray")
    if len(pairs) == 0: return 4.0
    inter = pairs[molid[pairs[:, 0]] != molid[pairs[:, 1]]]
    if len(inter) == 0: return 4.0
    d = np.mod(xyz[inter[:, 0]] - xyz[inter[:, 1]] + L / 2, L) - L / 2
    return float(np.sqrt((d ** 2).sum(1)).min())


def write_data(path, comp, ffs, xyz, L, title):
    # 타입 합치기: 원자 타입 = 이름 · 결합/각/이면각/비정규 = (타입 열 + 수치) 같으면 같은 번호
    at, am = OrderedDict(), {}
    for n in comp:
        for a in ffs[n]["atoms"]:
            k = a["ff_type"]; prm = (round(a["epsilon"], 5), round(a["sigma"], 5))
            if k in at and at[k] != prm: raise SystemExit(f"타입 {k} 의 ε · σ 가 분자마다 다름: {at[k]} ≠ {prm}")
            at[k] = prm; am[k] = MASS[a["element"]]
    tid = {k: i + 1 for i, k in enumerate(at)}
    tabs = {}
    for kind, prmf in (("bond", lambda t: (t["k"], t["r0"])), ("angle", lambda t: (t["k"], t["theta0"])),
                       ("dihedral", lambda t: tuple(map(tuple, t["terms"]))), ("improper", lambda t: (t["K"], t["d"], t["n"]))):
        tab = OrderedDict()
        for n in comp:
            for t in ffs[n][f"{kind}_types"]: tab.setdefault((t["key"], prmf(t)), len(tab) + 1)
        tabs[kind] = tab
    loc = {kind: {n: {t["id"]: tabs[kind][(t["key"], prmf(t))] for t in ffs[n][f"{kind}_types"]} for n in comp}
           for kind, prmf in (("bond", lambda t: (t["k"], t["r0"])), ("angle", lambda t: (t["k"], t["theta0"])),
                              ("dihedral", lambda t: tuple(map(tuple, t["terms"]))), ("improper", lambda t: (t["K"], t["d"], t["n"])))}
    atoms, inst = [], {"bond": [], "angle": [], "dihedral": [], "improper": []}
    off, mol, p = 0, 0, 0
    for n, c in comp.items():
        f = ffs[n]; na = len(f["atoms"])
        for _ in range(c):
            mol += 1
            for a in f["atoms"]:
                x, y, z = xyz[p]; p += 1
                atoms.append((off + a["index"], mol, tid[a["ff_type"]], a["charge"], x, y, z))
            for kind, key in (("bond", "bonds"), ("angle", "angles"), ("dihedral", "dihedrals"), ("improper", "impropers")):
                for row in f[key]: inst[kind].append([loc[kind][n][row[0]]] + [off + i for i in row[1:]])
            off += na
    qsum = sum(a[3] for a in atoms)
    with open(path, "w") as fh:
        fh.write(f"{title}\n\n{len(atoms)} atoms\n{len(inst['bond'])} bonds\n{len(inst['angle'])} angles\n{len(inst['dihedral'])} dihedrals\n{len(inst['improper'])} impropers\n\n")
        fh.write(f"{len(at)} atom types\n{len(tabs['bond'])} bond types\n{len(tabs['angle'])} angle types\n{len(tabs['dihedral'])} dihedral types\n{len(tabs['improper'])} improper types\n\n")
        fh.write(f"0.0 {L:.4f} xlo xhi\n0.0 {L:.4f} ylo yhi\n0.0 {L:.4f} zlo zhi\n\nMasses\n\n")
        for k in at: fh.write(f"{tid[k]} {am[k]:.4f}  # {k}\n")
        fh.write("\nPair Coeffs # lj/cut/coul/long\n\n")
        for k, (e, s) in at.items(): fh.write(f"{tid[k]} {e:.6f} {s:.6f}  # {k}\n")
        fh.write("\nBond Coeffs # harmonic\n\n")
        for (k, (K, r0)), i in tabs["bond"].items(): fh.write(f"{i} {K} {r0}  # {k}\n")
        fh.write("\nAngle Coeffs # harmonic\n\n")
        for (k, (K, th)), i in tabs["angle"].items(): fh.write(f"{i} {K} {th}  # {k}\n")
        fh.write("\nDihedral Coeffs # fourier\n\n")
        for (k, terms), i in tabs["dihedral"].items():
            fh.write(f"{i} {len(terms)} " + " ".join(f"{K} {n} {ph}" for K, n, ph in terms) + f"  # {k}\n")
        if tabs["improper"]:
            fh.write("\nImproper Coeffs # cvff\n\n")
            for (k, (K, d, n)), i in tabs["improper"].items(): fh.write(f"{i} {K} {d} {n}  # {k}\n")
        fh.write("\nAtoms # full\n\n")
        for a in atoms: fh.write(f"{a[0]} {a[1]} {a[2]} {a[3]:.6f} {a[4]:.4f} {a[5]:.4f} {a[6]:.4f}\n")
        for kind, title_ in (("bond", "Bonds"), ("angle", "Angles"), ("dihedral", "Dihedrals"), ("improper", "Impropers")):
            if inst[kind]:
                fh.write(f"\n{title_}\n\n")
                for j, r in enumerate(inst[kind], 1): fh.write(f"{j} " + " ".join(map(str, r)) + "\n")
    return {"atoms": len(atoms), "molecules": mol, "atom_types": len(at), "bond_types": len(tabs["bond"]), "angle_types": len(tabs["angle"]),
            "dihedral_types": len(tabs["dihedral"]), "improper_types": len(tabs["improper"]), "charge_sum": round(qsum, 5)}


def build(cid, comp, ws, rho0=0.5, tol=2.0, seed=1, sara_info=None):
    cell = ws / "cells" / cid; cell.mkdir(parents=True, exist_ok=True)
    ffs = {n: load_ff(ws, n) for n in comp}
    mass = sum(c * sum(MASS[a["element"]] for a in ffs[n]["atoms"]) for n, c in comp.items())
    L = (mass / NA / rho0 * 1e24) ** (1 / 3)
    molid = np.concatenate([np.full(len(ffs[n]["atoms"]), k) for k, (n, c) in enumerate((n, c) for n, c in comp.items() for _ in range(c))])
    gate = {}
    for attempt in range(3):
        ok, xyz = packmol(ws, cell, comp, ffs, L, tol, seed + attempt)
        n_ok = len(xyz) == len(molid)
        dmin = min_inter(xyz, molid, L) if n_ok else 0.0
        gate = {"attempt": attempt + 1, "seed": seed + attempt, "packmol_success": ok, "atom_count_ok": n_ok,
                "min_intermolecular_A": round(dmin, 3), "threshold_A": round(0.9 * tol, 3)}
        gate["pass"] = ok and n_ok and dmin >= 0.9 * tol
        if gate["pass"]: break
    if not gate["pass"]:
        dump({"id": cid, "comp": comp, "gate": gate}, cell / "cell.json")
        raise SystemExit(f"Packmol 게이트 실패 · {gate} · 초기 밀도(--rho0)를 낮추거나 tolerance 를 확인")
    info = write_data(cell / "system.data", comp, ffs, xyz, L, f"mdworkflow cell {cid} · GAFF2 + AM1-BCC")
    rep = OrderedDict(id=cid, comp=comp, sara=sara_info, mass_gmol=round(mass, 2), rho0=rho0, L_A=round(L, 3), tolerance=tol, gate=gate, data=info,
                      ff_files={n: f"ff/{n}_gaff2.json" for n in comp})
    rep["charge_ok"] = abs(info["charge_sum"]) < 0.01
    dump(rep, cell / "cell.json")
    return rep


def parse_comp(s):
    return OrderedDict((k, int(v)) for k, v in (x.split("=") for x in s.split(",")))


def main(argv=None):
    ap = argparse.ArgumentParser(description="셀 만들기 (MD 워크플로우 ③)")
    ap.add_argument("--id", required=True); ap.add_argument("--comp", help="이름=개수,…  예: Toluene=50")
    ap.add_argument("--sara", help="SARA wt%% 네 개 · 예: 11,33,44,12 → 12분자 개수 역산"); ap.add_argument("--atoms", type=int, default=3000)
    ap.add_argument("--rho0", type=float, default=0.5); ap.add_argument("--tol", type=float, default=2.0); ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--ws")
    a = ap.parse_args(argv); ws = workspace(a.ws)
    if a.sara:
        comp, actual = sara_to_counts([float(x) for x in a.sara.split(",")], ws, a.atoms)
        sara_info = {"target_wt": [float(x) for x in a.sara.split(",")], "actual_wt": actual}
    else:
        comp, sara_info = parse_comp(a.comp), None
    r = build(a.id, comp, ws, a.rho0, a.tol, a.seed, sara_info)
    print(f"셀 {a.id}: 분자 {r['data']['molecules']} · 원자 {r['data']['atoms']} · L {r['L_A']} Å (ρ0 {a.rho0}) · "
          f"최소 거리 {r['gate']['min_intermolecular_A']} Å · 전하 합 {r['data']['charge_sum']} · {'통과' if r['gate']['pass'] and r['charge_ok'] else '확인 필요'}")
    if sara_info: print("  SARA 목표", sara_info["target_wt"], "→ 실제", sara_info["actual_wt"], "· 개수", dict(comp))


if __name__ == "__main__":
    main()
