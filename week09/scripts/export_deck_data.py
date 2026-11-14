#!/usr/bin/env python3
"""export_deck_data.py — out/ 의 결과를 덱(W09_물성산출.html)의 `var W09 = /*__DATA__*/{...}` 에 넣는다 · expected_output 갱신.
  python3 scripts/export_deck_data.py [--deck ../../decks/W09_물성산출.html]
"""
import argparse, csv, json, re, shutil
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]

def sub(arr, n=300):
    arr = list(arr); k = max(1, len(arr) // n); return arr[::k]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--deck", default=str(ROOT.parents[1] / "decks/W09_물성산출.html")); a = ap.parse_args()
    out = ROOT / "out"; J = lambda n: json.loads((out / n).read_text(encoding="utf-8"))
    dens = J("density.json"); ced = J("ced.json"); gk = J("viscosity_gk.json"); tg = J("tg.json"); summ = J("summary.json")
    ser = np.loadtxt(out / "density_series.csv", delimiter=",", skiprows=1)
    series = {"step": [int(x) for x in sub(ser[:, 0])], "v": [round(float(x), 5) for x in sub(ser[:, 2])], "run": [round(float(x), 5) for x in sub(ser[:, 3])]}
    tr = list(csv.DictReader(open(out / "ced_trace.csv", encoding="utf-8")))
    cumA = [round(float(r["cum_sum_A"]), 2) for r in tr if r["cum_sum_A"]]; runB = [round(float(r["gas_running_mean_B"]), 3) for r in tr if r["gas_running_mean_B"]]
    g = np.loadtxt(out / "gk_curve.csv", delimiter=",", skiprows=1)
    gkc = {"t": [round(float(x), 1) for x in sub(g[:, 0], 400)], "C": [round(float(x), 4) for x in sub(g[:, 1], 400)], "eta": [round(float(x), 5) for x in sub(g[:, 2], 400)],
           "comp": [[round(float(x), 5) for x in sub(g[:, 3 + c], 400)] for c in range(3)]}
    st = np.loadtxt(out / "prod/stress.txt", comments="#")
    stress = {"t": [float(x) for x in sub(st[:400, 0], 400)], "p": [round(float(x), 1) for x in sub(st[:400, 1], 400)]}
    data = {"density": dens, "series": series, "ced": ced, "cedtrace": {"cumA": cumA, "runB": sub(runB, 100)}, "gk": gk, "gkcurve": gkc, "stress": stress, "tg": tg, "row": summ["row"], "summary": {"wall_s": summ["wall_s"]}}
    deck = Path(a.deck); h = deck.read_text(encoding="utf-8")
    h2 = re.sub(r"var W09 = /\*__DATA__\*/\{.*?\};", "var W09 = /*__DATA__*/" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";", h, count=1, flags=re.S)
    assert h2 != h or "__DATA__" in h, "placeholder not found"; deck.write_text(h2, encoding="utf-8")
    # expected_output 갱신
    eo = ROOT / "expected_output"; (eo / "prod").mkdir(parents=True, exist_ok=True); (eo / "tg").mkdir(exist_ok=True)
    for n in ["density.json", "density_series.csv", "ced.json", "ced_trace.csv", "viscosity_gk.json", "gk_curve.csv", "tg.json", "vt_points.csv", "results.csv", "summary.json"]: shutil.copy(out / n, eo / n)
    for n in ["log.prod", "stress.txt", "nvt_final.data"]: shutil.copy(out / "prod" / n, eo / "prod" / n)
    for f in (out / "tg").glob("tg_T*.txt"): shutil.copy(f, eo / "tg" / f.name)
    for f in (out / "tg").glob("log.tg_T*"): shutil.copy(f, eo / "tg" / f.name)
    (eo / "ced_single_log_mol1.txt").write_text((out / "ced_tmp/log.mol1").read_text(errors="replace")[-3000:], encoding="utf-8")
    (eo / "ced_gasB_log_tail.txt").write_text((out / "ced_tmp/log.gasB").read_text(errors="replace")[-3000:], encoding="utf-8")
    print("deck data injected ·", len(json.dumps(data)), "bytes · expected_output updated")
if __name__ == "__main__": main()
