# week18 expected_output · 기준 결과 = `../../loop/expected_output/` (복사하지 않음)

W18 의 기준 결과는 폐루프 폴더에 한 벌만 둔다. 재생 모드(`../../loop/scripts/loop_step.py`)가 그 파일을 직접 읽기 때문이다. 이 폴더에는 안내만 둔다.

## `../../loop/expected_output/avg_molecule_2target/` · 체비셰프 EI 기준 사례 (덱 W18 의 모든 루프 수치)
조건: 2026-11-14 · mdai · MD 워크플로우 표준 프로토콜 130 ps · 약 1,500 원자 단분자 상자 · 4코어 · 대리모델 gp(RBF 길이 하나) · 획득함수 cheb · 배치 2 · 3라운드 · 초기 6 · seed 7 · 실제 MD 12회(mode 열 = live)

| 파일 · 폴더 | 내용 | 덱 |
|---|---|---|
| `lit_values.csv` | 논문 노트 15편 → 값 30행(밀도 23 · CED 7) · `used_for_target` · 뺀 행 1(MD 밀도 0.947) | 5 · 6 · 13 |
| `lit_targets.json` | 밀도 1.018 (mean 1.0208 · n 22 · 11편) · CED 354.2 (mean 348.3549 · n 7 · 4편) · values · citekeys | 2 · 6 · 13 |
| `library.csv` | 후보 168 · 열 11개 · 원자 15 ~ 96 · 분자량 92 ~ 521 | 10 · 11 · 13 |
| `loop_results.csv` | 12행(id · round · cand · smiles · n_mol · n_atoms · 밀도 ± · CED ± · ok · wall_s · mode) | 16 · 17 · 19 · 23 |
| `state.json` | 라운드 0 ~ 3 · 고른 후보 · picks(score · mu · sd) · best · best_dist 3.04 → 3.04 → 2.64 → 1.965 · done | 15 · 16 · 20 |
| `model_compare.json` | 관측 12 · 단일 제외 교차검증 · gp · rf · xgb 의 밀도 · CED RMSE · 1σ 포함 비율 | 12 |
| `md_results.csv` | MD 워크플로우 결과 표 형식(store.py 열) · δ · seed 4928460 · 힘장 gaff2/am1-bcc | 23 |
| `runs/r*_*/` | 계산별 `cell.json` · `status.json` · `props.json` (궤적 · 로그는 용량 때문에 제외) | 7 · 19 |
| `vault/runs/` · `vault/rounds/` | 실행 노트 12 · 라운드 노트 4 (재생 · 실행 때 `../../loop/vault/` 에 같은 노트가 생김) | 22 · 25 |

## `../../loop/expected_output/avg_molecule_2target_ehvi/` · 같은 초기 6개 + EHVI (덱 18장)
`loop_results.csv` · `state.json`: 라운드 1 ~ 3 선택 = benzothiophene-1x4 · benzene-2x1 / benzene-1x1 · benzene-1x2 / naphthalene-2x2 · naphthalene-2x9(ok False) · 최선 d 3.04 유지. 비교용 읽기 자료다(지금 코드로 재생하면 라운드 1 의 두 번째 후보부터 달라짐 · 재생 재현 대상 아님).

## 내 결과와 비교하는 법
- 재생 모드: 라운드별 후보 이름 · 순서 · 값이 기준과 모두 같아야 한다(다르면 설정 · 버전 · 앞 라운드 결과를 확인 · `loop_step.py` 가 「기준 표와 다름」으로 멈춤). 기준 사례 12회 전체 약 2.5 s.
- 실행 모드: 라운드 0 의 6개 = 같은 후보 · 밀도 차 ≤ 0.015 g/cm³ · CED 차 ≤ 15 MJ/m³ 이면 같은 결과(`../../mdworkflow/README.md` 반복 흔들림의 약 1.5배). 그 뒤 경로는 MD 값 차이로 갈라질 수 있다. 후보 1개 약 5분(4코어).
- 같은 후보를 두 번 계산한 예: dibenzothiophene-2x6 = W17 후보 시험 0.9817 · 386.4 (`../../week17/expected_output/candidates/`) ↔ 루프 r3_2 0.9893 · 393.5 → 차 0.0076 · 7.1 → 같은 결과.
