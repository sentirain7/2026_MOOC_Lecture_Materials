#!/usr/bin/env python3
"""week05 — 조절기 3종 비교 · 평형 판정 · 블록 평균 · 자기상관 (노트북 01 · 02 와 같은 계산).

1. thermostats(): W03 과 같은 LJ 유체 64입자(탄소 ε 0.109 · σ 3.40 · real 단위)를 velocity rescale · Berendsen · Langevin 으로 각 2,000스텝 NVT
   → out/thermostat_sigma.csv (조절기 · 평균 T · σ_T · 기대 σ_T = T0·√(2/(3N)) · 도달 스텝)
2. equilibration(): 온도 시계열(data/T_series_week03.csv) → t_eq 탐색(전반 · 후반 평균 차 < 2 SE) · 블록 평균 SE(b) · 자기상관 C(τ) · τ_c · N_eff → out/block_stats.json
수치 출처: 조절기 식 = 원본 03주차 #23 · 판정 기준 = 03#27 · C(τ) · N_eff = 03#29 · 시계열 = week03 lj_energy.csv
실행: python3 scripts/md_stats.py (week05 폴더에서)
"""
import csv, json, math
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent.parent
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
EPS, SIG, M = 0.109, 3.40, 12.011
CONV, KB = 4.184e-4, 0.0019872


class LJFluid:
    """W03 lj_verlet.lj_fluid 와 같은 계 · 조절기만 추가."""
    def __init__(self, n_side=4, rho=0.012, T0=300.0, rc=8.5, seed=1):
        rng = np.random.default_rng(seed); self.N = n_side ** 3; self.L = (self.N / rho) ** (1 / 3); self.rc = rc; self.rng = rng
        g = np.arange(n_side) * self.L / n_side
        self.pos = np.array(np.meshgrid(g, g, g, indexing="ij")).reshape(3, -1).T + self.L / n_side / 2
        self.vel = rng.normal(0, np.sqrt(KB * T0 / M * CONV), size=(self.N, 3)); self.vel -= self.vel.mean(axis=0)
        self.u_rc = 4 * EPS * ((SIG / rc) ** 12 - (SIG / rc) ** 6)
        self.f, self.U = self.forces()
    def forces(self):
        d = self.pos[:, None, :] - self.pos[None, :, :]; d -= self.L * np.round(d / self.L)
        r2 = (d ** 2).sum(-1); np.fill_diagonal(r2, np.inf); mask = r2 < self.rc ** 2; r2m = np.where(mask, r2, np.inf)
        inv6 = (SIG ** 2 / r2m) ** 3
        u = np.where(mask, 4 * EPS * (inv6 ** 2 - inv6) - self.u_rc, 0.0)
        fmag = np.where(mask, 24 * EPS * (2 * inv6 ** 2 - inv6) / r2m, 0.0)
        return (fmag[:, :, None] * d).sum(axis=1), 0.5 * u.sum()
    def T(self): return M * (self.vel ** 2).sum() / CONV / (3 * self.N * KB)
    def step(self, dt=1.0, thermo=None, T0=300.0, tau=100.0, gamma=0.01):
        a = self.f / M * CONV
        self.vel += 0.5 * a * dt; self.pos += self.vel * dt; self.pos %= self.L
        self.f, self.U = self.forces(); a = self.f / M * CONV; self.vel += 0.5 * a * dt
        T = self.T()
        if thermo == "rescale":                       # 속도 비례 조정 λ = √(T0/T)
            self.vel *= math.sqrt(T0 / max(T, 1e-9))
        elif thermo == "berendsen":                   # λ = [1 + (dt/τ)(T0/T − 1)]^½  (원본 03#23)
            self.vel *= math.sqrt(1 + dt / tau * (T0 / max(T, 1e-9) - 1))
        elif thermo == "langevin":                    # dv = (F/m − γv)dt + √(2γ k_B T0/m) dW
            sig = math.sqrt(2 * gamma * KB * T0 / M * CONV * dt)
            self.vel += (-gamma * self.vel * dt + sig * self.rng.normal(size=self.vel.shape))


def thermostats(T0=300.0, steps=2000, dt=1.0):
    rows = []
    for name in ["none(NVE)", "rescale", "berendsen", "langevin"]:
        s = LJFluid(T0=T0, seed=1); Ts = []
        for i in range(steps):
            s.step(dt, None if name.startswith("none") else name, T0=T0, tau=100.0, gamma=0.01); Ts.append(s.T())
        Ts = np.array(Ts); tail = Ts[steps // 2:]
        reach = next((i for i, t in enumerate(Ts) if abs(t - T0) < T0 * math.sqrt(2 / (3 * s.N))), None)
        rows.append({"thermostat": name, "T_mean_tail": round(float(tail.mean()), 2), "sigma_T_tail": round(float(tail.std()), 2),
                     "sigma_T_expected_canonical": round(T0 * math.sqrt(2 / (3 * s.N)), 2), "reach_step": reach})
        np.savetxt(OUT / f"T_{name.split('(')[0]}.csv", Ts, fmt="%.3f", header="T_K", comments="")
    with open(OUT / "thermostat_sigma.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    return rows


# ---------- 평형 판정 · 블록 평균 · 자기상관 (원본 03#27 · #29) ----------
def block_se(x, b):
    n = len(x) // b
    if n < 2: return float("nan")
    m = x[: n * b].reshape(n, b).mean(axis=1)
    return float(m.std(ddof=1) / math.sqrt(n))


def autocorr(x, kmax=200):
    x = x - x.mean(); den = float(np.dot(x, x))
    return np.array([np.dot(x[: len(x) - k], x[k:]) / den for k in range(kmax)])


def equilibration(path=None, teq_grid=range(0, 600, 20)):
    d = np.loadtxt(path or HERE / "data/T_series_week03.csv", delimiter=",", skiprows=1); T = d[:, 5]
    # t_eq: 폐기 구간을 늘리며 전반 · 후반 평균 차 < 2 SE(블록 50) 가 처음 성립하는 지점
    # 기준(03#27 ①②): 폐기 구간 t0 를 늘리며, 직후 100스텝 평균과 나머지 평균의 차가 2 SE(블록 20) 안에 처음 드는 t0
    teq = None
    for t0 in teq_grid:
        x = T[t0:]; a, b = x[:100], x[100:]
        se = math.hypot(block_se(a, 20), block_se(b, 20))
        if abs(a.mean() - b.mean()) < 2 * se: teq = t0; break
    x = T[teq or 0:]
    blocks = [1, 2, 5, 10, 20, 50, 100, 200]
    se = {b: block_se(x, b) for b in blocks}
    ac = autocorr(x); first0 = int(np.argmax(ac < 0)); tau_c = 0.5 + float(ac[1:first0].sum())
    neff = len(x) / (2 * tau_c)
    res = {"n_total": int(len(T)), "t_eq_step": teq, "n_used": int(len(x)), "mean_T": round(float(x.mean()), 2), "std_T": round(float(x.std()), 2),
           "se_naive": round(float(x.std(ddof=1) / math.sqrt(len(x))), 3), "se_block": {str(b): round(v, 3) for b, v in se.items()},
           "tau_c_steps": round(tau_c, 1), "n_eff": round(neff, 1), "se_from_neff": round(float(x.std(ddof=1) / math.sqrt(neff)), 3),
           "autocorr_first_zero_step": first0}
    (OUT / "block_stats.json").write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    np.savetxt(OUT / "autocorr.csv", np.c_[np.arange(len(ac)), ac], delimiter=",", header="lag_step,C", comments="", fmt=["%d", "%.4f"])
    return res


if __name__ == "__main__":
    print(json.dumps(thermostats(), indent=1))
    print(json.dumps(equilibration(), indent=1))
