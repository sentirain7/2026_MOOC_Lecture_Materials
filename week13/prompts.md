# week13 Claude Code 지시문 · 덱 「만들어 보기」 장의 원문

사용 환경 · 순서 · 규칙: `../docs/prompt_setup.md` · `../docs/claude_code_quickstart.md` (W01 12장). 터미널 → `conda activate mdai` → `cd week13` → `claude` → 아래 지시를 복사해 붙여 넣고 [ ] 안만 바꾼다(지시 1개 = 대화 1개 · 주제가 바뀌면 `/clear`). 파일은 붙여 넣지 않는다 · Claude Code 가 `@경로` 와 실행 결과를 직접 읽는다. 명령 실행 · 파일 수정은 승인 창에서 확인 후 승인. 결과 파일 = `out/P13-n_result.md` (Claude Code 가 저장). 숫자는 저장소 스크립트의 JSON 이 기준 · Claude Code 가 낸 숫자는 JSON 과 글자까지 대조한다. `scripts/` 는 고치지 않는다(변형은 `out/` 아래 새 파일).

## P13-1 · 내 데이터의 행 · 그룹 · 표적 정의표 (덱 7장) → `out/P13-1_result.md`
```text
@notebooks/01_split_and_leak.ipynb 를 실행하고, 셀 1 의 데이터 요약 출력과 @data/bulk_md_373.csv 로 ① 한 행이 무엇 1회인지 ② 같은 조건 반복을 묶는 그룹 열 ③ 표적 3개(밀도 · CED · 체적탄성률)의 단위 · 범위 · 반복 간 표준편차 ④ 반복 간 표준편차보다 작은 RMSE 를 믿으면 안 되는 이유 한 줄 ⑤ 내 연구 데이터([내 재료 · 내 측정 종류])라면 그룹 기준이 무엇일지를 표로 정리해라. 요약에 없는 수치는 「확인 필요」로 표시해라. 노트북과 scripts/ 는 고치지 마라.
```
확인: 그룹 열이 「같은 조건의 반복」을 한 묶음으로 만드는가 · 표적마다 단위 · 범위 · 반복 SD 3칸이 모두 있는가.

## P13-2 · split_compare ▶ → 분할 4종 표 · 보고 문장 (덱 13장) → `out/P13-2_result.md`
```text
python3 scripts/split_compare.py 를 실행하고 결과 out/split_compare.json(같은 데이터 · 모델 4종 · 분할 4종)을 읽어 ① 분할 4종(random · cond · loago · t_extrap)이 각각 답하는 질문을 한 줄씩 ② 무작위 분할의 누수 비율(leak_frac)과 그것이 숲(forest) 점수를 얼마나 부풀렸는지 ③ 「처음 보는 노화 상태」 예측에 쓸 모델과 근거 ④ 보고 문장 1개(분할 방식 · RMSE 와 단위 · R² · 시험 n 포함)를 써라. 숫자는 expected_output/split_compare.json 과 대조하고, JSON 에 없는 값은 지어내지 마라.
```
확인: 보고 문장에 분할 방식 · 단위 · n 이 모두 있는가 · 숫자가 JSON 과 글자까지 같은가 · 다르면 LLM 이 지어낸 것.

## P13-3 · fit_linear_tree ▶ → 깊이 선택 · 근거 2줄 (덱 25장) → `out/P13-3_result.md`
```text
python3 scripts/fit_linear_tree.py 를 실행하고 결과 out/tree_depth.json(나무 깊이 1 ~ 12 · 조건 그룹 5겹의 학습 · 검증 RMSE · 물성 3종 · 무작위 KFold 비교)을 읽어 ① 물성별 검증 RMSE 가 최소인 깊이 ② 최소 이후 검증 오차가 오르는 물성과 평탄한 물성의 차이를 반복 간 표준편차(md_seed_sd_median)와 비교해 설명 ③ 내가 고를 깊이와 근거 2줄 ④ 무작위 KFold(random_kfold)의 검증 오차가 조건 그룹보다 낮은 이유를 표로 정리해라. 다른 깊이를 시험할 때는 scripts/ 대신 out/ 아래 새 스크립트로 돌려 강좌 결과와 비교해라. JSON 에 없는 값은 지어내지 마라.
```
확인: 고른 깊이의 근거에 검증 오차와 반복 SD 가 함께 있는가 · 깊이를 무작위 KFold 곡선으로 고르지 않았는가.
