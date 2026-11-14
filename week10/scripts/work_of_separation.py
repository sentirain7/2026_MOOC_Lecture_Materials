#!/usr/bin/env python3
"""week10 — 인장 기록(pull.csv)에서 분리일 두 경로를 계산한다.

경로 1 · 역학(힘–거리 적분)  W_mech = ∫ σ(d) dd   (MPa·Å → mJ/m² : 1 MPa·Å = 0.1 mJ/m²)   — 원본 06주차 보충A #15 「경로 2」
경로 2 · 에너지(같은 좌표 규약)  W_E = (⟨E_sep⟩ − ⟨E_int⟩) / A   (kcal/mol/Å² → mJ/m² : × 694.77)  — 원본 #12 · #13 · 계면 상태 = 처음 10 % 구간 평균 · 분리 상태 = 마지막 10 % 구간 평균
두 값이 같은 크기이면 검산 통과 · 다르면 어느 규약인지 보고서에 적는다(변형 에너지 · 열 요동 · 미분리).
실행: python3 scripts/work_of_separation.py out/wet/pull.csv [--area 627.1] [--smooth 9]
출력: out/<tag>/wsep.json · 표준 출력 요약
"""
import argparse, csv, json, math, statistics as st
from pathlib import Path
KCAL_A2_TO_MJ_M2 = 694.77   # 1 kcal/mol/Å² = 694.77 mJ/m²


def load(path):
    rows = list(csv.DictReader(open(path)))
    return [{k: float(v) for k, v in r.items()} for r in rows]


def smooth(y, w):
    if w <= 1: return y[:]
    h = w // 2; out = []
    for i in range(len(y)):
        a, b = max(0, i - h), min(len(y), i + h + 1); out.append(sum(y[a:b]) / (b - a))
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("csv"); ap.add_argument("--area", type=float, default=None); ap.add_argument("--smooth", type=int, default=9)
    a = ap.parse_args(); p = Path(a.csv); rows = load(p)
    summ = json.loads((p.parent / "pull_summary.json").read_text()); A = a.area or summ["area_A2"]
    d = [r["disp_A"] for r in rows]; sig = smooth([r["sigma_MPa"] for r in rows], a.smooth); pe = [r["pe_kcal_mol"] for r in rows]
    # 경로 1: 사다리꼴 적분 (양의 응력만 · 음수 = 압축 반력은 0 으로)
    W = 0.0; cum = []
    for i in range(1, len(d)):
        s0, s1 = max(0.0, sig[i - 1]), max(0.0, sig[i]); W += 0.5 * (s0 + s1) * (d[i] - d[i - 1]); cum.append(W * 0.1)
    ip = max([i for i in range(len(sig)) if d[i] >= 0.5] or [0], key=lambda i: sig[i])   # 처음 0.5 Å 의 시작 충격은 피크에서 제외
    # 경로 2: 에너지 차 (처음 10 % ↔ 마지막 10 %)
    n = len(pe); k = max(3, n // 10)
    e_int, e_sep = st.mean(pe[:k]), st.mean(pe[-k:]); sd_int, sd_sep = st.pstdev(pe[:k]), st.pstdev(pe[-k:])
    W_E = (e_sep - e_int) / A * KCAL_A2_TO_MJ_M2
    # 분리 판정: 응력이 피크의 10 % 아래로 떨어진 첫 변위
    d_sep = next((d[i] for i in range(ip, len(sig)) if sig[i] < 0.1 * sig[ip]), None)
    out = dict(tag=summ["tag"], area_A2=A, n_rows=n, sigma_peak_MPa=round(sig[ip], 1), d_peak_A=round(d[ip], 2), d_separation_A=(round(d_sep, 2) if d_sep else None),
               W_mech_mJ_m2=round(W * 0.1, 1), W_energy_mJ_m2=round(W_E, 1), E_int_kcal_mol=round(e_int, 1), E_sep_kcal_mol=round(e_sep, 1),
               E_sd_int=round(sd_int, 1), E_sd_sep=round(sd_sep, 1), E_window_rows=k, note="W_mech = ∫σ dd (σ<0 은 0) · W_E = (E_sep − E_int)/A · 열 요동 sd 가 ΔE 와 비슷하면 에너지법은 신뢰 불가(짧은 교육용 실행)",
               cumulative_W_mJ_m2=[round(x, 2) for x in cum[:: max(1, len(cum) // 60)]])
    (p.parent / "wsep.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(f"{summ['tag']}: σ_peak {out['sigma_peak_MPa']} MPa @ {out['d_peak_A']} Å · 분리 {out['d_separation_A']} Å · W_mech {out['W_mech_mJ_m2']} mJ/m² · W_E {out['W_energy_mJ_m2']} mJ/m² (sd {out['E_sd_int']}/{out['E_sd_sep']})")


if __name__ == "__main__":
    main()
