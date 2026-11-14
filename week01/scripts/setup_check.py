#!/usr/bin/env python3
"""week01 환경 점검 — 노트북 00_setup_check.ipynb 와 같은 일을 하는 스크립트 (Colab 이 아닌 환경용).

무엇을 하나
  1. 파이썬 · numpy · pandas · matplotlib 버전을 확인한다.
  2. 공개 데이터 week01/data/asphalt_ml_101.csv (아스팔트 기계학습 논문 101편 서지) 를 읽는다.
  3. 연도별 논문 수 막대그림 한 장을 그린다 → out/papers_by_year.png
  4. 결과를 out/setup_report.json 으로 남긴다 (이 파일이 이번 주 제출물이자 W02 의 입력).
실행:  python3 scripts/setup_check.py   (week01 폴더에서)
"""
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent          # week01/
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
report = {"python": platform.python_version(), "packages": {}, "data": {}, "ok": False,
          "created": datetime.now(timezone.utc).isoformat(timespec="seconds")}

# 1) 패키지 — 없으면 어떤 것이 없는지 적고 멈추지 않는다
for name in ("numpy", "pandas", "matplotlib"):
    try:
        mod = __import__(name)
        report["packages"][name] = mod.__version__
    except ImportError:
        report["packages"][name] = None

import pandas as pd                       # 여기서 실패하면 환경이 준비되지 않은 것 — SETUP.md 경로 ①(Colab) 을 쓴다
import matplotlib
matplotlib.use("Agg")                     # 화면 없는 서버에서도 그림 파일을 만들기 위해
import matplotlib.pyplot as plt

# 2) 데이터 읽기
csv = HERE / "data" / "asphalt_ml_101.csv"
df = pd.read_csv(csv)
report["data"] = {"file": csv.name, "rows": int(len(df)), "columns": list(df.columns),
                  "years": [int(df["year"].min()), int(df["year"].max())]}

# 3) 그림 한 장 — 연도별 논문 수
counts = df["year"].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(8, 4.5), dpi=120)
ax.bar(counts.index.astype(str), counts.values, color="#F99D1C", edgecolor="#E37F1A")
ax.set_xlabel("year"); ax.set_ylabel("papers"); ax.set_title("Asphalt x ML papers (n=101) by year")   # 영문 라벨: 서버 글꼴에 한글이 없어도 깨지지 않게
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig(OUT / "papers_by_year.png"); plt.close(fig)
report["figure"] = "out/papers_by_year.png"

# 4) 보고서
report["ok"] = all(report["packages"].values()) and report["data"]["rows"] == 101
(OUT / "setup_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, indent=2))
print("\n완료:", "환경 준비됨" if report["ok"] else "빠진 항목이 있다 — packages 에서 None 인 것을 설치한다")
