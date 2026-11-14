"""④ 대리모델: 결과 표(SARA 3변수 → 밀도 · CED) 학습 → 후보마다 평균 μ · 불확실성 σ.

모델 3종 (loop.yaml 의 model)
  gp  가우스 과정(W15): 상수 × RBF(길이 하나) + 백색 잡음 · σ = 사후 표준편차 · 데이터가 적을 때(≤ 30) 기본
      (관측 6 ~ 12개로 변수 5개의 길이를 따로 맞추면 과적합 → 길이 하나 · 기술자는 표준화해서 같은 척도)
  rf  랜덤 포레스트(W13): 나무 300 그루 · σ = 나무들 예측의 표준편차
  xgb XGBoost 앙상블(W14): 시드 5개 · 표본 80 % · σ = 다섯 모델 예측의 표준편차
고르는 기준: 단일 제외 교차검증(LOO) RMSE 와 보정(|오차| ≤ σ 비율 ≈ 68 %)을 함께 본다 → compare 로 세 모델 표
입력 = 후보 분자의 RDKit 기술자(loop.yaml design.features) · 출력 = 밀도 · CED (따로 학습)
  python scripts/surrogate.py compare        # 세 모델 LOO 표 → ws/<name>/model_compare.json
"""
import argparse
import numpy as np
from common import load_cfg, ws, results, xy, OBJ, dump


def fit_predict(model, X, y, Xq, seed=0):
    mx, sx = X.mean(0), X.std(0) + 1e-9; my, sy = y.mean(), y.std() + 1e-12
    Z, Zq, t = (X - mx) / sx, (Xq - mx) / sx, (y - my) / sy
    if model == "gp":
        from sklearn.gaussian_process import GaussianProcessRegressor
        from sklearn.gaussian_process.kernels import RBF, WhiteKernel, ConstantKernel
        k = ConstantKernel(1.0, (1e-2, 1e2)) * RBF(1.0, (1e-1, 1e2)) + WhiteKernel(0.01, (1e-4, 1.0))
        g = GaussianProcessRegressor(k, normalize_y=False, random_state=seed, n_restarts_optimizer=3).fit(Z, t)
        m, s = g.predict(Zq, return_std=True)
    elif model == "rf":
        from sklearn.ensemble import RandomForestRegressor
        f = RandomForestRegressor(300, min_samples_leaf=1, random_state=seed).fit(Z, t)
        P = np.stack([e.predict(Zq) for e in f.estimators_]); m, s = P.mean(0), P.std(0)
    elif model == "xgb":
        from xgboost import XGBRegressor
        P = np.stack([XGBRegressor(n_estimators=200, max_depth=2, learning_rate=0.1, subsample=0.8, random_state=seed + k, n_jobs=1)
                      .fit(Z, t).predict(Zq) for k in range(5)]); m, s = P.mean(0), P.std(0)
    else:
        raise SystemExit(f"모델 이름 오류: {model}")
    return m * sy + my, np.maximum(s * sy, 1e-9)


def loo(model, X, Y, seed=0):
    out = {}
    for j, o in enumerate(OBJ):
        err, sd = [], []
        for i in range(len(X)):
            k = np.arange(len(X)) != i
            m, s = fit_predict(model, X[k], Y[k, j], X[i:i + 1], seed); err.append(m[0] - Y[i, j]); sd.append(s[0])
        err, sd = np.array(err), np.array(sd)
        out[o] = {"rmse": round(float(np.sqrt((err ** 2).mean())), 4), "coverage_1sigma": round(float((np.abs(err) <= sd).mean()), 3)}
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("cmd", choices=["compare"]); ap.add_argument("--config")
    a = ap.parse_args(); cfg = load_cfg(a.config); w = ws(cfg)
    X, Y, ok = xy(cfg, results(w))
    if len(X) < 4: raise SystemExit("관측이 4개 미만 · 초기 설계를 먼저 돌린다")
    res = {m: loo(m, X, Y, cfg["seed"]) for m in ("gp", "rf", "xgb")}; res["n"] = len(X)
    dump(res, w / "model_compare.json")
    print(f"관측 {len(X)}개 · 단일 제외 교차검증")
    for m in ("gp", "rf", "xgb"):
        print(f"  {m:3s}  밀도 RMSE {res[m]['density']['rmse']:.4f} · 1σ 포함 {res[m]['density']['coverage_1sigma']:.2f}  |  CED RMSE {res[m]['ced']['rmse']:.1f} · 1σ 포함 {res[m]['ced']['coverage_1sigma']:.2f}")


if __name__ == "__main__":
    main()
