#!/usr/bin/env python3
"""바인더 × 노화 = 분자 개수 가중 평균 → MD 데이터(core672)와 결합 → 학습 표 (W14 · 14-1).

입력  out/mol_descriptors.csv · data/binder_compositions_LG2014.json(AAA1 · AAK1 · AAM1 분자 개수)
      data/comid_core672_dataset.csv(COMID MD 672행) · data/aging_recovered.csv(CNT · SBS 노화 라벨 복구)
      data/additive_properties.csv(첨가제 6종 문헌 대표값 · COMID)
출력  out/binder_features.csv (9행 = 바인더 3 × 노화 3)
      out/features.csv       (학습 표 · 행 = MD 실행 1건)
정제 (원본 09주차 #16 규칙)  CED < 0 제거 · 체적탄성률 > 10 GPa 제거 · 노화 라벨 없는 행 제거
"""
import csv, json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'out'
DESC = ['n_heavy', 'HC_ratio', 'O_frac', 'hetero_frac', 'aro_frac', 'MW', 'logP', 'TPSA', 'Rg', 'aspect']
AG = {'non_aging': 'U', 'short_aging': 'S', 'long_aging': 'L'}


def binder_table():
    md = pd.read_csv(OUT / 'mol_descriptors.csv')
    comp = json.load(open(ROOT / 'data/binder_compositions_LG2014.json', encoding='utf-8'))
    rows = []
    for b in ('AAA1', 'AAK1', 'AAM1'):
        counts = comp[b]['counts_X1']
        for ag in AG:
            tot, acc = 0, {k: 0.0 for k in DESC}
            for base, n in counts.items():
                cand = md[(md.base_id == base) & (md.aging == ag)]
                if cand.empty: cand = md[(md.base_id == base) & (md.aging == 'non_aging')]   # 포화분 = 노화 변이 없음
                r = cand.iloc[0]
                for k in DESC: acc[k] += n * r[k]
                tot += n
            rows.append({'binder_type': b, 'aging_state': ag, 'n_mol': tot, **{'b_' + k: acc[k] / tot for k in DESC}})
    return pd.DataFrame(rows)


def main():
    bt = binder_table(); bt.round(5).to_csv(OUT / 'binder_features.csv', index=False)
    md = pd.read_csv(ROOT / 'data/comid_core672_dataset.csv')
    rec = pd.read_csv(ROOT / 'data/aging_recovered.csv').rename(columns={'aging_state': 'aging_rec'})
    md = md.merge(rec, on='experiment_id', how='left')
    md['aging'] = md['aging_state'].fillna(md['aging_rec'])
    n0 = len(md)
    log = {'raw_rows': n0, 'aging_missing': int(md['aging'].isna().sum())}
    md = md[md['aging'].notna()].copy()
    log['ced_negative'] = int((md['cohesive_energy_density'] < 0).sum())
    log['bulk_over_10GPa'] = int((md['bulk_modulus'] > 10).sum())
    md.loc[md['cohesive_energy_density'] < 0, 'cohesive_energy_density'] = float('nan')
    md.loc[md['bulk_modulus'] > 10, 'bulk_modulus'] = float('nan')
    add = pd.read_csv(ROOT / 'data/additive_properties.csv')
    f = md.merge(bt.drop(columns='n_mol'), left_on=['binder_type', 'aging'], right_on=['binder_type', 'aging_state'], suffixes=('', '_b'))
    f = f.merge(add, on='additive_type', how='left')
    f['group_id'] = f['binder_type'] + '|' + f['additive_type'] + '|' + f['aging'].map(AG)
    keep = ['experiment_id', 'group_id', 'binder_type', 'additive_type', 'aging', 'temperature_K'] + ['b_' + k for k in DESC] + \
           ['add_density', 'add_inorganic', 'add_polymer', 'add_aspect', 'add_stiffness', 'add_nano'] + \
           ['density', 'cohesive_energy_density', 'bulk_modulus', 'e_inter_total']
    f = f[keep]
    f.to_csv(OUT / 'features.csv', index=False)
    log.update(rows=len(f), groups=int(f['group_id'].nunique()),
               n_density=int(f['density'].notna().sum()), n_ced=int(f['cohesive_energy_density'].notna().sum()),
               n_bulk=int(f['bulk_modulus'].notna().sum()), n_einter=int(f['e_inter_total'].notna().sum()))
    json.dump(log, open(OUT / 'features_log.json', 'w'), indent=1)
    print(bt.round(3).to_string(index=False)); print(log)


if __name__ == '__main__':
    main()
