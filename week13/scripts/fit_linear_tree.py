#!/usr/bin/env python3
"""선형 → 트리 → 숲. ① 나무 깊이 1~12 의 학습 · 검증 RMSE(과적합 곡선 · 조건 그룹 5겹)
② 특징 2개(T_K · aging)만 쓰는 깊이 3 나무의 분할선 · 잎 값(슬라이드 분할 애니) ③ 선형 계수.
  python3 scripts/fit_linear_tree.py   → out/tree_depth.json · out/tree2d.json"""
import warnings
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GroupKFold, KFold
from common import load, metrics, save, SEED, FEATURES

warnings.filterwarnings("ignore")


def depth_sweep(d, X, y, cv, groups=None):
    rows = []
    for depth in range(1, 13):
        tr_r, va_r = [], []
        for tr, va in cv.split(X, y, groups):
            m = DecisionTreeRegressor(max_depth=depth, random_state=SEED).fit(X[tr], y[tr])
            tr_r.append(metrics(y[tr], m.predict(X[tr]))["rmse"]); va_r.append(metrics(y[va], m.predict(X[va]))["rmse"])
        rows.append({"depth": depth, "train_rmse": round(float(np.mean(tr_r)), 5), "val_rmse": round(float(np.mean(va_r)), 5),
                     "n_leaves": int(DecisionTreeRegressor(max_depth=depth, random_state=SEED).fit(X, y).get_n_leaves())})
    return rows


def tree_struct(m, names):
    t = m.tree_; nodes = []
    for i in range(t.node_count):
        leaf = t.children_left[i] == -1
        nodes.append({"id": i, "leaf": bool(leaf), "feature": None if leaf else names[t.feature[i]],
                      "thr": None if leaf else round(float(t.threshold[i]), 3), "left": int(t.children_left[i]), "right": int(t.children_right[i]),
                      "value": round(float(t.value[i][0][0]), 5), "n": int(t.n_node_samples[i])})
    return nodes


def main():
    d, X, y = load()
    lin = LinearRegression().fit(X, y)
    coef = {f: round(float(c), 6) for f, c in zip(FEATURES, lin.coef_) if abs(c) > 0}
    sweeps = {}
    for tgt in ("density", "ced", "bulk_modulus"):        # 시드 잡음이 큰 물성(체적탄성률)일수록 과적합이 잘 보인다
        dt, Xt, yt = load(tgt)
        g = depth_sweep(dt, Xt, yt, GroupKFold(5), dt.cond)
        r = depth_sweep(dt, Xt, yt, KFold(5, shuffle=True, random_state=SEED))
        best = min(g, key=lambda q: q["val_rmse"])
        sweeps[tgt] = {"group": g, "random_kfold": r, "best": best, "y_sd": round(float(yt.std()), 5),
                       "md_seed_sd_median": round(float(dt.groupby("cond")[tgt].std().median()), 5)}
        print(tgt, "best depth (group CV)", best["depth"], best["val_rmse"], "· depth 12 val", g[-1]["val_rmse"], "train", g[-1]["train_rmse"])
    save("tree_depth.json", {"cv": "GroupKFold(5) by cell@T · KFold(5) 무작위 비교", "targets": sweeps,
                             "linear_coef_density": coef, "linear_intercept_density": round(float(lin.intercept_), 5)})
    # 2D 나무: T_K · aging 두 특징 · 깊이 3 → 분할선
    X2 = d[["T_K", "aging"]].to_numpy(float)
    t2 = DecisionTreeRegressor(max_depth=3, random_state=SEED).fit(X2, y)
    pts = d.groupby(["T_K", "aging"]).density.mean().reset_index()
    save("tree2d.json", {"features": ["T_K", "aging"], "depth": 3, "nodes": tree_struct(t2, ["T_K", "aging"]),
                         "train": metrics(y, t2.predict(X2)), "points": [[int(a), int(b), round(c, 5)] for a, b, c in pts.itertuples(index=False)]})


if __name__ == "__main__":
    main()
