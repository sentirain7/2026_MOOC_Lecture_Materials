"""폐루프 공용: 설정 · 경로 · 결과 표 · 후보 표."""
import csv, json, sys
from pathlib import Path
import numpy as np

LOOP = Path(__file__).resolve().parents[1]           # repo/loop
REPO = LOOP.parent
sys.path.insert(0, str(REPO / "mdworkflow"))         # MD 워크플로우(mdwf) 를 같은 저장소에서 부른다
OBJ = ["density", "ced"]
RES_COLS = ["id", "round", "cand", "smiles", "n_mol", "n_atoms", "density_gcm3", "density_se", "ced_MJm3", "ced_se", "ok", "wall_s", "mode"]


def load_cfg(path=None):
    import yaml
    return yaml.safe_load(open(path or LOOP / "config" / "loop.yaml", encoding="utf-8"))


def ws(cfg):
    w = LOOP / "ws" / cfg["name"]; (w / "db").mkdir(parents=True, exist_ok=True); return w


def library(cfg):
    p = ws(cfg) / cfg["design"]["library"]
    if not p.exists(): raise SystemExit(f"{p} 없음 · 먼저 python scripts/library.py")
    rows = list(csv.DictReader(open(p, encoding="utf-8")))
    X = np.array([[float(r[f]) for f in cfg["design"]["features"]] for r in rows])
    return rows, X


def results(w):
    p = w / "db" / "loop_results.csv"
    return list(csv.DictReader(open(p, encoding="utf-8"))) if p.exists() else []


def add_result(w, row):
    p = w / "db" / "loop_results.csv"; new = not p.exists()
    with open(p, "a", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, RES_COLS); (wr.writeheader() if new else None); wr.writerow({k: row.get(k, "") for k in RES_COLS})


def xy(cfg, rows_res):
    lib, X = library(cfg); idx = {r["cand"]: i for i, r in enumerate(lib)}
    ok = [r for r in rows_res if r["ok"] == "True"]
    Xo = np.array([X[idx[r["cand"]]] for r in ok]) if ok else np.zeros((0, X.shape[1]))
    Y = np.array([[float(r["density_gcm3"]), float(r["ced_MJm3"])] for r in ok]) if ok else np.zeros((0, 2))
    return Xo, Y, ok


def targets(cfg):
    p = ws(cfg) / "lit_targets.json"
    if not p.exists(): raise SystemExit("lit_targets.json 없음 · 먼저 python scripts/lit_extract.py (L-1)")
    t = json.loads(p.read_text(encoding="utf-8"))
    return {o: t[o]["value"] for o in OBJ}, {o: cfg["targets"][o]["tol"] for o in OBJ}, t


def dump(o, p): Path(p).write_text(json.dumps(o, ensure_ascii=False, indent=1), encoding="utf-8")
