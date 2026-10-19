#!/usr/bin/env python3
"""강의 스크립트 JSON 검증.  python3 tools/check_script_json.py <주차> [...]

형식 (스크립트/json/wNN.json):
{ "week": 1, "deck": "발표용/…dc.html",
  "slides": [ { "n": 1, "label": "표지", "session": "도입"|"1-1"|…|"마무리"|"부록",
                "seconds": 60, "script": ["문단", …], "cue": "조작 · 판서 안내(선택)" } ] }
검사: 슬라이드 수 = 발표용 덱 · label 일치 · 부록 제외 시간 합 50분 ±1분 ·
      차시별 시간 ≈ 강의계획서 (±2분) ·
      (【콘크리트 예시】는 개념과 자연스럽게 이어지는 곳에만 · 개수 검사 없음)
      분량: 말하기 속도 초당 약 4–6자 (부록 제외)
"""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
syl = {w["week"]: w for w in json.loads((ROOT / "tools/syllabus.json").read_text())["weeks"]}
decks = {d["week"]: d for d in json.loads((ROOT / "tools/decks.json").read_text())["decks"] if not d["supplement"]}
bad = 0
for a in sys.argv[1:]:
    w = int(a); p = ROOT / f"스크립트/json/w{w:02d}.json"
    errs = []
    if not p.exists():
        print(f"w{w:02d}: 파일 없음"); bad += 1; continue
    J = json.loads(p.read_text(encoding="utf-8"))
    t = (ROOT / "발표용" / decks[w]["file"]).read_text(encoding="utf-8")
    labels = re.findall(r'<section data-label="([^"]*)"', t)
    S = J["slides"]
    if len(S) != len(labels): errs.append(f"슬라이드 수 {len(S)} ≠ 덱 {len(labels)}")
    for i, (s, lab) in enumerate(zip(S, labels), 1):
        if s.get("n") != i: errs.append(f"#{i} n={s.get('n')}")
        if s.get("label") != lab: errs.append(f"#{i} label 「{s.get('label')}」 ≠ 「{lab}」")
        if not s.get("script"): errs.append(f"#{i} script 없음")
    body = [s for s in S if s.get("session") != "부록"]
    tot = sum(s.get("seconds", 0) for s in body)
    if abs(tot - 3000) > 60: errs.append(f"시간 합 {tot/60:.1f}분 (목표 50)")
    for ses in syl[w]["sessions"]:
        got = sum(s["seconds"] for s in body if s.get("session") == ses["code"]) / 60
        if abs(got - ses["minutes"]) > 2: errs.append(f"{ses['code']} {got:.1f}분 (계획서 {ses['minutes']})")
    chars = sum(len("".join(s["script"])) for s in body)
    rate = chars / max(tot, 1)
    if not 3.8 <= rate <= 6.5: errs.append(f"분량 {chars}자 / {tot}초 = 초당 {rate:.1f}자 (목표 4–6)")
    thin = [s["n"] for s in body if s["seconds"] >= 40 and len("".join(s["script"])) / s["seconds"] < 3.0]
    if thin: errs.append(f"시간 대비 스크립트가 짧은 슬라이드 {thin}")
    ex = sum("【콘크리트 예시】" in "".join(s["script"]) for s in body)
    print(f"w{w:02d}: 콘크리트 예시 {ex}곳 · {len(S)}장 · {tot/60:.1f}분 · {chars}자 · 초당 {rate:.1f}자 → " + ("OK" if not errs else "; ".join(errs)))
    bad += bool(errs)
sys.exit(1 if bad else 0)
