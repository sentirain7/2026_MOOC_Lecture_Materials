#!/usr/bin/env python3
"""획득함수 EI · UCB · PI · 최대 분산 + 1차원 BO 5라운드.  W15 · 15-4 (원본 10주차 보충B #7 · #8 · #9)
  EI(x) = (μ − f* − ξ)Φ(z) + σφ(z) · z = (μ − f* − ξ)/σ  ·  UCB = μ + κσ  ·  PI = Φ(z)  ·  최대 분산 = σ
  시작 3점(0.1 · 0.5 · 0.9) → 라운드마다 획득값 최대 x* 를 관측해 추가 · κ 0(μ 최대 = 점추정) ↔ κ 2 ↔ EI 비교
  python3 scripts/acquisition.py [--kappa 2] [--rounds 5] → out/acquisition.json"""
import argparse, json, os, warnings
warnings.filterwarnings('ignore')
import numpy as np
from scipy.stats import norm
from common_gp import f_true, GRID, gp_fixed, predict, observe
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def acq(kind, mu, sd, fbest, kappa=2.0, xi=0.0):
    sd = np.maximum(sd, 1e-9)
    if kind == 'ucb': return mu + kappa * sd
    z = (mu - fbest - xi) / sd
    if kind == 'ei': return (mu - fbest - xi) * norm.cdf(z) + sd * norm.pdf(z)
    if kind == 'pi': return norm.cdf(z)
    return sd

def run(kind, kappa, rounds, keep=False):
    rng = np.random.default_rng(1504)
    X = [0.1, 0.5, 0.9]; Y = list(observe(np.array(X), rng)); log = []
    for r in range(1, rounds + 1):
        mu, sd = predict(gp_fixed(), X, Y); fb = max(Y); a = acq(kind, mu, sd, fb, kappa)
        i = int(np.argmax(a)); xs = float(GRID[i])
        if any(abs(xs - x) < 1e-9 for x in X):      # 이미 관측한 점 → 같은 점 반복(점추정의 함정) 기록
            ys = float(observe(xs, rng)); dup = True
        else: ys = float(observe(xs, rng)); dup = False
        rec = {'round': r, 'x_next': round(xs, 2), 'mu_next': round(float(mu[i]), 4), 'sd_next': round(float(sd[i]), 4), 'acq_next': round(float(a[i]), 4), 'y_obs': round(ys, 4), 'best_before': round(fb, 4), 'duplicate': dup}
        if keep: rec.update({'x_obs': [round(v, 2) for v in X], 'y_obs_all': [round(v, 4) for v in Y], 'mu': np.round(mu, 4).tolist(), 'sd': np.round(sd, 4).tolist(), 'acq': np.round(a, 4).tolist()})
        log.append(rec); X.append(xs); Y.append(ys)
    return {'kind': kind, 'kappa': kappa, 'rounds': log, 'x_final': [round(v, 2) for v in X], 'best_y': round(max(Y), 4), 'best_x': round(X[int(np.argmax(Y))], 2), 'true_best_f': round(float(f_true(X[int(np.argmax(Y))])), 4)}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--kappa', type=float, default=2.0); ap.add_argument('--rounds', type=int, default=5); a = ap.parse_args()
    i_max = int(np.argmax(f_true(GRID)))
    runs = {'ucb_k2': run('ucb', a.kappa, a.rounds, keep=True), 'ucb_k0': run('ucb', 0.0, a.rounds), 'ucb_k01': run('ucb', 0.1, a.rounds), 'ei': run('ei', 0, a.rounds, keep=True), 'maxvar': run('maxvar', 0, a.rounds)}
    out = {'true_max_x': round(float(GRID[i_max]), 2), 'true_max_f': round(float(f_true(GRID)[i_max]), 4), 'start': [0.1, 0.5, 0.9], 'runs': runs}
    os.makedirs(os.path.join(ROOT, 'out'), exist_ok=True); json.dump(out, open(os.path.join(ROOT, 'out', 'acquisition.json'), 'w'), ensure_ascii=False, indent=1)
    print(f"가정 함수 전역 최대 x = {out['true_max_x']} · f = {out['true_max_f']}")
    for k, r in runs.items():
        print(f"{k:<8} x* 순서 {[s['x_next'] for s in r['rounds']]} · 반복 {sum(s['duplicate'] for s in r['rounds'])} · 최고 관측 {r['best_y']} @ x {r['best_x']} (참값 {r['true_best_f']})")
    print('→ out/acquisition.json')

if __name__ == '__main__': main()
