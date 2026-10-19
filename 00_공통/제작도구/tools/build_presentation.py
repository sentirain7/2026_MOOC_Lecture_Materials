#!/usr/bin/env python3
"""발표용 버전 생성 — 원본 덱은 그대로 두고 `발표용/` 폴더에 새 파일을 만든다.

  python3 tools/build_presentation.py            # 17개 덱 → 발표용/
  python3 tools/build_presentation.py --dry-run  # 무엇이 빠지는지만 출력

원본과 달라지는 점
  1. 보존용 부록 슬라이드 제거: data-label 이 「부록 · 이전 구성 원문…」「부록 · 이전 차시 구성」인 슬라이드
  2. 부록 구분 슬라이드의 부제 「본강의 흐름에서 빠진 슬라이드와 원문 보존」 제거
  3. 1·2 뒤 부록 구분 슬라이드 다음에 남은 슬라이드가 없으면 구분 슬라이드도 제거
  4. data-screen-label 순번 재부여
  5. 하위 폴더에서 열리도록 상대 경로(assets/ · _ds/ · uploads/ · support.js · deck-stage.js)에 ../ 추가
원본의 보존 원문은 원본 덱과 git 이력에 그대로 남는다 (STYLE_GUIDE §2.3).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "발표용"
DRY = "--dry-run" in sys.argv
PRESERVE = re.compile(r'data-label="부록 · 이전 (구성 원문|차시 구성)[^"]*"')
SUBTITLE = re.compile(r'\s*<p[^>]*>\s*본강의 흐름에서 빠진 슬라이드와 원문 보존\s*</p>')
SEC = re.compile(r"<section\b.*?</section>", re.S)


def relink(t):
    def fix(m):
        attr, q, v = m.group(1), m.group(2), m.group(3)
        if re.match(r"(https?:|data:|#|/|\.\./|mailto:|javascript:|\{\{)", v):
            return m.group(0)
        v = v[2:] if v.startswith("./") else v
        return f"{attr}={q}../{v}{q}"
    return re.sub(r'\b(src|href|from)=(["\'])([^"\']+)\2', fix, t)


def build(text):
    secs = list(SEC.finditer(text))
    keep, dropped = [], []
    for m in secs:
        s = m.group(0)
        head = s[: s.index(">") + 1]
        if PRESERVE.search(head):
            dropped.append(re.search(r'data-label="([^"]*)"', head).group(1))
            continue
        keep.append(SUBTITLE.sub("", s) if 'data-label="부록"' in head else s)
    # 부록 구분 슬라이드 뒤에 남은 슬라이드가 없으면 구분 슬라이드도 제거
    labels = [re.search(r'data-label="([^"]*)"', s).group(1) for s in keep]
    if "부록" in labels and labels.index("부록") == len(labels) - 1:
        keep.pop()
        dropped.append("부록 (구분 슬라이드 · 남은 부록 없음)")
    # 순번 재부여
    out = []
    for i, s in enumerate(keep, 1):
        out.append(re.sub(r'data-screen-label="[^"]*"', f'data-screen-label="{i:02d}"', s, count=1))
    # 원문에서 섹션 구간을 새 섹션 목록으로 교체 (섹션 사이 공백·스크립트 등 나머지는 유지)
    first, last = secs[0].start(), secs[-1].end()
    body = "\n\n".join(out)
    return relink(text[:first]) + relink(body) + relink(text[last:]), len(secs), len(keep), dropped


def main():
    decks = json.loads((ROOT / "tools/decks.json").read_text(encoding="utf-8"))["decks"]
    if not DRY:
        OUT.mkdir(exist_ok=True)
    for d in decks:
        src = (ROOT / d["file"]).read_text(encoding="utf-8")
        # 섹션 사이에 다른 내용(스크립트 등)이 끼어 있으면 교체 방식이 내용을 잃으므로 확인
        secs = list(SEC.finditer(src))
        between = "".join(src[a.end():b.start()] for a, b in zip(secs, secs[1:])).strip()
        if between:
            sys.exit(f"섹션 사이에 다른 내용이 있음: {d['file']} 「{between[:60]}」")
        new, n0, n1, dropped = build(src)
        print(f"{d['file'][:44]:<46} {n0:>3} → {n1:>3}장  제거: {', '.join(dropped) if dropped else '없음'}")
        if not DRY:
            (OUT / d["file"]).write_text(new, encoding="utf-8")


if __name__ == "__main__":
    main()
