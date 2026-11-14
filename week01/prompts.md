# week01 지시문 · 덱 「만들어 보기」 장의 Claude Code 지시 원문

사용 환경 · 순서 · 규칙: `../docs/prompt_setup.md` (덱 12장) · 설치 · 조작: `../docs/claude_code_quickstart.md`.
터미널에서 `conda activate mdai` → `cd week01` → `claude` 를 연 뒤 아래 지시를 붙여 넣는다. 대괄호 [ ] 안만 바꾼다. 파일은 붙여 넣지 않고 `@경로` 로 가리킨다. 명령 실행 · 파일 수정 · 설치는 승인 창에서 읽고 승인한다. 결과는 `out/P주차-순번_result.md` 로 저장된다(`../CLAUDE.md` 규칙). 받은 결과의 수치는 「확인 필요」 표시를 지우지 말고, W09 · W10 에서 계산으로 확인한다.

## P1-1 · 내 재료의 조성 변수 4개 · 표적 물성 2개 표 (덱 13장) → `out/P1-1_result.md`

```text
나는 [SBS 개질 아스팔트 바인더]를 연구한다. 역설계 대상 조성 변수 4개를 표로 만들어라 · 열: 변수 이름 · 범위 · 단위 · 수준 수(3~6). 이어서 표적 물성 2개를 표로 만들어라 · 열: 이름 · 단위 · 수치 범위 · 산출 방법(시험 또는 계산) · 방향(최대/최소). 마지막 줄에 수준 수의 곱 = 후보 조합 수를 python 으로 계산해 적어라. 근거 없는 수치는 「확인 필요」로 표시하고, 결과를 out/P1-1_result.md 로 저장해라.
```

확인 포인트: 표적 2개에 수치 · 단위 · 산출 방법 · 방향이 모두 있는가 · 조합 수가 연간 실험 수(예시 100)를 넘는가.
받은 「수준 수」를 `live/combination_space.ipynb` 또는 덱 6장 계산기에 넣어 자릿수 차를 본다.

## P1-2 · 환경 점검 실행 · 보고 · 조치 (덱 25장) → `out/P1-2_result.md`

```text
@notebooks/00_setup_check.ipynb 를 python ../run_nb.py 로 실행해 out/setup_report.json 을 만들어라. 이어서 claude --version · lmp 실행 가능 여부 · 현재 conda 환경 이름을 확인해 표 하나로 보고해라 · 열: 항목 · 값 · 판정(ok / 조치 필요). 조치 필요 항목마다 ① 원인 ② 내 환경([Windows WSL2 / macOS / Linux])의 조치 명령(mdai 안에서만) ③ 다시 확인하는 방법을 적고, 설치 · 변경은 내 승인을 받은 뒤 실행해라. 노트북과 scripts/ 는 고치지 마라. 끝나면 out/setup_report.json 의 ok · data_rows 를 expected_output/setup_report.json 과 비교해라.
```

확인 포인트: `out/setup_report.json` 의 `"ok": true` · `"data_rows"`(보고서의 `data.rows`) 101. `lmp` 는 W06 부터 쓰므로 지금 「없음」 이면 W06 전까지 mdai 에 설치한다. 그래도 안 되면 `expected_output/setup_report.json` 으로 W02 진행.

참고: `run_nb.py` 는 week01 폴더 기준으로 실행해 `out/setup_report.json` · `out/papers_by_year.png` 가 `week01/out/` 에 생긴다. Claude Code 없이: `python3 scripts/setup_check.py`(같은 점검).
