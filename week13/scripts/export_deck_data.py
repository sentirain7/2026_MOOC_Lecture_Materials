#!/usr/bin/env python3
"""덱(slides/W13_*.html)에 넣을 값 한 벌 → out/deck_data.json. 다른 스크립트의 out/*.json 을 모으고
선형 · 나무의 온도 외삽 곡선(비노화 · 133~433 K)을 계산한다.  python3 scripts/export_deck_data.py"""
import json, warnings
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from common import load, save, OUT, SEED, FEATURES

warnings.filterwarnings("ignore")


def rd(p): return json.loads((OUT / p).read_text(encoding="utf-8"))


def main():
    d, X, y = load()
    cond = d.groupby(["cell", "T_K"]).agg(n=("density", "size"), mean=("density", "mean"), sd=("density", "std")).reset_index()
    # 온도 외삽: 학습 173~393 K → 133 · 153 · 413 · 433 K 예측 (비노화 · 특징 6개 그대로)
    hold = d.T_K.isin([133, 153, 413, 433]).to_numpy()
    lin = LinearRegression().fit(X[~hold], y[~hold]); tr = DecisionTreeRegressor(max_depth=4, random_state=SEED).fit(X[~hold], y[~hold])
    Ts = sorted(d.T_K.unique()); grid = np.array([[0, t, 0, 0, 0, 0] for t in Ts], float)
    obs = d[d.aging == 0].groupby("T_K").density.mean()
    extrap = {"T": [int(t) for t in Ts], "obs": [round(float(obs[t]), 5) for t in Ts],
              "linear": [round(float(v), 5) for v in lin.predict(grid)], "tree_d4": [round(float(v), 5) for v in tr.predict(grid)],
              "train_range": [173, 393]}
    out = {"n_rows": len(d), "cells": sorted(d.cell.unique()), "T_levels": [int(t) for t in Ts],
           "cond": [[r.cell, int(r.T_K), int(r.n), round(float(r.mean), 5), None if np.isnan(r.sd) else round(float(r.sd), 5)] for r in cond.itertuples()],
           "split_density": rd("split_compare.json"), "split_bulk": rd("split_compare_bulk_modulus.json"), "split_ced": rd("split_compare_ced.json"),
           "tree2d": rd("tree2d.json"), "depth": rd("tree_depth.json"), "learning": rd("learning_curve.json"), "extrap": extrap, "features": FEATURES}
    save("deck_data.json", out)
    print("size", (OUT / "deck_data.json").stat().st_size)


if __name__ == "__main__":
    main()
