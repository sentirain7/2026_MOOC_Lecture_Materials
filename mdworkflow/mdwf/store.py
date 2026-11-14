"""⑥ 결과 표: 한 계산 = 한 줄 (조성 · 물성 · 오차 · 조건 · 출처) → ws/db/results.csv

열: id · SARA 목표/실제 wt% · 분자 수 · 원자 수 · T · 프로토콜 · seed · 코어 · 밀도 ± · CED ± · δ · 판정 · 힘장 · 벽시계 · 근거(citekey)
틀리기 쉬운 곳: 같은 id 를 두 번 기록 · 실패한 계산을 값 없이 지움(→ 지우지 않고 ok=False 로 남김) · 조건 열 누락
"""
import argparse, csv, json
from pathlib import Path
from .common import workspace

COLS = ["id", "S_wt", "A_wt", "R_wt", "As_wt", "S_act", "A_act", "R_act", "As_act", "n_mol", "n_atoms", "T_K", "protocol", "seed", "threads",
        "density_gcm3", "density_se", "ced_MJm3", "ced_se", "delta_MPa05", "ok", "ff", "wall_s", "source"]


def row(rid, ws, source=""):
    cell_id = json.loads((ws / "runs" / rid / "status.json").read_text())["cell"]
    c = json.loads((ws / "cells" / cell_id / "cell.json").read_text())
    s = json.loads((ws / "runs" / rid / "status.json").read_text())
    p = ws / "runs" / rid / "props.json"; pr = json.loads(p.read_text()) if p.exists() else {}
    sara = c.get("sara") or {}
    tw, aw = sara.get("target_wt", [""] * 4), sara.get("actual_wt", {})
    return {"id": rid, "S_wt": tw[0], "A_wt": tw[1], "R_wt": tw[2], "As_wt": tw[3],
            "S_act": aw.get("saturate", ""), "A_act": aw.get("aromatic", ""), "R_act": aw.get("resin", ""), "As_act": aw.get("asphaltene", ""),
            "n_mol": c["data"]["molecules"], "n_atoms": c["data"]["atoms"], "T_K": s["T"], "protocol": s["protocol"], "seed": s["seed"], "threads": s["threads"],
            "density_gcm3": pr.get("density_gcm3", ""), "density_se": pr.get("density_se", ""), "ced_MJm3": pr.get("ced_MJm3", ""), "ced_se": pr.get("ced_se", ""),
            "delta_MPa05": pr.get("delta_MPa05", ""), "ok": bool(s["ok"] and pr.get("density_ok", False)), "ff": "gaff2/am1-bcc (mdworkflow)",
            "wall_s": s["wall_s_total"], "source": source}


def store(rid, ws, source="", db=None):
    db = Path(db) if db else ws / "db" / "results.csv"
    rows = list(csv.DictReader(open(db, encoding="utf-8"))) if db.exists() else []
    if any(r["id"] == rid for r in rows):
        raise SystemExit(f"{rid} 는 이미 기록됨 · 다시 계산했다면 새 id 를 쓴다(기록은 지우지 않는다)")
    r = row(rid, ws, source); new = not db.exists()
    with open(db, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, COLS)
        if new: w.writeheader()
        w.writerow(r)
    return r


def main(argv=None):
    ap = argparse.ArgumentParser(description="결과 표 기록 (MD 워크플로우 ⑥)")
    ap.add_argument("id"); ap.add_argument("--source", default="", help="근거 citekey 등"); ap.add_argument("--ws")
    a = ap.parse_args(argv); ws = workspace(a.ws); r = store(a.id, ws, a.source)
    print(f"기록 {a.id} → {ws / 'db' / 'results.csv'} · ρ {r['density_gcm3']} · CED {r['ced_MJm3']} · ok {r['ok']}")


if __name__ == "__main__":
    main()
