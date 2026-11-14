#!/usr/bin/env python3
"""W14 전체 체인: 기술자 → 학습 표 → 학습 · 격자 → SHAP · PDP → 재정련 → 덱 데이터.  python3 scripts/run_all.py [--fast]"""
import subprocess, sys, time
from pathlib import Path
S = Path(__file__).resolve().parent
t0 = time.time()
for s in ('descriptors.py', 'binder_features.py', 'train_xgb.py', 'shap_report.py', 'refine_features.py', 'export_deck_data.py'):
    args = [sys.executable, str(S / s)] + (['--fast'] if s == 'train_xgb.py' and '--fast' in sys.argv else [])
    print(f'▶ {s}', flush=True); subprocess.run(args, check=True, cwd=S.parent)
print(f'완료 · {time.time() - t0:.0f} s')
