"""W13 공통: 데이터 읽기 · 특징 · 지표. 표준 라이브러리 + numpy · pandas · scikit-learn."""
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "bulk_md_373.csv"
OUT = ROOT / "out"
FEATURES = ["aging", "T_K", "h2o", "additive_wt", "binder_AAK1", "binder_AAM1"]
SEED = 42


CORE = ["AAA1-non_aging", "AAA1-short_aging", "AAA1-long_aging"]   # 기본 = AAA1 바인더 × 노화 3 × 온도 18 × 시드 반복 (336행)


def load(target="density", cells="core"):
    d = pd.read_csv(DATA)
    if cells == "core":
        d = d[d.cell.isin(CORE)].reset_index(drop=True)
    d["binder_AAK1"] = (d.binder == "AAK1").astype(int)
    d["binder_AAM1"] = (d.binder == "AAM1").astype(int)
    d["cond"] = d.cell + "@" + d.T_K.astype(str)      # 조건 그룹 = 같은 조성 셀 · 같은 온도 (시드만 다른 반복)
    return d, d[FEATURES].to_numpy(float), d[target].to_numpy(float)


def metrics(y, p):
    y, p = np.asarray(y, float), np.asarray(p, float)
    rmse = float(np.sqrt(np.mean((p - y) ** 2)))
    mae = float(np.mean(np.abs(p - y)))
    ss = float(np.sum((y - y.mean()) ** 2))
    r2 = float(1 - np.sum((p - y) ** 2) / ss) if ss > 0 else float("nan")
    return {"rmse": round(rmse, 5), "mae": round(mae, 5), "r2": round(r2, 3), "n": int(len(y)), "sd_y": round(float(y.std()), 5)}


def save(name, obj):
    OUT.mkdir(exist_ok=True)
    p = OUT / name
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    print("saved", p.relative_to(ROOT))
    return p
