#!/usr/bin/env python3
"""평가문항 JSON 검사 — 평가문항/json/qNN.json

  python3 tools/check_quiz_json.py        # 13주 전체
  python3 tools/check_quiz_json.py 3 8    # 일부 주차

형식
  {week, title, items:[{no, type, difficulty, session, question, options?, answer,
                        accept?, explanation, source:{slide, label}}]}
  type        객관식 | OX | 단답형
  difficulty  하 | 중 | 상
  options     객관식만, 4개 · answer = 1~4 (정답 번호)
  OX          answer = "O" | "X"
  단답형      answer = 대표 정답 문자열 · accept = 인정 답안 목록(선택)
  source      발표용 덱 슬라이드 번호(data-screen-label) · 그 슬라이드의 data-label

규칙
  - 주차당 6문항: 객관식 3 · OX 2 · 단답형 1
  - 본강의 차시(N-1 …)를 3개 이상 포함, 부록 슬라이드 근거 금지
  - 객관식 정답 번호가 한 번호에 몰리지 않음(3문항이 같은 번호 금지), 선택지 중복 금지
  - OX는 O · X 하나씩
  - 해설 40자 이상, source 라벨이 덱 슬라이드 라벨과 일치
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
syl = {w["week"]: w for w in json.loads((ROOT / "tools/syllabus.json").read_text(encoding="utf-8"))["weeks"]}


def labels(week):
    s = json.loads((ROOT / f"스크립트/json/w{week:02d}.json").read_text(encoding="utf-8"))
    deck = (ROOT / s["deck"]).read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r"<section\b[^>]*>", deck):
        h = m.group(0)
        lab = re.search(r'data-label="([^"]*)"', h)
        n = re.search(r'data-screen-label="(\d+)"', h)
        if lab and n:
            out[int(n.group(1))] = lab.group(1)
    return out


def check(week):
    errs = []
    p = ROOT / f"평가문항/json/q{week:02d}.json"
    if not p.exists():
        return [f"파일 없음 {p.name}"]
    q = json.loads(p.read_text(encoding="utf-8"))
    L = labels(week)
    items = q["items"]
    kinds = [i["type"] for i in items]
    if (kinds.count("객관식"), kinds.count("OX"), kinds.count("단답형")) != (3, 2, 1):
        errs.append(f"유형 구성 {kinds}")
    codes = {s["code"] for s in syl[week]["sessions"]}
    sess = {i["session"] for i in items}
    if not sess <= codes:
        errs.append(f"차시 코드 오류 {sess - codes}")
    if len(sess & codes) < 3:
        errs.append(f"차시 {len(sess & codes)}개만 포함")
    mc = [i["answer"] for i in items if i["type"] == "객관식"]
    if len(mc) == 3 and len(set(mc)) == 1:
        errs.append(f"객관식 정답 번호 쏠림 {mc}")
    ox = sorted(i["answer"] for i in items if i["type"] == "OX")
    if ox != ["O", "X"]:
        errs.append(f"OX 정답 {ox}")
    for i in items:
        t = f"#{i['no']}"
        if i.get("difficulty") not in ("하", "중", "상"):
            errs.append(f"{t} 난이도")
        if i["type"] == "객관식":
            o = i.get("options", [])
            if len(o) != 4 or len(set(o)) != 4:
                errs.append(f"{t} 선택지 4개·중복 없음")
            if i["answer"] not in (1, 2, 3, 4):
                errs.append(f"{t} 정답 번호")
        elif i["type"] == "단답형":
            if not isinstance(i["answer"], str) or not i["answer"].strip():
                errs.append(f"{t} 단답형 정답")
        if len(i.get("explanation", "")) < 40:
            errs.append(f"{t} 해설 짧음")
        src = i.get("source", {})
        n, lab = src.get("slide"), src.get("label")
        if L.get(n) != lab:
            errs.append(f"{t} 근거 슬라이드 #{n} 라벨 불일치 「{lab}」≠「{L.get(n)}」")
        elif lab.startswith("부록"):
            errs.append(f"{t} 부록 근거")
    return errs


def main():
    weeks = [int(a) for a in sys.argv[1:]] or range(1, 14)
    bad = 0
    for w in weeks:
        e = check(w)
        bad += len(e)
        print(f"{w:02d}주차  {'OK' if not e else '; '.join(e)}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
