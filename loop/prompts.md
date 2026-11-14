# 폐루프 · Claude Code 지시문 L-1 ~ L-8

시작: 터미널 → `conda activate mdai` → `cd 2026_MOOC_Lecture_Materials/loop` → `claude` · 설정 = `config/loop.yaml` · 결과 = `out/L-n_result.md`

## L-1 · 문헌 → 표적 (W02 · W18)
```
@vault/papers 의 논문 노트를 python scripts/lit_extract.py 로 읽어 표적을 만들어라.
ws/<이름>/lit_values.csv 와 lit_targets.json 을 읽고 ① 물성별 표적값(중앙값) · 평균 · 개수 · 근거 citekey ② 표적에서 뺀 행과 이유 ③ 밀도 실측 22개의 흩어짐(최소 · 최대 · 사분위)
을 표로 적어라. 노트 내용(값)은 고치지 마라. → out/L-1_result.md
```

## L-2 · 후보 분자 표 (W11)
```
python scripts/library.py 로 「아스팔트 평균 분자」 후보 표를 만들어라. 핵별 · 사슬 수별 후보 개수, 원자 수 · 분자량 범위,
기술자 5개(MW · fa · HC · het · rot)의 범위를 표로 적고, 이 후보들이 아스팔트의 어느 성분(방향족 · 레진)을 닮았는지 두 줄로 설명해라. → out/L-2_result.md
```

## L-3 · 후보 하나를 MD 로 (W09 · W17)
```
후보 [naphthalene-1x4] 를 MD 워크플로우로 계산해라: ../mdworkflow/mdwf.py 의 mol(--smiles) → ff → all(--comp 이름=개수 · 원자 약 1,500 · --threads 4 · 작업 폴더 --ws ws/<이름>).
밀도 · CED 를 표적(lit_targets.json)과 비교해 표적 폭(loop.yaml 의 tol) 대비 몇 배 떨어졌는지 적어라. → out/L-3_result.md
```

## L-4 · 대리모델 고르기 (W13 · W14 · W15)
```
python scripts/surrogate.py compare 로 gp · rf · xgb 를 단일 제외 교차검증해라(관측 4개 미만이면 L-6 을 먼저).
모델별 밀도 · CED 의 RMSE 와 1σ 포함 비율을 표로 적고, 지금 관측 수에서 어느 모델을 쓸지 근거 두 줄과 함께 고른 뒤 config/loop.yaml 의 model 을 [바꾸지 말고] 제안만 해라. → out/L-4_result.md
```

## L-5 · 다음 후보 고르기 (W15 · W16)
```
지금 결과로 대리모델을 학습해 후보 전체의 예측 μ · σ 를 구하고, scripts/acquire.py 의 [cheb] 획득함수(체비셰프 EI · 다른 선택 ehvi · ucb)로 다음 후보 [2]개를 골라라(아직 MD 하지 않음).
고른 후보의 예측 밀도 · CED ± σ, 표적과의 거리(표적 폭 단위 · 더 먼 쪽), 획득 점수를 표로 적고, 탐색(σ 큼)과 활용(μ 가 표적 가까움) 중 어느 쪽 선택인지 설명해라. → out/L-5_result.md
```

## L-6 · 한 라운드 돌리기 (W18)
```
python scripts/loop_step.py 를 [재생] 모드로 한 라운드 실행해라(실행 모드는 --mode live · 후보 하나 약 5분).
라운드 번호 · 고른 후보 · 결과 · 가장 가까운 계산 · 정지 여부를 표로 적고, vault/rounds/round_k.md 와 vault/runs/ 에 새 노트가 생겼는지 확인해라. → out/L-6_result.md
```

## L-7 · 볼트 환류 확인 (W18)
```
@vault/runs 와 @vault/rounds 의 노트를 읽어 라운드별로 어떤 후보를 왜 골랐는지(「고른 이유」) 표로 정리하고,
각 실행 노트가 근거 문헌 [[citekey]] 에 링크되어 있는지 확인해라. Obsidian 그래프에서 무엇을 보면 되는지 한 줄로 써라. → out/L-7_result.md
```

## L-8 · 기준 사례와 같은지 (W18)
```
ws/<이름>/db/loop_results.csv 와 state.json 을 @expected_output/<이름>/ 의 같은 파일과 비교해라.
재생 모드: 라운드별 후보 이름 · 순서가 모두 같아야 한다. 실행 모드: 라운드 0 의 6개는 같은 후보이고 밀도 차 ≤ 0.015 g/cm³ · CED 차 ≤ 15 MJ/m³ 이면 「같음」(같은 계산을 다시 돌린 흔들림의 약 1.5배).
항목별로 같음 · 허용 오차 안 · 다름을 표로 적어라. → out/L-8_result.md
```
