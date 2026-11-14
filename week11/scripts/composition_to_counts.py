#!/usr/bin/env python3
"""SARA wt% → 13분자 개수 역산 · Li & Greenfield 표와 대조 · 작은 벌크 셀 Packmol 통과 보고.
  python3 scripts/composition_to_counts.py [--sara 15,45,25,15] [--atoms 1500] [--packmol packmol] [--no-pack]
출력: out/composition_report.json · out/mix.inp · out/mix.pdb (Packmol) · out/pdb/*.pdb
규칙: 분획 안 분자는 Li & Greenfield AAA-1 의 분획 내 비율로 배분 · 개수는 반올림 뒤 wt% 오차 최소화(±1 조정).
"""
import argparse, csv, json, os, shutil, subprocess, math
from rdkit import Chem
from rdkit.Chem import AllChem
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(HERE)
ap = argparse.ArgumentParser(); ap.add_argument('--sara', default='15,45,25,15'); ap.add_argument('--atoms', type=int, default=1500); ap.add_argument('--rho0', type=float, default=0.2); ap.add_argument('--packmol', default='packmol'); ap.add_argument('--no-pack', action='store_true'); ap.add_argument('--tag', default='mix')
A = ap.parse_args()
lib = {m['base_id']: m for m in json.load(open('out/sara_library.json')) if m['aging'] == 'non_aging'}
comp = json.load(open('data/binder_compositions_LG2014.json'))
target = dict(zip(['saturate', 'aromatic', 'resin', 'asphaltene'], [float(x) / 100 for x in A.sara.split(',')]))
# 분획 내 비율 = AAA-1 X1 개수 비율 (HighS13 은 아스팔텐 분획에 1 추가 비율 = AS-Thio 와 같게)
aaa = comp['AAA1']['counts_X1']; frac_in = {}
for b, n in aaa.items(): frac_in.setdefault(lib[b]['sara'], {})[b] = n
frac_in['asphaltene']['AS-HighS13'] = frac_in['asphaltene']['AS-Thio']
def counts_for(total_mass):
    cnt = {}
    for sara, members in frac_in.items():
        mass_f = target[sara] * total_mass
        k = mass_f / sum(r * lib[b]['MW'] for b, r in members.items())
        for b, r in members.items(): cnt[b] = round(k * r)
        if sum(cnt[b] for b in members) == 0: cnt[max(members, key=members.get)] = 1
    # 탐욕 조정: 분획 wt% 절대 오차 합이 줄어드는 ±1 변경을 반복
    def err(c):
        w, _ = wt(c); return sum(abs(w.get(s, 0) - target[s]) for s in target)
    for _ in range(200):
        best = (err(cnt), None)
        for b in cnt:
            for d in (+1, -1):
                if cnt[b] + d < 0: continue
                if d == -1 and sum(cnt[x] for x in frac_in[lib[b]['sara']]) <= 1: continue
                c2 = dict(cnt); c2[b] += d; e = err(c2)
                if e < best[0] - 1e-9: best = (e, (b, d))
        if best[1] is None: break
        cnt[best[1][0]] += best[1][1]
    return cnt
def wt(cnt):
    tot = sum(cnt[b] * lib[b]['MW'] for b in cnt); w = {}
    for b in cnt: w[lib[b]['sara']] = w.get(lib[b]['sara'], 0) + cnt[b] * lib[b]['MW'] / tot
    return w, tot
def natoms(cnt): return sum(cnt[b] * lib[b]['n_atoms'] for b in cnt)
# 총 질량을 늘려 가며 원자 수 목표에 맞춤
total_mass = 3000; cnt = counts_for(total_mass)
while natoms(cnt) < A.atoms: total_mass *= 1.08; cnt = counts_for(total_mass)
w, tot = wt(cnt)
err = {s: round((w.get(s, 0) - target[s]) * 100, 1) for s in target}
# 원소비
el = {k: sum(cnt[b] * lib[b][k] for b in cnt) for k in ('C', 'H', 'N', 'O', 'S')}
HC = el['H'] / el['C']; SC = el['S'] / el['C']
L = (tot / 6.02214076e23 / A.rho0) ** (1 / 3) * 1e8  # Å
rep = dict(target_wt=target, counts=cnt, n_molecules=sum(cnt.values()), n_atoms=natoms(cnt), total_mass_gmol=round(tot, 1), actual_wt={k: round(v * 100, 1) for k, v in w.items()}, wt_error_pct=err,
           elements=el, HC=round(HC, 3), SC=round(SC, 4), NC=round(el['N'] / el['C'], 4), OC=round(el['O'] / el['C'], 4), rho0=A.rho0, L_A=round(L, 2),
           reference_tables={k: dict(counts=v['counts_X1'], sara=v['sara_fractions'], total=v['total_X1']) for k, v in comp.items()})
# LG 2014 표 3종의 원소비 · 분자량 가중 wt% 도 계산(대조용)
for k, v in comp.items():
    c = v['counts_X1']; ww, tt = wt(c); e = {q: sum(c[b] * lib[b][q] for b in c) for q in ('C', 'H', 'N', 'O', 'S')}
    rep['reference_tables'][k].update(wt_from_MW={a: round(b * 100, 1) for a, b in ww.items()}, HC=round(e['H'] / e['C'], 3), SC=round(e['S'] / e['C'], 4), n_atoms=natoms(c), mean_MW=round(tt / sum(c.values()), 1))
json.dump(rep, open(f'out/composition_report_{A.tag}.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps({k: rep[k] for k in ('counts', 'n_molecules', 'n_atoms', 'actual_wt', 'wt_error_pct', 'HC', 'SC', 'L_A')}, ensure_ascii=False))
if A.no_pack: raise SystemExit
# Packmol: 분자별 PDB (RDKit 3D) → 상자
os.makedirs('out/pdb', exist_ok=True)
for b in [x for x in cnt if cnt[x] > 0]:   # 개수 0 인 분자는 상자에 넣지 않는다(Packmol 은 1 이상만 받음)
    m = Chem.AddHs(Chem.MolFromSmiles(lib[b]['smiles'])); AllChem.EmbedMolecule(m, randomSeed=7); AllChem.MMFFOptimizeMolecule(m, maxIters=500); Chem.MolToPDBFile(m, f'out/pdb/{b}.pdb')
tol = 3.0
inp = [f"tolerance {tol}", f"filetype pdb", f"output out/{A.tag}.pdb", "seed 7", ""]
for b, n in cnt.items():
    if n < 1: continue
    inp += [f"structure out/pdb/{b}.pdb", f"  number {n}", f"  inside box 1.0 1.0 1.0 {L-1:.2f} {L-1:.2f} {L-1:.2f}", "end structure", ""]
open(f'out/{A.tag}.inp', 'w').write('\n'.join(inp))
r = subprocess.run(f"{A.packmol} < out/{A.tag}.inp", shell=True, capture_output=True, text=True)
ok = 'Success!' in r.stdout
open(f'out/{A.tag}_packmol.log', 'w').write(r.stdout[-6000:])
# 최소 거리 검사(서로 다른 분자 사이)
import numpy as np
xyz = []; resid = []
for line in open(f'out/{A.tag}.pdb'):
    if line.startswith(('ATOM', 'HETATM')): xyz.append([float(line[30:38]), float(line[38:46]), float(line[46:54])]); resid.append(int(line[22:26]))
xyz = np.array(xyz); resid = np.array(resid); dmin = 99
for i in range(0, len(xyz), 1):
    d = np.linalg.norm(xyz[i + 1:] - xyz[i], axis=1); mask = resid[i + 1:] != resid[i]
    if mask.any(): dmin = min(dmin, d[mask].min())
rep.update(packmol=dict(success=ok, tolerance=tol, min_intermolecular_distance_A=round(float(dmin), 3), n_atoms_pdb=len(xyz), box_L=round(L, 2)))
json.dump(rep, open(f'out/composition_report_{A.tag}.json', 'w'), ensure_ascii=False, indent=1)
print('packmol', ok, 'dmin', round(float(dmin), 3), 'atoms', len(xyz))
