#!/usr/bin/env python3
"""강의 덱(*.dc.html) 스타일·번호 점검 도구.

STYLE_GUIDE.md 의 규격을 기계적으로 검사한다.

  python3 tools/check_style.py                 # 전체 덱 요약표
  python3 tools/check_style.py 3               # 3주차 덱만 (본강의+보충) 상세
  python3 tools/check_style.py "10주차 강의 - 보충 - 능동학습과 탐색 전략.dc.html"
  python3 tools/check_style.py --rules font-size,numbering 1 2 3
  python3 tools/check_style.py --json          # 기계 판독용 출력

종료 코드: ERROR 가 하나라도 있으면 1, 아니면 0. WARN 은 종료 코드에 영향 없음.
<svg> 내부는 viewBox 좌표계라 글자 크기 규칙을 적용하지 않는다(색상만 검사).
"""
import argparse
import collections
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"

# ── 규격 (STYLE_GUIDE.md §3–§6 과 동일하게 유지) ──────────────────────────
ALLOWED_SIZES = {
    "sans": {24, 26, 28, 30, 32, 36, 38, 40, 52, 68, 88},
    "mono": {24, 26, 28, 32, 34, 44, 120},
    "math": {24, 26, 28, 30, 32, 36},
}
MIN_SIZE = 24
HEADING_SIZE = {"title": ("h1", 88), "divider": ("h2", 68), "content": ("h2", 52), "structural": ("h2", 52)}
PADDING = {
    "title": {"100px 100px 80px"},
    "divider": {"100px"},
    "content": {"56px 90px 44px", "40px 80px 28px", "34px 80px 22px"},
    "structural": {"56px 90px 44px"},
}
SECTION_BG = {"#0c1222", "#111827", "linear-gradient(135deg,#111827,#0c1222)"}
# NACMID tokens/colors.css 에 없지만 허용하는 확장색 (Tailwind slate/indigo)
EXTENDED_COLORS = {"#6366f1", "#cbd5e1", "#e2e8f0", "#f8fafc"}

STRUCTURAL_LABELS = {"지난 주차", "학습목표", "실습 안내"}
RULES = ["font-size", "heading", "padding", "background", "screen-label", "numbering", "minutes", "color", "tone"]
SEVERITY = {"color": "WARN", "background": "WARN"}

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


def load_palette():
    css = next((ROOT / "_ds").glob("*/tokens/colors.css")).read_text(encoding="utf-8")
    return {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}\b", css)} | EXTENDED_COLORS


def family_of(style, inherited):
    m = re.search(r"font-family:\s*([^;]+)", style)
    if not m:
        return inherited
    fam = m.group(1)
    if "JetBrains" in fam or "monospace" in fam:
        return "mono"
    if "STIX" in fam or "Cambria Math" in fam:
        return "math"
    return "sans"


def slide_type(label):
    if label == "부록":
        return "divider"
    if label == "표지":
        return "title"
    if re.fullmatch(r"\[\d+-S?\d+\] 섹션", label):
        return "divider"
    if label in STRUCTURAL_LABELS or re.search(r"주차 (구성|정리)$", label):
        return "structural"
    return "content"


class Deck(HTMLParser):
    """덱 하나를 파싱해 슬라이드별 요소 정보를 모은다."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []  # (tag, family, in_svg)
        self.slides = []
        self.cur = None
        self.text_sink = None  # (element dict) 텍스트를 모을 대상
        self.code_depth = 0  # <pre>/<code> 안인지

    def _push(self, tag, attrs, closing):
        a = dict(attrs)
        style = (a.get("style") or "").replace("\n", " ")
        parent_fam = self.stack[-1][1] if self.stack else "sans"
        in_svg = (self.stack[-1][2] if self.stack else False) or tag == "svg"
        fam = family_of(style, parent_fam)
        line = self.getpos()[0]

        if tag == "section":
            self.cur = {"attrs": a, "style": style, "line": line, "els": [], "colors": []}
            self.slides.append(self.cur)
        if self.cur is not None:
            for c in re.findall(r"#[0-9a-fA-F]{6}\b", " ".join(v or "" for v in a.values())):
                self.cur["colors"].append((c.lower(), line))
            sizes = re.findall(r"font-size:\s*([\d.]+)px", style)  # 중복 선언이면 마지막 값이 적용됨
            if sizes and not in_svg:
                el = {"tag": tag, "fam": fam, "size": float(sizes[-1]), "style": style, "line": line, "text": ""}
                self.cur["els"].append(el)
                if not closing:
                    self.text_sink = el
            elif tag in ("h1", "h2") and not in_svg:
                el = {"tag": tag, "fam": fam, "size": None, "style": style, "line": line, "text": ""}
                self.cur["els"].append(el)
                self.text_sink = el
        if not closing and tag not in VOID:
            self.stack.append((tag, fam, in_svg))

    def handle_starttag(self, tag, attrs):
        if tag in ("pre", "code", "script", "style"):
            self.code_depth += 1
        self._push(tag, attrs, False)

    def handle_startendtag(self, tag, attrs):
        self._push(tag, attrs, True)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if tag in ("pre", "code", "script", "style") and self.code_depth:
            self.code_depth -= 1
        while self.stack:
            t = self.stack.pop()[0]
            if t == tag:
                break
        if tag == "section":
            self.cur = None
        self.text_sink = None

    def handle_data(self, data):
        if self.text_sink is not None:
            self.text_sink["text"] += data
        if self.cur is not None and not self.code_depth and data.strip():
            fam = self.stack[-1][1] if self.stack else "sans"
            if fam != "mono":
                self.cur.setdefault("texts", []).append((data.strip(), self.getpos()[0]))


def fmt_px(v):
    return f"{v:g}px"


def check_deck(path, meta, syllabus, palette):
    p = Deck()
    p.feed(path.read_text(encoding="utf-8"))
    issues = []
    week = meta["week"]
    supp = meta.get("supplement")
    syl = syllabus[week]
    if supp:
        start = meta.get("s_start", 1)
        valid_codes = {f"{week}-S{i}" for i in range(start, start + 8)}
    else:
        valid_codes = {s["code"] for s in syl["sessions"]}
    syl_min = {s["code"]: s["minutes"] for s in syl["sessions"]}

    def add(rule, slide, line, msg):
        issues.append({"rule": rule, "sev": SEVERITY.get(rule, "ERROR"), "slide": slide, "line": line, "msg": msg})

    in_appendix = False  # 「부록」 구분 슬라이드 이후는 번호·시간 규칙 제외 (STYLE_GUIDE §2.3)
    for idx, s in enumerate(p.slides, 1):
        a = s["attrs"]
        label = a.get("data-label", "")
        kind = slide_type(label)
        line = s["line"]
        in_appendix = in_appendix or label == "부록"

        def add_num(rule, slide, ln, msg):
            if not in_appendix:
                add(rule, slide, ln, msg)

        # screen-label: 슬라이드 순번과 일치해야 함
        sl = a.get("data-screen-label", "")
        if sl != f"{idx:02d}":
            add("screen-label", idx, line, f'data-screen-label="{sl}" → "{idx:02d}"')

        # padding / background
        pad = re.search(r"padding:\s*([^;]+)", s["style"])
        pad = pad.group(1).strip() if pad else "(없음)"
        if pad not in PADDING[kind]:
            add("padding", idx, line, f"{kind} 슬라이드 padding {pad} → {' 또는 '.join(sorted(PADDING[kind]))}")
        bg = re.search(r"background:\s*([^;]+)", s["style"])
        bg = bg.group(1).replace(" ", "").lower() if bg else "(없음)"
        if bg not in SECTION_BG:
            add("background", idx, line, f"배경 {bg} → #0c1222 / #111827 / 정리용 gradient")

        # 글자 크기
        for el in s["els"]:
            if el["size"] is None:
                continue
            sz = el["size"]
            if sz < MIN_SIZE:
                add("font-size", idx, el["line"], f"{el['fam']} {fmt_px(sz)} < 최소 {MIN_SIZE}px  「{el['text'].strip()[:30]}」")
            elif int(sz) != sz or int(sz) not in ALLOWED_SIZES[el["fam"]]:
                add("font-size", idx, el["line"], f"{el['fam']} {fmt_px(sz)} 는 허용 크기 아님 {sorted(ALLOWED_SIZES[el['fam']])}  「{el['text'].strip()[:30]}」")

        # 제목 크기
        want_tag, want_size = HEADING_SIZE[kind]
        heads = [e for e in s["els"] if e["tag"] == want_tag]
        if not heads:
            add("heading", idx, line, f"{kind} 슬라이드에 <{want_tag}> 없음")
        for e in heads:
            if e["size"] != want_size:
                add("heading", idx, e["line"], f"<{want_tag}> {fmt_px(e['size']) if e['size'] else '크기 미지정'} → {want_size}px  「{e['text'].strip()[:30]}」")

        # 번호
        texts = [e["text"].strip() for e in s["els"]]
        eyebrow = next((e["text"].strip() for e in s["els"] if e["fam"] == "mono" and e["size"] == 26 and "0.14em" in e["style"]), "")
        head = heads[0]["text"].strip() if heads else ""
        if kind == "title":
            wk = next((t for t in texts if t.startswith("WEEK")), "")
            m = re.match(r"WEEK (\d+)", wk)
            if not m or int(m.group(1)) != week:
                add_num("numbering", idx, line, f"표지 「{wk}」 → WEEK {week:02d}")
            if supp and f"보충 {supp}" not in wk:
                add_num("numbering", idx, line, f"표지 「{wk}」에 '보충 {supp}' 표기 없음")
            mm = re.search(r"(\d+)분", wk)
            if not supp and (not mm or int(mm.group(1)) != syl["minutes"]):
                add_num("minutes", idx, line, f"표지 총 시간 {mm.group(0) if mm else '없음'} → {syl['minutes']}분")
        if kind == "divider" and label != "부록":
            code = re.fullmatch(r"\[(\d+-S?\d+)\] 섹션", label).group(1)
            if code not in valid_codes:
                add_num("numbering", idx, line, f"구분 슬라이드 [{code}] 는 {week}주차 차시 코드가 아님")
            mm = next((re.match(r"(\d+)분", t) for t in texts if re.match(r"\d+분", t)), None)
            if not supp and code in syl_min and mm and int(mm.group(1)) != syl_min[code]:
                add_num("minutes", idx, line, f"구분 슬라이드 [{code}] {mm.group(0)} → {syl_min[code]}분 (강의계획서)")
        if eyebrow:
            m = re.match(r"(\d+)-(S?\d+)\b", eyebrow)
            if m and f"{m.group(1)}-{m.group(2)}" not in valid_codes:
                add_num("numbering", idx, line, f"상단 라벨 「{eyebrow}」 의 차시 코드가 {week}주차와 맞지 않음")
            m = re.match(r"RECAP · WEEK (\d+)(?![\d–~])", eyebrow)  # 범위(WEEK 02–08)는 여러 주 회고로 허용
            if m and not supp and int(m.group(1)) != week - 1:
                add_num("numbering", idx, line, f"「{eyebrow}」 → RECAP · WEEK {week - 1:02d}")
        m = re.match(r"(\d+)주차 (구성|정리|학습목표)", head) or re.match(r"(\d+)주차 (구성|정리)", label)
        if m and int(m.group(1)) != week:
            add_num("numbering", idx, line, f"「{m.group(0)}」 → {week}주차 {m.group(2)}")

        # 구성(AGENDA) 행: 차시 코드 + 시간
        if re.search(r"주차 구성$", label):
            els = s["els"]
            for i, e in enumerate(els):
                if e["fam"] == "mono" and re.fullmatch(r"\d+-S?\d+", e["text"].strip()):
                    code = e["text"].strip()
                    if code not in valid_codes:
                        add_num("numbering", idx, e["line"], f"구성 행 {code} 는 {week}주차 차시 코드가 아님")
                    mins = next((x["text"].strip() for x in els[i + 1:i + 3] if re.fullmatch(r"\d+분", x["text"].strip())), None)
                    if not supp and code in syl_min and mins and int(mins[:-1]) != syl_min[code]:
                        add_num("minutes", idx, e["line"], f"구성 행 {code} {mins} → {syl_min[code]}분 (강의계획서)")

        # 문체: 화면 문장은 개조식 (STYLE_GUIDE §10.1) — 「…다」「…요」 종결 금지
        for txt, ln in s.get("texts", []):
            if re.search(r"(다|요|죠)[.!?。]?[\s\)\]」』”\"']*$", txt) and len(txt) >= 4:
                add("tone", idx, ln, f"서술형 종결 「{txt[-40:]}」")

        # 색상
        for c, ln in s["colors"]:
            if c not in palette:
                add("color", idx, ln, f"팔레트 밖 색상 {c}")
    return p.slides, issues


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("targets", nargs="*", help="주차 번호 또는 파일명 (생략 시 전체 요약)")
    ap.add_argument("--rules", help="검사할 규칙만 (쉼표 구분): " + ",".join(RULES))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    decks = json.loads((TOOLS / "decks.json").read_text(encoding="utf-8"))["decks"]
    syllabus = {w["week"]: w for w in json.loads((TOOLS / "syllabus.json").read_text(encoding="utf-8"))["weeks"]}
    palette = load_palette()
    rules = set(args.rules.split(",")) if args.rules else set(RULES)

    sel = decks
    if args.targets:
        sel = [d for d in decks if any(t == d["file"] or (t.isdigit() and int(t) == d["week"]) for t in args.targets)]
        if not sel:
            sys.exit(f"대상 덱을 찾지 못함: {args.targets}")
    detail = bool(args.targets)

    report, n_err = [], 0
    for d in sel:
        path = ROOT / d["file"]
        if not path.exists():
            report.append({"file": d["file"], "missing": True})
            n_err += 1
            continue
        slides, issues = check_deck(path, d, syllabus, palette)
        issues = [i for i in issues if i["rule"] in rules]
        n_err += sum(i["sev"] == "ERROR" for i in issues)
        report.append({"file": d["file"], "slides": len(slides), "issues": issues})

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=1))
        return 1 if n_err else 0

    shown = [r for r in RULES if r in rules]
    print(f"{'덱':<44} {'장':>3} " + " ".join(f"{r[:6]:>6}" for r in shown))
    for r in report:
        name = r["file"].replace(".dc.html", "")[:42]
        if r.get("missing"):
            print(f"{name:<44}  파일 없음")
            continue
        cnt = collections.Counter(i["rule"] for i in r["issues"])
        print(f"{name:<44} {r['slides']:>3} " + " ".join(f"{cnt.get(x, 0) or '·':>6}" for x in shown))
    total = collections.Counter(i["rule"] for r in report for i in r.get("issues", []))
    print(f"{'합계':<44} {'':>3} " + " ".join(f"{total.get(x, 0) or '·':>6}" for x in shown))
    print(f"\nERROR {n_err}건 · WARN {sum(total[r] for r in SEVERITY if r in rules)}건 (WARN: {', '.join(SEVERITY)})")

    if detail:
        for r in report:
            if r.get("missing") or not r["issues"]:
                continue
            print(f"\n── {r['file']}")
            for i in sorted(r["issues"], key=lambda i: (i["slide"], i["line"])):
                print(f"  [{i['sev']:<5}] #{i['slide']:02d} L{i['line']:<5} {i['rule']:<12} {i['msg']}")
    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main())
