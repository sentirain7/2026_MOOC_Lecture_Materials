# week18 · 폐루프 통합 실습: 아스팔트 평균 분자 역설계 · 최종 프로젝트 (모듈 M5 · 18주 과정의 마지막 주)

| 항목 | 내용 |
|---|---|
| 덱 | `slides/W18_폐루프통합실습.html` (v3 · 27장 · 54분 · 4차시: 18-1 문제와 표적 · 18-2 설계 후보와 대리모델 · 18-3 능동학습 한 바퀴 · 18-4 환류 · 검증 · 최종 프로젝트) |
| 학습목표 | ① 논문 노트(Obsidian 볼트)에서 표적 2개(밀도 1.018 g/cm³ · CED 354.2 MJ/m³)를 자동으로 뽑고, CED 표적이 실측 대신 바인더 값 7개의 중앙값인 이유를 말한다 ② 「평균 분자」 단순화의 뜻과 한계를 말하고, 후보 168개 · 기술자 5개 · 초기 설계 6개(최대 최소 거리)를 설명한다 ③ 관측 12개에서 대리모델 3종(gp · rf · xgb)을 단일 제외 교차검증(RMSE · 1σ 포함 비율)으로 비교한다 ④ 체비셰프 EI 로 다음 후보 2개를 고르는 원리를 말하고, 라운드별 경로(최선 d 3.04 → 3.04 → 2.64 → 1.97)와 EHVI 비교를 읽는다 ⑤ 재생 · 실행 모드의 「같은 결과」를 판정하고, 실행 노트 환류 · 한계(힘장 · 단순화 · 짧은 MD)를 최종 프로젝트 제출물로 옮긴다 |
| 선수 지식 | W02 Zotero · Obsidian 볼트 · W09 CED · W11 아스팔트 SARA · 분자 기술자 · W14 · W15 대리모델 · 불확실성 · 획득함수 · W16 체비셰프 스칼라화 · EHVI · 정지 규칙 · W17 MD 워크플로우 · 판정 폭 |
| 소요 시간 | 강의 54분 + 실습 약 20분(재생 모드 · 전체 약 2.5 s) · 실행 모드를 고르면 후보 1개 약 5분(4코어) · 12개 약 1시간 |
| 새 용어 (6) | 평균 분자 · 체비셰프 스칼라화 · 단일 제외 교차검증(LOO) · 재생 모드 · 실행 노트 · 정지 규칙 → `../GLOSSARY.md` |

## 실행 환경 · Claude Code (기본)
터미널 → `conda activate mdai` → `cd 2026_MOOC_Lecture_Materials/week18` → `claude` (설치 · 조작 = `../docs/claude_code_quickstart.md` · 강좌 규칙 = `../CLAUDE.md` 자동 적용 · 설치 지시문 I-3 Zotero · I-4 Obsidian · I-5 전체 점검 = `../docs/install_prompts.md`). 이 주차의 도구는 저장소 맨 위의 `../loop/`(폐루프 · 설명 = `../loop/README.md`)와 `../mdworkflow/`(MD 워크플로우 · W17)이다. 폐루프 명령은 week18 폴더에서 `cd ../loop && python scripts/<이름>.py …` 로 실행하고, 결과는 `../loop/ws/avg_molecule_2target/`(library · lit_values · lit_targets · db/loop_results.csv · state.json) 과 볼트 `../loop/vault/runs` · `../loop/vault/rounds` 에 남는다. Claude Code 의 보고서는 `out/L-n_result.md` (week18/out) 에 둔다. `../loop/scripts/` · `../mdworkflow/mdwf/` 의 강좌 코드는 고치지 않는다.

필요한 패키지(mdai 에 포함): RDKit · scikit-learn · XGBoost · PyYAML · (실행 모드) AmberTools · Packmol · LAMMPS. Obsidian · Zotero 는 볼트를 눈으로 보거나 내 문헌을 더할 때만 필요하다(강좌 저장소에 사례 서지 `../loop/lit/library.bib` 와 논문 노트 15편이 들어 있어 없어도 루프는 돈다).

## Claude Code 지시문 (덱 「만들어 보기」 장)
`prompts.md`: L-1 문헌 → 표적 · L-2 후보 표(13장) · L-4 대리모델 고르기(12장) · L-5 다음 후보 · L-6 한 라운드(20장) · L-7 볼트 환류 · L-8 기준과 같은지(25장) · L-3 후보 하나를 MD 로(실행 모드 · 덱 19장에서 안내). 결과 = `out/L-n_result.md`. 기준 원문 = `../loop/prompts.md` (loop 폴더에서 실행하는 판) · 이 파일은 week18 폴더에서 실행하도록 경로를 옮긴 판. 사용 환경 = `../docs/prompt_setup.md`.

## 실습 순서
1. **표적 · 후보** (18-2 · 약 1분) L-1 · L-2 → `../loop/ws/avg_molecule_2target/lit_values.csv`(30행) · `lit_targets.json`(밀도 1.018 · n 22 · CED 354.2 · n 7) · `library.csv`(168행 · 원자 15 ~ 96 · 분자량 92 ~ 521).
2. **라운드 0** (18-3) L-6 → 초기 설계 6개(quinoline-2x3 · tetralin-2x12 · phenanthrene-1x1 · benzene-1x9 · benzothiophene-1x1 · tetralin-2x1) · 최선 quinoline-2x3 d 3.04.
3. **다음 후보 예측** (18-3) L-5 → 라운드 1 선택 tetralin-1x1(점수 0.173) · benzene-1x3(0.159) 와 같은지.
4. **정지까지** (18-3) `cd ../loop && python scripts/loop_step.py --all` → 12회 · 최선 dibenzothiophene-2x6 d 1.97 · 정지(MD 12회 · 3라운드).
5. **모델 비교** (18-2 · 관측 12개 뒤) L-4 → `model_compare.json` (gp · rf · xgb).
6. **환류 · 대조** (18-4) L-7 · L-8 → 실행 노트 12 · 라운드 노트 4 · 기준 사례와 같음.
7. **선택 · 실행 모드** `loop.yaml` 의 `mode: live` 또는 `--mode live` (후보 1개 약 5분 · 4코어) · 후보 하나만 = L-3.

Claude Code 없이 터미널에서 직접(week18 폴더 · mdai):
```bash
cd ../loop && python scripts/lit_extract.py && python scripts/library.py
cd ../loop && python scripts/loop_step.py          # 라운드 0
cd ../loop && python scripts/loop_step.py --all    # 라운드 1 ~ 3 · 정지까지
cd ../loop && python scripts/surrogate.py compare  # 모델 3종 비교(관측 12)
```
처음부터 다시 하려면 `../loop/ws/avg_molecule_2target/` 와 `../loop/vault/runs` · `../loop/vault/rounds` 의 생성 파일을 지운다(Claude Code 에서는 지우기 전에 승인).

## 확인
- 표적: `lit_targets.json` 의 density.value 1.018 · mean 1.0208 · n 22(11편) · ced.value 354.2 · n 7 (용해도 시험 1 · MD 문헌 6) · 뺀 행 1(MD 밀도 0.947 · 「표적 아님」)
- 후보: 168행 = 핵 7 × 사슬 1 · 2 × 길이 1 ~ 12 · 열 11개(cand · core · n_chain · chain_len · smiles · n_atoms · MW · fa · HC · het · rot)
- 재생: 라운드별 후보 이름 · 순서 · 최선 거리(3.04 → 3.04 → 2.64 → 1.97)가 `../loop/expected_output/avg_molecule_2target/state.json` 과 같음 · 두 표적 안 0개
- 실행: 라운드 0 의 6개 = 같은 후보 · 밀도 차 ≤ 0.015 g/cm³ · CED 차 ≤ 15 MJ/m³
- 볼트: 실행 노트 12개 · 라운드 노트 4개 · 노트마다 근거 문헌 링크 15편 · `[[round_k]]` 링크

## 제출
`out/L-1_result.md` ~ `out/L-8_result.md`(L-3 은 실행 모드를 고른 경우) · 퀴즈 `quiz.md` 답 · 최종 프로젝트 제출 폴더(형식 = `../week16/docs/final_project.md` 「제출 폴더」 · 「W18 폐루프 결과 사용」 절 · 7파일 + slides · 평가 100점 = 문제 정의 20 · 계산 · 검증 설계 30 · 탐색 결과 25 · 재현성 15 · 한계 논의 10)

## 내 문제로 바꾸기 (최종 프로젝트 · 덱 24장)
- 강좌 스크립트는 고치지 않는다. 바꾸는 곳은 세 곳이다.
  1. 표적: `../loop/vault/papers/` 에 내 논문 노트(형식 = `../loop/vault/templates/논문노트.md` · `loop_role: target` · 「보고 물성」 표)
  2. 후보: `../loop/ws/<새 이름>/library.csv` (같은 열 이름 · 생성 스크립트는 `out/` 에 새로 · `../loop/scripts/library.py` 는 기준 코드)
  3. 설정: `../loop/config/loop.yaml` 을 `../loop/config/my.yaml` 로 복사 → `name` · `targets.*.tol` · `model` · `acquisition` · `batch` · `rounds` · `stop` 수정 → 명령마다 `--config config/my.yaml`
- 재생 모드는 `../loop/expected_output/<name>/` 이 있는 기준 사례 이름에서만 돈다 → 내 문제는 실행 모드(`mode: live`).
- 관측 12개 기준으로는 rf 의 1σ 포함 비율(0.58 · 0.75)이 68 % 에 가장 가깝다(L-4) · 모델을 바꾸면 `model` 이름만 바꾼다.

## 못 끝냈다면
`../loop/expected_output/avg_molecule_2target/` (재생 모드 기준 · 12회 실제 MD) 와 `_ehvi/`(같은 초기 6개 + EHVI) 로 덱 · 퀴즈 · 최종 프로젝트 기준선을 진행할 수 있다(`expected_output/README.md`).

## 숫자의 출처
- 표적 · 문헌: `../loop/expected_output/avg_molecule_2target/lit_targets.json` · `lit_values.csv`(30행) · `../loop/lit/library.bib`(15편) · `../loop/vault/papers/*.md`(15편) · δ → CED = δ² (19.15² = 366.7 · 17.96² = 322.6)
- 폭: `../loop/config/loop.yaml`(밀도 ±0.02 · CED ±20 · 사분위 약 1.01 ~ 1.04 주석) · 판정 폭(밀도 ±0.015 · CED ±15) = `../mdworkflow/README.md`
- 후보 · 기술자: `library.csv` (MW 92 ~ 521 · fa 0.18 ~ 0.93 · H/C 0.77 ~ 1.80 · het 0 ~ 0.10 · rot 0 ~ 0.73) · 계산 12개 = 168개의 약 7 % (12 ÷ 168 = 0.071)
- 라운드 · 예측 · 점수: `state.json` (picks 의 mu · sd · score · best_dist) · 실측: `loop_results.csv` · `md_results.csv` · `runs/*/props.json`
- 모델 비교: `model_compare.json` (n 12)
- EHVI 비교: `../loop/expected_output/avg_molecule_2target_ehvi/` (loop_results.csv · state.json) · 알킬벤젠 3개의 밀도 차를 폭으로 나눈 값 = (1.018 − 0.8796) ÷ 0.02 = 6.92 · (1.018 − 0.8649) ÷ 0.02 = 7.655
- 재생 모드 시간 약 2.5 s(기준 사례 12회 전체) · 실행 모드 후보 1개 약 5분(4코어 · `../mdworkflow/README.md` 표준 프로토콜 130 ps · 1,500 원자) · 12개 × 5분 = 약 1시간
- dibenzothiophene-2x6 두 번 계산: `../week17/expected_output/candidates/results.csv` (0.9817 · 386.4) ↔ 루프 r3_2 (0.9893 · 393.5) → 차 0.0076 · 7.1
- 힘장 CED 과대: `../mdworkflow/README.md` 힘장 검증(톨루엔 +6 % · n-데칸 +21 %) · 덱 23장의 나눗셈(393.5 ÷ 1.06 = 371.2 · 393.5 ÷ 1.21 = 325.2)은 같은 비율을 가정한 계산
- 체비셰프 거리 예: r3_2 = max(|0.9893 − 1.018| ÷ 0.02, |393.5 − 354.2| ÷ 20) = max(1.435, 1.965) = 1.965 (state.json best_dist · 덱 표기 1.97)
- 최종 프로젝트: `../week16/docs/final_project.md`
