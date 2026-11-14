"""폐루프 한 라운드: (라운드 0 = 초기 설계) · 대리모델 → 다음 후보 분자 → MD(재생 · 실행) → 결과 표 → 볼트 노트 → 정지 판단.
  python scripts/loop_step.py            # 한 라운드
  python scripts/loop_step.py --all      # 정지 규칙까지 반복
  python scripts/loop_step.py --mode live --threads 4    # 내 컴퓨터에서 MD 를 실제로(후보 하나 약 5분)
재생(replay) = expected_output 의 기준 MD 값을 그 자리에 넣는다 → 고른 후보 · 순서가 기준과 같아야 한다(L-8 로 확인).
실행(live) = MD 워크플로우가 후보 분자 1종으로 ① 3D → ② GAFF2 · AM1-BCC → ③ 단분자 상자 → ④ LAMMPS → ⑤ 밀도 · CED
"""
import argparse, csv, json
import numpy as np
from common import LOOP, load_cfg, ws, results, add_result, xy, targets, library, OBJ, dump
import surrogate, acquire, notes


def init_design(cfg, X):
    """기술자 공간(표준화)에서 서로 가장 먼 후보를 차례로(최대 최소 거리) · 첫 점 = seed 로 고른 후보."""
    Z = (X - X.mean(0)) / (X.std(0) + 1e-12); rng = np.random.default_rng(cfg["seed"])
    picks = [int(rng.integers(len(X)))]
    while len(picks) < cfg["init"]:
        d = np.min(np.linalg.norm(Z[:, None, :] - Z[picks][None, :, :], axis=2), axis=1); d[picks] = -1
        picks.append(int(np.argmax(d)))
    return picks


def run_md(cid, cand, cfg, w, mode, threads, rnd):
    if mode == "replay":
        ref = {r["id"]: r for r in csv.DictReader(open(LOOP / "expected_output" / cfg["name"] / "loop_results.csv", encoding="utf-8"))}
        if cid not in ref or ref[cid]["cand"] != cand["cand"]:
            raise SystemExit(f"기준 표와 다름: {cid} · {cand['cand']} ≠ 기준 {ref.get(cid, {}).get('cand')} · 설정 · 버전 · 앞 라운드 결과를 확인")
        r = dict(ref[cid]); r["mode"] = "replay"; add_result(w, r); return r
    from mdwf import molecule, forcefield, pipeline
    from mdwf.common import workspace
    workspace(w); name = cand["cand"]
    if not (w / "ff" / f"{name}_gaff2.json").exists():
        molecule.build(name, cand["smiles"], w); forcefield.make(name, w)
    n = max(10, round(cfg["md"]["atoms"] / int(cand["n_atoms"])))
    s = pipeline.one(cid, w, comp={name: n}, atoms=cfg["md"]["atoms"], T=cfg["md"]["T"], protocol=cfg["md"]["protocol"], seed=1, threads=threads, source="loop")
    r = {"id": cid, "round": rnd, "cand": name, "smiles": cand["smiles"], "n_mol": n, "n_atoms": s["n_atoms"], "density_gcm3": s["density_gcm3"],
         "density_se": s["density_se"], "ced_MJm3": s["ced_MJm3"], "ced_se": s["ced_se"], "ok": s["ok"], "wall_s": s["wall_s"], "mode": "live"}
    add_result(w, r); return r


def step(cfg, mode, threads):
    w = ws(cfg); stp = w / "state.json"
    st = json.loads(stp.read_text()) if stp.exists() else {"round": -1, "history": [], "done": False}
    if st["done"]: print("이미 정지 규칙에 도달 · state.json 확인"); return st
    t, tol, lit = targets(cfg); rnd = st["round"] + 1
    lib, X = library(cfg); done = {r["cand"] for r in results(w)}
    if rnd == 0:
        picks = init_design(cfg, X); why = ["초기 설계(기술자 공간 최대 최소 거리 · seed %d)" % cfg["seed"]] * len(picks); info = {}
    else:
        Xo, Y, ok = xy(cfg, results(w))
        MU = np.zeros((len(X), 2)); SD = np.zeros((len(X), 2))
        for j in range(2): MU[:, j], SD[:, j] = surrogate.fit_predict(cfg["model"], Xo, Y[:, j], X, cfg["seed"])
        skip = [i for i, r in enumerate(lib) if r["cand"] in done]
        picks, sc = acquire.select(MU, SD, Y, np.array([t[o] for o in OBJ]), np.array([tol[o] for o in OBJ]), cfg["batch"], cfg["acquisition"], cfg["seed"] + rnd, skip=skip)
        why = [f"{cfg['acquisition']} {sc[i]:.3f} · 예측 ρ {MU[i, 0]:.3f}±{SD[i, 0]:.3f} · CED {MU[i, 1]:.1f}±{SD[i, 1]:.1f}" for i in picks]
        info = {"n_obs": len(Xo), "picks": [{"cand": lib[i]["cand"], "score": float(sc[i]), "mu": MU[i].round(4).tolist(), "sd": SD[i].round(4).tolist()} for i in picks]}
    ids = []
    for k, i in enumerate(picks):
        cid = f"r{rnd}_{k + 1}"; r = run_md(cid, lib[i], cfg, w, mode, threads, rnd); ids.append(cid)
        hit = notes.run_note(r, rnd, t, tol, lit, why[k])
        print(f"  {cid}: {lib[i]['cand']:22s} → ρ {r['density_gcm3']} · CED {r['ced_MJm3']} {'· 두 표적 안' if hit else ''}")
    Xo, Y, ok = xy(cfg, results(w))
    dist = np.abs((Y - np.array([t[o] for o in OBJ])) / np.array([tol[o] for o in OBJ])).max(1); b = int(np.argmin(dist))
    best = ok[b]["id"]
    notes.round_note(rnd, cfg, ids, best, f"가장 가까운 계산 {best} ({ok[b]['cand']}): 표적 폭 대비 최대 {dist[b]:.2f} 배 (1 이하 = 두 표적 안)")
    st["round"] = rnd; st["history"].append({"round": rnd, "ids": ids, "cands": [lib[i]["cand"] for i in picks], "mode": mode, "model": cfg["model"], "acq": cfg["acquisition"], **info,
                                             "best": best, "best_cand": ok[b]["cand"], "best_dist": round(float(dist[b]), 4)})
    st["done"] = bool((cfg["stop"]["both_within_tol"] and dist[b] <= 1.0) or len(Y) >= cfg["stop"]["max_md"] or rnd >= cfg["rounds"])
    dump(st, stp)
    print(f"라운드 {rnd} 끝 · 관측 {len(Y)} · 가장 가까운 {best} {ok[b]['cand']} (표적 폭의 {dist[b]:.2f} 배) · {'정지' if st['done'] else '계속'}")
    return st


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--config"); ap.add_argument("--mode", choices=["replay", "live"]); ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--all", action="store_true"); a = ap.parse_args(); cfg = load_cfg(a.config); mode = a.mode or cfg["mode"]
    while True:
        st = step(cfg, mode, a.threads)
        if st["done"] or not a.all: break


if __name__ == "__main__":
    main()
