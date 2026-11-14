#!/usr/bin/env python3
"""DOI 정규화와 중복 제거 — 노트북 02_dedup_doi.ipynb 와 같은 계산.

무엇을 하나
  1. 서지 CSV 여러 개를 합친다 (같은 논문이 파일마다 다른 표기로 들어 있을 수 있다).
  2. DOI 문자열을 세 단계로 정규화한다: ① 공백 · 끝 마침표 제거 ② URL · doi: 접두 제거 ③ 소문자.
  3. 정규화한 키로 중복을 세고, 고유 논문 수를 out/dedup_report.json 에 남긴다.
규칙 출처: COMID 플랫폼 scripts/build_corpus_index.py 의 norm_doi() (키 우선순위 DOI → PII → 제목 앞 60자).
실행:  python3 scripts/norm_doi.py data/md_corpus_267.csv data/md_asphalt_literature_2021_2026.csv
       (week02 폴더에서 · 인자가 없으면 data/ 의 md_corpus_267.csv 를 두 번 합쳐 중복을 만든다)
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent.parent
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)


def norm_doi(d: str) -> str:
    """DOI 표기 변형을 하나의 키로. 빈 값이면 빈 문자열."""
    if not isinstance(d, str):
        return ""
    d = d.strip().rstrip(".")                                   # ① 공백 · 끝 마침표
    d = re.sub(r"^https?://(dx\.)?doi\.org/", "", d, flags=re.I)  # ② URL 접두
    d = re.sub(r"^doi:\s*", "", d, flags=re.I)                   # ② doi: 접두
    return d.lower()                                            # ③ 소문자


def main(paths):
    if not paths:                                               # 인자가 없으면 같은 파일을 두 번 → 전부 중복이 되는 연습용 입력
        paths = [HERE / "data/md_corpus_267.csv", HERE / "data/md_corpus_267.csv"]
    frames = [pd.read_csv(p) for p in paths]
    df = pd.concat(frames, ignore_index=True)
    raw_unique = df["doi"].nunique()                            # 정규화 전 고유 수
    keys = df["doi"].map(norm_doi)
    counts = Counter(k for k in keys if k)
    report = {
        "inputs": [str(Path(p).name) for p in paths],
        "records": int(len(df)),
        "unique_raw": int(raw_unique),
        "unique": int(len(counts)),
        "duplicates": int(len(df) - len(counts)),
        "missing_doi": int((keys == "").sum()),
        "top_duplicated": counts.most_common(3),
        "rule": "strip·rstrip('.') → ^https?://(dx.)?doi.org/ 제거 → ^doi: 제거 → lower()",
    }
    (OUT / "dedup_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main(sys.argv[1:])
