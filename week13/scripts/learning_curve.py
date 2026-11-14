#!/usr/bin/env python3
"""학습 곡선: 학습 표본 수 → 학습 · 검증 RMSE (조건 그룹 5겹 · 선형 · 숲).
  python3 scripts/learning_curve.py   → out/learning_curve.json"""
import warnings
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GroupKFold
from common import load, metrics, save, SEED

warnings.filterwarnings("ignore")
FRACS = [0.1, 0.2, 0.3, 0.5, 0.7, 1.0]


def main():
    d, X, y = load()
    rng = np.random.default_rng(SEED)
    out = {"fracs": FRACS, "models": {}}
    for name, mk in {"linear": LinearRegression, "forest": lambda: RandomForestRegressor(200, random_state=SEED, n_jobs=1)}.items():
        rows = []
        for f in FRACS:
            tr_r, va_r, ns = [], [], []
            for tr, va in GroupKFold(5).split(X, y, d.cond):
                conds = d.cond.iloc[tr].unique(); keep = rng.permutation(conds)[: max(2, int(round(len(conds) * f)))]
                sub = tr[np.isin(d.cond.iloc[tr], keep)]
                m = mk().fit(X[sub], y[sub])
                tr_r.append(metrics(y[sub], m.predict(X[sub]))["rmse"]); va_r.append(metrics(y[va], m.predict(X[va]))["rmse"]); ns.append(len(sub))
            rows.append({"frac": f, "n_train": int(np.mean(ns)), "train_rmse": round(float(np.mean(tr_r)), 5), "val_rmse": round(float(np.mean(va_r)), 5)})
            print(name, rows[-1])
        out["models"][name] = rows
    save("learning_curve.json", out)


if __name__ == "__main__":
    main()
