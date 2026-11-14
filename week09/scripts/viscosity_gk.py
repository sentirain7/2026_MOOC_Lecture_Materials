#!/usr/bin/env python3
"""viscosity_gk.py — Green–Kubo 점도: 비대각 응력 자기상관 → 시간 적분(러닝) → 평탄 구간(원본 06주차 #21 · #22)
  η(t) = (V / k_B T) ∫₀ᵗ ⟨P_αβ(0) P_αβ(t')⟩ dt'  · 성분 xy · xz · yz 와 여러 시간 원점을 평균
  단위: η[mPa·s] = 7.436e-10 × V[Å³]/T[K] × ∫⟨PP⟩[atm²] dt[fs]  (COMID metrics/viscosity.py 와 같은 상수)
  python3 scripts/viscosity_gk.py out/prod/stress.txt [--T 298] [--tmax 2000] [--out out]
출력 out/viscosity_gk.json · out/gk_curve.csv(t_fs, C_norm, eta_running) — 수십 ps 실행이면 평탄 구간 미도달 = 「형태만」.
"""
import argparse, json, math
from pathlib import Path
import numpy as np
GK = 1e-30 * (1.01325e5) ** 2 * 1e-15 / 1.380649e-23 * 1e3   # ≈ 7.436e-10

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("stress"); ap.add_argument("--T", type=float, default=298.0)
    ap.add_argument("--tmax", type=float, default=2000.0, help="상관 길이 상한 fs"); ap.add_argument("--out", default="out")
    a = ap.parse_args()
    d = np.loadtxt(a.stress, comments="#")        # step pxy pxz pyz vol
    t = d[:, 0]; dt = float(t[1] - t[0]); P = d[:, 1:4]; V = float(d[:, 4].mean())
    P = P - P.mean(axis=0)
    n = len(t); m = min(int(a.tmax / dt), n // 2)
    acf = np.zeros(m); comp = []
    for c in range(3):
        x = P[:, c]; f = np.fft.rfft(x, 2 * n); ac = np.fft.irfft(f * np.conj(f))[:m] / (n - np.arange(m))
        acf += ac / 3; comp.append(ac)
    tau = np.arange(m) * dt
    integ = np.concatenate([[0.0], np.cumsum(0.5 * (acf[1:] + acf[:-1]) * dt)])
    eta = GK * V / a.T * integ                    # mPa·s
    eta_c = [GK * V / a.T * np.concatenate([[0.0], np.cumsum(0.5 * (ac[1:] + ac[:-1]) * dt)]) for ac in comp]
    C0 = acf[0]
    # 첫 0 교차 · 평탄 판정(마지막 20 % 구간 기울기)
    zero = next((i for i in range(1, m) if acf[i] <= 0), None)
    tail = eta[int(0.8 * m):]; slope = (tail[-1] - tail[0]) / max(tail.mean(), 1e-12)
    res = {"n_samples": int(n), "dt_fs": dt, "t_total_ps": round(n * dt / 1000, 2), "V_mean_A3": round(V, 1), "T_K": a.T,
           "C0_atm2": round(float(C0), 1), "first_zero_fs": None if zero is None else round(float(tau[zero]), 1),
           "eta_running_at_tmax_mPas": round(float(eta[-1]), 4), "eta_max_mPas": round(float(eta.max()), 4), "tmax_fs": float(tau[-1]),
           "plateau_rel_slope_last20pct": round(float(slope), 3), "plateau_reached": bool(abs(slope) < 0.05),
           "note": "수십 ps 실행 — 러닝 적분의 형태(상승 → 흔들림)만 · 평탄 구간은 10~100 ns · 다중 시드에서(원본 06주차 #28)"}
    out = Path(a.out); out.mkdir(exist_ok=True)
    (out / "viscosity_gk.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    step = max(1, m // 400)
    with open(out / "gk_curve.csv", "w") as f:
        f.write("t_fs,C_norm,eta_running_mPas,eta_xy,eta_xz,eta_yz\n")
        for i in range(0, m, step): f.write(f"{tau[i]:.1f},{acf[i]/C0:.5f},{eta[i]:.6f},{eta_c[0][i]:.6f},{eta_c[1][i]:.6f},{eta_c[2][i]:.6f}\n")
    print(json.dumps(res, ensure_ascii=False))
if __name__ == "__main__": main()
