#!/usr/bin/env python3
"""SMILES → 분자 그래프(노드 = 중원자 · 엣지 = 결합) 특징 표.  W15 · 15-1
  python3 scripts/mol_graph.py                 # 톨루엔 + data/sara_molecules.csv 비노화 12종
  python3 scripts/mol_graph.py --smiles "CCO"   # 내 분자 1개
출력: out/graph_toluene.json · out/graph_summary.csv
노드 특징 = 원소 one-hot(C N O S) · 혼성(sp sp2 sp3) · 방향족 · 고리 · 수소 수 · 형식전하  (원본 10주차 #6)
엣지 특징 = 결합 차수 · 방향족 · 고리 내부"""
import argparse, csv, json, os
from rdkit import Chem
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
ELEM = ['C', 'N', 'O', 'S']; HYB = ['SP', 'SP2', 'SP3']

def featurize(smi):
    m = Chem.MolFromSmiles(smi)
    if m is None: raise ValueError('SMILES 해석 실패: ' + smi)
    nodes = []
    for a in m.GetAtoms():
        f = [1.0 if a.GetSymbol() == e else 0.0 for e in ELEM]
        f += [1.0 if str(a.GetHybridization()) == h else 0.0 for h in HYB]
        f += [1.0 if a.GetIsAromatic() else 0.0, 1.0 if a.IsInRing() else 0.0, float(a.GetTotalNumHs()), float(a.GetFormalCharge())]
        nodes.append({'idx': a.GetIdx(), 'symbol': a.GetSymbol(), 'hyb': str(a.GetHybridization()), 'aromatic': a.GetIsAromatic(), 'ring': a.IsInRing(), 'nH': a.GetTotalNumHs(), 'charge': a.GetFormalCharge(), 'x': f})
    edges = []
    for b in m.GetBonds():
        edges.append({'u': b.GetBeginAtomIdx(), 'v': b.GetEndAtomIdx(), 'order': b.GetBondTypeAsDouble(), 'aromatic': b.GetIsAromatic(), 'ring': b.IsInRing()})
    return m, nodes, edges

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--smiles'); ap.add_argument('--out', default=os.path.join(ROOT, 'out')); a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    if a.smiles:
        m, n, e = featurize(a.smiles)
        json.dump({'smiles': a.smiles, 'nodes': n, 'edges': e, 'feature_names': ELEM + HYB + ['aromatic', 'ring', 'nH', 'charge']}, open(os.path.join(a.out, 'graph_mine.json'), 'w'), ensure_ascii=False, indent=1)
        print(f'노드 {len(n)} · 엣지 {len(e)} · 특징 {len(n[0]["x"])}차원 → out/graph_mine.json'); return
    smi = 'Cc1ccccc1'
    m, n, e = featurize(smi)
    json.dump({'name': 'toluene', 'smiles': smi, 'nodes': n, 'edges': e, 'feature_names': ELEM + HYB + ['aromatic', 'ring', 'nH', 'charge']}, open(os.path.join(a.out, 'graph_toluene.json'), 'w'), ensure_ascii=False, indent=1)
    print(f'toluene  노드 {len(n)} · 엣지 {len(e)} · 노드 특징 {len(n[0]["x"])}차원 · 엣지 특징 3')
    rows = [('toluene', 'reference', smi)]
    for r in csv.DictReader(open(os.path.join(ROOT, 'data', 'sara_molecules.csv'), encoding='utf-8')):
        if r['aging'] == 'non_aging': rows.append((r['base_id'], r['sara'], r['smiles']))
    out = []
    for name, sara, s in rows:
        mm, nn, ee = featurize(s)
        ring = sum(1 for x in nn if x['ring']); aro = sum(1 for x in nn if x['aromatic'])
        out.append({'name': name, 'sara': sara, 'nodes': len(nn), 'edges': len(ee), 'aromatic_nodes': aro, 'ring_nodes': ring, 'hetero': sum(1 for x in nn if x['symbol'] != 'C')})
    with open(os.path.join(a.out, 'graph_summary.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
    for o in out: print(f"{o['name']:<22} {o['sara']:<10} 노드 {o['nodes']:>3} · 엣지 {o['edges']:>3} · 방향족 {o['aromatic_nodes']:>2} · 헤테로 {o['hetero']}")
    print(f'분자 {len(out)}개 → out/graph_summary.csv')

if __name__ == '__main__': main()
