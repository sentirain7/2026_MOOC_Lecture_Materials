#!/usr/bin/env python3
"""분자 1개 → 기술자 1행 (W14 · 14-1).

입력  data/sara_molecules.csv   (W11 과 같은 13분자 · 노화 변이 SMILES)
출력  out/mol_descriptors.csv  (분자 × 기술자)
      out/mol_fingerprints.json (ECFP4 1024 비트 중 켜진 비트 번호 — 모델 입력에는 쓰지 않음)

기술자 = RDKit 으로 SMILES 에서 바로 계산 · 모두 실험으로 잴 수 있는 양
  n_heavy(분자 크기 · MS/GPC) · HC_ratio · O_frac · hetero_frac(원소분석)
  aro_frac(방향족 원자 분율 · 13C NMR) · MW · logP · TPSA
  Rg · aspect(3D 회전반경 · 주관성모멘트 비 PMI3/PMI1 · 형상)
사용: python3 scripts/descriptors.py
"""
import csv, json, sys
from pathlib import Path
from rdkit import Chem, RDLogger
from rdkit.Chem import AllChem, Descriptors, rdMolDescriptors
RDLogger.DisableLog('rdApp.*')

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'out'; OUT.mkdir(exist_ok=True)


def describe(smiles, seed=7):
    m = Chem.MolFromSmiles(smiles)
    heavy = m.GetNumHeavyAtoms()
    sym = [a.GetSymbol() for a in m.GetAtoms()]
    nC, nO = sym.count('C'), sym.count('O')
    nHet = sum(1 for s in sym if s not in ('C', 'H'))
    nH = sum(a.GetTotalNumHs() for a in m.GetAtoms())
    aro = sum(1 for a in m.GetAtoms() if a.GetIsAromatic())
    mh = Chem.AddHs(m)
    ok = AllChem.EmbedMolecule(mh, randomSeed=seed)
    if ok == 0:
        AllChem.MMFFOptimizeMolecule(mh, maxIters=500)
        rg = rdMolDescriptors.CalcRadiusOfGyration(mh)
        p1, p3 = rdMolDescriptors.CalcPMI1(mh), rdMolDescriptors.CalcPMI3(mh)
        aspect = p3 / p1 if p1 > 0 else float('nan')
    else:
        rg = aspect = float('nan')
    fp = AllChem.GetMorganFingerprintAsBitVect(m, radius=2, nBits=1024)
    return dict(n_heavy=heavy, n_C=nC, n_H=nH, n_O=nO, n_hetero=nHet,
                HC_ratio=nH / nC, O_frac=nO / heavy, hetero_frac=nHet / heavy, aro_frac=aro / heavy,
                MW=Descriptors.MolWt(m), logP=Descriptors.MolLogP(m), TPSA=Descriptors.TPSA(m),
                Rg=rg, aspect=aspect), list(fp.GetOnBits())


def main():
    rows, fps = [], {}
    for r in csv.DictReader(open(ROOT / 'data/sara_molecules.csv', encoding='utf-8')):
        d, bits = describe(r['smiles'])
        rows.append({'mol_id': r['mol_id'], 'base_id': r['base_id'], 'aging': r['aging'], 'sara': r['sara'], **d})
        fps[r['mol_id']] = bits
    keys = list(rows[0].keys())
    with open(OUT / 'mol_descriptors.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=keys); w.writeheader()
        for r in rows: w.writerow({k: (round(v, 5) if isinstance(v, float) else v) for k, v in r.items()})
    json.dump({'radius': 2, 'nBits': 1024, 'on_bits': fps}, open(OUT / 'mol_fingerprints.json', 'w'))
    print(f'분자 {len(rows)}행 × 기술자 {len(keys) - 4}열 → out/mol_descriptors.csv')
    for r in rows[:3]: print(' ', r['mol_id'], {k: round(r[k], 3) for k in ('n_heavy', 'O_frac', 'aro_frac', 'aspect')})


if __name__ == '__main__':
    main()
