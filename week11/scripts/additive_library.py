#!/usr/bin/env python3
"""첨가제 라이브러리 — COMID mol 파일 23종 → SMILES · MW · logP · TPSA · 방향족 분율 · 회전결합 수.
  python3 scripts/additive_library.py → out/additive_library.csv · out/svg_add/*.svg
"""
import csv, json, os
from rdkit import Chem
from rdkit.Chem import Descriptors, Crippen, rdMolDescriptors
from rdkit.Chem.Draw import rdMolDraw2D
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(HERE); os.makedirs('out/svg_add', exist_ok=True)
meta = {r['additive_id']: r for r in csv.DictReader(open('data/additives_comid.csv', encoding='utf-8'))}
GROUP = {'polymer': '고분자 개질제', 'organic_polymer': '고분자 개질제', 'organic_wax': '왁스 · 상변화', 'chemical': '계면 · 부착 증진', 'inorganic': '나노 · 무기'}
out = []
for aid, m in meta.items():
    path = f"data/mol/additives/{aid}.mol"
    mol = Chem.MolFromMolFile(path, removeHs=False)
    if mol is None: mol = Chem.MolFromMolFile(path, sanitize=False, removeHs=False)
    if mol is None:
        print('parse fail (CTAB 형식) →', aid, '· COMID 분자량만 기록'); out.append(dict(additive_id=aid, name=m['name'], group=GROUP.get(m['category'], m['category']), category_comid=m['category'], formula='', MW=None, MW_comid=m['molecular_weight_comid'], n_heavy=None, logP=None, TPSA=None, aromatic_C_frac=None, n_rot=None, polar_atoms=None, ff='clayff', smiles='', source='COMID additives.yaml (mol 파일 파싱 실패 · 층상 광물)')); continue
    try:
        Chem.SanitizeMol(mol)
    except Exception as e:
        print('sanitize warn', aid, str(e)[:60]); mol.UpdatePropertyCache(strict=False); Chem.FastFindRings(mol)
        try: Chem.SanitizeMol(mol, sanitizeOps=Chem.SanitizeFlags.SANITIZE_ALL ^ Chem.SanitizeFlags.SANITIZE_PROPERTIES)
        except Exception as e2: print('  partial sanitize', str(e2)[:50])
    molh = Chem.AddHs(mol) if mol.GetNumAtoms() == mol.GetNumHeavyAtoms() else mol
    nC = sum(1 for a in mol.GetAtoms() if a.GetSymbol() == 'C')
    arom = sum(1 for a in mol.GetAtoms() if a.GetIsAromatic() and a.GetSymbol() == 'C')
    def safe(f, *a):
        try: return f(*a)
        except Exception: return None
    d = dict(additive_id=aid, name=m['name'], group=GROUP.get(m['category'], m['category']), category_comid=m['category'], formula=safe(rdMolDescriptors.CalcMolFormula, molh), MW=safe(lambda m: round(Descriptors.MolWt(m), 1), molh), MW_comid=m['molecular_weight_comid'],
             n_heavy=mol.GetNumHeavyAtoms(), logP=safe(lambda m: round(Crippen.MolLogP(m), 2), mol), TPSA=safe(lambda m: round(rdMolDescriptors.CalcTPSA(m), 1), mol), aromatic_C_frac=round(arom / nC, 2) if nC else 0, n_rot=safe(rdMolDescriptors.CalcNumRotatableBonds, mol),
             polar_atoms=sum(1 for a in mol.GetAtoms() if a.GetSymbol() in ('N', 'O', 'S', 'Cl', 'Na')), ff='clayff' if m['category'] == 'inorganic' and aid in ('SiO2', 'NanoClay') else 'gaff2', smiles=safe(lambda m: Chem.MolToSmiles(Chem.RemoveHs(m)), mol) or '', source='COMID data/molecules/additives.yaml + mol (2026)')
    out.append(d)
    try:
        mm = Chem.RemoveHs(mol); Chem.rdDepictor.Compute2DCoords(mm); dr = rdMolDraw2D.MolDraw2DSVG(360, 260); dr.drawOptions().clearBackground = False; dr.DrawMolecule(mm); dr.FinishDrawing(); open(f'out/svg_add/{aid}.svg', 'w').write(dr.GetDrawingText())
    except Exception as e: print('svg fail', aid, str(e)[:50])
out.sort(key=lambda r: (r['group'], r['MW'] or 0))
with open('out/additive_library.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
json.dump(out, open('out/additive_library.json', 'w'), ensure_ascii=False, indent=1)
print(len(out), '종')
for r in out: print(r["group"], r["additive_id"], r["formula"], "MW", r["MW"], "logP", r["logP"], "TPSA", r["TPSA"], "arom", r["aromatic_C_frac"], "ff", r["ff"])
