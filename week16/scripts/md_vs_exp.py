#!/usr/bin/env python3
"""W16 · MD ↔ 실측 대조 — 밀도 짝 28점(정량) · Tg 실험–MD 8쌍(방향) · 마스터커브 시간축 간격 Δ(형상).
원본 13주차 #24~#32 의 대조 방식: 밀도 = 짝지은 정량 · Tg = 절대값 대신 방향 · 강성 = 시간축 정합 후 형상.

  python3 scripts/md_vs_exp.py data/density_match28.csv data/tg_pairs8.csv --delta data/an116_exp_unified.json --out out/md_vs_exp.json
값의 구분: exp = 측정값(문헌 실측 · 12편) · md = 본연구 MD 계산값 · Tg 쌍 = 문헌값(같은 논문의 DSC 와 MD) · Δ = COMID AN116 정합 결과.
"""
import argparse, csv, json, statistics as st

ap = argparse.ArgumentParser(); ap.add_argument("dens"); ap.add_argument("tg"); ap.add_argument("--delta", default=None); ap.add_argument("--out", default="out/md_vs_exp.json")
a = ap.parse_args()
D = list(csv.DictReader(open(a.dens, encoding="utf-8")))
pts = [dict(exp=float(r["exp_density"]), md=float(r["our_MD"]), T_exp_K=float(r["exp_T_K"]), T_md_K=float(r["our_T_K"]), additive=r["additive"],
            rel=(float(r["our_MD"]) - float(r["exp_density"])) / float(r["exp_density"]) * 100) for r in D]
rel_abs = [abs(p["rel"]) for p in pts]; dev = [p["md"] - p["exp"] for p in pts]
by_T = {}
for p in pts: by_T.setdefault(p["T_md_K"], []).append(p)
dens = {"n": len(pts), "papers": "12편(원본 13주차 #25)", "median_abs_rel_pct": round(st.median(rel_abs), 2), "mae_gcc": round(st.mean(abs(x) for x in dev), 3),
        "mean_dev_gcc": round(st.mean(dev), 3), "median_signed_rel_pct": round(st.median(p["rel"] for p in pts), 2),
        "n_md_lower": sum(x < 0 for x in dev), "n_md_higher": sum(x > 0 for x in dev),
        "by_T": {str(int(k)): dict(n=len(v), exp_median=round(st.median(p["exp"] for p in v), 3), md=round(st.median(p["md"] for p in v), 3)) for k, v in sorted(by_T.items())},
        "points": [[p["exp"], p["md"], round(p["rel"], 2), int(p["T_md_K"]), p["additive"]] for p in pts]}
T = list(csv.DictReader(open(a.tg, encoding="utf-8")))
tg = {"n": len(T), "source": "jclepro.2023.139092 (같은 논문의 DSC · MD · 문헌값)",
      "pairs": [dict(sample=r["sample"], group=r["group"], exp_K=round(float(r["exp_K"]), 1), md_K=round(float(r["md_K"]), 1), diff_K=round(float(r["diff_K"]), 1)) for r in T]}
tg["diff_range_K"] = [round(min(p["diff_K"] for p in tg["pairs"]), 1), round(max(p["diff_K"] for p in tg["pairs"]), 1)]
aged = [p for p in tg["pairs"] if p["group"] == "aged-series"]
tg["aged_direction_same"] = (aged[-1]["exp_K"] > aged[0]["exp_K"]) == (aged[-1]["md_K"] > aged[0]["md_K"])
res = {"density": dens, "tg": tg}
if a.delta:
    d = json.load(open(a.delta, encoding="utf-8")); res["mastercurve"] = {"delta_decade": round(d["DELTA_log10"], 2), "delta_sd": round(d["DELTA_sd"], 2), "source": "COMID AN116 · S64-22 DSR · BBR ↔ AAA-1 G(t) 387점"}
json.dump(res, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"밀도 {dens['n']}점 · 중앙 |상대오차| {dens['median_abs_rel_pct']} % · MAE {dens['mae_gcc']} · 평균 편차 {dens['mean_dev_gcc']} · MD 낮음 {dens['n_md_lower']}/{dens['n']}")
print(f"Tg {tg['n']}쌍 · MD − 실험 {tg['diff_range_K'][0]} ~ {tg['diff_range_K'][1]} K · 노화 방향 일치 {tg['aged_direction_same']}")
if a.delta: print(f"마스터커브 Δ = {res['mastercurve']['delta_decade']} ± {res['mastercurve']['delta_sd']} decade")
