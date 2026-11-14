"""④ 실행: 셀 → LAMMPS 표준 프로토콜 → 로그 판독 → 실패 규칙 → 실행 기록.

넣는 것: ws/cells/<id>/system.data (③)    나오는 것: ws/runs/<id>/log.lammps · prod.lammpstrj · status.json
프로토콜 = templates/in.protocol (최소화 → 고온 섞기 · 압축 · 이완 → 냉각 → 평형 → 생산)
실패 규칙(W07 규칙의 축소판):
  R1 원자 잃음 · 결합 원자 없음 · 범위 밖 원자 → 시간 간격 절반으로 다시(1회)
  R2 그 밖의 ERROR → 멈추고 마지막 ERROR 줄 보고(사람 판단)
틀리기 쉬운 곳: 짧은 실행 = 수렴 전 값 · 코어 수가 바뀌면 궤적이 비트 단위로 달라짐(값은 오차 안)
확인(자동): 종료 코드 0 · 'Total wall time' · 생산 구간 프레임 수 · 벽시계
"""
import argparse, json, os, re, shutil, subprocess, time
from collections import OrderedDict
from pathlib import Path
from .common import workspace, need, dump, PKG

PROTOCOLS = {  # 스텝 수(시간 간격 1 fs 기준 · ps = 스텝/1000)
    "standard": dict(stepsA=10000, stepsB=20000, stepsC=20000, stepsD=20000, stepsE=20000, stepsP=40000, every=2000),
    "quick":    dict(stepsA=2000, stepsB=5000, stepsC=5000, stepsD=5000, stepsE=5000, stepsP=10000, every=1000),
}
FATAL_RETRY = re.compile(r"Lost atoms|Bond atoms missing|Out of range atoms|Angle atoms missing|Dihedral atoms missing")


def lmp_cmd(threads):
    exe = need("lmp")
    cmd = [exe]
    if threads > 1: cmd += ["-sf", "omp", "-pk", "omp", str(threads)]
    return cmd


def run_once(rdir, var, threads):
    cmd = lmp_cmd(threads) + ["-in", "in.protocol", "-log", "log.lammps", "-screen", "none"]
    for k, v in var.items(): cmd += ["-var", k, str(v)]
    env = dict(os.environ, OMP_NUM_THREADS=str(threads))
    t0 = time.time(); r = subprocess.run(cmd, cwd=rdir, env=env, capture_output=True, text=True); dt = time.time() - t0
    log = (rdir / "log.lammps").read_text(errors="replace") if (rdir / "log.lammps").exists() else ""
    err = [l for l in (log + r.stdout + r.stderr).splitlines() if "ERROR" in l]
    return r.returncode, dt, log, err


def execute(rid, ws, cell=None, T=298.0, Thot=500.0, Phi=1000.0, protocol="standard", seed=4928459, threads=4, dt=1.0):
    cell = cell or rid
    src = ws / "cells" / cell / "system.data"
    if not src.exists(): raise SystemExit(f"{src} 없음 · 먼저 ③ 셀: python mdwf.py build --id {cell} …")
    rdir = ws / "runs" / rid; rdir.mkdir(parents=True, exist_ok=True)
    shutil.copy(src, rdir / "system.data"); shutil.copy(PKG / "templates" / "in.protocol", rdir / "in.protocol")
    P = PROTOCOLS[protocol]
    status = OrderedDict(id=rid, cell=cell, protocol=protocol, T=T, Thot=Thot, Phi_atm=Phi, seed=seed, threads=threads, attempts=[])
    for attempt in range(2):
        var = dict(data="system.data", seed=seed, dt=dt, T=T, Thot=Thot, Phi=Phi, **P)
        rc, wall, log, err = run_once(rdir, var, threads)
        ok = rc == 0 and "Total wall time" in log
        status["attempts"].append({"dt_fs": dt, "exit": rc, "wall_s": round(wall, 1), "ok": ok, "error": err[-1] if err else None})
        if ok: break
        if err and FATAL_RETRY.search(" ".join(err)) and attempt == 0:
            dt = dt / 2; P = {k: (v * 2 if k.startswith("steps") else v * 2 if k == "every" else v) for k, v in P.items()}
            status["rule"] = "R1 원자 잃음 계열 → 시간 간격 절반 · 같은 물리 시간"; continue
        status["rule"] = "R2 그 밖의 오류 → 멈춤"; break
    status["ok"] = status["attempts"][-1]["ok"]
    status["wall_s_total"] = round(sum(a["wall_s"] for a in status["attempts"]), 1)
    if status["ok"]:
        status["frames"] = (rdir / "prod.lammpstrj").read_text().count("ITEM: TIMESTEP")
        status["lammps_version"] = (re.search(r"LAMMPS \((.*?)\)", log) or [None, None])[1]
    dump(status, rdir / "status.json")
    return status


def main(argv=None):
    ap = argparse.ArgumentParser(description="LAMMPS 실행 (MD 워크플로우 ④)")
    ap.add_argument("id"); ap.add_argument("--cell"); ap.add_argument("--T", type=float, default=298.0)
    ap.add_argument("--protocol", choices=list(PROTOCOLS), default="standard"); ap.add_argument("--seed", type=int, default=4928459)
    ap.add_argument("--threads", type=int, default=4); ap.add_argument("--ws")
    a = ap.parse_args(argv); ws = workspace(a.ws)
    s = execute(a.id, ws, a.cell, a.T, protocol=a.protocol, seed=a.seed, threads=a.threads)
    last = s["attempts"][-1]
    print(f"실행 {a.id}: {'성공' if s['ok'] else '실패'} · 시도 {len(s['attempts'])} · 벽시계 {s['wall_s_total']} s · 코어 {a.threads}"
          + (f" · 생산 프레임 {s['frames']}" if s["ok"] else f" · {last['error']}"))


if __name__ == "__main__":
    main()
