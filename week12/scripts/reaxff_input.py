#!/usr/bin/env python3
"""포틀란다이트 Ca(OH)2 슬래브 + 물 층 → ReaxFF(LAMMPS) 입력 생성 · 실행 · 결합 차수 · 전하 파싱.
  python3 scripts/reaxff_input.py --packmol packmol --lmp lmp [--steps 400] [--nwater 70]
산출: out/portlandite_water.data · in.reaxff · log.reaxff · bonds.reaxff · dump.q · reaxff_summary.json
구조: 포틀란다이트 P-3m1 · a 3.5853 Å · c 4.895 Å · Ca (0,0,0) · O ±(1/3,2/3,0.2341) · H ±(1/3,2/3,0.4248)
      (Desgranges 외 1993 중성자 회절 · 「확인 필요」 — 교육용 슬래브 · 표면 재구성 없음)
힘장: data/ffield.reax.cement = 연구실 보관 ffield.reax (머리글 「Si/O/H · Fogarty 외 2010」 + Ca · Fe · Cl · Na 확장 · 원소 C H O Ca Si Fe Cl Na X · 확장분 출처 미표기 → 확인 필요)
"""
import argparse, json, math, os, re, subprocess, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
A, C = 3.5853, 4.895; ZO, ZH = 0.2341, 0.4248
def portlandite_slab(nx=4, ny=2, nz=2):
    """직교 초격자: A1 = a(1,0,0) · A2 = a(0,√3,0) — 육방 셀 2개 = 직교 셀 1개."""
    Lx, Ly = nx * A, ny * A * math.sqrt(3); atoms = []
    frac = [('Ca', 0, 0, 0), ('O', 1/3, 2/3, ZO), ('O', 2/3, 1/3, -ZO), ('H', 1/3, 2/3, ZH), ('H', 2/3, 1/3, -ZH)]
    for ix in range(nx):
        for iy in range(ny):
            for iz in range(nz):
                for (el, fx, fy, fz) in frac:
                    for (sx, sy) in ((0, 0), (0.5, 0.5)):          # 직교 셀 안의 두 육방 격자점
                        # 육방 → 직교: x = a(fx + fy·cos120)… 간단히 육방 좌표계 (a1, a2 각 120°) 를 직교로
                        hx = (fx - 0.5 * fy) * A; hy = fy * A * math.sqrt(3) / 2
                        x = (hx + (ix + sx) * A) % Lx; y = (hy + (iy + sy) * A * math.sqrt(3)) % Ly
                        z = (fz + iz) * C
                        atoms.append((el, x, y, z + 2.0))
    return atoms, Lx, Ly, nz * C + 2.0
def write_pdb(path, atoms):
    with open(path, 'w') as f:
        for i, (el, x, y, z) in enumerate(atoms, 1):
            f.write("ATOM  %5d %-4s SLB A   1    %8.3f%8.3f%8.3f  1.00  0.00          %2s\n" % (i, el, x, y, z, el))
        f.write("END\n")
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--packmol', default='packmol'); ap.add_argument('--lmp', default='')
    ap.add_argument('--steps', type=int, default=400); ap.add_argument('--nwater', type=int, default=0); ap.add_argument('--out', default=os.path.join(ROOT, 'out'))
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    slab, Lx, Ly, ztop = portlandite_slab()
    wz0, wz1 = ztop - 1.5, ztop + 10.5; Lz = wz1 + 15.0
    nw = a.nwater or int(round(0.0334 * Lx * Ly * (wz1 - wz0)))    # 0.0334 분자/Å³ = 1 g/cm³
    write_pdb(os.path.join(a.out, 'slab.pdb'), slab)
    with open(os.path.join(a.out, 'water.pdb'), 'w') as f:                     # SPC 기하 · 0.9572 Å · 104.52°
        f.write("ATOM      1  O   HOH A   1       0.000   0.000   0.000  1.00  0.00           O\nATOM      2  H   HOH A   1       0.957   0.000   0.000  1.00  0.00           H\nATOM      3  H   HOH A   1      -0.240   0.927   0.000  1.00  0.00           H\nEND\n")
    inp = os.path.join(a.out, 'pack.inp')
    open(inp, 'w').write(f"tolerance 2.0\nfiletype pdb\noutput {a.out}/system.pdb\nseed 12345\nstructure {a.out}/slab.pdb\n  number 1\n  fixed 0. 0. 0. 0. 0. 0.\nend structure\nstructure {a.out}/water.pdb\n  number {nw}\n  inside box 0.5 0.5 {wz0:.2f} {Lx-0.5:.2f} {Ly-0.5:.2f} {wz1:.2f}\nend structure\n")
    subprocess.run(f"{a.packmol} < {inp} > {a.out}/packmol.log", shell=True, check=True)
    atoms = []; types = {'H': 1, 'O': 2, 'Ca': 3}; mass = {1: 1.008, 2: 15.999, 3: 40.078}
    for line in open(os.path.join(a.out, 'system.pdb')):
        if line.startswith(('ATOM', 'HETATM')):
            el = line[76:78].strip() or line[12:16].strip()[0]; atoms.append((el, float(line[30:38]), float(line[38:46]), float(line[46:54]), line[17:20].strip()))
    nslab = len(slab)
    with open(os.path.join(a.out, 'portlandite_water.data'), 'w') as f:
        f.write(f"portlandite slab + {nw} water · ReaxFF · week12\n\n{len(atoms)} atoms\n3 atom types\n\n0.0 {Lx:.4f} xlo xhi\n0.0 {Ly:.4f} ylo yhi\n0.0 {Lz:.4f} zlo zhi\n\nMasses\n\n1 1.008 # H\n2 15.999 # O\n3 40.078 # Ca\n\nAtoms # charge\n\n")
        for i, (el, x, y, z, res) in enumerate(atoms, 1): f.write(f"{i} {types[el]} 0.0 {x:.4f} {y:.4f} {z:.4f}\n")
    ffield = os.path.join(ROOT, 'data', 'ffield.reax.cement'); ctrl = os.path.join(ROOT, 'data', 'control.reax')
    infile = f"""# week12 · 포틀란다이트 슬래브 + 물 · ReaxFF (교육용 · 작은 계 · 짧은 시간)
units real
atom_style charge
boundary p p p
read_data portlandite_water.data
pair_style reaxff {ctrl} safezone 2.0 mincap 200
pair_coeff * * {ffield} H O Ca
neighbor 2.0 bin
neigh_modify every 1 delay 0 check yes
fix qeq all qeq/reaxff 1 0.0 10.0 1e-6 reaxff
group slab id <= {nslab}
group water id > {nslab}
velocity water create 300.0 4928 dist gaussian
timestep 0.25
thermo 50
thermo_style custom step temp pe etotal press
fix bo all reaxff/bonds 250 bonds.reaxff
dump q all custom 250 dump.q id type q x y z
dump_modify q sort id
fix nvt all nvt temp 300.0 300.0 25.0
run {a.steps}
write_data final.data
"""
    open(os.path.join(a.out, 'in.reaxff'), 'w').write(infile)
    summary = {'n_slab': nslab, 'n_water': nw, 'n_atoms': len(atoms), 'box': [Lx, Ly, Lz], 'water_z': [wz0, wz1], 'steps': a.steps, 'dt_fs': 0.25}
    if a.lmp:
        r = subprocess.run(f"cd {a.out} && {a.lmp} -in in.reaxff -log log.reaxff > lmp.stdout 2>&1", shell=True)
        summary['lmp_exit'] = r.returncode
        if r.returncode == 0:
            summary.update(parse(a.out, nslab, len(atoms)))
    json.dump(summary, open(os.path.join(a.out, 'reaxff_summary.json'), 'w'), indent=1, ensure_ascii=False)
    print(json.dumps(summary, indent=1, ensure_ascii=False))
def parse(out, nslab, natoms):
    """bonds.reaxff: 프레임별 Ca–O(물) 결합 수(BO ≥ 0.3) · 물 O 의 H 개수 분포(해리 여부) · dump.q: 종류별 평균 전하."""
    res = {'frames': []}
    txt = open(os.path.join(out, 'bonds.reaxff')).read()
    frames = re.split(r'# Timestep (\d+)', txt)[1:]
    for step, body in zip(frames[0::2], frames[1::2]):
        caow = 0; hcount = collections.Counter(); typ = {}
        rows = [l.split() for l in body.splitlines() if l.strip() and not l.startswith('#')]
        for r in rows: typ[int(r[0])] = int(r[1])
        for r in rows:
            i, t, nb = int(r[0]), int(r[1]), int(r[2]); nbrs = [int(x) for x in r[3:3 + nb]]; bos = [float(x) for x in r[4 + nb:4 + 2 * nb]]
            if t == 2 and i > nslab:                      # 물 O
                caow += sum(1 for j, bo in zip(nbrs, bos) if typ.get(j) == 3 and bo >= 0.3)
                hcount[sum(1 for j, bo in zip(nbrs, bos) if typ.get(j) == 1 and bo >= 0.3)] += 1
        res['frames'].append({'step': int(step), 'ca_ow_bonds': caow, 'water_O_by_nH': dict(sorted(hcount.items()))})
    qtxt = open(os.path.join(out, 'dump.q')).read().split('ITEM: TIMESTEP')[1:]
    qf = []
    for blk in qtxt:
        lines = blk.strip().splitlines(); step = int(lines[0]); rows = [l.split() for l in lines[lines.index([l for l in lines if l.startswith('ITEM: ATOMS')][0]) + 1:]]
        acc = collections.defaultdict(list)
        for r in rows:
            i, t, q = int(r[0]), int(r[1]), float(r[2]); key = {1: 'H', 2: 'O', 3: 'Ca'}[t] + ('_slab' if i <= nslab else '_water'); acc[key].append(q)
        qf.append({'step': step, **{k: round(sum(v) / len(v), 4) for k, v in acc.items()}})
    res['charges'] = qf
    th = re.findall(r'^\s*(\d+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s*$', open(os.path.join(out, 'log.reaxff')).read(), re.M)
    res['thermo'] = [{'step': int(a), 'temp': float(b), 'pe': float(c), 'etotal': float(d), 'press': float(e)} for a, b, c, d, e in th]
    m = re.search(r'Loop time of ([\d.]+) on (\d+) procs for (\d+) steps with (\d+) atoms', open(os.path.join(out, 'log.reaxff')).read())
    if m: res['loop_time_s'] = float(m.group(1))
    return res
if __name__ == '__main__': main()
