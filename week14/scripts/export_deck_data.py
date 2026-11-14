#!/usr/bin/env python3
"""덱 주입용 JSON 한 개 (out/deck_data.json) — 덱의 모든 실행값은 이 파일에서 온다."""
import json, csv
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; OUT = ROOT / 'out'
W11 = ROOT.parent / 'week11/out/mol2d.json'
J = lambda n: json.load(open(OUT / n, encoding='utf-8'))
md = {r['mol_id']: r for r in csv.DictReader(open(OUT / 'mol_descriptors.csv', encoding='utf-8'))}
fp = J('mol_fingerprints.json')['on_bits']
import sys
_need = [W11, OUT / 'hparam_grid.json']
if any(not q.exists() for q in _need):
    print('deck_data 생략 — 없음:', ', '.join(str(q) for q in _need if not q.exists()), '(덱 갱신 전용 단계 · 실습 결과에는 영향 없음)')
    sys.exit(0)
mol2d = json.load(open(W11, encoding='utf-8'))
pick = {'U': ('U-AS-Thio-0293', 'AS-Thio'), 'L': ('L-AS-Thio-0293', 'L-AS-Thio-0293')}
vec = {}
for k, (mid, did) in pick.items():
    r = md[mid]
    vec[k] = {'mol_id': mid, 'mol2d': mol2d[did], 'fp_on': len(fp[mid]), 'fp_bits': fp[mid],
              **{c: round(float(r[c]), 4) for c in ('n_heavy', 'n_C', 'n_H', 'n_O', 'n_hetero', 'HC_ratio', 'O_frac', 'hetero_frac', 'aro_frac', 'MW', 'logP', 'TPSA', 'Rg', 'aspect')}}
binder = [{k: (round(float(v), 4) if k.startswith('b_') else v) for k, v in r.items()} for r in csv.DictReader(open(OUT / 'binder_features.csv', encoding='utf-8'))]
oof = [{'g': r['group_id'], 'md': round(float(r['md']), 4), 'p': round(float(r['pred']), 4)} for r in csv.DictReader(open(OUT / 'oof_density.csv', encoding='utf-8'))]
data = {'log': J('features_log.json'), 'metrics': J('train_metrics.json'), 'boost': J('boosting_rounds.json'), 'grid': J('hparam_grid.json'),
        'shap': J('shap_summary.json'), 'waterfall': J('shap_waterfall.json'), 'pdp': J('pdp_density.json'), 'refine': J('refine_rounds.json'),
        'vec': vec, 'binder': binder, 'oof': oof[::3]}
json.dump(data, open(OUT / 'deck_data.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('deck_data.json', round((OUT / 'deck_data.json').stat().st_size / 1024, 1), 'KB')

# 덱에 주입: decks/W14_표현자와대리모델.html 의 var W14 = … ; 자리
import re
DECK = ROOT.parents[1] / 'decks' / 'W14_표현자와대리모델.html'
if DECK.exists():
    s = DECK.read_text(encoding='utf-8')
    blob = '/*W14_BEGIN*/' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '/*W14_END*/'
    s2, n = re.subn(r'/\*W14_BEGIN\*/.*?/\*W14_END\*/', lambda m: blob, s, flags=re.S)
    if n == 0: s2 = s.replace('/*__W14__*/null', blob)
    DECK.write_text(s2, encoding='utf-8'); print('주입 →', DECK.name)
