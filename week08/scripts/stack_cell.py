#!/usr/bin/env python3
"""week08 — 3층 계면 셀: 석영 슬래브(ClayFF) | 물(SPC/E) | 톨루엔 바인더(GAFF2 + AM1-BCC) 를 z 로 쌓아 LAMMPS data · in 파일을 만든다.

층 (아래 → 위)                       출처
  ① 석영 슬래브  α-quartz 보정 단위셀(Levien 1980 · COMID crystal_builder UNIT_CELLS_CORRECTED) · a 4.913 c 5.405 Å
                 정확한 직교 초격자 A1 = p·a1 · A2 = q·(a1 + 2a2) (|A2| = q√3 a · COMID exact_hex_orthogonal_supercell)
                 ClayFF 전하 Si +2.1 · O −1.05 (Cygan 2004 · COMID inorganic_profiles silica) · LJ = week04/data/clayff_lj.csv
                 온 셀 단위 적층 → 화학량론 SiO₂ → 전하 중성 · 슬래브 전체 고정(fix setforce 0 · COMID 「whole-fixed」 레인)
  ② 물 층        SPC/E (Berendsen 1987) · O −0.8476 H +0.4238 · ε_O 0.1553 σ_O 3.166 · O–H 1.0 Å · 109.47°
                 분자 수 = 두께 × 단면적 × 0.0334 분자/Å³ (1 g/cm³ · COMID layer_builder._calculate_water_molecules)
  ③ 바인더 층    톨루엔 N 분자 · week06/data/Toluene_gaff2.json (COMID GAFF2 + AM1-BCC) · 초기 밀도 ρ0 0.2 g/cm³ (W06 규칙)
  ④ 진공층       z 방향 ≥ 30 Å (원본 04주차 #39) · boundary p p f · kspace_modify slab 3.0 (원본 04#41 · COMID)
in 파일 설정 = COMID ff_stack.py clayff_gaff2_v1: lj/cut/coul/long 12.0 · mix arithmetic · pppm 1.0e-4 · special_bonds lj 0 0 0.5 coul 0 0 0.833333

실행: python3 scripts/stack_cell.py [--p 5 --q 3 --nz 2] [--water 10] [--ntol 20] [--vac 30] [--packmol packmol] [--lmp lmp --steps 500]
출력: out/stack.data · out/in.stack · out/stack_summary.json · (lmp 실행 시) out/log.lammps · out/final.data · out/sideview.json
"""
import argparse, json, math, subprocess, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE.parent / "week06" / "scripts"))
from build_toluene_box import read_mol, build_topology  # noqa: E402  (W06 와 같은 함수)

OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
NA = 6.02214076e23
MASS = {"Si": 28.0855, "O": 15.999, "H": 1.008, "C": 12.011}
# α-quartz 보정 단위셀 (분율 좌표 · 육방 · COMID UNIT_CELLS_CORRECTED "levien1980_corrected")
QUARTZ = {"a": 4.913, "c": 5.405, "atoms": [("Si", 0.4697, 0.0000, 0.0000), ("Si", 0.0000, 0.4697, 0.6667), ("Si", 0.5303, 0.5303, 0.3333),
          ("O", 0.4135, 0.2669, 0.1191), ("O", 0.2669, 0.4135, 0.5476), ("O", 0.7331, 0.1466, 0.7858), ("O", 0.5865, 0.8534, 0.2142), ("O", 0.8534, 0.5865, 0.4524), ("O", 0.1466, 0.7331, 0.8809)]}
CLAYFF = {"Si": {"q": 2.1, "eps": 1.8405e-06, "sig": 3.302}, "O": {"q": -1.05, "eps": 0.1554, "sig": 3.166}}  # week04/data/clayff_lj.csv
SPCE = {"OW": {"q": -0.8476, "eps": 0.1553, "sig": 3.166, "el": "O"}, "HW": {"q": 0.4238, "eps": 0.0, "sig": 0.0, "el": "H"}, "rOH": 1.0, "theta": 109.47}
WATER_PER_A3 = 0.0334  # 1 g/cm³ (COMID layer_builder)


def quartz_slab(p, q, nz):
    """정확한 직교 초격자 (p·a, q·√3·a) × nz 셀 → (원소, x, y, z) 목록"""
    a, c = QUARTZ["a"], QUARTZ["c"]; Lx, Ly = p * a, q * math.sqrt(3) * a
    a1 = np.array([a, 0.0]); a2 = np.array([-a / 2, a * math.sqrt(3) / 2])
    out, seen = [], set()
    for el, fx, fy, fz in QUARTZ["atoms"]:
        for i in range(-2 * q - 2, p + 2 * q + 3):
            for j in range(-1, 2 * q + 3):
                for k in range(nz):
                    xy = (fx + i) * a1 + (fy + j) * a2
                    x, y = xy[0] % Lx, xy[1] % Ly; z = (fz + k) * c
                    key = (el, round(x, 3), round(y, 3), round(z, 3))
                    if key in seen: continue
                    seen.add(key); out.append((el, x, y, z))
    n_expected = 9 * 2 * p * q * nz
    assert len(out) == n_expected, f"슬래브 원자 수 {len(out)} ≠ {n_expected}"
    return out, Lx, Ly, nz * c


def water_xyz(n, Lx, Ly, z0, z1, workdir, tol=2.0, seed=20240908, packmol="packmol"):
    th = math.radians(SPCE["theta"]); r = SPCE["rOH"]
    pdb = workdir / "spce.pdb"
    pdb.write_text(f"HETATM    1  OW  SOL A   1    {0:8.3f}{0:8.3f}{0:8.3f}  1.00  0.00           O\n"
                   f"HETATM    2  HW1 SOL A   1    {r:8.3f}{0:8.3f}{0:8.3f}  1.00  0.00           H\n"
                   f"HETATM    3  HW2 SOL A   1    {r*math.cos(th):8.3f}{r*math.sin(th):8.3f}{0:8.3f}  1.00  0.00           H\nEND\n")
    return pdb


def run_packmol(workdir, items, tol, seed, exe):
    """items = [(pdb 파일명, 개수, (x0,y0,z0,x1,y1,z1))]"""
    inp = f"tolerance {tol}\nfiletype pdb\noutput packed.pdb\nseed {seed}\n"
    for pdb, n, box in items:
        inp += f"\nstructure {pdb}\n  number {n}\n  inside box {box[0]:.2f} {box[1]:.2f} {box[2]:.2f} {box[3]:.2f} {box[4]:.2f} {box[5]:.2f}\nend structure\n"
    (workdir / "stack.inp").write_text(inp)
    with open(workdir / "stack.inp") as fin, open(workdir / "packmol.log", "w") as flog:
        rc = subprocess.run([exe], stdin=fin, stdout=flog, stderr=subprocess.STDOUT, cwd=workdir).returncode
    log = (workdir / "packmol.log").read_text()
    xyz = [(float(l[30:38]), float(l[38:46]), float(l[46:54])) for l in (workdir / "packed.pdb").read_text().splitlines() if l.startswith(("ATOM", "HETATM"))]
    return rc, log, np.array(xyz)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, default=5); ap.add_argument("--q", type=int, default=3); ap.add_argument("--nz", type=int, default=2)
    ap.add_argument("--water", type=float, default=10.0, help="물 층 두께 Å (0 = 건조 계면)"); ap.add_argument("--ntol", type=int, default=20)
    ap.add_argument("--rho0", type=float, default=0.2); ap.add_argument("--gap", type=float, default=2.5); ap.add_argument("--vac", type=float, default=30.0)
    ap.add_argument("--tol", type=float, default=2.0); ap.add_argument("--seed", type=int, default=20240908); ap.add_argument("--packmol", default="packmol")
    ap.add_argument("--lmp", default=None); ap.add_argument("--steps", type=int, default=500); ap.add_argument("--slab", default="on", choices=["on", "off"], help="off = boundary p p p · slab 보정 없음 (바꿔 보기)")
    ap.add_argument("--tag", default="stack")
    a = ap.parse_args()

    # ① 슬래브
    slab, Lx, Ly, tslab = quartz_slab(a.p, a.q, a.nz)
    area = Lx * Ly
    # ② 물
    n_w = int(round(a.water * area * WATER_PER_A3)) if a.water > 0 else 0
    z_w0 = tslab + a.gap; z_w1 = z_w0 + a.water
    # ③ 톨루엔 (초기 밀도 ρ0 → 두께)
    atoms_t, bonds_t = read_mol(HERE.parent / "week06" / "data" / "Toluene.mol"); art = json.load(open(HERE.parent / "week06" / "data" / "Toluene_gaff2.json"))
    m_tol = sum(MASS[x[3]] for x in atoms_t)
    t_tol = a.ntol * m_tol / (a.rho0 * NA) * 1e24 / area
    z_b0 = (z_w1 if n_w else tslab) + a.gap; z_b1 = z_b0 + t_tol
    Lz = z_b1 + a.vac
    work = OUT / f"pack_{a.tag}"; work.mkdir(exist_ok=True)
    # 톨루엔 pdb
    (work / "toluene.pdb").write_text("".join(f"HETATM{i:5d} {el+str(i):<4s} TOL A   1    {x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00          {el:>2s}\n" for i, (x, y, z, el) in enumerate(atoms_t, 1)) + "END\n")
    items = []
    if n_w: water_xyz(n_w, Lx, Ly, z_w0, z_w1, work); items.append(("spce.pdb", n_w, (1.0, 1.0, z_w0, Lx - 1.0, Ly - 1.0, z_w1)))
    items.append(("toluene.pdb", a.ntol, (1.0, 1.0, z_b0, Lx - 1.0, Ly - 1.0, z_b1)))
    rc, log, xyz = run_packmol(work, items, a.tol, a.seed, a.packmol)
    assert rc == 0 and "Success!" in log, "Packmol 실패 — out/pack_*/packmol.log 확인"
    assert len(xyz) == 3 * n_w + 15 * a.ntol
    # ── 타입 · 좌표 · 토폴로지 조립 ──
    types = [("Si", "ClayFF st", MASS["Si"], CLAYFF["Si"]["eps"], CLAYFF["Si"]["sig"]), ("O", "ClayFF ob", MASS["O"], CLAYFF["O"]["eps"], CLAYFF["O"]["sig"])]
    if n_w: types += [("OW", "SPC/E O", MASS["O"], SPCE["OW"]["eps"], SPCE["OW"]["sig"]), ("HW", "SPC/E H", MASS["H"], 0.0, 0.0)]
    ttypes = sorted({x["ff_type"] for x in art["atoms"]})
    for t in ttypes:
        ref = next(x for x in art["atoms"] if x["ff_type"] == t); types.append((t, "GAFF2 " + t, MASS[ref["element"]], ref["epsilon"], ref["sigma"]))
    tid = {t[0]: i + 1 for i, t in enumerate(types)}
    atoms = []  # (mol, type, q, x, y, z, layer)
    for el, x, y, z in slab: atoms.append((1, tid[el], CLAYFF[el]["q"], x, y, z, "slab"))
    bonds, angles, dihed = [], [], []
    btypes, atypes, dtypes = {}, {}, {}
    mol = 1; idx = 0
    if n_w:
        btypes["OW-HW"] = 1; atypes["HW-OW-HW"] = 1
        for w in range(n_w):
            mol += 1; base = len(atoms)
            for k, t in enumerate(["OW", "HW", "HW"]):
                x, y, z = xyz[idx]; idx += 1; atoms.append((mol, tid[t], SPCE[t]["q"], x, y, z, "water"))
            bonds += [(1, base + 1, base + 2), (1, base + 1, base + 3)]; angles.append((1, base + 2, base + 1, base + 3))
    ang_t, dih_t = build_topology(bonds_t)
    bt = {x["key"]: x for x in art["bond_types"]}; at = {x["key"]: x for x in art["angle_types"]}; dt = {x["key"]: x for x in art["dihedral_types"]}
    def key(table, ids):
        names = [art["atoms"][i - 1]["ff_type"] for i in ids]; k1, k2 = "-".join(names), "-".join(names[::-1]); return k1 if k1 in table else k2
    for m in range(a.ntol):
        mol += 1; base = len(atoms)
        for i, at_ in enumerate(art["atoms"]):
            x, y, z = xyz[idx]; idx += 1; atoms.append((mol, tid[at_["ff_type"]], at_["charge"], x, y, z, "binder"))
        for b in bonds_t: k = key(bt, b); btypes.setdefault(k, len(btypes) + 1); bonds.append((btypes[k], base + b[0], base + b[1]))
        for an in ang_t: k = key(at, an); atypes.setdefault(k, len(atypes) + 1); angles.append((atypes[k], base + an[0], base + an[1], base + an[2]))
        for d in dih_t: k = key(dt, d); dtypes.setdefault(k, len(dtypes) + 1); dihed.append((dtypes[k], base + d[0], base + d[1], base + d[2], base + d[3]))
    # ── data 파일 ──
    data = OUT / f"{a.tag}.data"
    with open(data, "w") as fh:
        fh.write(f"LAMMPS data · week08 3층 계면 셀 · 석영(ClayFF) {len(slab)} | 물(SPC/E) {n_w}분자 | 톨루엔(GAFF2) {a.ntol}분자 · 진공 {a.vac} Å\n\n")
        fh.write(f"{len(atoms)} atoms\n{len(bonds)} bonds\n{len(angles)} angles\n{len(dihed)} dihedrals\n\n{len(types)} atom types\n{len(btypes)} bond types\n{len(atypes)} angle types\n{len(dtypes)} dihedral types\n\n")
        fh.write(f"0.0 {Lx:.4f} xlo xhi\n0.0 {Ly:.4f} ylo yhi\n{-2.0:.4f} {Lz:.4f} zlo zhi\n\nMasses\n\n")
        for t in types: fh.write(f"{tid[t[0]]} {t[2]:.4f}  # {t[1]}\n")
        fh.write("\nPair Coeffs # lj/cut/coul/long\n\n")
        for t in types: fh.write(f"{tid[t[0]]} {t[3]:.6g} {t[4]:.5f}  # {t[1]}\n")
        fh.write("\nBond Coeffs # harmonic\n\n")
        for k, i in btypes.items(): fh.write(f"{i} 1000.0 {SPCE['rOH']}  # SPC/E (shake)\n" if k == "OW-HW" else f"{i} {bt[k]['k']} {bt[k]['r0']}  # {k}\n")
        fh.write("\nAngle Coeffs # harmonic\n\n")
        for k, i in atypes.items(): fh.write(f"{i} 100.0 {SPCE['theta']}  # SPC/E (shake)\n" if k == "HW-OW-HW" else f"{i} {at[k]['k']} {at[k]['theta0']:.3f}  # {k}\n")
        fh.write("\nDihedral Coeffs # fourier\n\n")
        for k, i in dtypes.items(): c = dt[k]["coeffs"]; fh.write(f"{i} 1 {c[0]} {int(c[1])} {c[2]}  # {k}\n")
        fh.write("\nAtoms # full\n\n")
        for i, (m, t, qq, x, y, z, lay) in enumerate(atoms, 1): fh.write(f"{i} {m} {t} {qq:.6f} {x:.4f} {y:.4f} {z:.4f}\n")
        if bonds: fh.write("\nBonds\n\n"); [fh.write(f"{i} {b[0]} {b[1]} {b[2]}\n") for i, b in enumerate(bonds, 1)]
        if angles: fh.write("\nAngles\n\n"); [fh.write(f"{i} {x[0]} {x[1]} {x[2]} {x[3]}\n") for i, x in enumerate(angles, 1)]
        if dihed: fh.write("\nDihedrals\n\n"); [fh.write(f"{i} {x[0]} {x[1]} {x[2]} {x[3]} {x[4]}\n") for i, x in enumerate(dihed, 1)]
    # ── in 파일 (COMID clayff_gaff2_v1 설정 · 원본 04#41 조립 순서) ──
    n_slab = len(slab); n_wat = 3 * n_w
    wtypes = f"{tid['OW']} {tid['HW']}" if n_w else ""
    shake = f"fix            shk water shake 1.0e-4 20 0 b 1 a 1\n" if n_w else ""
    bnd = "p p f" if a.slab == "on" else "p p p"
    ks = "kspace_style   pppm 1.0e-4\nkspace_modify  slab 3.0\n" if a.slab == "on" else "kspace_style   pppm 1.0e-4\n"
    ins = f"""# in.{a.tag} — week08 3층 계면 셀 · 석영(ClayFF) | 물(SPC/E) | 톨루엔(GAFF2) · COMID clayff_gaff2_v1 설정
units          real
atom_style     full
boundary       {bnd}
pair_style     lj/cut/coul/long 12.0
bond_style     harmonic
angle_style    harmonic
dihedral_style fourier
special_bonds  lj 0.0 0.0 0.5 coul 0.0 0.0 0.833333
read_data      {a.tag}.data

pair_modify    mix arithmetic
{ks}neighbor       2.0 bin
neigh_modify   every 1 delay 0 check yes

group          slab id 1:{n_slab}
group          water id {n_slab + 1}:{n_slab + n_wat}
group          binder id {n_slab + n_wat + 1}:{len(atoms)}
group          mobile subtract all slab

fix            frz slab setforce 0.0 0.0 0.0
compute        tm mobile temp
compute        zb binder reduce ave z
compute        zw water reduce ave z
thermo_style   custom step c_tm pe evdwl ecoul elong c_zw c_zb
thermo         50
minimize       1.0e-4 1.0e-6 2000 20000
reset_timestep 0
{shake}velocity       mobile create 298.0 4928459 mom yes rot yes dist gaussian
fix            nvt mobile nvt temp 298.0 298.0 100.0
fix_modify     nvt temp tm
timestep       1.0
dump           d1 all custom {a.steps} {a.tag}_last.dump id mol type q x y z
run            {a.steps}
write_data     {a.tag}_final.data
"""
    if not n_w:
        ins = ins.replace("group          water id " + f"{n_slab + 1}:{n_slab}\n", "").replace("compute        zw water reduce ave z\n", "").replace(" c_zw", "")
    (OUT / f"in.{a.tag}").write_text(ins)
    summary = {"p": a.p, "q": a.q, "nz": a.nz, "Lx_A": round(Lx, 3), "Ly_A": round(Ly, 3), "Lz_A": round(Lz, 3), "area_A2": round(area, 1),
               "slab": {"atoms": n_slab, "thickness_A": round(tslab, 3), "Si": sum(1 for s in slab if s[0] == "Si"), "O": sum(1 for s in slab if s[0] == "O"), "charge_sum": round(sum(CLAYFF[s[0]]["q"] for s in slab), 6)},
               "water": {"molecules": n_w, "atoms": n_wat, "thickness_A": a.water, "z0": round(z_w0, 2), "z1": round(z_w1, 2)},
               "binder": {"molecules": a.ntol, "atoms": 15 * a.ntol, "thickness_A": round(t_tol, 2), "z0": round(z_b0, 2), "z1": round(z_b1, 2), "rho0_g_cm3": a.rho0, "charge_sum": round(sum(x["charge"] for x in art["atoms"]) * a.ntol, 6)},
               "vacuum_A": a.vac, "gap_A": a.gap, "boundary": bnd, "slab_correction": a.slab == "on", "atoms_total": len(atoms), "bonds": len(bonds), "angles": len(angles), "dihedrals": len(dihed),
               "atom_types": [t[1] for t in types], "min_edge_over_2rc": round(min(Lx, Ly) / 24.0, 3), "packmol": {"tolerance": a.tol, "seed": a.seed, "success": "Success!" in log}}
    (OUT / f"{a.tag}_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1))
    print(json.dumps(summary, ensure_ascii=False))
    if a.lmp:
        r = subprocess.run([a.lmp, "-in", f"in.{a.tag}", "-log", f"log.{a.tag}"], cwd=OUT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        print("lmp rc", r.returncode); print(r.stdout[-1500:])
        if r.returncode == 0:
            # 측면 뷰: 마지막 프레임 (type, x, z) + 층 경계
            lines = (OUT / f"{a.tag}_last.dump").read_text().splitlines(); i = max(k for k, l in enumerate(lines) if l.startswith("ITEM: ATOMS"))
            rows = [l.split() for l in lines[i + 1:]]
            side = [{"id": int(r_[0]), "mol": int(r_[1]), "type": int(r_[2]), "x": round(float(r_[4]), 2), "y": round(float(r_[5]), 2), "z": round(float(r_[6]), 2)} for r_ in rows]
            lays = {}
            for s in side:
                lay = "slab" if s["id"] <= n_slab else ("water" if s["id"] <= n_slab + n_wat else "binder"); lays.setdefault(lay, []).append(s["z"])
            (OUT / f"{a.tag}_sideview.json").write_text(json.dumps({"box": [Lx, Ly, -2.0, Lz], "types": [t[1] for t in types], "layers": {k: {"n": len(v), "zmin": min(v), "zmax": max(v), "zmean": round(sum(v) / len(v), 2)} for k, v in lays.items()}, "atoms": side}, ensure_ascii=False))


if __name__ == "__main__":
    main()
