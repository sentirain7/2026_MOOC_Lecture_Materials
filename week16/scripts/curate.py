#!/usr/bin/env python3
"""W16 · 데이터 큐레이션 깔때기 — 코어 672행 → 물리 게이트(표시) → 계산 조건 필터 → 중복 조건 검사 → 표적 완비.
원칙(원본 12주차 #18 · #19): 실패 · 이상값은 지우지 않고 플래그를 단다. 값이 아니라 계산 조건이 원인이면 그 조건(tier)의 해당 물성만 뺀다.

  python3 scripts/curate.py data/core672.csv --fixed data/features614.csv --out out/curation.json --csv out/curated612.csv
입력: COMID claude_science_export/comid_core672_dataset.csv (MD 계산값 · 모델링 코어 672행)
      COMID final_feature_dataset (614행) = 재라벨 · 재백필이 끝난 스냅샷 — 이 스크립트는 차이를 세기만 한다(재계산 안 함)
"""
import argparse, csv, json, math

def f(x):
    try:
        v = float(x); return v if math.isfinite(v) else None
    except (TypeError, ValueError):
        return None

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("--fixed", default="data/features614.csv"); ap.add_argument("--out", default="out/curation.json"); ap.add_argument("--csv", default="out/curated612.csv")
ap.add_argument("--rho", default="0.7,1.3"); ap.add_argument("--kmax", type=float, default=50.0)
a = ap.parse_args()
rows = list(csv.DictReader(open(a.src, encoding="utf-8")))
lo, hi = map(float, a.rho.split(","))
stages = [{"stage": "raw", "label": "코어 행(완료 실험)", "n": len(rows)}]

# 1) 물리 범위 게이트 — 표시만(삭제 아님)
for r in rows:
    d, K, C = f(r["density"]), f(r["bulk_modulus"]), f(r["cohesive_energy_density"])
    fl = []
    if d is not None and not (lo <= d <= hi): fl.append("density_range")
    if K is not None and not (0.1 <= K <= a.kmax): fl.append("K_range")
    if C is not None and C < 0: fl.append("CED_negative")
    r["flags"] = ";".join(fl)
nK = sum("K_range" in r["flags"] for r in rows); nC = sum("CED_negative" in r["flags"] for r in rows)
nflag = sum(bool(r["flags"]) for r in rows)
stages.append({"stage": "gate", "label": "물리 범위 게이트(표시)", "n": len(rows), "flagged": nflag, "K_gt_50GPa": nK, "CED_negative": nC})

# 2) 계산 조건 필터 — 점도(전단) 런 = viscosity 값이 있는 행 · NPT 구간이 없어 K · CED 를 정의할 수 없다
visc = [r for r in rows if f(r["viscosity"]) is not None]
keep = [r for r in rows if f(r["viscosity"]) is None]
flag_in_visc = sum(bool(r["flags"]) for r in visc)
stages.append({"stage": "tier", "label": "점도(전단) 런 제외 — K · CED 정의 불가", "n": len(keep), "removed": len(visc),
               "removed_with_flag": flag_in_visc, "flag_left": sum(bool(r["flags"]) for r in keep)})

# 3) 라벨 복원 · 결측 재백필 (COMID 가 원본 로그 · exp_id 경로로 수행한 결과와 대조)
fx = {r["experiment_id"]: r for r in csv.DictReader(open(a.fixed, encoding="utf-8"))}
relab = sum(r["aging_state"] != fx[r["experiment_id"]]["aging_state"] for r in keep if r["experiment_id"] in fx)
backK = sum(f(r["bulk_modulus"]) is None and f(fx[r["experiment_id"]]["bulk_modulus"]) is not None for r in keep if r["experiment_id"] in fx)
for r in keep:
    g = fx.get(r["experiment_id"])
    if g:
        for c in ("aging_state", "bulk_modulus", "cohesive_energy_density", "density", "e_inter_total"): r[c] = g[c]
stages.append({"stage": "relabel", "label": "노화 라벨 복원 · K 재백필(원본 로그)", "n": len(keep), "aging_relabeled": relab, "K_backfilled": backK})

# 4) 중복 조건 검사 (바인더 · 첨가제 · 노화 · 온도)
key = lambda r: (r["binder_type"], r["additive_type"], r["aging_state"], r["temperature_K"])
seen, dup = set(), 0
for r in keep:
    k = key(r); dup += k in seen; seen.add(k)
stages.append({"stage": "dedup", "label": "중복 조건 검사", "n": len(keep), "duplicates": dup})

# 5) 표적 완비 — 두 목표(K · CED) 모두 있는 행
full = [r for r in keep if f(r["bulk_modulus"]) is not None and f(r["cohesive_energy_density"]) is not None]
miss = [(r["binder_type"], r["additive_type"]) for r in keep if r not in full]
stages.append({"stage": "complete", "label": "두 목표(K · CED) 완비", "n": len(full), "missing": len(keep) - len(full), "missing_rows": miss})

cols = ["experiment_id", "binder_type", "additive_type", "aging_state", "temperature_K", "density", "bulk_modulus", "cohesive_energy_density", "e_inter_total"]
with open(a.csv, "w", newline="", encoding="utf-8") as fo:
    w = csv.writer(fo); w.writerow(cols)
    for r in full: w.writerow([r[c] for c in cols])
res = {"source": a.src, "rule": "실패 · 이상값은 삭제 대신 플래그 · 원인이 계산 조건이면 그 조건의 물성만 제외", "stages": stages}
json.dump(res, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for s in stages: print(f"{s['stage']:9s} {s['n']:4d}  {s['label']}  " + " ".join(f"{k}={v}" for k, v in s.items() if k not in ('stage','label','n','missing_rows')))
print("→", a.out, a.csv)
