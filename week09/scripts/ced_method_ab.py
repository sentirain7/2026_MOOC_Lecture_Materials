#!/usr/bin/env python3
"""ced_method_ab.py — 응집에너지밀도 CED 두 경로 (원본 06주차 #16 · COMID metrics/ced.py 의 E_intra 차감)
  Method A (직접 · 고정 좌표): 벌크 마지막 좌표의 분자 50개를 하나씩 큰 상자에 그대로 두고 run 0 → ΣE_single(fixed)
      E_inter = E_bulk(같은 좌표 · run 0) − ΣE_single(fixed) · CED_A = −E_inter / V
  Method B (간접 · 이완 기상): 분자 1개를 큰 상자에서 NVT 298 K 로 돌려 ⟨E_gas⟩ 평균 → CED_B = (50⟨E_gas⟩ − ⟨E_bulk⟩) / ⟨V⟩
  δ = √CED (MPa^0.5).  python3 scripts/ced_method_ab.py out/prod/nvt_final.data out/prod/log.prod [--lmp lmp] [--gas-steps 20000]
표준 라이브러리만 · LAMMPS 실행 필요. 출력 out/ced.json · out/ced_trace.csv(Method A 누적 · Method B 평균 수렴)
"""
import argparse, json, math, re, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
KCALMOL_A3_TO_MJM3 = 4184.0 / 6.02214076e23 / 1e-30 / 1e6   # kcal/mol/Å³ → MJ/m³ (= 6.9477)

def read_data(path):
    txt = Path(path).read_text(encoding="utf-8").splitlines()
    head, sec, cur = [], {}, None
    for line in txt:
        s = line.strip()
        if not s: continue
        key = s.split("#")[0].strip()
        if key in ("Masses", "Atoms", "Velocities", "Bonds", "Angles", "Dihedrals", "Impropers") or key.endswith("Coeffs"):
            cur = key; sec[cur] = []; continue
        if cur is None: head.append(line)
        else: sec[cur].append(line)
    return head, sec

def write_single(head, sec, mol, path, box=100.0):
    """분자 mol 의 원자 · 결합 · 각 · 이면각만 추려 큰 상자(box Å) data 로 쓴다 (좌표는 그대로 · id 재부여)."""
    atoms = [l.split() for l in sec["Atoms"]]
    # 주기 이미지 플래그(nx ny nz · 8~10열)로 좌표를 풀어 분자가 상자 경계에서 끊기지 않게 한다
    Ls = {}
    for h in head:
        s = h.split()
        if len(s) == 4 and s[2].endswith("lo"): Ls[s[2][0]] = float(s[1]) - float(s[0])
    def unwrap(a):
        a = list(a)
        if len(a) >= 10:
            a[4] = str(float(a[4]) + int(a[7]) * Ls.get("x", 0)); a[5] = str(float(a[5]) + int(a[8]) * Ls.get("y", 0)); a[6] = str(float(a[6]) + int(a[9]) * Ls.get("z", 0))
        return a
    mine = [unwrap(a) for a in atoms if int(a[1]) == mol]
    idmap = {int(a[0]): i + 1 for i, a in enumerate(mine)}
    def keep(lines, nidx):
        out = []
        for l in lines:
            s = l.split(); ids = [int(x) for x in s[2:2+nidx]]
            if all(i in idmap for i in ids): out.append([str(len(out)+1), s[1]] + [str(idmap[i]) for i in ids])
        return out
    bonds, angles, dihs = keep(sec["Bonds"], 2), keep(sec["Angles"], 3), keep(sec["Dihedrals"], 4)
    # 좌표를 상자 중앙 근처로 옮긴다(주기 이미지 플래그 제거)
    xs = [float(a[4]) for a in mine]; ys = [float(a[5]) for a in mine]; zs = [float(a[6]) for a in mine]
    cx, cy, cz = sum(xs)/len(xs), sum(ys)/len(ys), sum(zs)/len(zs)
    L = []
    L.append(f"single molecule {mol} (week09 ced_method_ab)\n")
    L.append(f"{len(mine)} atoms\n{len(bonds)} bonds\n{len(angles)} angles\n{len(dihs)} dihedrals\n")
    for h in head:
        if "types" in h: L.append(h.strip() + "\n")
    L.append(f"0.0 {box} xlo xhi\n0.0 {box} ylo yhi\n0.0 {box} zlo zhi\n")
    for k in ("Masses", "Pair Coeffs", "Bond Coeffs", "Angle Coeffs", "Dihedral Coeffs"):
        for kk in sec:
            if kk == k or kk.startswith(k):
                L.append(f"\n{kk}\n\n" + "\n".join(sec[kk]) + "\n")
                break
    L.append("\nAtoms # full\n\n")
    for a in mine:
        L.append(f"{idmap[int(a[0])]} 1 {a[2]} {a[3]} {float(a[4])-cx+box/2:.6f} {float(a[5])-cy+box/2:.6f} {float(a[6])-cz+box/2:.6f}\n")
    for name, rows in (("Bonds", bonds), ("Angles", angles), ("Dihedrals", dihs)):
        L.append(f"\n{name}\n\n" + "\n".join(" ".join(r) for r in rows) + "\n")
    Path(path).write_text("".join(L), encoding="utf-8")
    return len(mine)

def lmp_pe(exe, infile, var, log, extra=""):
    cmd = [exe, "-in", str(infile), "-log", str(log), "-screen", "none"] + sum([["-var", k, str(v)] for k, v in var.items()], [])
    r = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    if r.returncode != 0: sys.stderr.write(r.stderr[-1500:]); sys.exit("LAMMPS 실패 " + str(infile))

def thermo(path):
    rows, cols, inb = [], None, False
    for line in Path(path).read_text(errors="replace").splitlines():
        s = line.split()
        if not s: continue
        if s[0] == "Step": cols = s; inb = True; continue
        if inb and s[0] == "Loop": inb = False; continue
        if inb and cols and len(s) == len(cols):
            try: rows.append([float(x) for x in s])
            except ValueError: pass
    return cols, rows

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("data"); ap.add_argument("log")
    ap.add_argument("--lmp", default="lmp"); ap.add_argument("--gas-steps", type=int, default=20000); ap.add_argument("--out", default="out"); ap.add_argument("--T", type=float, default=298.0)
    a = ap.parse_args(); out = ROOT / a.out; tmp = out / "ced_tmp"; tmp.mkdir(parents=True, exist_ok=True)
    head, sec = read_data(ROOT / a.data)
    nmol = max(int(l.split()[1]) for l in sec["Atoms"])
    # 벌크(같은 좌표 · run 0 · pppm 포함) 에너지
    inb = tmp / "in.bulk0"; inb.write_text((ROOT / "data/in.prod").read_text().split("timestep")[0] + "thermo_style custom step pe evdwl ecoul elong ebond eangle edihed vol\nrun 0\n")
    lmp_pe(a.lmp, inb, {"data": a.data, "out": a.out, "seed": 1, "npt_steps": 0, "nvt_steps": 0}, tmp / "log.bulk0")
    cols, rows = thermo(tmp / "log.bulk0"); r = dict(zip(cols, rows[-1])); E_bulk0, V0 = r["PotEng"], r["Volume"]
    # Method A: 분자별 고정 좌표 run 0
    in0 = tmp / "in.single0"; in0.write_text((ROOT / "data/in.gas").read_text() + "run 0\n")
    singles, trace = [], []
    for m in range(1, nmol + 1):
        d = tmp / f"mol{m}.data"; write_single(head, sec, m, d)
        lmp_pe(a.lmp, in0, {"data": str(d.relative_to(ROOT)), "thermo": 1}, tmp / f"log.mol{m}")
        c2, r2 = thermo(tmp / f"log.mol{m}"); e = dict(zip(c2, r2[-1]))["PotEng"]; singles.append(e)
        trace.append((m, e, sum(singles)))
    E_intra_fixed = sum(singles); E_inter = E_bulk0 - E_intra_fixed
    ced_A = -E_inter / V0 * KCALMOL_A3_TO_MJM3
    # Method B: 분자 1 이완 기상 NVT 평균 · 벌크 ⟨E⟩ · ⟨V⟩ 는 생산 구간 로그 평균
    ing = tmp / "in.gasB"; ing.write_text((ROOT / "data/in.gas").read_text() + f"velocity all create {a.T} 12345 mom yes rot yes dist gaussian\nfix nvt all nvt temp {a.T} {a.T} 100.0\nrun {a.gas_steps}\n")
    lmp_pe(a.lmp, ing, {"data": str((tmp / "mol1.data").relative_to(ROOT)), "thermo": 100}, tmp / "log.gasB")
    c3, r3 = thermo(tmp / "log.gasB"); pes = [dict(zip(c3, x))["PotEng"] for x in r3]; k0 = len(pes) // 4; Egas = sum(pes[k0:]) / len(pes[k0:])
    gas_run = []; acc = 0.0
    for i, v in enumerate(pes): acc += v; gas_run.append(acc / (i + 1))
    cl, rl = thermo(ROOT / a.log); recs = [dict(zip(cl, x)) for x in rl]
    # 생산(NVT) 구간 = 두 번째 run 블록(step 이 다시 작아진 뒤)
    cut = 0
    for i in range(1, len(recs)):
        if recs[i]["Step"] <= recs[i-1]["Step"]: cut = i
    prod = recs[cut:] if cut else recs[len(recs)//2:]
    Eb = sum(x["PotEng"] for x in prod) / len(prod); Vb = sum(x["Volume"] for x in prod) / len(prod)
    ced_B = (nmol * Egas - Eb) / Vb * KCALMOL_A3_TO_MJM3
    res = {"n_mol": nmol, "E_bulk_run0_kcalmol": round(E_bulk0, 2), "V_run0_A3": round(V0, 1), "sum_E_single_fixed": round(E_intra_fixed, 2),
           "E_inter_kcalmol": round(E_inter, 2), "CED_A_MJm3": round(ced_A, 1), "delta_A_MPa05": round(math.sqrt(max(ced_A, 0)), 2),
           "E_gas_relaxed_mean": round(Egas, 3), "E_bulk_prod_mean": round(Eb, 2), "V_prod_mean_A3": round(Vb, 1),
           "CED_B_MJm3": round(ced_B, 1), "delta_B_MPa05": round(math.sqrt(max(ced_B, 0)), 2),
           "diff_pct": round(abs(ced_A - ced_B) / max(ced_A, 1e-9) * 100, 1), "gas_steps": a.gas_steps,
           "note": "짧은 실행(수십 ps · ρ 수렴 전) — 두 경로의 「구조」와 차이를 보는 값 · 데이터셋 전체에서 한 방식 고정(원본 06주차 #16)"}
    (out / "ced.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    with open(out / "ced_trace.csv", "w") as f:
        f.write("i,E_single_fixed,cum_sum_A,gas_step,gas_running_mean_B\n")
        for i in range(max(len(trace), len(gas_run))):
            t = trace[i] if i < len(trace) else ("", "", ""); g = (r3[i][0], gas_run[i]) if i < len(gas_run) else ("", "")
            f.write(f"{t[0]},{t[1]},{t[2]},{g[0]},{g[1]}\n")
    print(json.dumps(res, ensure_ascii=False))
if __name__ == "__main__": main()
