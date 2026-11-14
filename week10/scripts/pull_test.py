#!/usr/bin/env python3
"""week10 — 3층 계면 셀(W08 stack_cell.py) 인장(pull) 시험: 바인더 윗부분(그립)을 z 로 정속 당기며 그립 반력 · 변위 · 에너지를 기록한다.

셀 = W08 의 stack_cell.py 로 다시 만든다(같은 석영 슬래브 540 · 같은 물 층 10 Å · 톨루엔 GAFF2).
  차이 = 바인더를 인장에 견딜 밀도로 채운다: --ntol 60 --rho0 0.6 (W08 기본 20분자 · 0.2 g/cm³ 는 기체처럼 성겨 당기면 그냥 흩어진다 → 형태 확인용)
프로토콜(원본 06주차 보충A #8 · COMID Protocol B 정속 당김을 교육용으로 축소):
  fix setforce 0 0 0  석영 슬래브 고정  ·  grip = 바인더 상단 6 Å 원자 → fix move linear 0 0 v  ·  나머지(mobile) NVT 298 K
  v 0.0025 Å/fs (= 250 m/s · 변형률 속도 ~10¹¹ s⁻¹ · 실제 캠페인 10⁸~10¹⁰) · 4,000 스텝 · Δt 1 fs → 변위 10 Å
  기록: 변위 d · 그립 반력 F_z(kcal/mol/Å · fix ave/time 로 20 스텝 평균) · 퍼텐셜 에너지 · 바인더 · 물 평균 z (20 스텝마다) · 덤프 500 스텝마다
  응력 σ = F_z / A (1 kcal/mol/Å / Å² = 6.9477 × 10³ MPa · A = 627.1 Å² → 1 kcal/mol/Å = 11.08 MPa)
실행:  python3 scripts/pull_test.py --water 10 --tag wet [--v 0.0025 --steps 4000] [--build]
출력:  out/<tag>/{in.pull, log.pull, pull.csv, pull.dump, pull_summary.json}
"""
import argparse, json, re, shutil, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent          # repo/week10
W08 = HERE.parent / "week08"
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
KCAL_A_TO_PN = 69.4786          # 1 kcal/mol/Å = 69.48 pN
LMP = shutil.which("lmp") or "lmp"   # conda activate mdai 의 lmp


def build_cell(water, ntol, rho0, tag, lmp, packmol):
    """W08 stack_cell.py 로 셀을 만들고 500 스텝 NVT 로 풀어 준다 → week08/out/<tag>_final.data 를 week10/data/ 로 복사"""
    cmd = [sys.executable, str(W08 / "scripts/stack_cell.py"), "--water", str(water), "--ntol", str(ntol), "--rho0", str(rho0), "--tag", tag,
           "--lmp", lmp, "--steps", "500", "--packmol", packmol]
    print("[build]", " ".join(cmd)); subprocess.run(cmd, check=True, cwd=W08)
    src = W08 / "out" / f"{tag}_final.data"; dst = HERE / "data" / f"{tag}_final.data"
    shutil.copy(src, dst); shutil.copy(W08 / "out" / f"{tag}_summary.json", HERE / "data" / f"{tag}_summary.json")
    return dst


def read_box_groups(data_path, summary_path):
    s = json.loads(Path(summary_path).read_text())
    txt = Path(data_path).read_text().splitlines()
    xlo = xhi = ylo = yhi = None
    for l in txt[:40]:
        if l.strip().endswith("xlo xhi"): xlo, xhi = map(float, l.split()[:2])
        if l.strip().endswith("ylo yhi"): ylo, yhi = map(float, l.split()[:2])
    n_slab = s["slab"]["atoms"]; n_w = s["water"]["atoms"] if s["water"]["molecules"] else 0; n_b = s["binder"]["atoms"]
    # Atoms 절에서 바인더 z 최대 찾기 (그립 경계)
    zs = []
    on = False
    for l in txt:
        if l.startswith("Atoms"): on = True; continue
        if on and l.strip() == "": 
            if zs: break
            continue
        if on and l.startswith(("Velocities", "Bonds")): break
        if on:
            p = l.split()
            if len(p) >= 7:
                i = int(p[0]); z = float(p[6])
                if i > n_slab + n_w: zs.append(z)
    zmax = max(zs); zmin = min(zs)
    return dict(area=(xhi - xlo) * (yhi - ylo), n_slab=n_slab, n_w=n_w, n_b=n_b, zb_max=zmax, zb_min=zmin, Lx=xhi - xlo, Ly=yhi - ylo)


def write_in(d, g, v, steps, grip_thk, T=298.0):
    first_w = g["n_slab"] + 1; last_w = g["n_slab"] + g["n_w"]; first_b = last_w + 1; last_b = last_w + g["n_b"]
    zg = g["zb_max"] - grip_thk
    water_lines = f"group          water id {first_w}:{last_w}\nfix            shk water shake 1.0e-4 20 0 b 1 a 1\ncompute        zw water reduce ave z\n" if g["n_w"] else "variable       zw_dummy equal 0.0\n"
    zw_out = "c_zw" if g["n_w"] else "v_zw_dummy"
    return f"""# in.pull — week10 계면 인장 · 석영(고정) | {'물 | ' if g['n_w'] else ''}톨루엔(그립 정속 당김) · COMID clayff_gaff2_v1 설정 · 교육용 축소 프로토콜
units          real
atom_style     full
boundary       p p f
pair_style     lj/cut/coul/long 12.0
bond_style     harmonic
angle_style    harmonic
dihedral_style fourier
special_bonds  lj 0.0 0.0 0.5 coul 0.0 0.0 0.833333
read_data      {d.name}
pair_modify    mix arithmetic
kspace_style   pppm 1.0e-4
kspace_modify  slab 3.0
neighbor       2.0 bin
neigh_modify   every 1 delay 0 check yes

group          slab id 1:{g['n_slab']}
group          binder id {first_b}:{last_b}
{water_lines}region         top block INF INF INF INF {zg:.2f} INF units box
group          topg region top
group          grip intersect binder topg
group          mobile subtract all slab grip
region         near block INF INF INF INF INF {g['zb_min'] + 6.0:.2f} units box
compute        tm mobile temp
compute        zb binder reduce ave z
compute        fg grip reduce sum fz
fix            fav grip ave/time 1 20 20 c_fg
variable       disp equal step*dt*{v}
variable       nb_near equal count(binder,near)

fix            frz slab setforce 0.0 0.0 0.0
velocity       mobile create {T} 4928459 mom yes rot yes dist gaussian
fix            nvt mobile nvt temp {T} {T} 100.0
fix_modify     nvt temp tm
fix            pull grip move linear 0.0 0.0 {v} units box
timestep       1.0
thermo_style   custom step v_disp f_fav pe c_tm c_zb {zw_out} v_nb_near
thermo_modify  format float %14.4f
thermo         20
dump           d1 all custom 500 pull.dump id mol type q x y z
dump_modify    d1 sort id
run            {steps}
write_data     pull_final.data
"""


def parse_log(log_path):
    rows, on, head = [], False, None
    for l in Path(log_path).read_text().splitlines():
        if l.startswith("   Step") or l.startswith("Step"):
            head = l.split(); on = True; continue
        if on:
            if l.startswith("Loop time"): on = False; continue
            p = l.split()
            if len(p) == len(head):
                try: rows.append([float(x) for x in p])
                except ValueError: pass
    return head, rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--water", type=float, default=10.0); ap.add_argument("--ntol", type=int, default=60); ap.add_argument("--rho0", type=float, default=0.6)
    ap.add_argument("--tag", default="wet"); ap.add_argument("--v", type=float, default=0.0025, help="그립 속도 Å/fs"); ap.add_argument("--steps", type=int, default=4000)
    ap.add_argument("--grip", type=float, default=6.0, help="그립 두께 Å (바인더 상단)"); ap.add_argument("--build", action="store_true", help="W08 stack_cell.py 로 셀을 새로 만든다")
    ap.add_argument("--lmp", default=LMP); ap.add_argument("--packmol", default="packmol"); ap.add_argument("--cell", default=None, help="셀 태그(기본 = --tag)")
    a = ap.parse_args()
    cell = a.cell or a.tag
    data = HERE / "data" / f"{cell}_final.data"; summ = HERE / "data" / f"{cell}_summary.json"
    if a.build or not data.exists():
        data = build_cell(a.water, a.ntol, a.rho0, cell, a.lmp, a.packmol)
    g = read_box_groups(data, summ)
    run = OUT / a.tag; run.mkdir(exist_ok=True)
    shutil.copy(data, run / data.name)
    (run / "in.pull").write_text(write_in(data, g, a.v, a.steps, a.grip))
    print(f"[run] {a.tag}: 원자 {g['n_slab'] + g['n_w'] + g['n_b']} · 그립 z ≥ {g['zb_max'] - a.grip:.1f} Å · v {a.v} Å/fs · {a.steps} 스텝")
    r = subprocess.run([a.lmp, "-in", "in.pull", "-log", "log.pull", "-screen", "none"], cwd=run)
    if r.returncode != 0: sys.exit(f"LAMMPS 종료 코드 {r.returncode} — {run}/log.pull 확인")
    head, rows = parse_log(run / "log.pull")
    A = g["area"]
    # 응력 MPa = F(kcal/mol/Å) * 69.4786 pN / A(Å²) → pN/Å² = 1e-12 N / 1e-20 m² = 1e8 Pa = 100 MPa
    with (run / "pull.csv").open("w") as f:
        f.write("step,disp_A,F_grip_kcal_mol_A,sigma_MPa,pe_kcal_mol,T_mobile_K,z_binder_A,z_water_A,n_binder_near_slab\n")
        for p in rows:
            step, disp, fg, pe, tm, zb, zw, nb = p
            f.write(f"{int(step)},{disp:.3f},{fg:.3f},{-fg * KCAL_A_TO_PN / A * 100:.2f},{pe:.2f},{tm:.1f},{zb:.2f},{zw:.2f},{int(nb)}\n")
    summary = dict(tag=a.tag, cell=cell, atoms=g["n_slab"] + g["n_w"] + g["n_b"], n_slab=g["n_slab"], n_water=g["n_w"], n_binder=g["n_b"], area_A2=round(A, 1),
                   v_A_per_fs=a.v, v_m_per_s=a.v * 1e5, steps=a.steps, displacement_A=a.v * a.steps, grip_thickness_A=a.grip, grip_z_min_A=round(g["zb_max"] - a.grip, 2),
                   binder_z_range_A=[round(g["zb_min"], 2), round(g["zb_max"], 2)], strain_rate_per_s=a.v / (g["zb_max"] - g["zb_min"]) * 1e15,
                   stress_unit="sigma_MPa = -F_grip(kcal/mol/A) * 69.4786 / A(A^2) * 100", rows=len(rows))
    (run / "pull_summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False))
    print(json.dumps(summary, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
