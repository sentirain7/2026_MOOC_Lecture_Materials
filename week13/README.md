# week13 · 기계학습 기초: 분할 · 누수 · 지표 · 선형 → 트리 (모듈 M4 · 도구 주차)

| 항목 | 내용 |
|---|---|
| 덱 | `slides/W13_기계학습기초.html` (27장 · 54분 · 4차시 · v3) |
| 학습목표 | ① MD 결과 표에서 한 행 · 그룹 열 · 표적 · MD 반복 오차를 정의한다 ② 분할 4종(행 무작위 · 조건 그룹 · 노화 상태 빼기 · 온도 외삽)으로 같은 모델을 평가하고 누수를 진단한다 ③ RMSE · MAE · R² 를 시험 범위 · n · 반복 오차와 함께 보고한다 ④ 선형 · 트리 · 숲의 외삽 한계와 깊이에 따른 과적합을 확인한다 |
| 선수 지식 | W01 12장(Claude Code 실습 환경) · W09 `results.csv` 열 구조(밀도 · CED · 체적탄성률) |
| 소요 시간 | 강의 54분 + 실습 약 10분 (노트북 2개 · CPU) |
| 새 용어 (5) | 지도학습 · 분할 · 누수 · 과적합 · 결정계수 R² → `../GLOSSARY.md` |
| 도구 주차 | 새 물리 없음 · 다음 주차(W14 대리모델 · W15 불확실성 · W16 역설계 검증)가 쓰는 분할 · 지표 · 보고 형식만 |

## 만들어 보기 (덱 7 · 13 · 25장 · Claude Code 지시문 = `prompts.md`)
- **P13-1** 내 데이터의 행 · 그룹 · 표적 정의표 → `out/P13-1_result.md`
- **P13-2** split_compare ▶ → 분할 4종 표 · 보고 문장 → `out/P13-2_result.md`
- **P13-3** fit_linear_tree ▶ → 깊이 선택 · 근거 2줄 → `out/P13-3_result.md`

## 실습 순서 (Claude Code · 설치 · 조작 = `../docs/claude_code_quickstart.md`)
1. **열기** · 터미널 → `conda activate mdai` → `cd week13` → `claude` (scikit-learn 은 mdai 에 포함 · `../environment.yml`).
2. **실행** · 덱 7장 지시(P13-1) 또는 「`@notebooks/01_split_and_leak.ipynb` 를 실행하고 결과를 요약해」 → Claude Code 가 week13 폴더에서 `python ../run_nb.py notebooks/01_split_and_leak.ipynb` 실행(승인 · 출력이 노트북에 저장) · 셀 1(데이터 요약) → 셀 2(`split_compare.py` · 약 1분) → 셀 3(`SPLIT` 만 `'random'` ↔ `'loago'` · 직접 바꿔 보려면 `jupyter lab`).
3. **실행** · `notebooks/02_tree_depth.ipynb` 같은 방식 · 셀 1(`fit_linear_tree.py` · 깊이 곡선 그림) → 셀 2(`learning_curve.py`).
4. **확인** · 숲 RMSE random 0.0036 · cond 0.0062 · loago 0.0299 g/cm³ / 체적탄성률 최소 깊이 2 · Claude Code 가 `out/` 과 `expected_output/` 을 비교해 보고.
5. **제출** · `out/P13-1~3_result.md` (Claude Code 가 저장) · `out/split_compare.json` · `out/tree_depth.png`.
- `scripts/` 는 기준 코드 · 다른 깊이 · 모델을 시험할 때는 `out/` 아래 새 스크립트로 만들어 강좌 결과와 비교한다(`../CLAUDE.md`).
- (선택) Colab: 노트북 첫 셀이 저장소를 받아 `week13` 으로 이동한다.

스크립트만 한 번에 돌릴 때(터미널 · Claude Code 안에서는 앞에 `!`) week13 폴더에서:
```
python3 scripts/split_compare.py && python3 scripts/split_compare.py --target ced && python3 scripts/split_compare.py --target bulk_modulus
python3 scripts/fit_linear_tree.py && python3 scripts/learning_curve.py && python3 scripts/export_deck_data.py
```

## 스크립트
| 파일 | 하는 일 | 출력 |
|---|---|---|
| `common.py` | 데이터 읽기(기본 = AAA1 노화 3셀 336행) · 특징 6개 · 지표 | · |
| `export_dataset.py` | 강사용 · 플랫폼 DB 읽기 전용 → CSV | `data/bulk_md_373.csv` (이미 포함) |
| `split_compare.py` | 모델 4(선형 · 나무 깊이 4 · 나무 제한 없음 · 숲 200) × 분할 4 · 누수 비율 · 파리티 점 | `out/split_compare[_ced·_bulk_modulus].json` |
| `fit_linear_tree.py` | 깊이 1 ~ 12 · 조건 그룹 5겹 vs 무작위 KFold · 2특징 깊이 3 나무 | `out/tree_depth.json` · `out/tree2d.json` |
| `learning_curve.py` | 학습 조건 10 ~ 100 % · 선형 · 숲 | `out/learning_curve.json` |
| `export_deck_data.py` | 위 결과 + 온도 외삽 곡선 → 덱 주입용 한 벌 | `out/deck_data.json` |

## 숫자의 출처
- 데이터 = COMID 플랫폼 벌크 MD 실행(GAFF2 · NPT · `status = completed` 373건 · 2026-07 ~ 09 캠페인). DB 는 읽기 전용으로 한 번 내보냈고 실행 ID 는 순번으로 바꿨다 → `data/README.md`
- 덱 표기(2026-11-14 · 18주 과정): 이 데이터 = **참고 사례 데이터(연구 플랫폼 결과)** · 숫자 그대로. 같은 종류의 내 데이터(분자 · 물성 표)는 W17 · W18 에서 MD 워크플로우(`../mdworkflow/`)와 폐루프(`../loop/`)로 직접 만든다(`loop/ws/<이름>/db/loop_results.csv`).
- 덱의 모든 성능 수치 = 이 폴더의 스크립트를 2026-11-08 에 scikit-learn 1.9.1 (conda env mdai · CPU · seed 42) 로 실제 실행한 값 → `expected_output/`. 노트북을 다시 돌려도 같은 값이 나온다(확인함).
- 분할 = 평가 질문 · 그룹 조회 실패 시 무작위 대체 금지 · R² 와 시험 범위 · 두 층위 오차: 원본 10주차 보충A #6 · #7 · #10 · #11 · #13 · #15 ~ #19
- 원본의 XGBoost/GP 결과표(프로토콜 8종 · 홀드아웃 · 오프그리드 파리티 · δ 편차 · MD vs 문헌) = `docs/metrics_notes.md`. 불확실성 · 적용 영역(원본 10-S3 · 10-S4)은 W15.

## 기대 결과 (`expected_output/`)
| 파일 | 내용 |
|---|---|
| `split_compare.json` | 밀도 · 336행 · 숲 R² random 0.989 · cond 0.954 · loago 0.268 · t_extrap 0.930 / 선형 loago RMSE 0.0077 · R² 0.951 · MD 반복 SD 0.0027 |
| `split_compare_ced.json` · `split_compare_bulk_modulus.json` | 같은 표 · CED(MJ/m³) · 체적탄성률(GPa) |
| `tree_depth.json` | 최소 깊이: 밀도 8 · CED 6 · 체적탄성률 2(검증 0.611 → 깊이 12 0.625 · 학습 0.483 · 반복 SD 0.436) |
| `tree2d.json` | T_K · aging 2특징 · 깊이 3 · 잎 8 · 학습 RMSE 0.01207 · R² 0.88 |
| `learning_curve.json` | 숲 검증 0.0319(27) → 0.0062(268) · 선형 0.0108 → 0.0064 |
| `deck_data.json` | 덱 주입용 모음 |

## 못 끝냈다면
`expected_output/` 의 JSON 으로 P13-2 · P13-3 을 하고 W14 로 간다. W14 는 같은 표에 분자 표현자 열을 더하고, 오늘의 조건 그룹 · 노화 빼기 분할을 그대로 쓴다.
