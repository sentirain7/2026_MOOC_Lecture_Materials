"""공용: 작업 폴더 · 분자 목록 · 상수 · 명령 실행 기록."""
import csv, json, os, shutil, subprocess, time
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]            # mdworkflow/
DATA = PKG / "data"
NA = 6.02214076e23
KCALMOL_A3_TO_MJM3 = 4184.0 / NA / 1e-30 / 1e6       # kcal/mol/Å³ → MJ/m³ (= 6947.7)
MASS = {"C": 12.011, "H": 1.008, "O": 15.999, "N": 14.007, "S": 32.06}


def workspace(ws=None):
    """작업 폴더: 기본 = mdworkflow/ws · 폐루프는 loop/ws 를 넘긴다."""
    w = Path(ws) if ws else PKG / "ws"
    for d in ("mol", "ff", "cells", "runs", "db"):
        (w / d).mkdir(parents=True, exist_ok=True)
    return w


def molecules():
    """data/molecules.csv → {이름: {sara, smiles, source}}"""
    with open(DATA / "molecules.csv", encoding="utf-8") as f:
        return {r["name"]: r for r in csv.DictReader(f)}


def need(exe):
    p = shutil.which(exe)
    if not p:
        raise SystemExit(f"실행 파일 {exe} 가 없음 · conda activate mdai 를 했는지 확인 (설치 지시문 I-2)")
    return p


def run(cmd, cwd, log, stdin=None, env=None):
    """외부 명령 실행 · 출력은 log 파일에 · 실패하면 마지막 줄을 보여 주고 멈춘다."""
    t0 = time.time()
    with open(log, "w") as fl:
        fin = open(stdin) if stdin else None
        r = subprocess.run(cmd, cwd=cwd, stdin=fin, stdout=fl, stderr=subprocess.STDOUT, env=env)
        if fin: fin.close()
    dt = time.time() - t0
    if r.returncode != 0:
        tail = Path(log).read_text(errors="replace").splitlines()[-15:]
        raise SystemExit(f"명령 실패({r.returncode}): {' '.join(map(str, cmd))}\n" + "\n".join(tail))
    return dt


def dump(obj, path):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
