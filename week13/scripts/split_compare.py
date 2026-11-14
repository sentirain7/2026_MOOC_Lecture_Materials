#!/usr/bin/env python3
"""같은 모델 4종 · 같은 데이터 · 분할만 4가지 → RMSE · MAE · R² 표 + 누수 지표.
  python3 scripts/split_compare.py [--target density|ced] [--cells core|all]   → out/split_compare[_ced].json
분할 4: random(행 무작위 80/20 · 20회 반복 평균) · cond(조건 그룹 = 셀@온도 단위 80/20 · 20회)
        · loago(노화 상태 1종 빼기 · 3겹) · t_extrap(온도 133 · 153 · 413 · 433 K 시험)
누수 지표 = 시험 행 중 같은 셀@온도(시드만 다른 쌍둥이)가 학습에도 있는 비율."""
import argparse, warnings
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import ShuffleSplit, GroupShuffleSplit
from common import load, metrics, save, SEED

warnings.filterwarnings("ignore")
MODELS = {
    "linear": lambda: LinearRegression(),
    "tree_d4": lambda: DecisionTreeRegressor(max_depth=4, random_state=SEED),
    "tree_full": lambda: DecisionTreeRegressor(random_state=SEED),
    "forest": lambda: RandomForestRegressor(n_estimators=200, random_state=SEED, n_jobs=1),
}
REPEAT = 20


def splits(d):
    idx = np.arange(len(d))
    yield "random", list(ShuffleSplit(REPEAT, test_size=0.2, random_state=SEED).split(idx)), True
    yield "cond", list(GroupShuffleSplit(REPEAT, test_size=0.2, random_state=SEED).split(idx, groups=d.cond)), True
    yield "loago", [(idx[d.aging != k], idx[d.aging == k]) for k in sorted(d.aging.unique())], False
    hold = d.T_K.isin([133, 153, 413, 433]).to_numpy()
    yield "t_extrap", [(idx[~hold], idx[hold])], False


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--target", default="density"); ap.add_argument("--cells", default="core"); a = ap.parse_args()
    d, X, y = load(a.target, a.cells)
    sd = d.groupby("cond")[a.target].std()
    res = {"target": a.target, "cells": a.cells, "n_rows": len(d), "n_cells": int(d.cell.nunique()), "n_cond": int(d.cond.nunique()),
           "y_range": [round(float(y.min()), 5), round(float(y.max()), 5)], "y_sd": round(float(y.std()), 5),
           "md_seed_sd": {"median": round(float(sd.median()), 5), "mean": round(float(sd.mean()), 5)}, "repeat": REPEAT, "splits": {}}
    for sname, folds, repeated in splits(d):
        leak = [float(np.mean([c in set(d.cond.iloc[tr]) for c in d.cond.iloc[te]])) for tr, te in folds]
        row = {"folds": len(folds), "repeated": repeated, "n_test": int(len(folds[0][1])), "leak_frac": round(float(np.mean(leak)), 3), "models": {}}
        for mname, mk in MODELS.items():
            per, ys, ps, tr_rmse = [], [], [], []
            for tr, te in folds:
                m = mk().fit(X[tr], y[tr]); p = m.predict(X[te])
                per.append(metrics(y[te], p)); ys.append(y[te]); ps.append(p)
                tr_rmse.append(metrics(y[tr], m.predict(X[tr]))["rmse"])
            if repeated:     # 반복 분할: 회차별 지표의 평균 ± 표준편차
                agg = {k: round(float(np.mean([q[k] for q in per])), 5 if k != "r2" else 3) for k in ("rmse", "mae", "r2")}
                agg.update({"rmse_sd": round(float(np.std([q["rmse"] for q in per])), 5), "r2_sd": round(float(np.std([q["r2"] for q in per])), 3),
                            "sd_y": round(float(np.mean([q["sd_y"] for q in per])), 5), "n": per[0]["n"]})
            else:            # 겹(fold) 분할: 시험 점을 모아 한 번에
                agg = metrics(np.concatenate(ys), np.concatenate(ps))
            agg["train_rmse"] = round(float(np.mean(tr_rmse)), 5)
            agg["fold_r2"] = [q["r2"] for q in per] if not repeated else None
            row["models"][mname] = agg
        res["splits"][sname] = row
        print(f"{sname:9s} leak {row['leak_frac']:.2f} · " + " · ".join(f"{k} {v['rmse']:.4f}/{v['r2']:.3f}" for k, v in row["models"].items()))
    # 파리티 점 2벌(슬라이드 지표 계산기 · 바꿔 보기): random 1회차 · loago(장기 노화 빼기) — forest
    tr, te = next(ShuffleSplit(1, test_size=0.2, random_state=SEED).split(np.arange(len(d))))
    m = MODELS["forest"]().fit(X[tr], y[tr])
    res["parity_random_forest"] = {"y": [round(v, 5) for v in y[te]], "p": [round(v, 5) for v in m.predict(X[te])], "T": d.T_K.iloc[te].tolist(), "aging": d.aging.iloc[te].tolist()}
    idx = np.arange(len(d)); tr, te = idx[d.aging != 2], idx[d.aging == 2]
    m = MODELS["forest"]().fit(X[tr], y[tr])
    res["parity_loago2_forest"] = {"y": [round(v, 5) for v in y[te]], "p": [round(v, 5) for v in m.predict(X[te])], "T": d.T_K.iloc[te].tolist()}
    save("split_compare.json" if a.target == "density" else f"split_compare_{a.target}.json", res)


if __name__ == "__main__":
    main()
