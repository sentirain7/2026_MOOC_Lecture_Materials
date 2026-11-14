#!/usr/bin/env python3
"""MD 워크플로우 명령 하나로: python mdwf.py <단계> [인자]
  mol      ① 분자 3D          python mdwf.py mol Toluene
  ff       ② 힘장 GAFF2       python mdwf.py ff Toluene
  build    ③ 셀 만들기         python mdwf.py build --comp Toluene=50 --id tol50
  run      ④ LAMMPS 실행      python mdwf.py run tol50
  analyze  ⑤ 밀도 · CED        python mdwf.py analyze tol50
  store    ⑥ 결과 표 기록      python mdwf.py store tol50
  all      ③~⑥ 한 번에        python mdwf.py all --comp ... --id ...
각 단계 설명 = README.md · 강좌 지시문 = prompts.md
"""
import sys, importlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
STEPS = {"mol": "molecule", "ff": "forcefield", "build": "builder", "run": "runner", "analyze": "analyze", "store": "store", "all": "pipeline"}
if len(sys.argv) < 2 or sys.argv[1] not in STEPS:
    print(__doc__); sys.exit(0 if len(sys.argv) < 2 else 1)
importlib.import_module("mdwf." + STEPS[sys.argv[1]]).main(sys.argv[2:])
