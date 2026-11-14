#!/usr/bin/env python3
"""노트북 실행기 · 주차 폴더를 작업 폴더로 삼아 노트북을 끝까지 실행하고 출력을 노트북에 저장한다.
  cd weekNN && python ../run_nb.py notebooks/02_dedup_doi.ipynb [더 많은 노트북 …]
  - 노트북 안의 data/ · scripts/ · out/ 경로가 주차 폴더 기준으로 맞는다(jupyter nbconvert 는 notebooks/ 폴더에서 실행해 경로가 어긋남).
  - '../scripts' 처럼 notebooks/ 기준으로 쓴 노트북은 자동으로 노트북 폴더에서 실행한다.
  - 오류가 나면 멈춘 셀 번호와 오류를 출력하고, 그때까지의 출력은 노트북에 저장한다.
"""
import sys, os, re, nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError
rc = 0
for p in sys.argv[1:] or sys.exit(__doc__):
    nb = nbformat.read(p, as_version=4)
    code = '\n'.join(c.source for c in nb.cells if c.cell_type == 'code')
    # notebooks/ 폴더 기준으로 쓴 노트북('../scripts' · '../out' · cwd='..')은 노트북 폴더에서, 나머지는 주차 폴더에서 실행
    here = os.path.dirname(os.path.abspath(p)) if re.search(r"['\"]\.\./(scripts|data|out|expected_output)|cwd\s*=\s*['\"]\.\.['\"]", code) else os.getcwd()
    client = NotebookClient(nb, timeout=1800, kernel_name='python3', resources={'metadata': {'path': here}})
    try:
        client.execute(); print(f'완료 · {p}')
    except CellExecutionError as e:
        rc = 1; print(f'오류 · {p}\n{str(e)[-2000:]}')
    finally:
        nbformat.write(nb, p)
sys.exit(rc)
