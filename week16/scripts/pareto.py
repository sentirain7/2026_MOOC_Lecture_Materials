#!/usr/bin/env python3
"""W16 · 파레토 전선 · 초부피(HV) — 두 목표 모두 최대화(체적탄성계수 K GPa · CED MJ/m³).
점을 고정 난수 순서로 하나씩 넣으며 전선 · HV 를 갱신한 기록도 남긴다(덱 애니의 입력).

  python3 scripts/pareto.py out/curated612.csv --ref 1.0,250 --out out/pareto.json
원본 13주차 #7 · #8: 참조점 (1.0 GPa, 250 MJ/m³) · 612건 전선 6점.
"""
import argparse, csv, json, random

def front(P):
    """두 목표 최대화 · 비지배 점 (K 내림차순 정렬 후 CED 최고 갱신)"""
    S = sorted(P, key=lambda p: (-p[0], -p[1])); F, best = [], -1e18
    for p in S:
        if p[1] > best: F.append(p); best = p[1]
    return F

def hv(F, ref):
    """전선이 지배하는 면적(참조점 위 · 오른쪽) — F 는 K 내림차순"""
    area, prev = 0.0, ref[1]
    for p in sorted(F, key=lambda p: -p[0]):
        k, c = p[0], p[1]
        if k <= ref[0] or c <= prev: continue
        area += (k - ref[0]) * (c - prev); prev = c
    return area

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("--ref", default="1.0,250")
    ap.add_argument("--out", default="out/pareto.json"); ap.add_argument("--seed", type=int, default=7); ap.add_argument("--first", type=int, default=20)
    a = ap.parse_args(); ref = tuple(map(float, a.ref.split(",")))
    R = list(csv.DictReader(open(a.src, encoding="utf-8")))
    P = [(float(r["bulk_modulus"]), float(r["cohesive_energy_density"]), r["binder_type"], r["additive_type"], r["aging_state"], float(r["temperature_K"])) for r in R]
    F = front(P); H = hv(F, ref)
    order = list(range(len(P))); random.Random(a.seed).shuffle(order)
    traj, cur = [], []
    for i, j in enumerate(order):
        cur.append(P[j])
        if i + 1 >= a.first and (i + 1 in (20, 30, 50, 100, 200, 300, 400, 500) or i + 1 == len(P) or i < 60):
            Fi = front(cur); traj.append({"n": i + 1, "front_n": len(Fi), "hv": round(hv(Fi, ref), 2)})
    alt = (3.0, 350.0)
    res = {"n": len(P), "ref": ref, "objectives": ["bulk_modulus_GPa (max)", "CED_MJm3 (max)"],
           "front": [dict(K=round(p[0], 3), CED=round(p[1], 1), binder=p[2], additive=p[3], aging=p[4], T_K=p[5]) for p in F],
           "hv": round(H, 2), "hv_alt_ref": {"ref": alt, "hv": round(hv(F, alt), 2)}, "order_seed": a.seed, "trajectory": traj,
           "points": [[round(p[0], 3), round(p[1], 1)] for p in (P[j] for j in order)]}
    json.dump(res, open(a.out, "w", encoding="utf-8"), ensure_ascii=False)
    print(f"n={len(P)} front={len(F)} HV={H:.2f} (ref {ref}) · ref {alt} → HV={res['hv_alt_ref']['hv']}")
    for p in F: print(f"  K {p[0]:.3f}  CED {p[1]:.1f}  {p[2]} {p[3]} {p[4]} {p[5]:.0f} K")
