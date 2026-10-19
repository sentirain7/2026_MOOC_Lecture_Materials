#!/usr/bin/env python3
"""내용 보존 감사 · 복원 (STYLE_GUIDE §2.3).

기준 커밋(기본 9557563)의 화면 글자 중 현재 덱 어디에도(화면·노트) 남지 않은 문구를 찾아,
덱 맨 뒤 부록에 「부록 · 이전 구성 원문」 슬라이드로 모아 둔다. 부록 구분 슬라이드가 없으면 만든다.
차시 코드·시간·상단 라벨처럼 번호 규칙으로 바뀐 형식 문구는 제외한다.

  python3 tools/preserve_original_text.py --audit     # 누락 목록만
  python3 tools/preserve_original_text.py             # 부록 슬라이드 추가
"""
import html, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "9557563"
FMT = re.compile(r"^(\d+[-–]S?\d+ · |\d+분 ·|RECAP|다음 주차|[A-Z0-9 &;/·()-]+$|WEEK |.*주차 (보충 [AB] )?(구성|정리|학습목표)$|\d+[-–]S?\d+$|\d+분$)")
norm = lambda s: re.sub(r"\s+", "", s)
SEC = "background:#0c1222;color:#f1f5f9;font-family:'Pretendard Variable',Pretendard,'Noto Sans KR',sans-serif;"


def texts(t):
    t = t.split("<x-import", 1)[1]
    t = re.sub(r"<script.*?</script>", "", t, flags=re.S)
    return [html.unescape(x).strip() for x in re.findall(r">([^<>]+)<", t) if len(x.strip()) >= 6]


def missing(file, orig=None):
    old = subprocess.run(["git", "show", f"{BASE}:{orig or file}"], capture_output=True, text=True, cwd=ROOT).stdout
    if not old:
        return []
    hay = norm(html.unescape((ROOT / file).read_text(encoding="utf-8")))
    out = []
    for x in dict.fromkeys(texts(old)):
        k = norm(x)
        if k in hay or FMT.match(x) or k[:12] in hay:
            continue
        out.append(x)
    return out


def divider():
    return (f'<section data-label="부록" data-screen-label="00" data-speaker-notes="[부록] 부록 구간 시작. 본강의 흐름에서 뺀 원문을 보존한다." '
            f'style="background:#111827;color:#f1f5f9;font-family:\'Pretendard Variable\',Pretendard,\'Noto Sans KR\',sans-serif;padding:100px;display:flex;flex-direction:column;justify-content:center;gap:40px;">\n'
            '  <div style="width:200px;height:6px;background:linear-gradient(135deg,#3377ff,#8b5cf6);border-radius:999px;"></div>\n'
            '  <div style="font-family:\'JetBrains Mono\',monospace;font-size:120px;color:#1f2937;font-weight:700;line-height:1;">APPX</div>\n'
            '  <h2 style="font-size:68px;font-weight:700;letter-spacing:-0.02em;margin:0;line-height:1.1;">부록 · 참고 자료</h2>\n'
            '  <p style="font-size:30px;color:#94a3b8;margin:0;">본강의 흐름에서 빠진 슬라이드와 원문 보존</p>\n</section>')


def slide(items, n, k):
    lab = "부록 · 이전 구성 원문" + (f" ({n}/{k})" if k > 1 else "")
    rows = "\n".join(f'    <div style="display:flex;gap:20px;align-items:baseline;border-bottom:1px solid #1f2937;padding:8px 0;">'
                     f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:24px;color:#64748b;width:48px;">{i:02d}</span>'
                     f'<span style="font-size:24px;color:#94a3b8;line-height:1.4;flex:1;">{html.escape(x)}</span></div>'
                     for i, x in items)
    return (f'<section data-label="{lab}" data-screen-label="00" data-speaker-notes="[부록] 원래 위치: 표지·학습목표·구성·구분·정리·본문 슬라이드 (커밋 {BASE}). 5단계 재구성에서 화면 문구가 계획서 기준으로 바뀌며 빠진 원문을 그대로 보존한다." '
            f'style="{SEC}padding:40px 80px 28px;display:flex;flex-direction:column;gap:16px;">\n'
            f'  <div style="font-family:\'JetBrains Mono\',monospace;font-size:26px;letter-spacing:0.14em;color:#599eff;">APPENDIX · ORIGINAL TEXT{f" · {n} / {k}" if k > 1 else ""}</div>\n'
            '  <h2 style="font-size:52px;font-weight:700;letter-spacing:-0.02em;line-height:1.1;margin:0;">이전 구성의 원문 문구</h2>\n'
            '  <div style="background:#111827;border:1px solid #1f2937;border-radius:12px;padding:14px 30px;display:flex;flex-direction:column;">\n'
            f'{rows}\n  </div>\n</section>')


def main():
    decks = json.loads((ROOT / "tools/decks.json").read_text(encoding="utf-8"))["decks"]
    for d in decks:
        f = d["file"]
        miss = missing(f, d.get("orig"))
        print(f"{f[:40]:<42} 누락 {len(miss)}")
        if "--audit" in sys.argv or not miss:
            for x in miss:
                print("   -", x[:100])
            continue
        p = ROOT / f
        t = p.read_text(encoding="utf-8")
        per = 12
        chunks = [list(enumerate(miss, 1))[i:i + per] for i in range(0, len(miss), per)]
        new = "\n\n".join(slide(c, n, len(chunks)) for n, c in enumerate(chunks, 1))
        if 'data-label="부록"' not in t:
            new = divider() + "\n\n" + new
        end = t.rindex("</section>") + len("</section>")
        p.write_text(t[:end] + "\n\n" + new + t[end:], encoding="utf-8")


if __name__ == "__main__":
    main()
