#!/usr/bin/env python3
"""SARA 13분자 라이브러리 — SMILES → 분자량 · 원소 · 기술자 · 2D 그림(SVG).
  python3 scripts/sara_library.py            → out/sara_library.csv · out/svg/*.svg · out/sara_library.json
입력: data/sara_molecules.csv (Li & Greenfield 2014 12분자 U/S/L 변이 · COMID id map) + data/mol/binder/S6422-AS-HighS13.mol (고황 13번째)
"""
import csv, json, os, sys
from rdkit import Chem
from rdkit.Chem import Descriptors, Crippen, rdMolDescriptors, Draw
from rdkit.Chem.Draw import rdMolDraw2D
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(HERE); os.makedirs('out/svg', exist_ok=True)

def desc(mol):
    mol_h = Chem.AddHs(mol)
    el = {}
    for a in mol_h.GetAtoms(): el[a.GetSymbol()] = el.get(a.GetSymbol(), 0) + 1
    heavy = mol.GetNumHeavyAtoms()
    arom = sum(1 for a in mol.GetAtoms() if a.GetIsAromatic())
    nC = el.get('C', 0); nH = el.get('H', 0)
    return dict(formula=rdMolDescriptors.CalcMolFormula(mol_h), MW=round(Descriptors.MolWt(mol_h), 2), n_atoms=mol_h.GetNumAtoms(), n_heavy=heavy,
                C=nC, H=nH, N=el.get('N', 0), O=el.get('O', 0), S=el.get('S', 0), HC=round(nH / nC, 3) if nC else None,
                aromatic_C_frac=round(sum(1 for a in mol.GetAtoms() if a.GetIsAromatic() and a.GetSymbol() == 'C') / nC, 3) if nC else None,
                n_rings=rdMolDescriptors.CalcNumRings(mol), n_arom_rings=rdMolDescriptors.CalcNumAromaticRings(mol),
                logP=round(Crippen.MolLogP(mol), 2), TPSA=round(rdMolDescriptors.CalcTPSA(mol), 1), n_rot=rdMolDescriptors.CalcNumRotatableBonds(mol))

def svg(mol, path, w=360, h=260):
    m = Chem.RemoveHs(mol); Chem.rdDepictor.Compute2DCoords(m)
    d = rdMolDraw2D.MolDraw2DSVG(w, h); o = d.drawOptions(); o.clearBackground = False; o.bondLineWidth = 2
    d.DrawMolecule(m); d.FinishDrawing(); open(path, 'w').write(d.GetDrawingText())

rows = list(csv.DictReader(open('data/sara_molecules.csv', encoding='utf-8')))
# 13번째 고황 분자 (COMID paper7 S6422 세트) — mol 파일에서 SMILES
hs = Chem.MolFromMolFile('data/mol/binder/S6422-AS-HighS13.mol')
rows.append(dict(mol_id='S6422-AS-HighS13', base_id='AS-HighS13', aging='non_aging', sara='asphaltene', name='High-sulfur asphaltene (HighS13)', smiles=Chem.MolToSmiles(Chem.RemoveHs(hs)), source='COMID data/molecules/asphalt_binder/paper7_s6422_moles (paper7 · 2026)'))
out = []
for r in rows:
    mol = Chem.MolFromSmiles(r['smiles'])
    if mol is None: print('parse fail', r['mol_id']); continue
    d = desc(mol); d.update(mol_id=r['mol_id'], base_id=r['base_id'], aging=r['aging'], sara=r['sara'], name=r['name'], smiles=Chem.MolToSmiles(mol), source=r['source'])
    out.append(d)
    if r['aging'] == 'non_aging': svg(mol, f"out/svg/{r['base_id']}.svg")
keys = ['mol_id', 'base_id', 'aging', 'sara', 'name', 'formula', 'MW', 'n_atoms', 'n_heavy', 'C', 'H', 'N', 'O', 'S', 'HC', 'aromatic_C_frac', 'n_rings', 'n_arom_rings', 'logP', 'TPSA', 'n_rot', 'smiles', 'source']
with open('out/sara_library.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(out)
json.dump(out, open('out/sara_library.json', 'w'), ensure_ascii=False, indent=1)
base = [o for o in out if o['aging'] == 'non_aging']
print(f"분자 {len(out)}행 · 비노화 13종 · SVG {len(base)}")
for o in base: print(f"{o['sara'][:2]:3} {o['base_id']:14} {o['formula']:14} MW {o['MW']:8} H/C {o['HC']:5} arom {o['aromatic_C_frac']:5} S {o['S']} N {o['N']} O {o['O']}")
