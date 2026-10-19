#!/usr/bin/env python3
"""STYLE_GUIDE.md §4.4·§5 정규화 — 인라인 style 의 글자 크기·제목 크기·슬라이드 여백을 규격값으로 맞춘다.

  python3 tools/normalize_style.py 1 2 3            # 주차 번호 또는 파일명
  python3 tools/normalize_style.py --dry-run 1      # 바뀔 값 통계만
  python3 tools/normalize_style.py --tighten "파일명" 12 17   # 해당 슬라이드 여백을 한 단계 줄임
  python3 tools/normalize_style.py --enlarge "파일명" 21 27    # 성긴 슬라이드 본문 글자를 규격 안에서 한 단계 키움
                                                               (--steps 2 로 두 단계, 제목·상단 라벨은 그대로)

- <svg> 내부는 건드리지 않는다. 텍스트·구조·색상도 건드리지 않는다.
- 이미 규격값인 요소는 그대로 둔다(재실행 안전).
- 본문 슬라이드 여백은 현재 위쪽 여백으로 단계를 고른다: ≥50 → 기본, 38–49 → 조밀, <38 → 최조밀.
"""
import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from check_style import ALLOWED_SIZES, slide_type, family_of  # noqa: E402

TIERS = ["56px 90px 44px", "40px 80px 28px", "34px 80px 22px"]
PAD = {"title": "100px 100px 80px", "divider": "100px", "structural": "56px 90px 44px"}
SECONDARY = ("#94a3b8", "#64748b", "#475569")
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
TAG = re.compile(r"<(/?)([a-zA-Z][\w-]*)((?:[^>\"']|\"[^\"]*\"|'[^']*')*)>")


def snap(fam, size, style, tag):
    """허용되지 않은 크기를 §4.4 규칙대로 바꾼다."""
    allowed = ALLOWED_SIZES[fam]
    if size in allowed:
        return size
    if size < 24:
        return 24
    weight = re.search(r"font-weight:\s*(\d+)", style)
    bold = weight and int(weight.group(1)) >= 600
    secondary = any(c in style.lower() for c in SECONDARY)
    if fam == "sans":
        rule = {25: 24 if secondary else 26, 27: 28 if bold else 26, 29: 28, 31: 32, 33: 32, 34: 32, 35: 36, 37: 38, 39: 40}
        if size in rule:
            return rule[size]
        if 41 <= size <= 48:
            return 40
    if fam == "mono":
        eyebrow = "0.14em" in style
        rule = {25: 26 if eyebrow else 24, 27: 26 if eyebrow else 28, 29: 28, 30: 28, 31: 32, 33: 34, 35: 34, 36: 34}
        if size in rule:
            return rule[size]
        if 38 <= size <= 56:
            return 44
    # 나머지: 가장 가까운 허용값 (같으면 큰 쪽)
    return min(sorted(allowed, reverse=True), key=lambda a: abs(a - size))


def tier_of(pad):
    top = re.match(r"(\d+)px", pad)
    top = int(top.group(1)) if top else 56
    return 0 if top >= 50 else 1 if top >= 38 else 2


ENLARGE_CAP = {"sans": 32, "mono": 34, "math": 36}


def bump(fam, size, steps):
    seq = sorted(a for a in ALLOWED_SIZES[fam] if a <= ENLARGE_CAP[fam])
    if size not in seq:
        return size
    return seq[min(seq.index(size) + steps, len(seq) - 1)]


def normalize(text, tighten=(), enlarge=(), steps=1):
    stats = collections.Counter()
    out, pos = [], 0
    stack = []  # (tag, fam, in_svg)
    kind = None
    slide = 0
    for m in TAG.finditer(text):
        out.append(text[pos:m.start()])
        pos = m.end()
        closing, tag, attrs = m.group(1), m.group(2).lower(), m.group(3)
        if closing:
            while stack:
                if stack.pop()[0] == tag:
                    break
            out.append(m.group(0))
            continue
        selfclose = attrs.rstrip().endswith("/")
        parent_fam = stack[-1][1] if stack else "sans"
        in_svg = (stack[-1][2] if stack else False) or tag == "svg"
        sm = re.search(r'style="([^"]*)"', attrs)
        style = sm.group(1) if sm else ""
        fam = family_of(style, parent_fam)
        new = style

        if tag == "section":
            slide += 1
            lab = re.search(r'data-label="([^"]*)"', attrs)
            kind = slide_type(lab.group(1) if lab else "")
            pm = re.search(r"padding:\s*([^;]+)", style)
            cur = pm.group(1).strip() if pm else ""
            if kind in PAD:
                want = PAD[kind]
            else:
                t = tier_of(cur) if cur not in TIERS else TIERS.index(cur)
                if slide in tighten:
                    t = min(t + 1, 2)
                want = TIERS[t]
            if pm and cur != want:
                new = new.replace(pm.group(0), f"padding:{want}", 1)
                stats[f"padding {cur} → {want}"] += 1

        if not in_svg and style:
            decls = list(re.finditer(r"font-size:\s*([\d.]+)px;?", style))
            if len(decls) > 1:  # 중복 선언: 마지막 값만 남긴다
                for d in decls[:-1]:
                    new = new.replace(d.group(0), "", 1)
                stats["font-size 중복 선언 정리"] += 1
            fm = re.search(r"font-size:\s*([\d.]+)px", new)
            if fm:
                size = round(float(fm.group(1)))
                if tag == "h1":
                    want = 88
                elif tag == "h2":
                    want = 68 if kind == "divider" else 52
                else:
                    want = snap(fam, size, style, tag)
                    if slide in enlarge and "0.14em" not in style and kind == "content":
                        want = bump(fam, want, steps)
                if want != float(fm.group(1)):
                    new = new.replace(fm.group(0), f"font-size:{want}px", 1)
                    stats[f"{fam} {fm.group(1)} → {want}"] += 1

        if new != style:
            attrs = attrs.replace(f'style="{style}"', f'style="{new}"', 1)
        out.append(f"<{tag if m.group(2).islower() else m.group(2)}{attrs}>")
        if not selfclose and tag not in VOID:
            stack.append((tag, fam, in_svg))
    out.append(text[pos:])
    return "".join(out), stats


def main():
    args = sys.argv[1:]
    dry = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]
    decks = json.loads((ROOT / "tools/decks.json").read_text(encoding="utf-8"))["decks"]
    steps = 1
    if "--steps" in args:
        i = args.index("--steps")
        steps = int(args[i + 1])
        del args[i:i + 2]
    if args and args[0] in ("--tighten", "--enlarge"):
        f, slides = args[1], {int(x) for x in args[2:]}
        p = ROOT / f
        kw = {"tighten": slides} if args[0] == "--tighten" else {"enlarge": slides, "steps": steps}
        t, st = normalize(p.read_text(encoding="utf-8"), **kw)
        if not dry:
            p.write_text(t, encoding="utf-8")
        print(f, dict(st))
        return
    sel = [d for d in decks if not args or any(a == d["file"] or (a.isdigit() and int(a) == d["week"]) for a in args)]
    for d in sel:
        p = ROOT / d["file"]
        src = p.read_text(encoding="utf-8")
        t, st = normalize(src)
        if not dry and t != src:
            p.write_text(t, encoding="utf-8")
        print(f"── {d['file']}  ({sum(st.values())}건)")
        for k, v in sorted(st.items(), key=lambda kv: -kv[1]):
            print(f"   {v:>4}  {k}")


if __name__ == "__main__":
    main()
