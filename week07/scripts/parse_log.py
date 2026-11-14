#!/usr/bin/env python3
"""week07 ③ 로그 파싱 — log.lammps 의 thermo 블록(Step … 머리줄 다음의 숫자 줄) 을 CSV 로, 요약을 JSON 으로.

  python3 scripts/parse_log.py [--runs out/runs] [--out out/thermo]

규칙: 머리줄 = 'Step' 으로 시작 · 자료 줄 = 숫자만 · 'Loop time' 에서 블록 끝 (COMID parsers/log_parser.py 와 같은 규칙).
요약 = 마지막 절반 구간의 평균 temp · press · pe · etotal · 그리고 E 표류 (etotal 끝 − 처음) / |처음|.
"""
import argparse, csv, json, re, statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
NUM = re.compile(r"^\s*-?\d")


def parse(log_path):
    cols, rows, inblock = None, [], False
    for line in Path(log_path).read_text(errors="ignore").splitlines():
        if line.strip().startswith("Step"):
            cols, inblock = line.split(), True; continue
        if inblock and line.startswith("Loop time"):
            inblock = False; continue
        if inblock and NUM.match(line):
            vals = line.split()
            if len(vals) == len(cols):
                rows.append([float(v) for v in vals])
    return cols, rows


def summarize(cols, rows):
    if not rows: return {"n": 0}
    half = rows[len(rows) // 2:]
    i = {c.lower(): k for k, c in enumerate(cols)}
    s = {"n": len(rows), "step_last": int(rows[-1][i["step"]])}
    for c in ("temp", "press", "poteng", "toteng"):
        if c in i: s[c + "_mean"] = round(statistics.fmean(r[i[c]] for r in half), 4)
    if "toteng" in i and rows[0][i["toteng"]]:
        s["etot_drift_rel"] = round((rows[-1][i["toteng"]] - rows[0][i["toteng"]]) / abs(rows[0][i["toteng"]]), 4)
    return s


def main(runs, out):
    runs, out = Path(runs), Path(out); out.mkdir(parents=True, exist_ok=True)
    summary = {}
    for log in sorted(runs.glob("*/log.lammps")) + sorted(runs.glob("*/retry/log.lammps")):
        rid = log.parent.name if log.parent.name != "retry" else log.parent.parent.name + "_retry"
        cols, rows = parse(log)
        with open(out / f"{rid}.csv", "w", newline="") as fh:
            w = csv.writer(fh); w.writerow([c.lower() for c in cols] if cols else ["(no thermo)"]); w.writerows(rows)
        summary[rid] = summarize(cols, rows)
        print(f"{rid:14s} thermo 행 {len(rows):4d}  " + (f"T̄ {summary[rid].get('temp_mean')}  Ē {summary[rid].get('toteng_mean')}  drift {summary[rid].get('etot_drift_rel')}" if rows else "(실패 로그 · 자료 없음)"))
    (out / "summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    print(f"{len(summary)} 로그 → {out}/*.csv · summary.json")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default=HERE / "out/runs"); ap.add_argument("--out", default=HERE / "out/thermo")
    a = ap.parse_args(); main(a.runs, a.out)
