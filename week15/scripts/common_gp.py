"""W15 공통: 가정 함수 · GP 설정. 수치는 모두 이 파일의 가정 함수에서 계산한다(실측 아님 · 원본 10주차 보충A #22 「가정 예시」와 같은 성격)."""
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel, ConstantKernel as C

def f_true(x):
    """가정 함수(조성 x ∈ [0,1] → 물성). 봉우리 2개: 왼쪽 국소 최대(x 0.25) · 오른쪽 전역 최대(x 0.72)."""
    x = np.asarray(x, float)
    return 0.5 * np.exp(-((x - 0.25) / 0.1) ** 2) + 0.85 * np.exp(-((x - 0.72) / 0.07) ** 2) + 0.15

GRID = np.linspace(0, 1, 101)
NOISE = 0.05            # 관측 잡음 표준편차(알레아토릭)
ELL, SF = 0.15, 0.6     # 고정 커널: 길이척도 ℓ · 신호 표준편차 σ_f

def gp_fixed(ell=ELL, sf=SF, sn=NOISE):
    k = C(sf ** 2, 'fixed') * RBF(ell, 'fixed') + WhiteKernel(sn ** 2, 'fixed')
    return GaussianProcessRegressor(kernel=k, optimizer=None, normalize_y=False)

def gp_fitted(seed=0):
    k = C(0.36, (1e-2, 1e1)) * RBF(0.15, (0.02, 2.0)) + WhiteKernel(0.0025, (1e-6, 0.5))
    return GaussianProcessRegressor(kernel=k, n_restarts_optimizer=5, random_state=seed)

def predict(gp, X, y, grid=GRID):
    gp.fit(np.asarray(X).reshape(-1, 1), np.asarray(y))
    mu, sd = gp.predict(grid.reshape(-1, 1), return_std=True)
    return mu, sd

def observe(x, rng):
    return f_true(x) + rng.normal(0, NOISE, np.shape(x))
