#!/usr/bin/env python3
"""보정 곡선(calibration curve): 명목 신뢰 수준 p vs 실제 적중률.  W15 · 15-3 (원본 10주차 #23 · 보충A #23 · #24)
  ① 가정 함수 · 학습 30점 · 시험 300점 → 잡음항 적합 GP(양호) vs 같은 커널에 잡음항만 σ_n 0.03 으로 낮춤(과신)
  ② COMID 커버리지 4물성(data/comid_coverage.csv) → 정규 가정 포함률 2Φ(r·z_p)−1 에 r 적합 → 완전 보정 배율 s = 1/r
  python3 scripts/calibration.py → out/calibration.json"""
import csv, json, os, warnings
warnings.filterwarnings('ignore')
import numpy as np
from scipy.stats import norm
from scipy.optimize import minimize_scalar
from common_gp import f_true, NOISE, gp_fitted, gp_fixed, observe, ELL, SF
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.68, 0.8, 0.9, 0.95]

def coverage(mu, sd, y):
    z = np.abs(y - mu) / sd
    return [round(float(np.mean(z <= norm.ppf(0.5 + p / 2))), 3) for p in P]

def main():
    rng = np.random.default_rng(1503)
    Xtr = np.sort(rng.uniform(0, 1, 30)); ytr = observe(Xtr, rng)
    Xte = rng.uniform(0, 1, 300); yte = observe(Xte, rng)
    good = gp_fitted(); good.fit(Xtr.reshape(-1, 1), ytr); mu_g, sd_g = good.predict(Xte.reshape(-1, 1), return_std=True)
    kp = good.kernel_.get_params(); ell_f = float(kp['k1__k2__length_scale']); sf_f = float(np.sqrt(kp['k1__k1__constant_value']))
    bad = gp_fixed(ell=ell_f, sf=sf_f, sn=0.03); bad.fit(Xtr.reshape(-1, 1), ytr); mu_b, sd_b = bad.predict(Xte.reshape(-1, 1), return_std=True)
    cov_g, cov_b = coverage(mu_g, sd_g, yte), coverage(mu_b, sd_b, yte)
    comid = []
    for r in csv.DictReader(open(os.path.join(ROOT, 'data', 'comid_coverage.csv'), encoding='utf-8')):
        obs = {0.68: float(r['nominal_68']), 0.95: float(r['nominal_95'])}
        loss = lambda rr: sum((2 * norm.cdf(rr * norm.ppf(0.5 + p / 2)) - 1 - c) ** 2 for p, c in obs.items())
        rr = minimize_scalar(loss, bounds=(0.3, 2.0), method='bounded').x
        comid.append({'property': r['property'], 'cov68': obs[0.68], 'cov95': obs[0.95], 'judgement': r['judgement'], 'r_fit': round(float(rr), 3), 's_full': round(float(1 / rr), 3),
                      'curve': [round(float(2 * norm.cdf(rr * norm.ppf(0.5 + p / 2)) - 1), 3) for p in P]})
    out = {'nominal': P, 'train_n': 30, 'test_n': 300, 'good': {'label': '잡음항 적합', 'kernel': str(good.kernel_), 'coverage': cov_g, 'rmse': round(float(np.sqrt(np.mean((mu_g - yte) ** 2))), 4), 'mean_sd': round(float(sd_g.mean()), 4)},
           'over': {'label': '같은 커널 · 잡음항만 σ_n 0.03 고정(참값 0.05)', 'coverage': cov_b, 'rmse': round(float(np.sqrt(np.mean((mu_b - yte) ** 2))), 4), 'mean_sd': round(float(sd_b.mean()), 4)}, 'comid': comid}
    os.makedirs(os.path.join(ROOT, 'out'), exist_ok=True); json.dump(out, open(os.path.join(ROOT, 'out', 'calibration.json'), 'w'), ensure_ascii=False, indent=1)
    print('명목 p      ', ' '.join(f'{p:>5}' for p in P))
    print('적합 GP     ', ' '.join(f'{c:>5}' for c in cov_g), f"· 평균 σ {out['good']['mean_sd']}")
    print('잡음 과소   ', ' '.join(f'{c:>5}' for c in cov_b), f"· 평균 σ {out['over']['mean_sd']}")
    for c in comid: print(f"COMID {c['property']:<8} 68→{c['cov68']} · 95→{c['cov95']} · r {c['r_fit']} · 완전 보정 s {c['s_full']} ({c['judgement']})")
    print('→ out/calibration.json')

if __name__ == '__main__': main()
