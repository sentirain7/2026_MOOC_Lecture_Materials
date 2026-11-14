# week16 · 자율 탐색 파이프라인과 검증: 큐레이션 · 파레토 · EHVI · 에이전트 · MD ↔ 실측 · 최종 프로젝트 (모듈 M5 · 다음 = W17 MD 워크플로우 조립 · W18 폐루프 통합)

| 항목 | 내용 |
|---|---|
| 덱 | `slides/W16_자율탐색파이프라인과검증.html` (v3 · 27장 · 55.0분 · 4차시 · 16-1 큐레이션 / 16-2 다목적 최적화 / 16-3 에이전트 · 자동 루프 / 16-4 검증 · 최종 프로젝트) |
| 학습목표 | ① 역설계 문제를 4칸(설계 변수 · 목표 · 제약 · 방향)으로 적고, MD 결과 표를 지우지 않고 큐레이션한다(672 → 612 · 이유 기록) ② 파레토 전선 · 초부피(HV)로 두 목표의 교환 관계를 보고, EHVI 로 다음 계산 3개를 골라 무작위와 비교한다 ③ 에이전트 루프의 역할 분리 · 사람 승인 · 정지 규칙 3종을 내 프로젝트 숫자로 적는다 ④ MD 를 실측과 대조할 때 크기와 부호(밀도) · 방향(Tg) · 시간축(강성)을 구분하고, 최종 프로젝트 폴더를 점검한다 |
| 선수 지식 | W05 오차 · W09 물성 표 · W13 ~ W15 대리모델 · 불확실성 · 획득함수 |
| 소요 시간 | 강의 50분(+ 확인 5분) + 실습 25분(CPU · 체인 전체 약 30초) |
| 새 용어 (5) | 파레토 전선(Pareto front) · 초부피(hypervolume · HV) · EHVI(expected hypervolume improvement) · 사용성 게이트(desirability gate) · 삼각 대조(triangulation) → `docs/glossary_w16.md` |

## Claude Code 지시 (덱 「만들어 보기」 장)
`prompts.md` · P16-1 curation.json → 단계표 · 큐레이션 보고(7장) · P16-2 ehvi.json → 추천 3건 보고서(14장) · P16-3 checklist.json → 보완 목록 · 발표 10장 계획(24장). 결과 = `out/P16-n_result.md`. 사용 환경 = `../docs/prompt_setup.md`.

## 실습 순서 (기본 = 내 컴퓨터 · mdai · Claude Code · `../docs/claude_code_quickstart.md`)
0. **시작** 터미널 → `conda activate mdai` → `cd 2026_MOOC_Lecture_Materials/week16` → `claude` · 덱 지시 P16-1 ~ P16-3 을 붙여 넣으면 Claude Code 가 아래 스크립트를 실행 · 승인 창에서 명령 확인 후 승인
1. **01** `notebooks/01_curate_pareto.ipynb` · curate → pareto → ehvi_select (`out/curation.json` · `pareto.json` · `ehvi.json`)
2. **02** `notebooks/02_validate_submit.ipynb` · md_vs_exp → final_project_check (`out/md_vs_exp.json` · `checklist.json`)
3. **제출** `out/my_project/`(형식 = `docs/final_project.md`) · P16-1 ~ P16-3 결과 · 내 파이프라인을 Claude Code 로 돌리는 방법(프로젝트 규칙 `CLAUDE.md` · `claude -p` 한 번 실행 · 승인 지점) = `docs/final_project.md` 「Claude Code 로 내 파이프라인 돌리기」
4. **바꿔 보기** `pareto.py --ref 3.0,350`(덱 9장) · `ehvi_select.py --obs 300 --batch 5` · 덱 12장 가중치 슬라이더(같은 612점)

직접 실행할 때는 week16 폴더에서(mdai · Claude Code 안에서는 명령 앞에 `!`):
```bash
python3 scripts/curate.py data/core672.csv --fixed data/features614.csv --out out/curation.json --csv out/curated612.csv
python3 scripts/pareto.py out/curated612.csv --ref 1.0,250 --out out/pareto.json
python3 scripts/ehvi_select.py data/features614.csv out/curated612.csv --obs 400 --batch 3 --out out/ehvi.json
python3 scripts/md_vs_exp.py data/density_match28.csv data/tg_pairs8.csv --delta data/an116_exp_unified.json --out out/md_vs_exp.json
python3 scripts/final_project_check.py out/my_project --out out/checklist.json
python3 scripts/export_deck_data.py out --out out/w16_deck_data.json   # 덱이 읽는 묶음(새 값 없음)
```
선택 경로: Claude Code 를 쓸 수 없으면 노트북 첫 셀(Colab 에서 저장소 받기)과 `../docs/colab_quickstart.md` · 채팅형 지시 사용법 `../docs/prompt_setup.md` §5.
노트북 전체 실행(출력이 노트북에 저장 · 그림 확인용): week16 폴더에서 `python ../run_nb.py notebooks/01_curate_pareto.ipynb notebooks/02_validate_submit.ipynb` · Claude Code 에는 「`@notebooks/…ipynb` 를 실행하고 결과를 요약해」. `jupyter nbconvert --execute` 는 notebooks/ 에서 실행되어 경로가 어긋나므로 쓰지 않는다. 노트북 첫 셀(저장소 받기 · pip 설치)은 Colab 용 · 로컬 mdai 에는 패키지가 이미 있음.

## 스크립트
| 파일 | 역할 | 산출 |
|---|---|---|
| `scripts/curate.py` | 코어 672행 → 물리 게이트(0.1~50 GPa · CED ≥ 0 · 표시만) → 점도(전단) 런의 K · CED 제외 → 노화 라벨 복원 · K 재백필 수 대조(COMID 정리 스냅샷과 비교 · 재계산 안 함) → 중복 조건 → 두 목표 완비 | `curation.json` · `curated612.csv` |
| `scripts/pareto.py` | 두 목표 최대화 전선 · HV(참조점 1.0 GPa · 250 MJ/m³) · 참조점 (3, 350) HV · 고정 난수 7 순서로 하나씩 넣은 회차별 HV | `pareto.json` |
| `scripts/ehvi_select.py` | 관측 400 / 후보 212 · 목표별 GP(상수 × RBF ARD 12 + 백색 잡음) · 몬테카를로 EHVI 512 · 가상 관측 배치 3 · 실제값 공개 · 무작위 3개 200회 비교 | `ehvi.json` |
| `scripts/md_vs_exp.py` | 밀도 짝 28점(크기 · 부호 · 온도별) · Tg 실험–MD 8쌍(방향) · 마스터커브 Δ | `md_vs_exp.json` |
| `scripts/final_project_check.py` | 제출 폴더의 파일 · 필드 → 평가 5항목 요건 체크리스트 | `checklist.json` |
| `scripts/export_deck_data.py` | 위 JSON 5개 → 덱 데이터 1개 | `w16_deck_data.json` |

## 이번 주 실행값 (`expected_output/` · 2026-11-08 · mdai Python 3.11 · scikit-learn · 재실행 일치 확인)
| 단계 | 값 |
|---|---|
| 큐레이션 | 672 → 표시 56(K > 50 GPa 50 · CED < 0 48) → 점도 런 58 제외 614 → 노화 재라벨 182 · K 재백필 36 → 중복 0 → 완비 612(결측 2) |
| 파레토 | 612점 · 전선 6점 · HV 871.28 · 참조점 (3, 350) HV 180.97 |
| EHVI | GP 홀드아웃 RMSE K 0.415 GPa · CED 6.4 · HV 865.06 → 871.28(+6.22) · 무작위 3개 평균 +0.09 · 무작위 ≥ EHVI 1.5 % · 추천 3건 모두 SiO₂ |
| 대조 | 밀도 28점 중앙 |상대오차| 2.33 % · MAE 0.033 g/cm³ · 26점 MD 낮음 · Tg 차이 11.1 ~ 65.5 K · Δ 4.72 ± 0.39 decade |
| 점검 | 예시 폴더 요건 100 / 100 · 슬라이드 0장(✗ · 형식 요건) |

GP 학습 때 sklearn ConvergenceWarning(길이척도 상한) 5건이 나온다 · 해당 특징이 거의 쓰이지 않는다는 뜻이며 `example_project/limits.md` 의 한계 1로 기록했다.

## W17 · W18 과의 연결 (2026-11-14 · 18주 과정)
- 덱 표기: 이번 주 데이터(612건 · 672행)와 연구 플랫폼 문서 · 정책 출처 = **참고 사례 데이터 · 참고 사례(연구 플랫폼 결과)** · 숫자 그대로.
- 이번 주 EHVI 는 이미 계산된 값 안에서 고르고 실제값을 공개한다(덱 11장). **추천 → MD 재검증**은 W18 폐루프(`../loop/`)에서 MD 워크플로우(`../mdworkflow/`)로 실제로 돈다(덱 8장 · 27장).
- 덱 22장 오른쪽 아래 = 강좌 MD 워크플로우의 힘장 점검(톨루엔 · n-데칸 MD ↔ NIST: 밀도 +1 % 안 · CED 방향족 +6 % · 포화 +21 % · 출처 `../mdworkflow/README.md`). 연구 플랫폼 MD 는 밀도를 낮게, 강좌 GAFF2 단분자 액체는 높게 낸다 → 치우침의 부호는 계와 힘장마다 따로 확인.
- 최종 프로젝트는 W18 폐루프 결과(`loop_results.csv` · `state.json` · 볼트 노트)를 쓴다 → `docs/final_project.md` 「W18 폐루프 결과 사용」.

## 숫자의 출처
- MD 계산값: COMID `comid_core672_dataset.csv`(672행) · `final_feature_dataset`(614행 · 재라벨 · 재백필 완료 스냅샷) · 함량확장 재실행 전 값.
- 측정값: 밀도 실측 28점 = 문헌 12편(원본 13주차 #25) · Tg 8쌍 = jclepro.2023.139092(같은 논문의 DSC · MD · 문헌값) · Δ = COMID AN116(S64-22 DSR · BBR ↔ AAA-1 G(t) 387점).
- 원본 덱 인용값(새로 계산하지 않음): 운영 실적 3,800건 · GPU 6 · 동시 36 · 6차원 가중치(13주차 #14 · #15) · 세 처방 · 밀도 창 0.93~1.10(13주차 #20 · #21) · 정지 규칙 5 · 60 · SE × 1.0 · 2회(10주차 보충B #25) · 평가 배점 · 발표 10장(13주차 보충A #23 · #24).
- 덱에 싣지 못한 원본 장(플랫폼 운영 · 스키마 · 비용 인지 · 레올로지 상세 · 특징 재정련 등 45장) = `docs/original_preserved.md`(매핑 112행 대응표 + 원문).
- 덱에서 옮긴 식 · 설계 세부(EHVI 기대값 식 · 가중합 점수 · 운영 구조 가중치) = `docs/pipeline_notes.md`(2026-11-14 · 규칙 16).
- 예시 제출 폴더 `expected_output/example_project/` = 이번 주 실행 결과를 제출 형식으로 옮긴 견본(새 값 없음).
