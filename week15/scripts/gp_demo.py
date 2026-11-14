#!/usr/bin/env python3
"""가우스 과정(GP) 1차원 · 2차원 예제.  W15 · 15-3  (원본 10주차 보충A #22 · COMID 설정 = RBF + WhiteKernel)
  1D: 관측점을 하나씩 추가하며 μ ± σ 갱신(점 2 → 6) · 적합 커널 값
  2D: 학습점 15개 · 1-최근접 거리 vs |오차| → 적용 영역 임계 d 0.12 안 · 밖 평균 오차 (보충A #28)
  python3 scripts/gp_demo.py  → out/gp_demo.json"""
import json, os, warnings
warnings.filterwarnings('ignore')
import numpy as np
from common_gp import f_true, GRID, NOISE, ELL, SF, gp_fixed, gp_fitted, predict, observe
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel, ConstantKernel as C
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    rng = np.random.default_rng(15)
    order = [0.08, 0.92, 0.5, 0.28, 0.72, 0.62]
    yobs = observe(np.array(order), rng)
    stages = []
    for n in range(2, len(order) + 1):
        mu, sd = predict(gp_fixed(), order[:n], yobs[:n])
        stages.append({'n': n, 'x': order[:n], 'y': [round(v, 4) for v in yobs[:n]], 'mu': np.round(mu, 4).tolist(), 'sd': np.round(sd, 4).tolist(),
                       'sd_max': round(float(sd.max()), 4), 'sd_mean': round(float(sd.mean()), 4), 'x_sd_max': round(float(GRID[sd.argmax()]), 2)})
    g = gp_fitted(); g.fit(np.array(order).reshape(-1, 1), yobs)
    kp = g.kernel_.get_params()
    fitted = {'sf': round(float(np.sqrt(kp['k1__k1__constant_value'])), 4), 'ell': round(float(kp['k1__k2__length_scale']), 4), 'sn': round(float(np.sqrt(kp['k2__noise_level'])), 4), 'kernel': str(g.kernel_)}
    # 2D 적용 영역
    rng2 = np.random.default_rng(152)
    f2 = lambda P: np.sin(3 * P[:, 0]) * np.cos(2 * P[:, 1]) + 0.5 * P[:, 1]
    Xtr = rng2.uniform(0, 1, (15, 2)) * np.array([0.6, 1.0])   # x1 ∈ [0, 0.6] 만 학습 → 오른쪽 = 외삽
    ytr = f2(Xtr) + rng2.normal(0, NOISE, 15)
    k2 = C(1.0, (1e-2, 1e1)) * RBF([0.3, 0.3], (0.02, 3.0)) + WhiteKernel(0.0025, (1e-6, 0.5))
    g2 = GaussianProcessRegressor(kernel=k2, n_restarts_optimizer=5, random_state=0).fit(Xtr, ytr)
    gx = np.stack(np.meshgrid(np.linspace(0, 1, 21), np.linspace(0, 1, 21)), -1).reshape(-1, 2)
    mu2, sd2 = g2.predict(gx, return_std=True); err = np.abs(mu2 - f2(gx))
    dnn = np.min(np.linalg.norm(gx[:, None, :] - Xtr[None, :, :], axis=2), axis=1)
    d0 = 0.12; inside = dnn <= d0
    ad = {'train_points': 15, 'grid_points': int(len(gx)), 'd_threshold': d0, 'inside_n': int(inside.sum()), 'outside_n': int((~inside).sum()),
          'mae_inside': round(float(err[inside].mean()), 4), 'mae_outside': round(float(err[~inside].mean()), 4),
          'sd_inside': round(float(sd2[inside].mean()), 4), 'sd_outside': round(float(sd2[~inside].mean()), 4),
          'corr_d_err': round(float(np.corrcoef(dnn, err)[0, 1]), 3), 'corr_sd_err': round(float(np.corrcoef(sd2, err)[0, 1]), 3),
          'train_x1_range': [0, 0.6]}
    out = {'assumed_function': '0.5·exp(−((x−0.25)/0.1)²) + 0.85·exp(−((x−0.72)/0.07)²) + 0.15 (가정 · 실측 아님)', 'noise_sd': NOISE, 'kernel_fixed': {'sf': SF, 'ell': ELL, 'sn': NOISE},
           'grid': GRID.round(2).tolist(), 'f_true': np.round(f_true(GRID), 4).tolist(), 'stages': stages, 'fitted_6pts': fitted, 'ad_2d': ad}
    os.makedirs(os.path.join(ROOT, 'out'), exist_ok=True); json.dump(out, open(os.path.join(ROOT, 'out', 'gp_demo.json'), 'w'), ensure_ascii=False, indent=1)
    for s in stages: print(f"점 {s['n']} · σ 최대 {s['sd_max']:.3f} (x={s['x_sd_max']}) · σ 평균 {s['sd_mean']:.3f}")
    print(f"6점 적합 커널: σ_f {fitted['sf']} · ℓ {fitted['ell']} · σ_n {fitted['sn']}")
    print(f"2D 적용 영역 d ≤ {d0}: {ad['inside_n']}점 · 평균 |오차| {ad['mae_inside']} · σ {ad['sd_inside']}  |  밖 {ad['outside_n']}점 · |오차| {ad['mae_outside']} · σ {ad['sd_outside']}")
    print(f"상관: 최근접 거리 ↔ |오차| {ad['corr_d_err']} · σ ↔ |오차| {ad['corr_sd_err']}")
    print('→ out/gp_demo.json')

if __name__ == '__main__': main()
