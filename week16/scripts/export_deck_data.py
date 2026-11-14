#!/usr/bin/env python3
"""W16 · 덱 데이터 내보내기 — 스크립트 결과 JSON 5개를 덱(slides/W16_*.html)이 읽는 한 파일로 묶는다. 새 값은 만들지 않는다.

  python3 scripts/export_deck_data.py out --out out/w16_deck_data.json
입력: curation.json · pareto.json · ehvi.json · md_vs_exp.json · checklist.json (같은 폴더)
"""
import argparse, json, os

ap = argparse.ArgumentParser(); ap.add_argument("src", nargs="?", default="out"); ap.add_argument("--out", default="out/w16_deck_data.json"); a = ap.parse_args()
L = lambda n: json.load(open(os.path.join(a.src, n), encoding="utf-8"))
p, e, m, c, k = L("pareto.json"), L("ehvi.json"), L("md_vs_exp.json"), L("curation.json"), L("checklist.json")
keep = ["n_obs", "n_cand", "holdout_rmse", "hv_obs", "front_obs", "picks", "top12_first_round", "hv_after_true",
        "hv_gain_ehvi", "hv_gain_random_mean", "hv_gain_random_p_ge", "candidates_all"]
D = dict(pts=p["points"], front=p["front"], hv=p["hv"], hv_alt=p["hv_alt_ref"], traj=p["trajectory"], ref=p["ref"],
         ehvi={x: e[x] for x in keep}, dens=m["density"], tg=m["tg"], mc=m["mastercurve"], cur=c["stages"], check=k)
json.dump(D, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print(a.out, os.path.getsize(a.out), "B")
