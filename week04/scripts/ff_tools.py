#!/usr/bin/env python3
"""week04 — 조합 규칙 3종 이종쌍 표 · LJ 유체 컷오프 스캔 (노트북 01 · 02 와 같은 계산).

1. mixing_table(): data/gaff2_atom_types.csv (+ clayff_lj.csv) 의 타입 쌍마다 산술(LB) · 기하 · 6제곱(WH) σ_ij · ε_ij → out/mixing_table.csv
2. cutoff_scan(): W03 과 같은 LJ 유체 64입자(탄소 ε 0.109 · σ 3.40) 를 컷오프 8 · 10 · 12 Å 로 퍼텐셜 계산 · 꼬리 보정 → out/cutoff_scan.json
단위 LAMMPS real. 수치 출처: COMID forcefield_artifacts/organic_gaff2 · data/forcefields/*.yaml (Cygan 2004) · 원본 02주차 #8 · #24
실행: python3 scripts/ff_tools.py (week04 폴더에서)
"""
import csv, json, math
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent.parent
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)


def load_types():
    T = {}
    for r in csv.DictReader(open(HERE / "data/gaff2_atom_types.csv", encoding="utf-8")):
        T[r["ff_type"]] = (float(r["epsilon_kcal_mol"]), float(r["sigma_A"]))
    for r in csv.DictReader(open(HERE / "data/clayff_lj.csv", encoding="utf-8")):
        T[r["element"] + "_clay"] = (float(r["epsilon_kcal_mol"]), float(r["sigma_A"]))
    return T


def mix(ei, si, ej, sj):
    """세 규칙. 반환 dict: lb(산술 σ · 기하 ε) · geo(기하 · 기하) · wh(6제곱 · Waldman–Hagler)"""
    s6i, s6j = si ** 6, sj ** 6
    return {"lb": ((si + sj) / 2, math.sqrt(ei * ej)),
            "geo": (math.sqrt(si * sj), math.sqrt(ei * ej)),
            "wh": (((s6i + s6j) / 2) ** (1 / 6), 2 * math.sqrt(ei * ej) * si ** 3 * sj ** 3 / (s6i + s6j))}


def mixing_table(pairs=None):
    T = load_types(); keys = sorted(T)
    rows = []
    for a in keys:
        for b in keys:
            if a > b: continue
            if pairs and (a, b) not in pairs and (b, a) not in pairs: continue
            m = mix(*T[a], *T[b])
            rows.append({"type_i": a, "type_j": b, "sigma_lb": round(m["lb"][0], 4), "eps_lb": round(m["lb"][1], 6),
                         "sigma_geo": round(m["geo"][0], 4), "eps_geo": round(m["geo"][1], 6),
                         "sigma_wh": round(m["wh"][0], 4), "eps_wh": round(m["wh"][1], 6)})
    with open(OUT / "mixing_table.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    return rows


# ---------- LJ 유체 컷오프 스캔 (W03 lj_verlet.lj_fluid 와 같은 배치 · 시드) ----------
EPS, SIG, M = 0.109, 3.40, 12.011
CONV, KB = 4.184e-4, 0.0019872


def lj_fluid_positions(n_side=4, rho=0.012, T0=300.0, seed=1, steps=300, dt=1.0, rc=8.5):
    """짧게 300스텝 돌려 격자를 흐트러뜨린 좌표를 돌려준다 (W03 노트북 02 와 같은 초기 조건)."""
    rng = np.random.default_rng(seed); N = n_side ** 3; L = (N / rho) ** (1 / 3)
    g = np.arange(n_side) * L / n_side
    pos = np.array(np.meshgrid(g, g, g, indexing="ij")).reshape(3, -1).T + L / n_side / 2
    vel = rng.normal(0, np.sqrt(KB * T0 / M * CONV), size=(N, 3)); vel -= vel.mean(axis=0)
    def forces(p):
        d = p[:, None, :] - p[None, :, :]; d -= L * np.round(d / L)
        r2 = (d ** 2).sum(-1); np.fill_diagonal(r2, np.inf); mask = r2 < rc * rc
        r2m = np.where(mask, r2, np.inf); inv6 = (SIG ** 2 / r2m) ** 3
        return (np.where(mask, 24 * EPS * (2 * inv6 ** 2 - inv6) / r2m, 0.0)[:, :, None] * d).sum(axis=1)
    a = forces(pos) / M * CONV
    for _ in range(steps):
        vel += 0.5 * a * dt; pos += vel * dt; pos %= L; a = forces(pos) / M * CONV; vel += 0.5 * a * dt
    return pos, L


def potential(pos, L, rc, shift=False):
    """최소 이미지 · 컷오프 rc 의 LJ 퍼텐셜 합. shift=True 면 U(rc) 를 빼서 불연속 제거."""
    d = pos[:, None, :] - pos[None, :, :]; d -= L * np.round(d / L)
    r2 = (d ** 2).sum(-1); iu = np.triu_indices(len(pos), 1); r2 = r2[iu]
    r2 = r2[r2 < rc * rc]; inv6 = (SIG ** 2 / r2) ** 3
    u = 4 * EPS * (inv6 ** 2 - inv6)
    if shift: u -= 4 * EPS * ((SIG / rc) ** 12 - (SIG / rc) ** 6)
    return float(u.sum()), int(len(r2))


def tail_correction(N, L, rc):
    """균일 밀도 가정 꼬리 보정 U_tail = (8/3)πNρε σ³ [ (1/3)(σ/rc)⁹ − (σ/rc)³ ]"""
    rho = N / L ** 3
    return (8 / 3) * math.pi * N * rho * EPS * SIG ** 3 * ((1 / 3) * (SIG / rc) ** 9 - (SIG / rc) ** 3)


def cutoff_scan(rcs=(6.0, 8.0, 10.0, 12.0), n_side=6):
    """n_side 6 → 216 원자 · L 26.2 Å → L/2 13.1 Å 라 컷오프 12 Å 까지 유효. 기준 = rc L/2 + 꼬리 보정.
    (W03 상자 64원자 · L 17.5 Å 는 L/2 8.7 Å 라 10 · 12 Å 컷오프를 쓸 수 없다 — 슬라이드 22 규칙 ③)"""
    pos, L = lj_fluid_positions(n_side=n_side)
    N = len(pos); ref_rc = L / 2 * 0.999          # 최소 이미지 한계 = L/2
    U_ref = potential(pos, L, ref_rc)[0] + tail_correction(N, L, ref_rc)
    res = {"N": N, "L_A": round(L, 3), "min_image_limit_A": round(L / 2, 3), "U_ref_rc_L2_plus_tail": round(U_ref, 4), "rows": []}
    for rc in rcs:
        ok = rc <= L / 2
        U, npair = potential(pos, L, min(rc, ref_rc))
        tail = tail_correction(N, L, rc)
        res["rows"].append({"rc_A": rc, "valid_rc_le_L2": ok, "pairs_in_cutoff": npair, "U_cut": round(U, 4), "U_tail": round(tail, 4),
                            "U_cut_plus_tail": round(U + tail, 4), "rel_diff_vs_ref_pct": round((U - U_ref) / abs(U_ref) * 100, 3),
                            "rel_diff_with_tail_pct": round((U + tail - U_ref) / abs(U_ref) * 100, 3)})
    (OUT / "cutoff_scan.json").write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    return res


if __name__ == "__main__":
    rows = mixing_table(); print("mixing_table.csv:", len(rows), "pairs")
    (OUT / "mixing_examples.json").write_text(json.dumps({f"{a}-{b}": {k: [round(v[0], 4), round(v[1], 6)] for k, v in mix(*load_types()[a], *load_types()[b]).items()} for a, b in [("ca", "hc"), ("ca", "O_clay"), ("ca", "Si_clay"), ("ca", "ca"), ("ca", "ss")]}, indent=1), encoding="utf-8")
    T = load_types()
    for a, b in [("ca", "hc"), ("ca", "O_clay"), ("ca", "Si_clay"), ("ca", "ca")]:
        m = mix(*T[a], *T[b]); print(f"{a}-{b}: LB σ {m['lb'][0]:.3f} ε {m['lb'][1]:.4g} · geo σ {m['geo'][0]:.3f} · WH σ {m['wh'][0]:.3f} ε {m['wh'][1]:.4g}")
    print(json.dumps(cutoff_scan(), indent=1))
