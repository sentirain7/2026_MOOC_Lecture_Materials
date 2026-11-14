#!/usr/bin/env python3
"""week06 — 톨루엔 벌크 셀: mol → pdb → Packmol 상자 → GAFF2 data 파일 → LAMMPS in 파일 (노트북 02 와 같은 계산).

절차 (덱 4차시)
  1. data/Toluene.mol (COMID 단분자 좌표 · 원자 15) → data/toluene.pdb
  2. 분자 수 N 을 초기 밀도 ρ0 = 0.2 g/cm³ 에서 역산한 상자 L 에 Packmol 로 배치 (tolerance 3.0 Å · seed 기록) → out/toluene_box.pdb
  3. 품질 게이트: 종료 코드 0 · 'Success!' · 분자간 최소 원자 거리 ≥ 0.9 × tolerance · 원자 수 일치 → out/packmol_quality.json
  4. 원자 타입 · 전하 · 결합 · 각 · 이면각 = data/Toluene_gaff2.json (COMID GAFF2 + AM1-BCC 아티팩트) → out/toluene_box.data
  5. in.toluene (units real · lj/cut/coul/long 12.0 · pppm 1.0e-4 · special_bonds amber · minimize → NPT 298 K) → out/in.toluene
숫자 출처: 원본 04주차 #34 · #35 · #37 (ρ0 0.2 · tolerance 3.0 · 경계 2 Å) · 04#20 (in 스크립트) · COMID Toluene.json
실행: python3 scripts/build_toluene_box.py [--n 50] [--packmol packmol] [--run-lammps lmp]
"""
import argparse, json, math, os, shutil, subprocess, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent.parent
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
NA = 6.02214076e23
MASS = {"C": 12.011, "H": 1.008, "O": 15.999, "N": 14.007, "S": 32.06}


def read_mol(path):
    L = Path(path).read_text().splitlines()
    na, nb = int(L[3][:3]), int(L[3][3:6])
    atoms = [(float(l[:10]), float(l[10:20]), float(l[20:30]), l[31:34].strip()) for l in L[4:4 + na]]
    bonds = [(int(l[:3]), int(l[3:6])) for l in L[4 + na:4 + na + nb]]
    return atoms, bonds


def write_pdb(atoms, path, resname="TOL"):
    with open(path, "w") as fh:
        for i, (x, y, z, el) in enumerate(atoms, 1):
            fh.write(f"HETATM{i:5d} {el+str(i):<4s} {resname} A   1    {x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00          {el:>2s}\n")
        fh.write("END\n")


def box_edge(n_mol, mol_mass, rho):
    """ρ (g/cm³) 에서 상자 한 변 (Å): V = N M / (ρ N_A) · 1 cm³ = 1e24 Å³"""
    return (n_mol * mol_mass / (rho * NA) * 1e24) ** (1 / 3)


def packmol_input(n_mol, L, tol=3.0, seed=20240901, margin=2.0):
    return f"""tolerance {tol}
filetype pdb
output toluene_box.pdb
seed {seed}

structure toluene.pdb
  number {n_mol}
  inside box {margin} {margin} {margin} {L - margin:.2f} {L - margin:.2f} {L - margin:.2f}
end structure
"""


def run_packmol(inp_text, workdir, exe="packmol"):
    (workdir / "toluene.inp").write_text(inp_text)
    with open(workdir / "toluene.inp") as fin, open(workdir / "packmol.log", "w") as flog:
        r = subprocess.run([exe], stdin=fin, stdout=flog, stderr=subprocess.STDOUT, cwd=workdir)
    log = (workdir / "packmol.log").read_text()
    return r.returncode, log


def read_pdb_xyz(path):
    xyz = []
    for l in Path(path).read_text().splitlines():
        if l.startswith(("ATOM", "HETATM")): xyz.append((float(l[30:38]), float(l[38:46]), float(l[46:54])))
    return np.array(xyz)


def quality_gate(rc, log, xyz, n_mol, n_atoms_mol, tol):
    """원본 04#37 게이트: 0 수렴 보고 · 1 분자간 최소 거리 · (2 실패 시 시드 변경은 호출측)"""
    ok_rc = rc == 0; ok_success = "Success!" in log
    ok_count = len(xyz) == n_mol * n_atoms_mol
    mol_id = np.repeat(np.arange(n_mol), n_atoms_mol)
    d = np.linalg.norm(xyz[:, None, :] - xyz[None, :, :], axis=-1)
    inter = d[mol_id[:, None] != mol_id[None, :]]
    dmin = float(inter.min()) if inter.size else float("nan")
    ok_dist = dmin >= 0.9 * tol
    return {"exit_code": rc, "success_in_log": ok_success, "atom_count_ok": ok_count, "n_atoms": int(len(xyz)),
            "min_intermolecular_distance_A": round(dmin, 3), "threshold_A": 0.9 * tol, "min_distance_ok": ok_dist,
            "pass": ok_rc and ok_success and ok_count and ok_dist}


def build_topology(bonds):
    """결합 목록 → 각(i-j-k) · 이면각(i-j-k-l) 목록 (1-based)"""
    nb = {}
    for a, b in bonds: nb.setdefault(a, set()).add(b); nb.setdefault(b, set()).add(a)
    angles = set()
    for j in nb:
        for i in nb[j]:
            for k in nb[j]:
                if i < k: angles.add((i, j, k))
    dihed = set()
    for j, k in bonds:
        for i in nb[j]:
            if i == k: continue
            for l in nb[k]:
                if l == j or l == i: continue
                t = (i, j, k, l); dihed.add(t if t[0] < t[3] or (t[0] == t[3] and t[1] < t[2]) else t[::-1])
    return sorted(angles), sorted(dihed)


def write_data(xyz, art, bonds, n_mol, L, path):
    atoms = art["atoms"]; n = len(atoms)
    types = sorted({a["ff_type"] for a in atoms}); tid = {t: i + 1 for i, t in enumerate(types)}
    tmass = {t: MASS[next(a["element"] for a in atoms if a["ff_type"] == t)] for t in types}
    teps = {t: next((a["epsilon"], a["sigma"]) for a in atoms if a["ff_type"] == t) for t in types}
    angles, dihed = build_topology(bonds)
    def key(idx, kind):
        names = [atoms[i - 1]["ff_type"] for i in idx]
        k1, k2 = "-".join(names), "-".join(names[::-1])
        table = {x["key"]: x for x in art[kind]}
        return table.get(k1) or table.get(k2), (k1 if k1 in table else k2)
    btypes, atypes, dtypes = {}, {}, {}
    bl = [(key(b, "bond_types")[1]) for b in bonds]; al = [key(a, "angle_types")[1] for a in angles]; dl = [key(d, "dihedral_types")[1] for d in dihed]
    for k in bl: btypes.setdefault(k, len(btypes) + 1)
    for k in al: atypes.setdefault(k, len(atypes) + 1)
    for k in dl: dtypes.setdefault(k, len(dtypes) + 1)
    bt = {x["key"]: x for x in art["bond_types"]}; at = {x["key"]: x for x in art["angle_types"]}; dt = {x["key"]: x for x in art["dihedral_types"]}
    with open(path, "w") as fh:
        fh.write(f"LAMMPS data · toluene x {n_mol} · GAFF2 + AM1-BCC (COMID Toluene.json) · week06\n\n")
        fh.write(f"{n * n_mol} atoms\n{len(bonds) * n_mol} bonds\n{len(angles) * n_mol} angles\n{len(dihed) * n_mol} dihedrals\n\n")
        fh.write(f"{len(types)} atom types\n{len(btypes)} bond types\n{len(atypes)} angle types\n{len(dtypes)} dihedral types\n\n")
        fh.write(f"0.0 {L:.4f} xlo xhi\n0.0 {L:.4f} ylo yhi\n0.0 {L:.4f} zlo zhi\n\nMasses\n\n")
        for t in types: fh.write(f"{tid[t]} {tmass[t]:.4f}  # {t}\n")
        fh.write("\nPair Coeffs # lj/cut/coul/long\n\n")
        for t in types: fh.write(f"{tid[t]} {teps[t][0]:.4f} {teps[t][1]:.5f}  # {t}\n")
        fh.write("\nBond Coeffs # harmonic\n\n")
        for k, i in btypes.items(): fh.write(f"{i} {bt[k]['k']} {bt[k]['r0']}  # {k}\n")
        fh.write("\nAngle Coeffs # harmonic\n\n")
        for k, i in atypes.items(): fh.write(f"{i} {at[k]['k']} {at[k]['theta0']:.3f}  # {k}\n")
        fh.write("\nDihedral Coeffs # fourier\n\n")
        for k, i in dtypes.items():
            c = dt[k]["coeffs"]; fh.write(f"{i} 1 {c[0]} {int(c[1])} {c[2]}  # {k}\n")
        fh.write("\nAtoms # full\n\n")
        for m in range(n_mol):
            for i, a in enumerate(atoms):
                x, y, z = xyz[m * n + i]; fh.write(f"{m * n + i + 1} {m + 1} {tid[a['ff_type']]} {a['charge']:.6f} {x:.4f} {y:.4f} {z:.4f}\n")
        fh.write("\nBonds\n\n"); c = 0
        for m in range(n_mol):
            for (a, b), k in zip(bonds, bl): c += 1; fh.write(f"{c} {btypes[k]} {m * n + a} {m * n + b}\n")
        fh.write("\nAngles\n\n"); c = 0
        for m in range(n_mol):
            for (i, j, kk), k in zip(angles, al): c += 1; fh.write(f"{c} {atypes[k]} {m * n + i} {m * n + j} {m * n + kk}\n")
        fh.write("\nDihedrals\n\n"); c = 0
        for m in range(n_mol):
            for (i, j, kk, l), k in zip(dihed, dl): c += 1; fh.write(f"{c} {dtypes[k]} {m * n + i} {m * n + j} {m * n + kk} {m * n + l}\n")
    return {"atoms": n * n_mol, "bonds": len(bonds) * n_mol, "angles": len(angles) * n_mol, "dihedrals": len(dihed) * n_mol,
            "atom_types": len(types), "bond_types": len(btypes), "angle_types": len(atypes), "dihedral_types": len(dtypes),
            "charge_sum": round(sum(a["charge"] for a in atoms) * n_mol, 6)}


IN_SCRIPT = """# in.toluene — week06 · 톨루엔 {n_mol}분자 · GAFF2 + AM1-BCC · 최소화 → NPT 298 K (원본 04주차 #20 구조)
units          real
atom_style     full
boundary       p p p

# 스타일 선언은 read_data 보다 앞 — data 파일 안의 Coeffs 절을 읽을 때 필요 (없으면 ERROR: Must define pair_style before Pair Coeffs)
pair_style     lj/cut/coul/long 12.0
bond_style     harmonic
angle_style    harmonic
dihedral_style fourier
special_bonds  amber

read_data      toluene_box.data

pair_modify    mix arithmetic tail yes
kspace_style   pppm 1.0e-4
neighbor       2.0 bin
neigh_modify   every 1 delay 0 check yes

thermo_style   custom step temp press density pe
thermo         100
minimize       1.0e-4 1.0e-6 5000 50000
reset_timestep 0

velocity       all create 298.0 4928459 mom yes rot yes dist gaussian
timestep       1.0
fix            eq all npt temp 298.0 298.0 100.0 iso 1.0 1.0 1000.0
thermo         {thermo}
run            {nsteps}
unfix          eq

variable       dens equal density
fix            avg all ave/time 100 10 1000 v_dens file density.txt
fix            prod all nvt temp 298.0 298.0 100.0
dump           d1 all custom 1000 prod.lammpstrj id type x y z
run            {nsteps_prod}
write_data     final.data
write_restart  final.restart
"""


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--n", type=int, default=50); ap.add_argument("--rho0", type=float, default=0.2)
    ap.add_argument("--tol", type=float, default=3.0); ap.add_argument("--seed", type=int, default=20240901); ap.add_argument("--packmol", default="packmol")
    ap.add_argument("--run-lammps", default=None, help="lmp 실행 파일 경로 (있으면 in.toluene 실행)"); ap.add_argument("--nsteps", type=int, default=20000)
    a = ap.parse_args()
    atoms, bonds = read_mol(HERE / "data/Toluene.mol"); art = json.load(open(HERE / "data/Toluene_gaff2.json"))
    assert [x[3] for x in atoms] == [b["element"] for b in art["atoms"]], "mol 원자 순서 ≠ 아티팩트 순서"
    write_pdb(atoms, OUT / "toluene.pdb")
    mol_mass = sum(MASS[x[3]] for x in atoms); L = box_edge(a.n, mol_mass, a.rho0)
    print(f"toluene M {mol_mass:.3f} g/mol · N {a.n} · ρ0 {a.rho0} → L {L:.2f} Å")
    rep = {"n_mol": a.n, "mol_mass": round(mol_mass, 3), "rho0": a.rho0, "L_A": round(L, 2), "tolerance": a.tol, "seed": a.seed}
    if shutil.which(a.packmol):
        for attempt in range(3):
            rc, log = run_packmol(packmol_input(a.n, L, a.tol, a.seed + attempt), OUT, a.packmol)
            xyz = read_pdb_xyz(OUT / "toluene_box.pdb") if (OUT / "toluene_box.pdb").exists() else np.zeros((0, 3))
            q = quality_gate(rc, log, xyz, a.n, len(atoms), a.tol); q["attempt"] = attempt + 1; q["seed"] = a.seed + attempt
            print("packmol attempt", attempt + 1, "→", "PASS" if q["pass"] else "FAIL", q["min_intermolecular_distance_A"], "Å")
            if q["pass"]: break
        rep["packmol"] = q
        if q["pass"]:
            rep["data"] = write_data(xyz, art, bonds, a.n, L, OUT / "toluene_box.data")
            (OUT / "in.toluene").write_text(IN_SCRIPT.format(n_mol=a.n, nsteps=a.nsteps, nsteps_prod=a.nsteps // 2, thermo=max(100, a.nsteps // 100)))
            print("data:", rep["data"])
    else:
        rep["packmol"] = "packmol 실행 파일 없음 — expected_output/ 사용"; print(rep["packmol"])
    if a.run_lammps and (OUT / "in.toluene").exists():
        r = subprocess.run([a.run_lammps, "-in", "in.toluene", "-log", "log.toluene"], cwd=OUT, capture_output=True, text=True)
        rep["lammps_exit"] = r.returncode; print("lammps exit", r.returncode, r.stderr[-400:] if r.returncode else "")
    (OUT / "build_report.json").write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
