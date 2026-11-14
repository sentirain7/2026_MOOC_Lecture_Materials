# week15 · 신경망 · 그래프 · 불확실성 (모듈 M4 · 도구 주차)

| 항목 | 내용 |
|---|---|
| 덱 | `slides/W15_신경망그래프불확실성.html` (27장 · 55분 · 4차시 · v3) |
| 학습목표 | ① 분자를 노드 · 엣지 특징 그래프로 바꾸고 메시지 패싱 층 수와 도달 범위를 연결한다 ② 스칼라 물성은 불변 설계로 충분함을 회전 대칭으로 판단한다 ③ GP 의 μ · σ 를 얻고 보정 곡선으로 σ 를 확인한다 ④ 획득함수 · κ 를 탐색 단계에 맞게 고르고 적용 영역 판정을 붙인다 |
| 선수 지식 | W13 학습 · 검증 분할 · 누수 · W14 표현자 · 트리 대리모델(이름만) · W09 밀도 · CED |
| 소요 시간 | 강의 55분 + 실습 25분 |
| 새 용어 (5) | 메시지 패싱 · 등변성 · 가우스 과정 · 보정 · 획득함수 → `../GLOSSARY.md` |
| 도구 주차 | 새 물리 없음 · W16 자율 탐색 루프에서 쓰는 모델 계열 · 불확실성 · 다음 계산 대상 선정만 |
| 환경 | numpy · scipy · scikit-learn · RDKit (torch · GPU 불필요 · 학습 없이 순전파와 GP 만) |

## 만들어 보기 (덱 9 · 21 · 26장 · `prompts.md`)
- **P15-1** 내 분자 그래프 → 3층 순전파 → 도달 원자 수 해석 → `out/P15-1_result.md`
- **P15-2** calibration.json → 물성별 보정 판정 · σ 배율 s → `out/P15-2_result.md`
- **P15-3** 획득함수 5종 비교 → 내 단계의 κ 선택 · 근거 → `out/P15-3_result.md`

## 실습 순서 (기본 = 내 컴퓨터 · mdai · Claude Code · `../docs/claude_code_quickstart.md`)
1. **열기** · 터미널 → `conda activate mdai` → `cd 2026_MOOC_Lecture_Materials/week15` → `claude` (저장소 `CLAUDE.md` 의 강좌 규칙을 자동으로 읽음).
2. **실행** · 덱의 Claude Code 지시 P15-1 ~ P15-3(`prompts.md`)을 붙여 넣고 [ ] 안만 바꾼다 → Claude Code 가 아래 스크립트를 실행 · 승인 창에서 명령 확인 후 승인. 노트북 `notebooks/01_graph_mpnn.ipynb` · `02_gp_calibration_acquisition.ipynb` 은 같은 순서 + 그림. 전체 약 30초(CPU).
3. **확인** · `out/mpnn_forward.json` 의 `readout_y` = `readout_y_permuted` · `out/calibration.json` 적합 GP 68 % → 0.75 · 95 % → 0.943 · `out/acquisition.json` UCB κ 2 의 x* 0.29 → 0.71 → 0.67 → 0.77 → 0.72.
4. **제출** · 위 세 JSON + P15-1 ~ 3 결과.
5. **바꿔 보기** · `mol_graph.py --smiles` 에 내 분자 · `acquisition.py --kappa 0 / 3` · 덱 19장 슬라이더.

직접 실행할 때는 week15 폴더에서(Claude Code 안에서는 명령 앞에 `!`):
```
python3 scripts/mol_graph.py && python3 scripts/mpnn_forward.py
python3 scripts/gp_demo.py && python3 scripts/calibration.py && python3 scripts/acquisition.py
python3 scripts/export_deck_data.py          # 덱용 데이터(선택)
```
선택 경로: Claude Code 를 쓸 수 없으면 노트북 첫 셀(Colab 에서 저장소 받기)과 `../docs/colab_quickstart.md` · 채팅형 지시 사용법 `../docs/prompt_setup.md` §5.
노트북 전체 실행(출력이 노트북에 저장 · 그림 확인용): week15 폴더에서 `python ../run_nb.py notebooks/01_graph_mpnn.ipynb notebooks/02_gp_calibration_acquisition.ipynb` · Claude Code 에는 「`@notebooks/…ipynb` 를 실행하고 결과를 요약해」. `jupyter nbconvert --execute` 는 notebooks/ 에서 실행되어 경로가 어긋나므로 쓰지 않는다. 노트북 첫 셀(저장소 받기 · pip 설치)은 Colab 용 · 로컬 mdai 에는 패키지가 이미 있음.

## 숫자의 출처
- 그래프 · 메시지 패싱 · GP · 보정 · 획득함수 수치 = 이 폴더의 스크립트를 2026-11-08 에 conda env mdai(numpy 2.4 · scikit-learn 1.9 · RDKit 2026.09)으로 실제 실행한 값 → `expected_output/`
- GP · 보정 · 획득함수 예제의 함수는 **가정 함수**(`scripts/common_gp.py` · 봉우리 2개 · 실측 아님 · 원본 10주차 보충A #22 「가정 예시」와 같은 성격)
- COMID 실측: 커버리지 4물성(밀도 68 → 62 · 95 → 88 % 등)과 LOGO R² = `claude_science_export/comid_reliability.md` §1 · §2 → `data/comid_coverage.csv` · RMSE 0.0078 · 0.0085 · 0.0109 · 행 수 5,346 · 165 · Graphormer-3D 4층 · 4헤드 · 엣지 특징 6 = 원본 10주차 #13 ~ #20 · 콜드스타트 라벨 12 · 시드 8 = COMID `contracts/policies/inverse_pipeline.py`(원본 보충B #10)
- σ 배율 s = COMID 커버리지 두 점에 정규 가정 포함률 2Φ(r · z_p) − 1 을 맞춘 r 의 역수(`calibration.py`)

## 기대 결과 (`expected_output/`)
| 파일 | 내용 |
|---|---|
| `graph_toluene.json` · `graph_summary.csv` | 톨루엔 노드 7 · 엣지 7 · 특징 11 + 3 · SARA 12분자 + 톨루엔 노드 20 ~ 67 · 엣지 24 ~ 77 |
| `mpnn_forward.json` | 은닉 4 · 2층 · y −0.4244 · 섞은 입력 동일 · 노드 0 도달 L1 2 · L2 4 · L3 6 · L4 7 |
| `gp_demo.json` | 점 2 → 6 · σ 평균 0.423 → 0.114 · 2D 적용 영역 d 0.12 안 |오차| 0.048 · 밖 0.173 |
| `calibration.json` | 적합 GP 68 → 0.75 · 95 → 0.943 · 잡음 과소 0.47 · 0.773 · COMID r · s |
| `acquisition.json` | UCB κ 2 · κ 0 · κ 0.1 · EI · 최대 분산 5라운드 · 찾은 최고 참값 0.983 ↔ 0.607 |
| `w15_deck_data.js` | 덱이 읽는 데이터(위 JSON 요약) |

## W18 폐루프와의 연결 (2026-11-14 · 18주 과정)
- 덱 표기: 연구 플랫폼의 커버리지 · LOGO R² · GP 설정 · 콜드스타트 정책 · 기본 κ 0.1 = **참고 사례(연구 플랫폼 결과)** · 숫자 그대로.
- 이번 주 획득함수는 W18 폐루프(`../loop/`)에서 실제로 돈다: 대리모델의 μ · σ → 두 표적(밀도 · CED)에 동시에 가까워질 기대 초부피 개선(EHVI · `../loop/scripts/acquire.py`) → 다음 후보 2개 → MD 워크플로우(`../mdworkflow/`)로 계산 → 결과 환류. Claude Code 지시문 L-5(`../loop/prompts.md`) · 덱 22장 「강좌 안의 위치」.

## 보충 문서
- `docs/gnn_notes.md` · 덱에서 뺀 내용: 결정 그래프 엣지 규칙 · 등변 GNN 식 · Graphormer-3D 어텐션 식 · 학습 루프 코드 · 불확실성 추정 3종 · 오차 합성 사슬 · 외삽 사례 · κ 선택 표 · 콜드스타트
