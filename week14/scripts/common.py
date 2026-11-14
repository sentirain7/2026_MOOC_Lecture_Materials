"""W14 공용: 특징 세트 · 표적 · 그룹 교차검증."""
import numpy as np, pandas as pd
from pathlib import Path
from sklearn.model_selection import GroupKFold, KFold
import xgboost as xgb

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'out'
T = ['temperature_K']
BINDER = ['b_n_heavy', 'b_HC_ratio', 'b_O_frac', 'b_hetero_frac', 'b_aro_frac', 'b_MW', 'b_logP', 'b_TPSA', 'b_Rg', 'b_aspect']
ADD = ['add_density', 'add_inorganic', 'add_polymer', 'add_aspect', 'add_stiffness', 'add_nano']
TARGETS = {'density': ('density', 'g/cm³'), 'CED': ('cohesive_energy_density', 'MJ/m³'),
           'bulk': ('bulk_modulus', 'GPa'), 'E_inter': ('e_inter_total', 'kcal/mol')}
KO = {'temperature_K': '온도', 'b_n_heavy': '바인더 분자 크기', 'b_HC_ratio': '바인더 H/C', 'b_O_frac': '바인더 O 분율',
      'b_hetero_frac': '바인더 헤테로 분율', 'b_aro_frac': '바인더 방향족 분율', 'b_MW': '바인더 분자량', 'b_logP': '바인더 logP',
      'b_TPSA': '바인더 TPSA', 'b_Rg': '바인더 회전반경', 'b_aspect': '바인더 종횡비', 'add_density': '첨가제 밀도',
      'add_inorganic': '첨가제 무기', 'add_polymer': '첨가제 고분자', 'add_aspect': '첨가제 종횡비', 'add_stiffness': '첨가제 강성',
      'add_nano': '첨가제 나노'}
PARAMS = dict(n_estimators=800, learning_rate=0.03, max_depth=5, subsample=0.8, colsample_bytree=0.8, reg_lambda=1.0)


def load(target):
    f = pd.read_csv(OUT / 'features.csv')
    col = TARGETS[target][0]
    return f[f[col].notna()].reset_index(drop=True), col


def model(**kw):
    p = dict(PARAMS); p.update(kw)
    return xgb.XGBRegressor(random_state=0, n_jobs=4, **p)


def cv(df, feats, col, split='group', n=5, seed=0, **kw):
    """폴드마다 학습 · 검증 · 표준화는 학습 폴드 μ · σ (원본 09주차 #19 절차) · 반환 = 폴드 밖 예측과 지표."""
    X, y, g = df[feats].values.astype(float), df[col].values, df['group_id'].values
    sp = GroupKFold(n_splits=n).split(X, y, g) if split == 'group' else KFold(n_splits=n, shuffle=True, random_state=seed).split(X)
    pred = np.zeros(len(y)); r2s = []
    for tr, va in sp:
        mu, sd = X[tr].mean(0), X[tr].std(0); sd[sd == 0] = 1
        m = model(**kw); m.fit((X[tr] - mu) / sd, y[tr]); pred[va] = m.predict((X[va] - mu) / sd)
        r2s.append(1 - ((y[va] - pred[va]) ** 2).sum() / ((y[va] - y[va].mean()) ** 2).sum())
    rmse = float(np.sqrt(((y - pred) ** 2).mean()))
    r2 = float(1 - ((y - pred) ** 2).sum() / ((y - y.mean()) ** 2).sum())
    return dict(R2=round(r2, 4), RMSE=round(rmse, 5), R2_fold_mean=round(float(np.mean(r2s)), 4),
                R2_fold_sd=round(float(np.std(r2s)), 4), n=int(len(y))), pred
