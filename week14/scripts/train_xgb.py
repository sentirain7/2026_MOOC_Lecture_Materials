#!/usr/bin/env python3
"""XGBoost 대리모델 · 그룹 5-fold (W14 · 14-2).

출력 out/train_metrics.json — 표적 4 × 특징 세트 3 · 무작위 ↔ 그룹 분할 · 선형(Ridge) 기준선
     out/boosting_rounds.json — 부스팅 애니용(AAA1 무첨가 · 깊이 1 · η 0.3 · 라운드별 예측 · 학습 RMSE)
     out/hparam_grid.json — 나무 수 × 깊이 × 학습률 격자의 밀도 그룹 CV R² (조작형 장)
     out/oof_density.csv — 밀도 폴드 밖 예측(산점)
사용: python3 scripts/train_xgb.py [--fast]   (--fast = 격자 생략)
"""
import json, sys, time
import numpy as np, pandas as pd
from sklearn.linear_model import Ridge
from sklearn.model_selection import GroupKFold
from common import *

FS = {'T': T, 'T+binder': T + BINDER, 'T+binder+additive': T + BINDER + ADD}


def ridge_cv(df, feats, col):
    X, y, g = df[feats].values.astype(float), df[col].values, df['group_id'].values
    pred = np.zeros(len(y))
    for tr, va in GroupKFold(5).split(X, y, g):
        mu, sd = X[tr].mean(0), X[tr].std(0); sd[sd == 0] = 1
        m = Ridge(alpha=1.0).fit((X[tr] - mu) / sd, y[tr]); pred[va] = m.predict((X[va] - mu) / sd)
    return round(float(1 - ((y - pred) ** 2).sum() / ((y - y.mean()) ** 2).sum()), 4)


def main():
    t0 = time.time(); res = {}
    for tg in TARGETS:
        df, col = load(tg); res[tg] = {'unit': TARGETS[tg][1], 'n': len(df), 'sets': {}}
        for name, feats in FS.items():
            m, pred = cv(df, feats, col); res[tg]['sets'][name] = m
            if tg == 'density' and name == 'T+binder+additive':
                pd.DataFrame({'group_id': df.group_id, 'T': df.temperature_K, 'md': df[col], 'pred': pred}).to_csv(OUT / 'oof_density.csv', index=False)
        res[tg]['ridge_full'] = ridge_cv(df, FS['T+binder+additive'], col)
    df, col = load('density')
    rnd = [cv(df, FS['T+binder+additive'], col, split='random', seed=s)[0]['R2'] for s in range(3)]
    res['split_compare'] = {'random_R2_seeds': rnd, 'group_R2': res['density']['sets']['T+binder+additive']['R2'],
                            'groups': int(df.group_id.nunique()), 'dup_rows': int(df.duplicated(['group_id', 'temperature_K', 'density']).sum())}
    # 부스팅 애니: AAA1 무첨가 · 노화 3 · 깊이 1
    sub = df[(df.binder_type == 'AAA1') & (df.additive_type == 'none')].reset_index(drop=True)
    X = sub[['temperature_K', 'b_O_frac']].values; y = sub[col].values
    m = model(n_estimators=100, learning_rate=0.3, max_depth=1, subsample=1.0, colsample_bytree=1.0, reg_lambda=0.0); m.fit(X, y)
    grid_T = np.arange(213, 434, 4); rounds = [0, 1, 2, 3, 5, 10, 20, 50, 100]
    curves = {}
    for ag in ('non_aging', 'short_aging', 'long_aging'):
        o = float(sub[sub.aging == ag].b_O_frac.iloc[0]); Xg = np.c_[grid_T, np.full(len(grid_T), o)]
        curves[ag] = {str(r): [round(float(v), 5) for v in (np.full(len(grid_T), y.mean()) if r == 0 else m.predict(Xg, iteration_range=(0, r)))] for r in rounds}
    rm = [round(float(np.sqrt(((y - (np.full(len(y), y.mean()) if r == 0 else m.predict(X, iteration_range=(0, r)))) ** 2).mean())), 5) for r in range(0, 101)]
    json.dump({'T': grid_T.tolist(), 'rounds': rounds, 'curves': curves, 'train_rmse': rm,
               'points': [{'T': float(a), 'aging': g, 'y': round(float(b), 5)} for a, g, b in zip(sub.temperature_K, sub.aging, y)],
               'n': len(sub), 'eta': 0.3, 'depth': 1}, open(OUT / 'boosting_rounds.json', 'w'))
    res['boosting_demo'] = {'n': len(sub), 'rmse_r0': rm[0], 'rmse_r10': rm[10], 'rmse_r100': rm[100]}
    if '--fast' not in sys.argv:
        grid = []
        for ne in (50, 100, 200, 400, 800):
            for dp in (2, 3, 4, 6):
                for lr in (0.03, 0.1, 0.3):
                    grid.append({'n_estimators': ne, 'max_depth': dp, 'learning_rate': lr,
                                 'R2': cv(df, FS['T+binder+additive'], col, n_estimators=ne, max_depth=dp, learning_rate=lr)[0]['R2']})
        json.dump(grid, open(OUT / 'hparam_grid.json', 'w'))
        best = max(grid, key=lambda g: g['R2']); worst = min(grid, key=lambda g: g['R2'])
        res['hparam'] = {'runs': len(grid), 'best': best, 'worst': worst}
    else:  # --fast: 이전 격자 결과가 있으면 그대로 싣는다
        hp = OUT / 'hparam_grid.json'
        if hp.exists():
            grid = json.load(open(hp)); best = max(grid, key=lambda g: g['R2']); worst = min(grid, key=lambda g: g['R2'])
            res['hparam'] = {'runs': len(grid), 'best': best, 'worst': worst, 'reused': True}
    res['wall_s'] = round(time.time() - t0, 1)
    json.dump(res, open(OUT / 'train_metrics.json', 'w'), ensure_ascii=False, indent=1)
    for tg in TARGETS: print(tg, {k: v['R2'] for k, v in res[tg]['sets'].items()}, 'ridge', res[tg]['ridge_full'])
    print('split', res['split_compare']); print('boost', res['boosting_demo']); print('hparam', res.get('hparam')); print('wall', res['wall_s'])


if __name__ == '__main__':
    main()
