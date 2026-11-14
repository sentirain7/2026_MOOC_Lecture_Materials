#!/usr/bin/env python3
"""특징 재정련 상태 표 (W14 · 14-4) — 라운드마다 특징을 줄이고 그룹 CV R² 를 다시 잰다.

R0 전체 17 → R1 기여 ≈ 0 제거(mean|SHAP| < 최대의 1 %) → R2 상관 |r| > 0.95 쌍에서 기여 작은 쪽 제거 → R3 상위 k = 6 유지
점수 = 밀도 · CED 그룹 5-fold R² (train_xgb 와 같은 절차)
출력 out/refine_rounds.json · out/feature_correlation.json
"""
import json
import numpy as np, pandas as pd
from common import *
K = 6   # R3 상위 k (바꿔 보기: 4)

FEATS = T + BINDER + ADD


def score(feats):
    out = {}
    for tg in ('density', 'CED'):
        df, col = load(tg); out[tg] = cv(df, feats, col)[0]['R2']
    return out


def main():
    summ = json.load(open(OUT / 'shap_summary.json'))
    imp = {}
    for tg in ('density', 'CED'):
        for r in summ[tg]['rank']: imp[r['feature']] = max(imp.get(r['feature'], 0), r['mean_abs'] / summ[tg]['rank'][0]['mean_abs'])
    rounds = []
    cur = list(FEATS); rounds.append({'round': 'R0', 'rule': '전체', 'n': len(cur), 'removed': [], **score(cur)})
    drop1 = [f for f in cur if imp[f] < 0.01]; cur = [f for f in cur if f not in drop1]
    rounds.append({'round': 'R1', 'rule': '기여 ≈ 0 제거 (< 최대의 1 %)', 'n': len(cur), 'removed': [KO[f] for f in drop1], **score(cur)})
    f = pd.read_csv(OUT / 'features.csv'); C = f[cur].astype(float).corr()
    pairs = [(a, b, round(float(C.loc[a, b]), 3)) for i, a in enumerate(cur) for b in cur[i + 1:] if abs(C.loc[a, b]) > 0.95]
    drop2 = []
    for a, b, r in sorted(pairs, key=lambda t: -abs(t[2])):
        if a in drop2 or b in drop2: continue
        drop2.append(a if imp[a] < imp[b] else b)
    cur = [x for x in cur if x not in drop2]
    rounds.append({'round': 'R2', 'rule': '상관 |r| > 0.95 쌍 → 기여 작은 쪽 제거', 'n': len(cur), 'removed': [KO[x] for x in drop2], **score(cur)})
    top = sorted(cur, key=lambda x: -imp[x])[:K]; rem3 = [x for x in cur if x not in top]; cur = top
    rounds.append({'round': 'R3', 'rule': f'상위 k = {K} 유지', 'n': len(cur), 'removed': [KO[x] for x in rem3], **score(cur)})
    json.dump({'rounds': rounds, 'final': [KO[x] for x in cur], 'final_keys': cur,
               'corr_pairs': [{'a': KO[a], 'b': KO[b], 'r': r} for a, b, r in pairs]}, open(OUT / 'refine_rounds.json', 'w'), ensure_ascii=False, indent=1)
    for r in rounds: print(r['round'], r['n'], r['density'], r['CED'], r['removed'][:6])
    print('final', [KO[x] for x in cur]); print('pairs', len(pairs))


if __name__ == '__main__':
    main()
