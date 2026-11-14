#!/usr/bin/env python3
"""tg_fit.py — 온도별 평형 부피(밀도) → 두 직선 적합 → 교점 = Tg (원본 06주차 #11 · COMID metrics/tg.py 의 격자 탐색)
  python3 scripts/tg_fit.py out/tg [--out out]     (tg_T*.txt: fix ave/time 출력 · 열 = step dens vol)
출력 out/tg.json · out/vt_points.csv — 온도점 4개 · 짧은 실행이면 「형태만 · 수렴 전」. 냉각률 의존(MD 는 실험보다 10^10 배 빠름) 은 노트.
"""
import argparse, glob, json, re
from pathlib import Path
import numpy as np

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("folder"); ap.add_argument("--out", default="out"); a = ap.parse_args()
    pts = []
    for f in sorted(glob.glob(str(Path(a.folder) / "tg_T*.txt"))):
        T = float(re.search(r"tg_T([\d.]+)", f).group(1)); d = np.loadtxt(f, comments="#")
        d = d.reshape(-1, 3); pts.append((T, float(d[:, 1].mean()), float(d[:, 2].mean()), float(d[:, 2].std(ddof=1)) if len(d) > 1 else 0.0))
    pts.sort(); T = np.array([p[0] for p in pts]); rho = np.array([p[1] for p in pts]); V = np.array([p[2] for p in pts])
    best = None
    if len(T) >= 4:
        for Tb in np.linspace(T[0], T[-1], 200):
            lo, hi = T <= Tb, T > Tb
            if lo.sum() < 2 or hi.sum() < 2: continue
            a1, b1 = np.polyfit(T[lo], V[lo], 1); a2, b2 = np.polyfit(T[hi], V[hi], 1)
            rss = ((np.polyval([a1, b1], T[lo]) - V[lo]) ** 2).sum() + ((np.polyval([a2, b2], T[hi]) - V[hi]) ** 2).sum()
            if a1 != a2:
                Tx = (b2 - b1) / (a1 - a2)
                if best is None or rss < best[0]: best = (rss, Tx, a1, b1, a2, b2)
    res = {"points": [{"T_K": p[0], "rho_gcc": round(p[1], 4), "V_A3": round(p[2], 1), "V_std": round(p[3], 2)} for p in pts], "n_T": len(pts)}
    if best:
        rss, Tx, a1, b1, a2, b2 = best
        res.update({"Tg_K_bilinear": round(float(Tx), 1), "slope_glassy_A3perK": round(float(a1), 3), "slope_rubbery_A3perK": round(float(a2), 3),
                    "intercept_glassy": round(float(b1), 1), "intercept_rubbery": round(float(b2), 1), "rss": round(float(rss), 2),
                    "alpha_rubbery_perK": round(float(a2 / np.polyval([a2, b2], T[-1])), 6)})
    res["note"] = "온도점 4 × 수 ps · 수렴 전 「형태만」 — 실제 Tg 는 온도 8점 × 1 ns · 냉각률 의존 · 조성 간 상대 비교용(원본 06주차 #11 · #28)"
    out = Path(a.out); out.mkdir(exist_ok=True)
    (out / "tg.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    with open(out / "vt_points.csv", "w") as f:
        f.write("T_K,rho_gcc,V_A3,V_std\n"); [f.write(f"{p[0]},{p[1]:.5f},{p[2]:.2f},{p[3]:.2f}\n") for p in pts]
    print(json.dumps(res, ensure_ascii=False))
if __name__ == "__main__": main()
