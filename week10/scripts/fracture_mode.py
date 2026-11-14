#!/usr/bin/env python3
"""week10 — 마지막 덤프 프레임에서 파괴 모드를 판정한다 (원본 06주차 보충A #25 · #27 · paper13 R6 2.3절 규칙의 교육용 축소판).

지표 2
  e      = 노출률: 슬래브 윗면을 2 × 2 Å 격자로 나눠 바인더(또는 물) 원자가 5 Å 안에 하나도 없는 칸의 비율
  t_res  = 잔류 두께: 슬래브 윗면 위 12 Å 안에 남은 바인더 원자의 z 90 백분위 − 슬래브 윗면 (Å)
판정   e > 0.5 → 계면 박리(adhesive) · t_res ≥ z1(기본 4.0 Å · 단분자층 두께) → 응집 파괴(cohesive) · 그 사이 → 박층 응집(thin-layer)
실행: python3 scripts/fracture_mode.py out/wet/pull.dump [--z1 4.0] [--e 0.5] [--frame -1]
출력: out/<tag>/fracture.json
"""
import argparse, json, math
from pathlib import Path


def frames(path):
    lines = Path(path).read_text().splitlines(); i = 0; out = []
    while i < len(lines):
        if lines[i].startswith("ITEM: TIMESTEP"):
            step = int(lines[i + 1]); n = int(lines[i + 3]); box = [list(map(float, lines[i + 5 + k].split()[:2])) for k in range(3)]
            cols = lines[i + 8].split()[2:]; rows = [dict(zip(cols, l.split())) for l in lines[i + 9:i + 9 + n]]
            out.append((step, box, rows)); i += 9 + n
        else: i += 1
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("dump"); ap.add_argument("--z1", type=float, default=4.0); ap.add_argument("--e", type=float, default=0.5); ap.add_argument("--frame", type=int, default=-1)
    a = ap.parse_args(); p = Path(a.dump); summ = json.loads((p.parent / "pull_summary.json").read_text())
    fr = frames(p); step, box, rows = fr[a.frame]
    ns, nw = summ["n_slab"], summ["n_water"]
    at = [(int(r["id"]), float(r["x"]), float(r["y"]), float(r["z"])) for r in rows]
    slab_top = max(z for i, x, y, z in at if i <= ns)
    binder = [(x, y, z) for i, x, y, z in at if i > ns + nw]; water = [(x, y, z) for i, x, y, z in at if ns < i <= ns + nw]
    Lx, Ly = box[0][1] - box[0][0], box[1][1] - box[1][0]; g = 2.0; nx, ny = int(Lx // g), int(Ly // g)
    cover = [[False] * ny for _ in range(nx)]
    for x, y, z in binder + water:
        if slab_top < z <= slab_top + 5.0: cover[int(((x - box[0][0]) % Lx) // g) % nx][int(((y - box[1][0]) % Ly) // g) % ny] = True
    e = 1 - sum(map(sum, cover)) / (nx * ny)
    near = sorted(z - slab_top for x, y, z in binder if slab_top < z <= slab_top + 12.0)
    t_res = near[int(0.9 * (len(near) - 1))] if near else 0.0
    zb = sorted(z for x, y, z in binder); zb_low, zb_high = zb[int(0.05 * len(zb))], zb[int(0.95 * len(zb))]
    gap = (min(zb) - (max(z for x, y, z in water) if water else slab_top))
    mode = "adhesive(계면 박리)" if e > a.e else ("cohesive(응집 파괴)" if t_res >= a.z1 else "thin-layer(박층 응집)")
    out = dict(tag=summ["tag"], frame_step=step, slab_top_A=round(slab_top, 2), exposure_e=round(e, 3), t_res_A=round(t_res, 2), z1_A=a.z1, e_threshold=a.e, mode=mode,
               binder_z_5_95_A=[round(zb_low, 1), round(zb_high, 1)], gap_binder_below_A=round(gap, 2), n_binder_within_12A=len(near), grid=[nx, ny],
               rule="e > e_th → adhesive · t_res ≥ z1 → cohesive · else thin-layer (paper13 R6 2.3절 축소판)")
    (p.parent / "fracture.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(f"{summ['tag']} step {step}: e {e:.2f} · t_res {t_res:.1f} Å · {mode} · 바인더 z {zb_low:.1f}~{zb_high:.1f} · 아래 틈 {gap:.1f} Å")


if __name__ == "__main__":
    main()
