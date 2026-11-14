# week14 Claude Code 지시문 · 덱 「만들어 보기」 장의 원문

사용 환경 · 순서 · 규칙: `../docs/prompt_setup.md` · `../docs/claude_code_quickstart.md` (W01 12장). 터미널 → `conda activate mdai` → `cd week14` → `claude` → 아래 지시를 복사해 붙여 넣고 [ ] 안만 바꾼다(지시 1개 = 대화 1개 · 주제가 바뀌면 `/clear`). 파일은 붙여 넣지 않는다 · Claude Code 가 `@경로` 와 실행 결과를 직접 읽는다. 명령 실행 · 파일 수정은 승인 창에서 확인 후 승인. 결과 파일 = `out/P14-n_result.md` (Claude Code 가 저장). 수치의 「확인 필요」 표시는 지우지 않는다. JSON · CSV 에 없는 값은 지어내지 않는다. `scripts/` 는 고치지 않는다(변형은 `out/` 아래 새 파일).

## P14-1 · 기술자 표 · 학습 표 features.csv · 내 분자 1행 (덱 8장) → `out/P14-1_result.md`
Claude Code 가 지시 안에서 실행: `data/sara_molecules.csv` 끝에 내 분자 SMILES 1행 추가(승인) → `python3 scripts/descriptors.py` → `python3 scripts/binder_features.py` → `out/mol_descriptors.csv` · `out/features.csv` (노트북 01 의 앞 두 단계와 같음).
```text
@data/sara_molecules.csv 끝에 내 분자 [SMILES] 1행을 기존 열 형식대로 추가하고, descriptors.py → binder_features.py 를 실행해 out/mol_descriptors.csv 로 ① 내 분자의 n_heavy · O_frac · aro_frac · logP 를 13분자의 분획(포화 · 방향족 · 수지 · 아스팔텐) 평균과 표로 비교해 어느 분획에 가까운지 써라 ② 각 열에 실험 측정법(MS · 원소분석 · ¹³C NMR · SAXS)을 짝지어라 ③ 이 분자를 바인더에 넣을 때 바뀔 바인더 특징 2개와 방향을 써라. 표에 없는 값은 「확인 필요」로 표시하고, out/features.csv 의 행 수 · 그룹 수를 out/features_log.json 과 대조해라.
```
기대 결과(AS-Thio 비노화 U ↔ 장기 노화 L · 실행값): n_heavy 52 ↔ 57 · O_frac 0.000 ↔ 0.088 · aro_frac 0.481 ↔ 0.421 · logP 16.10 ↔ 13.49 · TPSA 0.0 ↔ 85.4 Å² · 종횡비 4.40 ↔ 3.56 · 측정법 n_heavy = MS · GPC · O_frac = 원소분석 · aro_frac = ¹³C NMR · 종횡비 = SAXS · logP · TPSA = 계산값(측정법 칸 「확인 필요」). 학습 표 = 672행 × 특징 17 + 표적 4 · 54그룹.
확인: 표의 각 기술자 열에 측정법 또는 「확인 필요」 가 있는가 · features.csv 의 행 수 672 · 그룹 수 54 가 `features_log.json` 과 같은가.

## P14-2 · 성능표 · 기준선 비교 · 누수 한 문장 (덱 15장) → `out/P14-2_result.md`
Claude Code 가 지시 안에서 실행: `python3 scripts/train_xgb.py` (전체 119 s · 격자 생략 `--fast` · 노트북 01 의 학습 단계와 같음) → `out/train_metrics.json` · `out/hparam_grid.json`.
```text
python3 scripts/train_xgb.py 를 실행하고(시간이 없으면 --fast) 결과 out/train_metrics.json 을 읽어 ① 표적 4개에 대해 특징 세트별 R² · RMSE(단위 포함) · 선형(Ridge) 기준선을 한 표로 정리해라 ② XGBoost 가 기준선을 넘지 못한 표적을 찾고 이유 후보 2개(온도 지배 · 행 수 · 특징 중복 등)를 써라 ③ 무작위 분할 R² 와 그룹 분할 R² 의 차이를 「누수」 라는 말로 한 문장 설명해라. 숫자는 expected_output/train_metrics.json 과 대조하고, 매개변수를 바꿔 볼 때는 scripts/ 대신 out/ 아래 변형 스크립트로 돌려 강좌 결과와 비교해라. JSON 에 없는 값은 지어내지 마라.
```
기대 결과(그룹 5-fold · 실행값): XGB 전체 / Ridge / RMSE · 밀도 0.975 / 0.967 / 0.0078 g/cm³ · CED 0.979 / 0.940 / 5.92 MJ/m³ · 체적탄성률 0.727 / **0.822** / 0.52 GPa · E_inter 0.849 / **0.879** / 94.9 kcal/mol. 기준선을 못 넘은 표적 = 체적탄성률 · E_inter. 이유 후보 = 온도 지배(체적탄성률은 온도만 0.800) · 행 수 576 · 특징 중복. 무작위 0.989 ↔ 그룹 0.975 · 격자 최고 0.986.
확인: RMSE 열에 단위가 붙고 표적별 n(670 · 613 · 576 · 576)이 있는가 · 「누수」 문장이 중복 · 이웃 온도라는 원인을 말하는가.

## P14-3 · SHAP 표 · 상관 쌍 선택 · 인과 없는 해석 문단 (덱 21장) → `out/P14-3_result.md`
Claude Code 가 지시 안에서 실행: `python3 scripts/shap_report.py` → `python3 scripts/refine_features.py` (노트북 02 와 같음) → `out/shap_summary.json` · `out/refine_rounds.json`.
```text
shap_report.py → refine_features.py 를 실행하고 결과 out/shap_summary.json(밀도 · CED)과 out/refine_rounds.json 을 읽어 ① 표적마다 상위 3 특징 · 방향(+/−) · 물리 해석 · 판정(일치 / 확인 필요)을 표로 써라 ② 상관이 높은 쌍(|r| > 0.95)에서 기여가 나뉜 사례를 하나 골라, 실험으로 잴 수 있는 쪽을 남기는 기준으로 어느 특징을 남길지 제안해라 ③ 해석 문단 3문장을 쓰되 「때문에」 같은 인과 표현은 쓰지 마라. 「확인 필요」 표시는 지우지 마라.
```
기대 결과(실행값): 밀도 = 온도 0.033(−) · logP 0.015(−) · O 분율 0.0075(+) · CED = 온도 27.8(−) · O 분율 12.4(+) · 첨가제 고분자 7.2(−, 「확인 필요」). 상관 쌍 4개 · 예 = O 분율 ↔ logP r −0.961 → 남길 쪽 = O 분율(원소분석) · R2 규칙은 logP 를 남겼다.
확인: 해석 문단에 인과 표현이 없고 「확인 필요」 행이 그대로 있는가 · 남길 특징의 근거가 측정법(원소분석 · NMR)으로 적혀 있는가.
