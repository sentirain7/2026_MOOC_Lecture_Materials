#!/usr/bin/env python3
"""postprocess_all.py — 후처리 체인: 폴더 하나 → 표 한 줄 (원본 06주차 #26)
  python3 scripts/postprocess_all.py --exp-id toluene50_w09 [--lmp lmp] [--skip-md]
  순서: run_md prod → density_from_log → ced_method_ab → viscosity_gk → run_md tg → tg_fit → results.csv 1행 + summary.json
  규칙: 평형 구간 · 적합 구간은 인수 · 모든 값은 평균 ± 오차(없으면 「수렴 전」 표시) · 열 이름 = W16 데이터베이스 스키마와 동일
"""
import argparse, csv, json, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; PY = sys.executable

def run(args, label):
    t0 = time.time(); r = subprocess.run([PY] + args, cwd=ROOT, text=True, capture_output=True)
    if r.returncode != 0: sys.stderr.write(r.stdout[-800:] + r.stderr[-1500:]); sys.exit(f"[{label}] 실패")
    print(f"✔ {label:<22} {time.time()-t0:6.1f} s"); return r.stdout

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--exp-id", default="toluene50_w09"); ap.add_argument("--lmp", default="lmp")
    ap.add_argument("--skip-md", action="store_true"); ap.add_argument("--npt", type=int, default=30000); ap.add_argument("--nvt", type=int, default=20000)
    a = ap.parse_args(); out = ROOT / "out"; out.mkdir(exist_ok=True); T0 = time.time()
    if not a.skip_md:
        run(["scripts/run_md.py", "prod", "--lmp", a.lmp, "--npt", str(a.npt), "--nvt", str(a.nvt)], "① run_md prod")
    run(["scripts/density_from_log.py", "out/prod/log.prod"], "② density_from_log")
    run(["scripts/ced_method_ab.py", "out/prod/nvt_final.data", "out/prod/log.prod", "--lmp", a.lmp], "③ ced_method_ab")
    run(["scripts/viscosity_gk.py", "out/prod/stress.txt"], "④ viscosity_gk")
    if not a.skip_md: run(["scripts/run_md.py", "tg", "--lmp", a.lmp], "⑤ run_md tg")
    run(["scripts/tg_fit.py", "out/tg"], "⑥ tg_fit")
    J = lambda n: json.loads((out / n).read_text(encoding="utf-8"))
    d, c, v, g = J("density.json"), J("ced.json"), J("viscosity_gk.json"), J("tg.json")
    row = {"exp_id": a.exp_id, "n_atoms": 750, "n_mol": c["n_mol"], "T_K": 298, "rho_gcc": d["mean"], "rho_se": d["block_se"], "rho_converged": d["converged_0p5pct"],
           "ced_A_MJm3": c["CED_A_MJm3"], "ced_B_MJm3": c["CED_B_MJm3"], "ced_method_fixed": "B", "delta_MPa05": c["delta_B_MPa05"],
           "eta_gk_running_mPas": v["eta_running_at_tmax_mPas"], "eta_plateau": v["plateau_reached"], "Tg_K": g.get("Tg_K_bilinear"), "Tg_n_T": g["n_T"],
           "t_total_ps": d["t_total_ps"] + v["t_total_ps"], "scripts_version": "week09-v3", "flags": "short-run;rho-not-converged" if not d["converged_0p5pct"] else "short-run"}
    with open(out / "results.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(row)); w.writeheader(); w.writerow(row)
    summary = {"row": row, "wall_s": round(time.time() - T0, 1), "inputs": ["data/toluene_eq.data", "data/in.prod", "data/in.tg", "data/in.gas"],
               "outputs": ["out/density.json", "out/ced.json", "out/viscosity_gk.json", "out/tg.json", "out/results.csv"]}
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(row, ensure_ascii=False))
if __name__ == "__main__": main()
