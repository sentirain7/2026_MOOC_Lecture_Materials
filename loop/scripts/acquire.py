"""⑤ 능동학습: 대리모델 μ · σ → 두 표적에 동시에 가까워질 기대 개선(EHVI) → 다음 MD 조성 배치.

두 목표: f_ρ = −|ρ − ρ*| / tol_ρ ,  f_CED = −|CED − CED*| / tol_CED   (클수록 좋음 · 0 = 표적과 같음)
EHVI: 후보마다 ρ · CED 를 N(μ, σ) 에서 256번 뽑아 f 로 바꾸고, 지금까지 관측의 파레토 전선 초부피(HV) 증가 평균 (W16)
배치: 1등을 고른 뒤 그 예측값을 임시 관측으로 넣고 다시 계산(가상 관측 · W16 과 같은 방법)
UCB(대안): 점수 = −Σ (|μ − t| − κσ)/tol  · κ = 2
cheb(기본): 두 표적 중 더 먼 쪽의 거리 d = max(|ρ − ρ*|/tol_ρ, |CED − CED*|/tol_CED) 를 줄일 기대 개선
      EI = E[max(0, d_best − d)] · d_best = 지금까지 관측의 최소 d · 두 표적을 「동시에」 맞추는 목적에 바로 맞춘 한 숫자
"""
import numpy as np


def front(P):
    P = sorted(map(tuple, P), key=lambda p: (-p[0], -p[1])); F, best = [], -np.inf
    for p in P:
        if p[1] > best: F.append(p); best = p[1]
    return F


def hv(F, ref):
    F = sorted(front(F), key=lambda p: -p[0]); h, prev = 0.0, ref[1]
    for x, y in F:
        if x > ref[0] and y > prev: h += (x - ref[0]) * (y - prev); prev = y
    return h


def f_obj(Y, t, tol):
    return np.stack([-np.abs(Y[..., j] - t[j]) / tol[j] for j in range(2)], -1)


def select(MU, SD, Yobs, t, tol, batch, method="ehvi", seed=7, ns=256, ref=(-5.0, -5.0), kappa=2.0, skip=()):
    rng = np.random.default_rng(seed); F = [tuple(p) for p in f_obj(Yobs, t, tol)]
    picks, scores = [], None; skip = list(skip)
    for b in range(batch):
        if method == "cheb":
            Zs = np.random.default_rng(seed + b).standard_normal((ns, 2))
            dobs = np.abs((np.vstack([Yobs] + [MU[i][None, :] for i in picks]) - t) / tol).max(1) if len(Yobs) else np.array([np.inf])
            best = dobs.min()
            S = Zs[None, :, :] * SD[:, None, :] + MU[:, None, :]
            d = np.abs((S - t) / tol).max(2)
            sc = np.maximum(0, best - d).mean(1)
        elif method == "ehvi":
            base = hv(F, ref); Z = rng.standard_normal((ns, 2))
            sc = np.array([np.mean([hv(F + [tuple(q)], ref) - base for q in f_obj(Z * SD[i] + MU[i], t, tol)]) for i in range(len(MU))])
        else:
            sc = -(((np.abs(MU - t) - kappa * SD) / tol).sum(1))
        sc = np.round(sc, 6); sc[picks + skip] = -np.inf
        if scores is None: scores = sc.copy()
        i = int(np.argmax(sc)); picks.append(i); F.append(tuple(f_obj(MU[i], t, tol)))
    return picks, scores
