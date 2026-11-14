#!/usr/bin/env python3
"""노화 = 조성 치환: 같은 골격의 비노화(U) → 단기(S) → 장기(L) 변이 분자 비교(산소 수 · 분자량 · TPSA · 극성).
  python3 scripts/aging_substitute.py  → out/aging_table.csv · out/aging_table.json (sara_library.py 먼저)
"""
import csv, json, os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(HERE)
lib = json.load(open('out/sara_library.json'))
by = {}
for m in lib: by.setdefault(m['base_id'], {})[m['aging']] = m
rows = []
for base, d in by.items():
    if 'short_aging' not in d: continue
    u, s, l = d['non_aging'], d['short_aging'], d['long_aging']
    rows.append(dict(base_id=base, sara=u['sara'], MW_U=u['MW'], MW_S=s['MW'], MW_L=l['MW'], O_U=u['O'], O_S=s['O'], O_L=l['O'], S_U=u['S'], TPSA_U=u['TPSA'], TPSA_S=s['TPSA'], TPSA_L=l['TPSA'],
                     dMW_L=round(l['MW'] - u['MW'], 2), dO_L=l['O'] - u['O'], dTPSA_L=round(l['TPSA'] - u['TPSA'], 1), groups_L='C=O ' + str(l['smiles'].count('C(=O)') + l['smiles'].count('(=O)')) + ' · S=O ' + str(l['smiles'].count('S@@](=O)') + l['smiles'].count('S](=O)') + l['smiles'].count('S@](=O)'))))
rows.sort(key=lambda r: ['saturate', 'aromatic', 'resin', 'asphaltene'].index(r['sara']))
with open('out/aging_table.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
json.dump(rows, open('out/aging_table.json', 'w'), ensure_ascii=False, indent=1)
for r in rows: print(f"{r['base_id']:12} MW {r['MW_U']:7}→{r['MW_S']:7}→{r['MW_L']:7}  O {r['O_U']}→{r['O_S']}→{r['O_L']}  TPSA {r['TPSA_U']:5}→{r['TPSA_L']:5}  ΔMW_L {r['dMW_L']:+6}")
print('포화분 2종(Squalane · Hopane)은 노화 변이 없음 — COMID fallback_to non_aging')
