# week18 Claude Code 지시 · 덱 「만들어 보기」 장의 원문 (L-1 ~ L-8)

사용 환경 · 순서 · 규칙: `../docs/prompt_setup.md` (W01 12장). 터미널 → `conda activate mdai` → `cd 2026_MOOC_Lecture_Materials/week18` → `claude` → 아래 블록을 붙여 넣고 [ ] 안만 바꾼다. 지시 1개 = 대화 1개(주제가 바뀌면 `/clear`). 명령 실행은 승인 창에서 확인한다. 결과 파일 = `out/L-n_result.md` (week18/out).
기준 원문 = `../loop/prompts.md` (loop 폴더에서 실행하는 판) · 이 파일은 week18 폴더에서 실행하도록 경로를 옮긴 판이다: 명령 = `cd ../loop && python scripts/…` · 파일 = `../loop/…` · 작업 폴더 = `../loop/ws/<이름>` (이름 = `../loop/config/loop.yaml` 의 `name` · 기준 사례 = `avg_molecule_2target`).
역할 나눔: 계산은 `../loop/scripts/` · `../mdworkflow/mdwf/` 의 강좌 코드가 한다(고치지 않음) · Claude Code 는 실행 · 파일 읽기 · 표 · 판정 근거 · 비교 · 파일에 없는 값은 쓰지 않는다.

## 시작 전 · 설치 지시문 (`../docs/install_prompts.md`)
- **I-3 · Zotero + Better BibTeX** (W02): 내 문헌을 더할 때 · 내보내기 위치 = `loop/lit/library.bib` · 강좌 사례 서지 15편은 이미 들어 있다(없어도 루프는 돈다).
- **I-4 · Obsidian + 강좌 볼트** (W02): 「폴더를 보관함으로 열기」 → `loop/vault` · 그래프 보기로 papers · runs · rounds 노트 연결 확인(L-7).
- **I-5 · 전체 점검** (W01 · W06 · W18): 작은 MD 한 번 + 폐루프 재생 1라운드 · 라운드 0 후보 6개가 `loop/expected_output/` 과 같은지.

## L-1 · 문헌 → 표적 (덱 13장 · W02 · W18) → `out/L-1_result.md`
```text
../loop 폴더에서 python scripts/lit_extract.py 를 실행해 @../loop/vault/papers 의 논문 노트로 표적을 만들어라. ../loop/ws/<이름>/lit_values.csv 와 lit_targets.json 을 읽고(이름 = ../loop/config/loop.yaml 의 name) ① 물성별 표적값(중앙값) · 평균 · 개수 · 근거 citekey ② 표적에서 뺀 행과 이유 ③ 밀도 실측 22개의 흩어짐(최소 · 최대 · 사분위)을 표로 적어라. 노트 내용(값)은 고치지 마라. → out/L-1_result.md
```
확인: density 1.018 (mean 1.0208 · n 22 · 11편) · ced 354.2 (n 7 · citekey 4개) · 값 30행 · 뺀 행 1(rouidi2024molecular 밀도 0.947 · MD 값 → 「표적 아님」) · 밀도 최소 0.94 · 최대 1.08 · 사분위 약 1.01 ~ 1.04. 기준 = `../loop/expected_output/avg_molecule_2target/lit_targets.json` · `lit_values.csv`.

## L-2 · 후보 분자 표 (덱 13장 · W11) → `out/L-2_result.md`
```text
../loop 폴더에서 python scripts/library.py 로 「아스팔트 평균 분자」 후보 표를 만들어라. 핵별 · 사슬 수별 후보 개수, 원자 수 · 분자량 범위, 기술자 5개(MW · fa · HC · het · rot)의 범위를 표로 적고, 이 후보들이 아스팔트의 어느 성분(방향족 · 레진)을 닮았는지 두 줄로 설명해라. → out/L-2_result.md
```
확인: 168개 = 핵 7 × 사슬 1 · 2 × 길이 1 ~ 12 (핵마다 24) · 원자 15 ~ 96 · 분자량 92 ~ 521 · 열 11개. 기준 = `../loop/expected_output/avg_molecule_2target/library.csv`.

## L-3 · 후보 하나를 MD 로 (덱 19장 · 실행 모드 · W09 · W17) → `out/L-3_result.md`
```text
후보 [naphthalene-1x4] 를 MD 워크플로우로 계산해라: python ../mdworkflow/mdwf.py 의 mol(--smiles · SMILES 는 ../loop/ws/<이름>/library.csv) → ff → all(--comp 이름=개수 · 원자 약 1,500 · --threads 4 · 작업 폴더 --ws out/ws). 밀도 · CED 를 표적(../loop/ws/<이름>/lit_targets.json)과 비교해 표적 폭(../loop/config/loop.yaml 의 tol) 대비 몇 배 떨어졌는지 적어라. → out/L-3_result.md
```
확인: 약 5분(4코어) · 기준 = `../week17/expected_output/candidates/results.csv` 의 naphthalene-1x4 (0.9784 · 420.6) · 판정 폭 밀도 ±0.015 · CED ±15 안이면 같은 결과.

## L-4 · 대리모델 고르기 (덱 12장 · W13 · W14 · W15) → `out/L-4_result.md`
```text
../loop 폴더에서 python scripts/surrogate.py compare 로 gp · rf · xgb 를 단일 제외 교차검증해라(관측 4개 미만이면 L-6 을 먼저). 모델별 밀도 · CED 의 RMSE 와 1σ 포함 비율을 표로 적고, 지금 관측 수에서 쓸 모델을 근거 두 줄과 함께 제안만 해라(../loop/config/loop.yaml 은 바꾸지 마라). 관측 12개면 @../loop/expected_output/avg_molecule_2target/model_compare.json 과 비교해라. → out/L-4_result.md
```
확인(관측 12): gp 밀도 0.0630 · 0.33 / CED 33.2 · 0.50 · rf 0.0607 · 0.58 / 27.9 · 0.75 · xgb 0.0654 · 0.00 / 33.9 · 0.17 → 1σ 포함 비율이 0.68 에 가장 가까운 모델 = rf.

## L-5 · 다음 후보 고르기 (덱 20장 · W15 · W16) → `out/L-5_result.md`
```text
../loop 폴더에서 지금 결과로 대리모델을 학습해 후보 전체의 예측 μ · σ 를 구하고, scripts/acquire.py 의 [cheb] 획득함수(체비셰프 EI · 다른 선택 ehvi · ucb)로 다음 후보 [2]개를 골라라(아직 MD 하지 않음 · loop_step.py 와 같은 seed · 계산한 후보 제외 · scripts 는 고치지 말고 out/ 에 새 파일로). 고른 후보의 예측 밀도 · CED ± σ, 표적과의 거리(표적 폭 단위 · 더 먼 쪽), 획득 점수를 표로 적고, 탐색(σ 큼)과 활용(μ 가 표적 가까움) 중 어느 쪽 선택인지 설명해라. 라운드 0 뒤라면 @../loop/expected_output/avg_molecule_2target/state.json 의 라운드 1 picks 와 비교해라. → out/L-5_result.md
```
확인(라운드 0 뒤 · seed = 7 + 라운드 번호 1): tetralin-1x1 점수 0.173 · 예측 0.9624 ± 0.0055 · 409.2 ± 2.9 (활용) · benzene-1x3 점수 0.159 · 0.953 ± 0.0226 · 404.8 ± 11.8 (탐색). 점수 = 지금 최선 d 3.04 기준 · 2번째 후보 = 1번째 예측을 가상 관측으로 넣고 다시 계산(W16 과 같은 방법).

## L-6 · 한 라운드 돌리기 (덱 20장 · W18) → `out/L-6_result.md`
```text
../loop 폴더에서 python scripts/loop_step.py 를 [재생] 모드로 한 라운드 실행해라(--all = 정지까지 · 실행 모드는 --mode live · 후보 하나 약 5분). 라운드 번호 · 고른 후보 · 결과 · 가장 가까운 계산 · 정지 여부를 표로 적고, ../loop/vault/rounds/round_k.md 와 ../loop/vault/runs/ 에 새 노트가 생겼는지 확인해라. → out/L-6_result.md
```
확인: 라운드 0 = 초기 설계 6개 · 최선 quinoline-2x3 (표적 폭의 3.04 배) · `--all` 뒤 MD 12회 · 최선 dibenzothiophene-2x6 1.97 · 정지 · 재생 전체 약 2.5 s.

## L-7 · 볼트 환류 확인 (덱 25장 · W18) → `out/L-7_result.md`
```text
@../loop/vault/runs 와 @../loop/vault/rounds 의 노트를 읽어 라운드별로 어떤 후보를 왜 골랐는지(「고른 이유」) 표로 정리하고, 각 실행 노트가 근거 문헌 [[citekey]] 에 링크되어 있는지 확인해라. Obsidian 그래프에서 무엇을 보면 되는지 한 줄로 써라. → out/L-7_result.md
```
확인: 실행 노트 12 · 라운드 노트 4 · 노트마다 근거 문헌 15편(밀도 11 + CED 4) · `[[round_k]]` · 「고른 이유」 = 라운드 0 「초기 설계(기술자 공간 최대 최소 거리 · seed 7)」 · 라운드 1 ~ 3 「cheb 점수 · 예측 ρ ± σ · CED ± σ」 · tags 의 hit 0개. 기준 = `../loop/expected_output/avg_molecule_2target/vault/`.

## L-8 · 기준 사례와 같은지 (덱 25장 · W18) → `out/L-8_result.md`
```text
../loop/ws/<이름>/db/loop_results.csv 와 state.json 을 @../loop/expected_output/<이름>/ 의 같은 파일과 비교해라. 재생 모드: 라운드별 후보 이름 · 순서가 모두 같아야 한다. 실행 모드: 라운드 0 의 6개는 같은 후보이고 밀도 차 ≤ 0.015 g/cm³ · CED 차 ≤ 15 MJ/m³ 이면 「같음」(같은 계산을 다시 돌린 흔들림의 약 1.5배). 항목별로 같음 · 허용 오차 안 · 다름을 표로 적어라. → out/L-8_result.md
```
확인: 재생 = 12 / 12 같음(id · 라운드 · 후보 · 값) · mode 열만 replay · 실행 = 라운드 0 의 6개 같은 후보 · 판정 폭 안(예: dibenzothiophene-2x6 두 번 계산 차 0.0076 · 7.1).

## 선택 · EHVI 로 바꿔 보기 (덱 18장)
```text
../loop/config/loop.yaml 을 out/ehvi.yaml 로 복사해 acquisition 만 ehvi 로 바꾼 설정을 제안하고(원본은 고치지 마라), 그 설정의 기준 결과 @../loop/expected_output/avg_molecule_2target_ehvi/loop_results.csv · state.json 을 체비셰프 기준 결과와 라운드별 최선 거리 · 고른 후보로 비교해라. → out/L-ehvi_result.md
```
확인: EHVI 최선 d 3.04 유지(3라운드 내내) · 고른 후보 = benzothiophene-1x4 · benzene-2x1 · benzene-1x1 · benzene-1x2 · naphthalene-2x2 · naphthalene-2x9(ok False) · 알킬벤젠 3개는 CED 폭 안 · 밀도 폭 밖. 이 비교는 기준 파일을 읽는 것으로 한다(EHVI 기준 결과는 재생 모드의 재현 대상이 아님 · 지금 코드로 재생하면 라운드 1 의 두 번째 후보부터 달라짐).
