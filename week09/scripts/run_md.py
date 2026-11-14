#!/usr/bin/env python3
"""run_md.py — week09 · 짧은 MD 실행 2종 (교육용 · 수렴 전 「형태」)
  python3 scripts/run_md.py prod  [--lmp lmp] [--npt 30000] [--nvt 20000]   → out/prod/{log.prod, stress.txt, npt_final.data, nvt_final.data}
  python3 scripts/run_md.py tg    [--lmp lmp] [--temps 100,175,250,325] [--steps 6000] [--avg 2000] → out/tg/tg_T*.txt · log.tg_T*
입력 = data/toluene_eq.data (W06 final.data · 톨루엔 50분자 · GAFF2 + AM1-BCC). 표준 라이브러리만.
"""
import argparse, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def lmp(exe, infile, var, logfile):
    cmd = [exe, "-in", str(infile), "-log", str(logfile), "-screen", "none"]
    for k, v in var.items(): cmd += ["-var", k, str(v)]
    t0 = time.time(); r = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    dt = time.time() - t0
    if r.returncode != 0:
        sys.stderr.write(r.stderr[-2000:]); sys.exit(f"LAMMPS 실패 ({infile.name}) · 종료 코드 {r.returncode}")
    return dt

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("mode", choices=["prod", "tg"])
    ap.add_argument("--lmp", default="lmp"); ap.add_argument("--data", default="data/toluene_eq.data")
    ap.add_argument("--npt", type=int, default=30000); ap.add_argument("--nvt", type=int, default=20000)
    ap.add_argument("--temps", default="100,175,250,325"); ap.add_argument("--steps", type=int, default=6000); ap.add_argument("--avg", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=4928459)
    a = ap.parse_args()
    if a.mode == "prod":
        out = ROOT / "out/prod"; out.mkdir(parents=True, exist_ok=True)
        dt = lmp(a.lmp, ROOT / "data/in.prod", {"data": a.data, "out": "out/prod", "seed": a.seed, "npt_steps": a.npt, "nvt_steps": a.nvt}, out / "log.prod")
        print(f"prod 완료 · NPT {a.npt} + NVT {a.nvt} 스텝 · 벽시계 {dt:.1f} s → {out}")
    else:
        out = ROOT / "out/tg"; out.mkdir(parents=True, exist_ok=True)
        for T in [int(x) for x in a.temps.split(",")]:
            dt = lmp(a.lmp, ROOT / "data/in.tg", {"data": a.data, "out": "out/tg", "T": T, "seed": a.seed + T, "steps": a.steps, "avg_steps": a.avg}, out / f"log.tg_T{T}")
            print(f"tg T={T} K · {a.steps}+{a.avg} 스텝 · {dt:.1f} s")
if __name__ == "__main__": main()
