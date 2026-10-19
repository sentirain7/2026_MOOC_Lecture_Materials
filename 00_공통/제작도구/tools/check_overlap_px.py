#!/usr/bin/env python3
"""check_overlap_px.js 결과 분석 — 글자 본체 자리에 배경이 아닌 픽셀이 있으면 겹침으로 보고한다.

  python3 tools/check_overlap_px.py <작업폴더> [--detail]

판정: 글자 상자(위아래 18% 제외한 본체)의 픽셀 중, 상자 둘레 2px 테두리 띠의 대표색(최빈색)과
      색 차이가 큰 픽셀이 MIN_FRAC 이상이고 MIN_PIX 개 이상이면 겹침.
"""
import json, sys, collections
from pathlib import Path
from PIL import Image

MIN_FRAC, MIN_PIX, DIFF = 0.012, 25, 60


def mode_color(px, pts):
    c = collections.Counter(px[x, y][:3] for x, y in pts)
    return c.most_common(1)[0][0]


def analyze(dirp):
    meta = json.loads((dirp / "boxes.json").read_text())
    res = []
    for s in meta["slides"]:
        im = Image.open(dirp / f"{s['slide']:02d}_notext.png").convert("RGB")
        W, H = im.size
        sx, sy = W / 1920, H / 1080
        px = im.load()
        for b in s["boxes"]:
            x0, x1 = int(b["x"] * sx), int((b["x"] + b["w"]) * sx)
            y0, y1 = int((b["y"] + b["h"] * 0.18) * sy), int((b["y"] + b["h"] * 0.82) * sy)
            x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, W - 1), min(y1, H - 1)
            if x1 - x0 < 3 or y1 - y0 < 3:
                continue
            ring = [(x, y) for x in range(x0, x1) for y in (max(y0 - 2, 0), min(y1 + 1, H - 1))] + \
                   [(x, y) for y in range(y0, y1) for x in (max(x0 - 2, 0), min(x1 + 1, W - 1))]
            bg = mode_color(px, ring)
            tot = bad = 0
            for y in range(y0, y1):
                for x in range(x0, x1):
                    c = px[x, y]
                    tot += 1
                    if abs(c[0] - bg[0]) + abs(c[1] - bg[1]) + abs(c[2] - bg[2]) > DIFF:
                        bad += 1
            if bad >= MIN_PIX and bad / tot >= MIN_FRAC:
                res.append({"slide": s["slide"], "label": s["label"], "txt": b["txt"], "svg": b["svg"], "frac": round(bad / tot, 3)})
    # 같은 슬라이드·같은 글자 중복 제거
    seen, out = set(), []
    for r in res:
        k = (r["slide"], r["txt"])
        if k not in seen:
            seen.add(k); out.append(r)
    return meta["file"], len(meta["slides"]), out


def main():
    work = Path(sys.argv[1])
    detail = "--detail" in sys.argv
    total = 0
    allres = {}
    for d in sorted(p for p in work.iterdir() if (p / "boxes.json").exists()):
        f, n, out = analyze(d)
        allres[f] = out
        total += len(out)
        sl = sorted({r["slide"] for r in out})
        print(f"{f[:44]:<46} {n:>3}장  겹침 {len(out):>3}건 · 슬라이드 {sl}")
        if detail:
            for r in out:
                print(f"    #{r['slide']:02d} {r['label'][:18]:<18} {'svg' if r['svg'] else 'html'} {r['frac']*100:4.1f}%  「{r['txt']}」")
    (work / "overlap_px.json").write_text(json.dumps(allres, ensure_ascii=False, indent=1))
    print("합계", total)


if __name__ == "__main__":
    main()
