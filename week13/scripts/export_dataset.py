#!/usr/bin/env python3
"""COMID 플랫폼 DB(읽기 전용)에서 W13 학습용 표를 CSV 로 내보낸다.

  python3 scripts/export_dataset.py --db <asphalt_agent.db 경로>   # 강사용 (DB 접근 필요)
  → data/bulk_md_373.csv  (이 저장소에 이미 들어 있다 — 수강생은 실행하지 않는다)

대상 = study_type 'bulk' · status 'completed' 인 MD 실행 한 건 = 한 행.
열: run(실행 번호) · binder(AAA1/AAK1/AAM1) · aging(0 비노화 · 1 단기 · 2 장기) · additive_wt · h2o(물 분자 수)
    · T_K · seed · cell(조성 셀 이름 = 그룹) · density(g/cm3) · ced(MJ/m3) · bulk_modulus(GPa)
개인 · 경로 · 호스트 정보는 넣지 않는다(실행 ID 는 순번으로 바꾼다).
"""
import argparse, csv, json, sqlite3, sys
from pathlib import Path

AGING = {"non_aging": 0, "short_aging": 1, "long_aging": 2}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True)
    ap.add_argument("--out", default=str(Path(__file__).resolve().parents[1] / "data" / "bulk_md_373.csv"))
    a = ap.parse_args()
    con = sqlite3.connect(f"file:{a.db}?mode=ro", uri=True)
    q = """select e.id, e.temperature_K, e.seed, e.additive_type, e.additive_wt, e.prepared_artifact_json,
      (select value from metrics where experiment_id=e.id and metric_name='density' and namespace='bulk_ff_gaff2'),
      (select value from metrics where experiment_id=e.id and metric_name='cohesive_energy_density'),
      (select value from metrics where experiment_id=e.id and metric_name='bulk_modulus')
      from experiments e where e.status='completed' order by e.id"""
    rows = []
    for eid, T, seed, add, addwt, pj, rho, ced, K in con.execute(q):
        j = json.loads(pj)
        pr = j.get("protocol_request") or {}
        if pr.get("study_type") != "bulk" or rho is None:
            continue
        mat = j.get("material_id") or ""
        binder, _, aging = mat.split("_", 2)          # AAA1_X3_non_aging → AAA1 · X3 · non_aging
        aging = aging.split("_", 1)[1] if aging.startswith("X") else aging
        cnt = (j.get("build_request") or {}).get("prebuilt_molecule_counts") or {}
        h2o = int(cnt.get("H2O", 0))
        cell = f"{binder}-{aging}" + (f"+{add}" if add else "") + (f"+w{h2o}" if h2o else "")
        rows.append(dict(binder=binder, aging=AGING[aging], additive_wt=round(addwt or 0.0, 4), h2o=h2o,
                         T_K=int(T), seed=int(seed), cell=cell, density=round(rho, 5),
                         ced=None if ced is None else round(ced, 2), bulk_modulus=None if K is None else round(K, 4)))
    rows.sort(key=lambda r: (r["cell"], r["T_K"], r["seed"]))
    for i, r in enumerate(rows, 1):
        r["run"] = i
    cols = ["run", "binder", "aging", "additive_wt", "h2o", "T_K", "seed", "cell", "density", "ced", "bulk_modulus"]
    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
    print(f"{len(rows)} rows · {len({r['cell'] for r in rows})} cells → {a.out}")


if __name__ == "__main__":
    sys.exit(main())
