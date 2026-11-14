#!/usr/bin/env python3
"""week07 ② 반복 실행 + 실패 감지 + 재시도 1회 — 입력 폴더의 in.* 를 차례로 LAMMPS 로 돌린다.

  python3 scripts/run_batch.py [--inputs out/inputs] [--lmp lmp] [--out out/runs]

실패 감지 규칙 4 (로그 · 종료 코드):  ERROR 줄 · 'Lost atoms' · nan/inf · 종료 코드 ≠ 0
재시도 규칙 1 :  Δt 를 절반으로 바꾼 입력을 한 번만 다시 돌린다 (원본 05주차 #17 「Δt 절반」 · 상한 = 1회)
결과 = out/runs/status.csv (run_id · 시도 · dt · 상태 · 원인 · 벽시계 초) + 로그 파일
표준 라이브러리만 쓴다.
"""
import argparse, csv, re, subprocess, time, shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
RULES = [("lost_atoms", re.compile(r"Lost atoms")), ("nan", re.compile(r"\b(nan|inf)\b", re.I)), ("error", re.compile(r"^ERROR", re.M))]


def classify(log_text, code):
    for name, rx in RULES:
        if rx.search(log_text):
            return name
    return "exit_code" if code != 0 else "ok"


def run_one(lmp, infile, workdir):
    workdir.mkdir(parents=True, exist_ok=True)
    log = workdir / "log.lammps"
    t0 = time.time()
    p = subprocess.run([lmp, "-in", str(infile.resolve()), "-log", str(log.resolve()), "-screen", "none"], cwd=workdir, capture_output=True, text=True)
    sec = time.time() - t0
    text = (log.read_text(errors="ignore") if log.exists() else "") + p.stderr
    return classify(text, p.returncode), sec, log


def halve_dt(infile, outfile):
    txt = infile.read_text()
    m = re.search(r"^timestep\s+([0-9.eE+-]+)", txt, re.M)
    dt = float(m.group(1)); new = dt / 2
    outfile.write_text(re.sub(r"^timestep\s+[0-9.eE+-]+", f"timestep {new:g}", txt, flags=re.M))
    return dt, new


def main(inputs, lmp, out):
    inputs, out = Path(inputs), Path(out); out.mkdir(parents=True, exist_ok=True)
    rows = []
    for infile in sorted(inputs.glob("in.*")):
        rid = infile.name[3:]
        dt = float(re.search(r"^timestep\s+([0-9.eE+-]+)", infile.read_text(), re.M).group(1))
        status, sec, log = run_one(lmp, infile, out / rid)
        rows.append([rid, 1, dt, status, sec])
        print(f"{rid:8s} 시도 1  dt {dt:<6g} → {status:10s} {sec:5.2f} s")
        if status != "ok":                                   # 재시도 1회: Δt 절반
            retry_in = out / rid / f"in.{rid}.retry"
            old, new = halve_dt(infile, retry_in)
            status2, sec2, _ = run_one(lmp, retry_in, out / rid / "retry")
            rows.append([rid, 2, new, status2, sec2])
            print(f"{rid:8s} 시도 2  dt {new:<6g} → {status2:10s} {sec2:5.2f} s   (Δt {old:g} → {new:g})")
    with open(out / "status.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["run_id", "attempt", "dt", "status", "wall_s"])
        for r in rows: w.writerow([r[0], r[1], f"{r[2]:g}", r[3], f"{r[4]:.2f}"])
    ok = sum(1 for r in rows if r[3] == "ok"); print(f"완료 {ok} / 실행 {len(rows)} · status.csv")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--inputs", default=HERE / "out/inputs")
    ap.add_argument("--lmp", default=shutil.which("lmp") or "lmp")
    ap.add_argument("--out", default=HERE / "out/runs")
    a = ap.parse_args(); main(a.inputs, a.lmp, a.out)
