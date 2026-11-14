#!/usr/bin/env python3
"""density_from_log.py — LAMMPS log 의 thermo 블록 → 밀도 시계열 · 누적 평균 · 폐기 구간 · 블록 표준오차
  python3 scripts/density_from_log.py out/prod/log.prod [--col Density] [--discard 0.3] [--block 10] [--dt 1.0] [--thermo 100]
출력: out/density.json · out/density_series.csv (step, t_ps, value, running_mean)
규칙(원본 06주차 #7 · #27): ρ = M/⟨V⟩ 의 요동은 V 뿐 → 평형 구간 평균 ± 블록 SE · 전반 · 후반 차 < 0.5 % 면 수렴.
"""
import argparse, json, math, re, sys
from pathlib import Path

def parse_thermo(path):
    """log 안의 모든 thermo 블록(Step 머리줄 ~ Loop time)을 이어 붙인다. 열 이름 → 값 목록."""
    rows, cols, inblock = [], None, False
    for line in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
        s = line.split()
        if not s: continue
        if s[0] == "Step": cols = s; inblock = True; continue
        if inblock and s[0] == "Loop": inblock = False; continue
        if inblock and cols and len(s) == len(cols):
            try: rows.append([float(x) for x in s])
            except ValueError: pass
    if not cols or not rows: sys.exit("thermo 블록을 찾지 못함")
    return {c: [r[i] for r in rows] for i, c in enumerate(cols)}

def block_se(x, nblock):
    n = len(x) // nblock
    if n < 2: return float("nan")
    means = [sum(x[i*n:(i+1)*n]) / n for i in range(nblock)]
    m = sum(means) / nblock
    var = sum((v - m) ** 2 for v in means) / (nblock - 1)
    return math.sqrt(var / nblock)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("log"); ap.add_argument("--col", default="Density")
    ap.add_argument("--discard", type=float, default=0.3, help="앞쪽 폐기 비율"); ap.add_argument("--block", type=int, default=10)
    ap.add_argument("--dt", type=float, default=1.0); ap.add_argument("--out", default="out")
    a = ap.parse_args(); th = parse_thermo(a.log)
    steps, x = th["Step"], th[a.col]
    # NPT 구간만(밀도가 변하는 구간): 같은 step 값이 두 번 나오면(run 2회) 첫 블록만 쓴다
    cut = len(steps)
    for i in range(1, len(steps)):
        if steps[i] <= steps[i-1]: cut = i; break
    steps, x = steps[:cut], x[:cut]
    k0 = int(len(x) * a.discard); eq = x[k0:]
    mean = sum(eq) / len(eq); se = block_se(eq, a.block)
    half = len(eq) // 2; m1 = sum(eq[:half]) / half; m2 = sum(eq[half:]) / (len(eq) - half)
    run = []; acc = 0.0
    for i, v in enumerate(x): acc += v; run.append(acc / (i + 1))
    out = Path(a.out); out.mkdir(exist_ok=True)
    with open(out / "density_series.csv", "w", encoding="utf-8") as f:
        f.write("step,t_ps,value,running_mean\n")
        for s, v, r in zip(steps, x, run): f.write(f"{int(s)},{s*a.dt/1000:.3f},{v:.6f},{r:.6f}\n")
    res = {"column": a.col, "n_samples": len(x), "n_used": len(eq), "discard_fraction": a.discard, "t_total_ps": steps[-1]*a.dt/1000,
           "mean": round(mean, 5), "block_se": round(se, 5), "n_block": a.block, "first_half": round(m1, 5), "second_half": round(m2, 5),
           "half_diff_pct": round(abs(m2 - m1) / mean * 100, 3), "converged_0p5pct": abs(m2 - m1) / mean < 0.005,
           "naive_se": round((sum((v-mean)**2 for v in eq)/(len(eq)-1))**0.5/len(eq)**0.5, 5), "unit": "g/cm3" if a.col == "Density" else ""}
    (out / "density.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False))
if __name__ == "__main__": main()
