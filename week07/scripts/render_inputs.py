#!/usr/bin/env python3
"""week07 ① 템플릿 치환 — 매개변수 표(CSV) 한 줄 = 입력 파일 한 개.

  python3 scripts/render_inputs.py [--params data/params.csv] [--template data/in.lj.template] [--out out/inputs]

템플릿의 자리표시 {T} {seed} {dt} {steps} {run_id} 를 표의 값으로 채운다 (str.format).
입력 파일은 산출물이다 — 고치려면 표를 고치고 다시 만든다 (원본 05주차 #8 · #10 의 규칙).
표준 라이브러리만 쓴다.
"""
import argparse, csv, json, hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent


def render(params_csv, template, outdir):
    tpl = Path(template).read_text(encoding="utf-8")
    outdir = Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader(open(params_csv, encoding="utf-8")))
    manifest = []
    for r in rows:
        text = tpl.format(**r)                         # 자리표시 → 값
        path = outdir / f"in.{r['run_id']}"
        path.write_text(text, encoding="utf-8")
        h = hashlib.sha1(text.encode()).hexdigest()[:6]  # 입력 해시 6자리 (원본 05주차 #15)
        manifest.append({"run_id": r["run_id"], "file": str(path.relative_to(HERE)), "hash": h, **{k: r[k] for k in r if k != "run_id"}})
        print(f"{r['run_id']:8s} T={r['T']:>4s} seed={r['seed']:>3s} dt={r['dt']:>6s} steps={r['steps']:>5s} → {path.name}  #{h}")
    (outdir / "manifest.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"{len(rows)} 개 생성 · manifest.json")
    return manifest


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--params", default=HERE / "data/params.csv")
    ap.add_argument("--template", default=HERE / "data/in.lj.template")
    ap.add_argument("--out", default=HERE / "out/inputs")
    a = ap.parse_args()
    render(a.params, a.template, a.out)
