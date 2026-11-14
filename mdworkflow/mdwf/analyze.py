"""⑤ 물성: 생산 구간 → 밀도(블록 평균 ± 표준오차) · CED(응집에너지밀도) · 용해도 매개변수 δ = √CED.

밀도  ρ = 생산 구간 thermo 의 Density 평균 · 블록 5개 표준오차(W05)
CED  E_inter = E_bulk − Σ E_분자 하나(같은 좌표) · CED = −⟨E_inter⟩ / ⟨V⟩  (W09 Method A 와 같은 정의)
      Σ E_분자 하나 = 생산 프레임마다 분자를 격자 간격 S 로 떼어 놓고 LAMMPS rerun 한 번으로 계산(templates/in.intra)
      벌크 = PPPM 장거리 전하 · tail 보정 포함 / 분자 하나 = 전하 직접 합(절단 rc > 분자 크기) · LJ 12 Å 같은 절단
넣는 것: ws/runs/<id>/ (④)      나오는 것: ws/runs/<id>/props.json · ced_frames.csv
틀리기 쉬운 곳: 평형 전 구간 포함 · 프레임 수 부족(표준오차가 큼) · 분자가 상자 경계에서 잘린 좌표 사용(→ xu 풀린 좌표)
확인(자동): 전반 · 후반 밀도 차 < 1 % · 분자 최대 크기 < rc · 프레임마다 벌크 · 분자 에너지 짝 맞음
"""
import argparse, math, re
from collections import OrderedDict
from pathlib import Path
import numpy as np
from .common import workspace, need, run, dump, PKG, KCALMOL_A3_TO_MJM3


def thermo_blocks(log):
    blocks, cols, cur = [], None, None
    for line in Path(log).read_text(errors="replace").splitlines():
        s = line.split()
        if not s: continue
        if s[0] == "Step": cols = s; cur = []; blocks.append((cols, cur)); continue
        if s[0] == "Loop": cur = None; continue
        if cur is not None and len(s) == len(cols):
            try: cur.append([float(x) for x in s])
            except ValueError: pass
    return [{c: np.array([r[i] for r in rows]) for i, c in enumerate(cols)} for cols, rows in blocks if rows]


def block_se(x, nb=5):
    n = len(x) // nb
    if n < 1: return float("nan")
    m = np.array([x[i * n:(i + 1) * n].mean() for i in range(nb)])
    return float(m.std(ddof=1) / math.sqrt(nb))


def read_frames(path):
    frames, L = [], Path(path).read_text().splitlines(); i = 0
    while i < len(L):
        if L[i].startswith("ITEM: TIMESTEP"):
            step = int(L[i + 1]); n = int(L[i + 3])
            box = [tuple(map(float, L[i + 5 + k].split()[:2])) for k in range(3)]
            cols = L[i + 8].split()[2:]
            arr = np.array([l.split() for l in L[i + 9:i + 9 + n]], dtype=float)
            frames.append((step, box, {c: arr[:, j] for j, c in enumerate(cols)})); i += 9 + n
        else: i += 1
    return frames


def spread_dump(frames, path, S):
    """분자마다 질량 중심 대신 좌표 평균을 격자점으로 옮긴다(분자 모양 · 내부 거리는 그대로)."""
    mol = frames[0][2]["mol"].astype(int); ids = frames[0][2]["id"].astype(int)
    mols = np.unique(mol); side = math.ceil(len(mols) ** (1 / 3)); B = side * S
    grid = {m: (np.array(np.unravel_index(k, (side, side, side))) + 0.5) * S for k, m in enumerate(mols)}
    ext = 0.0
    with open(path, "w") as f:
        for step, box, d in frames:
            xyz = np.stack([d["xu"], d["yu"], d["zu"]], 1); out = np.empty_like(xyz)
            for m in mols:
                sel = mol == m; c = xyz[sel].mean(0); out[sel] = xyz[sel] - c + grid[m]
                ext = max(ext, float(np.ptp(xyz[sel], axis=0).max()))
            f.write(f"ITEM: TIMESTEP\n{step}\nITEM: NUMBER OF ATOMS\n{len(ids)}\nITEM: BOX BOUNDS ff ff ff\n0 {B}\n0 {B}\n0 {B}\nITEM: ATOMS id x y z\n")
            for i, (x, y, z) in zip(ids, out): f.write(f"{i} {x:.5f} {y:.5f} {z:.5f}\n")
    return B, ext, len(mols)


def analyze(rid, ws, S=120.0, rc=55.0, threads=1):
    rdir = ws / "runs" / rid
    blocks = thermo_blocks(rdir / "log.lammps")
    prod = blocks[-1]                                   # 생산 구간 = 마지막 run
    rho = prod["Density"]; k0 = len(rho) // 5; eq = rho[k0:]   # 앞 20 % 는 버림
    h = len(eq) // 2; half = abs(eq[h:].mean() - eq[:h].mean()) / eq.mean() * 100
    res = OrderedDict(id=rid, density_gcm3=round(float(eq.mean()), 4), density_se=round(block_se(eq), 4),
                      density_half_diff_pct=round(float(half), 3), density_ok=bool(half < 1.0), n_thermo=int(len(eq)),
                      t_prod_ps=float(prod["Step"][-1] / 1000))
    frames = read_frames(rdir / "prod.lammpstrj")
    frames = frames[len(frames) // 5:] if len(frames) > 5 else frames
    B, ext, nmol = spread_dump(frames, rdir / "spread.lammpstrj", S)
    if ext + 2 >= rc or S - ext <= rc: raise SystemExit(f"분자 크기 {ext:.1f} Å 가 너무 큼 · S · rc 를 키워야 함")
    need("lmp")
    run(["lmp", "-in", str(PKG / "templates" / "in.intra"), "-log", "log.intra", "-screen", "none",
         "-var", "data", "system.data", "-var", "rc", str(rc), "-var", "B", str(B), "-var", "dump", "spread.lammpstrj"], rdir, rdir / "intra.out")
    intra = thermo_blocks(rdir / "log.intra")[-1]
    e_in = dict(zip(intra["Step"].astype(int), intra["PotEng"]))
    bulk = dict(zip(prod["Step"].astype(int), zip(prod["PotEng"], prod["Volume"])))
    rows = []
    for step, box, d in frames:
        if step in bulk and step in e_in:
            Eb, V = bulk[step]; Ei = -(Eb - e_in[step]) / V * KCALMOL_A3_TO_MJM3
            rows.append((step, Eb, e_in[step], V, Ei))
    with open(rdir / "ced_frames.csv", "w") as f:
        f.write("step,E_bulk_kcalmol,E_intra_sum_kcalmol,V_A3,CED_MJm3\n")
        for r in rows: f.write(",".join(f"{x:.4f}" if isinstance(x, float) else str(x) for x in r) + "\n")
    ced = np.array([r[4] for r in rows])
    res.update(ced_MJm3=round(float(ced.mean()), 1), ced_se=round(block_se(ced, min(5, len(ced))), 1),
               delta_MPa05=round(math.sqrt(max(ced.mean(), 0)), 2), n_frames=len(rows), n_molecules=nmol,
               max_molecule_extent_A=round(ext, 1), ced_note="E_inter = E_bulk(PPPM · tail) − Σ E_분자(직접 합) · 생산 구간 앞 20 % 버림")
    dump(res, rdir / "props.json")
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description="밀도 · CED 계산 (MD 워크플로우 ⑤)")
    ap.add_argument("id"); ap.add_argument("--ws")
    a = ap.parse_args(argv); ws = workspace(a.ws); r = analyze(a.id, ws)
    print(f"물성 {a.id}: ρ {r['density_gcm3']} ± {r['density_se']} g/cm³ (전후반 차 {r['density_half_diff_pct']} %) · "
          f"CED {r['ced_MJm3']} ± {r['ced_se']} MJ/m³ · δ {r['delta_MPa05']} MPa^0.5 · 프레임 {r['n_frames']}")


if __name__ == "__main__":
    main()
