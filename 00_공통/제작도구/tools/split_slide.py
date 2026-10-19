#!/usr/bin/env python3
"""슬라이드 하나를 두 장으로 나눈다 (STYLE_GUIDE §8 가시성 우선 · 슬라이드 분할).

  python3 tools/split_slide.py "파일명" 순번 --list                 # 최상위 자식 목록
  python3 tools/split_slide.py "파일명" 순번 "2,4" "3,5"             # 1/2 장에 자식 2·4, 2/2 장에 3·5
  python3 tools/split_slide.py "파일명" 순번 "2,3.0" "3.1,3.2"       # 자식 3 안쪽을 나눔 (감싸는 태그는 양쪽에 복사)
                               [--title2 "둘째 장 제목"]

- 상단 라벨(자식 0)과 제목 <h2>(자식 1)는 두 장 모두에 복사하고, 라벨 끝에 「· 1 / 2」를 붙인다.
- data-label 에 (1/2)·(2/2), 발표자 노트는 첫 장에 원문, 둘째 장에 [분할] 표기.
- 어느 쪽에도 넣지 않은 자식이 있으면 거부한다(내용 삭제 금지).
- 순번은 1부터. 실행 뒤 renumber_step2.py 로 screen-label 을 다시 매긴다.
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


def line_offsets(text):
    offs, acc = [0], 0
    for ln in text.splitlines(keepends=True):
        acc += len(ln)
        offs.append(acc)
    return offs


class Children(HTMLParser):
    """section 의 최상위 자식 [start, end) 오프셋."""

    def __init__(self, text):
        super().__init__(convert_charrefs=False)
        self.text, self.offs = text, line_offsets(text)
        self.depth, self.kids, self.cur = 0, [], None

    def pos(self):
        l, c = self.getpos()
        return self.offs[l - 1] + c

    def handle_starttag(self, tag, attrs):
        if self.depth == 1:
            self.cur = [self.pos(), None, tag]
        if tag not in VOID:
            self.depth += 1
        elif self.depth == 1:
            self.cur[1] = self.pos() + len(self.get_starttag_text())
            self.kids.append(self.cur)

    def handle_startendtag(self, tag, attrs):
        if self.depth == 1:
            self.kids.append([self.pos(), self.pos() + len(self.get_starttag_text()), tag])

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        self.depth -= 1
        if self.depth == 1 and self.cur:
            end = self.text.index(">", self.pos()) + 1
            self.cur[1] = end
            self.kids.append(self.cur)
            self.cur = None


def main():
    a = sys.argv[1:]
    f, idx = a[0], int(a[1])
    p = ROOT / f
    t = p.read_text(encoding="utf-8")
    secs = [m for m in re.finditer(r"<section\b.*?</section>", t, re.S)]
    m = secs[idx - 1]
    sec = m.group(0)
    open_end = sec.index(">") + 1
    ch = Children(sec)
    ch.feed(sec)
    kids = ch.kids
    def _inner_kids(inner, s0):
        # inner = <tag ...> ... </tag> → 그 안의 최상위 자식
        head_end = inner.index(">") + 1
        close = inner.rindex("</")
        body = inner[head_end:close]
        g = Children(f"<section>{body}</section>")
        g.feed(f"<section>{body}</section>")
        base = s0 + head_end - len("<section>")
        return [(x + base, y + base, t) for x, y, t in g.kids]

    if "--list" in a:
        for i, (s, e, tag) in enumerate(kids):
            txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", sec[s:e]))[:70]
            print(f"{i}: <{tag}> {e - s}자  {txt}")
            if "--deep" in a and i >= 2:
                for j, (gs, ge, gt) in enumerate(_inner_kids(sec[s:e], s)):
                    gtxt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", sec[gs:ge]))[:60]
                    print(f"   {i}.{j}: <{gt}> {ge - gs}자  {gtxt}")
        return
    part1 = a[2].split(",")
    part2 = a[3].split(",")
    title2 = a[a.index("--title2") + 1] if "--title2" in a else None
    nested = {int(x.split(".")[0]) for x in part1 + part2 if "." in x}
    want = set()
    for i in range(2, len(kids)):
        if i in nested:
            want |= {f"{i}.{j}" for j in range(len(_inner_kids(sec[kids[i][0]:kids[i][1]], kids[i][0])))}
        else:
            want.add(str(i))
    if set(part1) | set(part2) != want or set(part1) & set(part2):
        sys.exit(f"{sorted(want)} 을 두 장에 빠짐없이·겹치지 않게 나눠야 함 (내용 삭제 금지)")
    opening = sec[:open_end]
    label = re.search(r'data-label="([^"]*)"', opening).group(1)
    notes = re.search(r'data-speaker-notes="([^"]*)"', opening)
    eyebrow = sec[kids[0][0]:kids[0][1]]
    h2 = sec[kids[1][0]:kids[1][1]]

    def build(n, parts):
        o = opening.replace(f'data-label="{label}"', f'data-label="{label} ({n}/2)"', 1)
        if n == 2 and notes:
            o = o.replace(notes.group(0), f'data-speaker-notes="[분할] 앞 장에서 이어짐. {notes.group(1)}"', 1)
        eb = re.sub(r"(</\w+>)$", rf" · {n} / 2\1", eyebrow)
        hh = h2 if not (n == 2 and title2) else re.sub(r">[^<]*</h2>$", f">{title2}</h2>", h2)
        pieces, done = [], set()
        for x in parts:
            if "." not in x:
                pieces.append(sec[kids[int(x)][0]:kids[int(x)][1]])
                continue
            i = int(x.split(".")[0])
            if i in done:
                continue
            done.add(i)
            s0, e0, _ = kids[i]
            outer = sec[s0:e0]
            gk = _inner_kids(outer, s0)
            sel = [p for p in parts if p.startswith(f"{i}.")]
            inner = "\n    ".join(sec[gk[int(p.split(".")[1])][0]:gk[int(p.split(".")[1])][1]] for p in sel)
            pieces.append(outer[:outer.index(">") + 1] + "\n    " + inner + "\n  " + outer[outer.rindex("</"):])
        body = "\n  ".join(pieces)
        return f"{o}\n  {eb}\n  {hh}\n  {body}\n</section>"

    new = build(1, part1) + "\n\n" + build(2, part2)
    p.write_text(t[:m.start()] + new + t[m.end():], encoding="utf-8")
    print(f"분할 완료: #{idx} 「{label}」 → (1/2) 자식 {part1}, (2/2) 자식 {part2}")


if __name__ == "__main__":
    main()
