#!/usr/bin/env python3
"""week03 — velocity-Verlet 손계산 재현 · Δt 스윕 · LJ 유체 64입자 NVE (노트북 01 · 02 와 같은 계산).

무엇을 하나
  1. 탄소 원자쌍 한 스텝: U · F · a · r 전진 (덱 슬라이드 12 · 23 의 숫자) → out/lj_pair_step.json
  2. C–C 결합 1차원 진동에서 Δt 1 · 2 · 4 · 8 fs 에너지 오차 표 (슬라이드 25 와 같은 모델)
  3. LJ 유체 64입자 · 주기 상자 · NVE 1,000스텝 (numpy) → out/lj_energy.csv (step, t_fs, E_kin, E_pot, E_tot, T)
단위: LAMMPS real — Å · fs · kcal/mol · g/mol. 환산 1 (kcal/mol/Å)/(g/mol) = 4.184e-4 Å/fs² · k_B = 0.0019872 kcal/mol/K
수치 출처: 원본 02주차 덱 #8 (ε 0.109, σ 3.40, m 12.011) · #16 노트 (방향족 C–C(원본 02#16 노트 값) K 478.4, r₀ 1.387)
실행:  python3 scripts/lj_verlet.py   (week03 폴더에서)
"""
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent.parent
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
CONV = 4.184e-4            # (kcal/mol/Å) / (g/mol) → Å/fs²
KB = 0.0019872             # kcal/mol/K
EPS, SIG, M = 0.109, 3.40, 12.011


def lj_u(r): return 4 * EPS * ((SIG / r) ** 12 - (SIG / r) ** 6)
def lj_f(r): return 24 * EPS / r * (2 * (SIG / r) ** 12 - (SIG / r) ** 6)   # 양수 = 반발(바깥쪽)


# ---------- 1) 한 스텝 손계산 ----------
def pair_step(r=4.0, v=0.01, dt=1.0):
    a = lj_f(r) / M * CONV
    v_half = v + 0.5 * a * dt
    r_new = r + v_half * dt
    a_new = lj_f(r_new) / M * CONV
    v_new = v_half + 0.5 * a_new * dt
    return {"inputs": {"eps": EPS, "sigma": SIG, "m": M, "r": r, "v": v, "dt_fs": dt},
            "U_kcal_mol": round(lj_u(r), 4), "F_kcal_mol_A": round(lj_f(r), 4), "a_A_fs2": float(f"{a:.3e}"),
            "v_half": round(v_half, 8), "r_new": round(r_new, 8), "a_new": float(f"{a_new:.3e}"), "v_new": round(v_new, 8),
            "note": "덱 슬라이드 12·23: U −0.102 · F −0.0606 · a −2.11e−6 · r 4.00 → 4.01 Å"}


# ---------- 2) Δt 스윕 (C–C 결합 1차원 진동) ----------
def bond_sweep(dts=(0.5, 1, 2, 4, 6, 8), x0=0.10, tmax=300.0, K=478.4, mu=M / 2):
    omega = np.sqrt(2 * K * CONV / mu); period = 2 * np.pi / omega
    rows = []
    for dt in dts:
        x, v = x0, 0.0; a = -2 * K * x * CONV / mu; E0 = K * x * x; err = 0.0; div = False
        for _ in range(int(tmax / dt)):
            v += 0.5 * a * dt; x += v * dt; a = -2 * K * x * CONV / mu; v += 0.5 * a * dt
            E = 0.5 * mu * v * v / CONV + K * x * x
            err = max(err, abs(E - E0) / E0)
            if abs(x) > 5: div = True; break
        rows.append({"dt_fs": dt, "omega_dt": round(omega * dt, 3), "max_rel_energy_error": None if div else round(err, 5), "diverged": div})
    return {"period_fs": round(period, 1), "stability_dt_fs": round(2 / omega, 2), "rows": rows}


# ---------- 3) LJ 유체 64입자 NVE ----------
def lj_fluid(n_side=4, rho=0.012, T0=300.0, dt=1.0, steps=1000, rc=8.5, seed=1):
    """n_side³ 입자를 단순 입방 격자에 놓고 Maxwell–Boltzmann 속도로 시작. 최소 영상 규약 · 컷오프 rc (에너지 이동 보정)."""
    rng = np.random.default_rng(seed)
    N = n_side ** 3; L = (N / rho) ** (1 / 3)
    g = np.arange(n_side) * L / n_side
    pos = np.array(np.meshgrid(g, g, g, indexing="ij")).reshape(3, -1).T + L / n_side / 2
    vel = rng.normal(0, np.sqrt(KB * T0 / M * CONV), size=(N, 3)); vel -= vel.mean(axis=0)        # 중심 운동량 0
    u_rc = lj_u(rc)
    def forces(p):
        d = p[:, None, :] - p[None, :, :]; d -= L * np.round(d / L)
        r2 = (d ** 2).sum(-1); np.fill_diagonal(r2, np.inf)
        mask = r2 < rc * rc; r2m = np.where(mask, r2, np.inf)
        inv6 = (SIG ** 2 / r2m) ** 3
        u = np.where(mask, 4 * EPS * (inv6 ** 2 - inv6) - u_rc, 0.0)
        fmag = np.where(mask, 24 * EPS * (2 * inv6 ** 2 - inv6) / r2m, 0.0)
        f = (fmag[:, :, None] * d).sum(axis=1)
        return f, 0.5 * u.sum()
    f, U = forces(pos); a = f / M * CONV
    rows = []
    for s in range(steps + 1):
        K_e = 0.5 * M * (vel ** 2).sum() / CONV; T = 2 * K_e / (3 * N * KB)
        rows.append((s, s * dt, K_e, U, K_e + U, T))
        vel += 0.5 * a * dt; pos += vel * dt; pos %= L
        f, U = forces(pos); a = f / M * CONV; vel += 0.5 * a * dt
    arr = np.array(rows)
    np.savetxt(OUT / "lj_energy.csv", arr, delimiter=",", header="step,t_fs,E_kin,E_pot,E_tot,T_K", comments="", fmt=["%d", "%.1f", "%.5f", "%.5f", "%.5f", "%.2f"])
    np.savez_compressed(OUT / "lj_fluid_final.npz", pos=pos, vel=vel, L=L)
    e = arr[:, 4]; drift = (e[-1] - e[0]) / abs(e[0]) if e[0] else float("nan")
    return {"N": N, "L_A": round(L, 3), "steps": steps, "dt_fs": dt, "E0": round(e[0], 4), "E_end": round(e[-1], 4),
            "drift_rel": round(float(drift), 5), "E_std_rel": round(float(e.std() / abs(e.mean())), 5), "T_mean": round(float(arr[:, 5].mean()), 1)}


if __name__ == "__main__":
    step = pair_step(); (OUT / "lj_pair_step.json").write_text(json.dumps(step, ensure_ascii=False, indent=2), encoding="utf-8")
    sweep = bond_sweep(); (OUT / "dt_sweep.json").write_text(json.dumps(sweep, ensure_ascii=False, indent=2), encoding="utf-8")
    fluid = lj_fluid(); (OUT / "lj_fluid_summary.json").write_text(json.dumps(fluid, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"pair_step": step, "dt_sweep": sweep, "fluid": fluid}, ensure_ascii=False, indent=2))
