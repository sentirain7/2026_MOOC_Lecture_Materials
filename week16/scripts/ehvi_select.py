#!/usr/bin/env python3
"""W16 · EHVI 로 다음 MD 후보 고르기 — 관측 400건으로 GP 대리모델(목표별) 학습 → 미관측 212건의 EHVI(몬테카를로)
→ 상위 1개 선택 → 그 예측 평균을 임시 관측(가상 관측 · Kriging believer)으로 넣고 다시 계산 → 3개 배치.
고른 3개의 실제 MD 값(이미 계산된 표)을 공개해 HV 증가를 확인하고, 무작위 3개(200회 평균)와 비교한다.

  python3 scripts/ehvi_select.py data/features614.csv out/curated612.csv --obs 400 --batch 3 --out out/ehvi.json
설명용 단순화: 목표 2개 독립 정규 · 표본 512 · 고정 난수(seed 7). 실제 플랫폼 = BoTorch qNEHVI(원본 13주차 #9).
"""
import argparse, csv, json, random, sys, os
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel, ConstantKernel
sys.path.insert(0, os.path.dirname(__file__))
from pareto import front, hv

FEAT = ["temperature_K", "add_density", "add_inorganic", "add_polymer", "add_aspect", "add_stiffness", "add_nano",
        "ox_O_per_mol", "w_n_heavy", "w_HC_ratio", "w_aspect_ratio", "w_aromaticity_proxy"]

def ehvi(mu, sd, F, ref, rng, ns=512):
    base = hv(F, ref); s = rng.standard_normal((ns, 2)) * sd + mu
    gain = np.array([hv(front(F + [(x[0], x[1])]), ref) - base for x in s])
    return float(gain.mean()), float((gain > 0).mean())

ap = argparse.ArgumentParser(); ap.add_argument("feat"); ap.add_argument("cur"); ap.add_argument("--obs", type=int, default=400)
ap.add_argument("--batch", type=int, default=3); ap.add_argument("--ref", default="1.0,250"); ap.add_argument("--seed", type=int, default=7)
ap.add_argument("--out", default="out/ehvi.json"); a = ap.parse_args(); ref = tuple(map(float, a.ref.split(",")))
ok = {r["experiment_id"] for r in csv.DictReader(open(a.cur, encoding="utf-8"))}
R = [r for r in csv.DictReader(open(a.feat, encoding="utf-8")) if r["experiment_id"] in ok]
X = np.array([[float(r[c]) for c in FEAT] for r in R]); Y = np.array([[float(r["bulk_modulus"]), float(r["cohesive_energy_density"])] for r in R])
idx = list(range(len(R))); random.Random(a.seed).shuffle(idx); O, U = idx[:a.obs], idx[a.obs:]
mx, sx = X[O].mean(0), X[O].std(0) + 1e-9; Z = (X - mx) / sx
models, pred = [], []
for t in range(2):
    my, sy = Y[O, t].mean(), Y[O, t].std()
    k = ConstantKernel(1.0) * RBF(length_scale=np.ones(len(FEAT))) + WhiteKernel(0.1)
    g = GaussianProcessRegressor(kernel=k, normalize_y=False, random_state=0, n_restarts_optimizer=1).fit(Z[O], (Y[O, t] - my) / sy)
    m, s = g.predict(Z[U], return_std=True); pred.append((m * sy + my, s * sy)); models.append(str(g.kernel_)[:120])
MU = np.stack([pred[0][0], pred[1][0]], 1); SD = np.stack([pred[0][1], pred[1][1]], 1)
rmse = [float(np.sqrt(np.mean((MU[:, t] - Y[U, t]) ** 2))) for t in range(2)]
F0 = front([tuple(Y[i]) for i in O]); hv0 = hv(F0, ref)
rng = np.random.default_rng(a.seed); Fb = list(F0); picks, cand_scores = [], None
for b in range(a.batch):
    sc = [ehvi(MU[j], SD[j], Fb, ref, rng) if j not in picks else (-1, 0) for j in range(len(U))]
    if b == 0: cand_scores = sc
    j = int(np.argmax([s[0] for s in sc])); picks.append(j); Fb = front(Fb + [tuple(MU[j])])
true_after = front(F0 + [tuple(Y[U[j]]) for j in picks]); hv1 = hv(true_after, ref)
rr = random.Random(11); rand_gain = [hv(front(F0 + [tuple(Y[U[j]]) for j in rr.sample(range(len(U)), a.batch)]), ref) - hv0 for _ in range(200)]
top = sorted(range(len(U)), key=lambda j: -cand_scores[j][0])[:12]
def lab(i): r = R[i]; return dict(binder=r["binder_type"], additive=r["additive_type"], aging=r["aging_state"], T_K=float(r["temperature_K"]))
res = {"n_obs": a.obs, "n_cand": len(U), "features": FEAT, "kernel": models, "holdout_rmse": {"K_GPa": round(rmse[0], 3), "CED_MJm3": round(rmse[1], 1)},
       "ref": ref, "hv_obs": round(hv0, 2), "front_obs": [[round(p[0], 3), round(p[1], 1)] for p in F0],
       "picks": [dict(rank=b + 1, **lab(U[j]), mu=[round(float(MU[j, 0]), 3), round(float(MU[j, 1]), 1)], sd=[round(float(SD[j, 0]), 3), round(float(SD[j, 1]), 1)],
                      ehvi=round(cand_scores[j][0], 2) if b == 0 else None, true=[round(float(Y[U[j], 0]), 3), round(float(Y[U[j], 1]), 1)]) for b, j in enumerate(picks)],
       "top12_first_round": [dict(**lab(U[j]), mu=[round(float(MU[j, 0]), 3), round(float(MU[j, 1]), 1)], sd=[round(float(SD[j, 0]), 3), round(float(SD[j, 1]), 1)],
                                   ehvi=round(cand_scores[j][0], 2), p_improve=round(cand_scores[j][1], 3)) for j in top],
       "hv_after_true": round(hv1, 2), "hv_gain_ehvi": round(hv1 - hv0, 2),
       "hv_gain_random_mean": round(float(np.mean(rand_gain)), 2), "hv_gain_random_p_ge": round(float(np.mean(np.array(rand_gain) >= hv1 - hv0)), 3),
       "candidates_all": [[round(float(MU[j, 0]), 3), round(float(MU[j, 1]), 1), round(float(SD[j, 0]), 3), round(float(SD[j, 1]), 1), round(cand_scores[j][0], 2)] for j in range(len(U))],
       "seed": a.seed, "mc_samples": 512}
json.dump(res, open(a.out, "w", encoding="utf-8"), ensure_ascii=False)
print(f"obs {a.obs} · cand {len(U)} · holdout RMSE K {rmse[0]:.3f} GPa · CED {rmse[1]:.1f}")
print(f"HV obs {hv0:.2f} → after 3 EHVI picks (true) {hv1:.2f} (+{hv1-hv0:.2f}) · random 3 mean +{np.mean(rand_gain):.2f} · P(random ≥ EHVI) {np.mean(np.array(rand_gain) >= hv1-hv0):.3f}")
for p in res["picks"]: print(" ", p)
