#!/usr/bin/env python3
"""week06 노트북 01 — W03 의 LJ 유체(탄소 64원자 · ε 0.109 kcal/mol · σ 3.40 Å · L 17.47 Å)를 LAMMPS 입력 두 파일로 쓴다.
  out/lj.data : 단순 입방 4×4×4 격자 64원자 (W03 lj_verlet.py 와 같은 상자)
  out/in.lj   : units real · pair lj/cut 8.0 (L/2 = 8.7 Å 안) · velocity 240 K · NVE · 1 fs · 1,000 스텝 · thermo 50
숫자 출처: W03 노트북 02(lj_energy.csv: N 64 · L 17.47 · T 평균 213.9 K) · W01 LJ 탄소 ε σ.  실행: python3 scripts/build_lj_lammps.py [--run lmp]
"""
import argparse, subprocess
from pathlib import Path
HERE = Path(__file__).resolve().parent.parent; OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
N_SIDE, L, EPS, SIG, MASS = 4, 17.47, 0.109, 3.40, 12.011

def write_data(path):
    a = L / N_SIDE; lines = [f"LJ fluid · carbon {N_SIDE**3} atoms · week06 (W03 상자)", "", f"{N_SIDE**3} atoms", "1 atom types", "",
             f"0.0 {L} xlo xhi", f"0.0 {L} ylo yhi", f"0.0 {L} zlo zhi", "", "Masses", "", f"1 {MASS}", "", "Atoms # atomic", ""]
    i = 0
    for x in range(N_SIDE):
        for y in range(N_SIDE):
            for z in range(N_SIDE):
                i += 1; lines.append(f"{i} 1 {(x + 0.5) * a:.4f} {(y + 0.5) * a:.4f} {(z + 0.5) * a:.4f}")
    path.write_text("\n".join(lines) + "\n")

IN = f"""# in.lj — week06 노트북 01 · W03 LJ 유체를 LAMMPS 로 (units real · NVE)
units          real
atom_style     atomic
boundary       p p p
read_data      lj.data

pair_style     lj/cut 8.0          # L/2 = 8.7 Å 안 (W04 규칙 ③)
pair_coeff     1 1 {EPS} {SIG}       # 탄소 ε kcal/mol · σ Å (W01 · W03)
pair_modify    tail yes

velocity       all create 240.0 12345 mom yes dist gaussian
timestep       1.0
fix            1 all nve
thermo_style   custom step temp pe ke etotal press density
thermo         50
dump           d1 all custom 100 lj.lammpstrj id type x y z
run            1000
write_data     lj_final.data
"""

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--run", default=None, help="lmp 실행 파일 (있으면 바로 실행)"); a = ap.parse_args()
    write_data(OUT / "lj.data"); (OUT / "in.lj").write_text(IN)
    print("wrote out/lj.data (64 atoms · L %.2f Å) · out/in.lj" % L)
    if a.run:
        r = subprocess.run([a.run, "-in", "in.lj", "-log", "log.lj"], cwd=OUT, capture_output=True, text=True)
        print("lmp exit", r.returncode); print("\n".join(r.stdout.splitlines()[-12:]))
