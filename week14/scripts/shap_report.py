#!/usr/bin/env python3
"""SHAP 해석 (W14 · 14-3) — TreeSHAP · 전체 데이터로 학습한 모델.

출력 out/pdp_density.json — 밀도 부분의존도(PDP) 2개: 온도 · 첨가제 밀도 + 실제 데이터 위치(rug)
     out/shap_summary.json — 표적별 mean|SHAP| 순위 · 방향(+/−) · 단조성(|Spearman|)
     out/shap_waterfall.json — 밀도 샘플 6개의 기준값 + 특징별 기여 = 예측값 (워터폴 애니)
     out/shap_values_density.csv — 밀도 행별 SHAP
"""
import json
import numpy as np, pandas as pd, shap
from scipy.stats import spearmanr
from common import *

FEATS = T + BINDER + ADD
PICK = [('AAA1|none|U', 293), ('AAA1|none|L', 293), ('AAA1|SiO2|L', 293), ('AAM1|Carbon_Nano_Tube|U', 413), ('AAK1|SBS_3_7|S', 253), ('AAM1|Graphine|L', 333)]


def main():
    summ = {}
    for tg in TARGETS:
        df, col = load(tg); X = df[FEATS].astype(float); m = model(); m.fit(X, df[col])
        ex = shap.TreeExplainer(m); sv = ex.shap_values(X)
        rows = []
        for j, f in enumerate(FEATS):
            a = np.abs(sv[:, j]).mean()
            if X[f].nunique() > 1 and np.std(sv[:, j]) > 0:
                rho = spearmanr(X[f], sv[:, j]).correlation
            else:
                rho = 0.0
            rows.append({'feature': f, 'ko': KO[f], 'mean_abs': float(a), 'direction': '+' if rho > 0 else '−', 'monotonic': round(abs(float(rho)), 2)})
        rows.sort(key=lambda r: -r['mean_abs'])
        summ[tg] = {'unit': TARGETS[tg][1], 'n': len(df), 'base': float(ex.expected_value), 'rank': rows}
        if tg == 'density':
            pd.DataFrame(sv, columns=FEATS).assign(group_id=df.group_id, T=df.temperature_K).to_csv(OUT / 'shap_values_density.csv', index=False)
            wf = []
            for gid, temp in PICK:
                idx = df.index[(df.group_id == gid) & (df.temperature_K == temp)]
                if len(idx) == 0: continue
                i = idx[0]; contrib = sorted([(FEATS[j], float(sv[i, j])) for j in range(len(FEATS))], key=lambda t: -abs(t[1]))
                wf.append({'group_id': gid, 'T': temp, 'base': float(ex.expected_value), 'pred': float(m.predict(X.iloc[[i]])[0]), 'md': float(df.loc[i, col]),
                           'contrib': [{'feature': f, 'ko': KO[f], 'phi': round(v, 5)} for f, v in contrib]})
            json.dump(wf, open(OUT / 'shap_waterfall.json', 'w'), ensure_ascii=False, indent=1)
            pdp = {}
            for fcol, lo, hi in (('temperature_K', 213, 433), ('add_density', 0.0, 2.8)):
                grid = np.linspace(lo, hi, 45); ys = []
                for v in grid:
                    Xv = X.copy(); Xv[fcol] = v; ys.append(float(m.predict(Xv).mean()))
                pdp[fcol] = {'ko': KO[fcol], 'x': [round(float(v), 4) for v in grid], 'y': [round(v, 5) for v in ys],
                             'rug': sorted(set(round(float(v), 3) for v in X[fcol])), 'span': round(max(ys) - min(ys), 4)}
            json.dump(pdp, open(OUT / 'pdp_density.json', 'w'), ensure_ascii=False, indent=1)
    for tg in summ:
        for r in summ[tg]['rank']: r['mean_abs'] = round(r['mean_abs'], 5)
    json.dump(summ, open(OUT / 'shap_summary.json', 'w'), ensure_ascii=False, indent=1)
    for tg, s in summ.items(): print(tg, [(r['ko'], r['mean_abs'], r['direction']) for r in s['rank'][:4]])


if __name__ == '__main__':
    main()
