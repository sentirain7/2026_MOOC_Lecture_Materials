# week14 · 표현자와 대리모델: RDKit 기술자 · XGBoost · SHAP · 특징 재정련 (모듈 M4 · 기계학습 1)

| 항목 | 내용 |
|---|---|
| 덱 | `slides/W14_표현자와대리모델.html` (v3 · 28장 · 4차시 · 14-1 표현자와 feature library 14.5분 · 14-2 XGBoost 대리모델 15분 · 14-3 SHAP 해석 12.5분 · 14-4 특징 재정련과 보고 12.5분) |
| 학습목표 | ① SMILES 에서 측정 가능한 분자 기술자 10종을 RDKit 으로 계산하고 개수 가중 평균으로 바인더 특징을 만든다 ② core672 MD 표를 정제해 그룹 5-fold 로 XGBoost 를 학습하고 Ridge 기준선과 비교한다 ③ 무작위 분할과 그룹 분할의 차이를 누수로 설명한다 ④ SHAP 가법성 · 순위 · 부분의존도로 예측을 해석하고 물리 방향과 대조한다 ⑤ 기여 · 상관 · 상위 k 규칙으로 특징을 17 → 6 으로 줄이고 성능 유지를 확인한다 |
| 선수 지식 | W11 13분자 SMILES · Li & Greenfield 조성 · W13 분할 · 지표 · W09 물성(밀도 · CED · 체적탄성률 · E_inter) |
| 소요 시간 | 강의 54.5분 + 실습 25분(실행: `train_xgb.py` 단독 119 s · `run_all.py --fast` 87 s · 1코어) |
| 새 용어 (5) | 표현자(descriptor) · 조성 가중 평균(count-weighted mean) · 그룹 분할(group k-fold) · 그래디언트 부스팅(gradient boosting) · SHAP → `../GLOSSARY.md` |

## Claude Code 지시문 (덱 「만들어 보기」 장)
`prompts.md` · P14-1 기술자 표 · 내 분자 1행(8장) · P14-2 성능표 · 기준선 · 누수 한 문장(15장) · P14-3 SHAP 표 · 상관 쌍 선택 · 해석 문단(21장). 결과 = `out/P14-n_result.md` (Claude Code 가 저장). 사용 환경 = `../docs/claude_code_quickstart.md` · `../docs/prompt_setup.md`.

## 실습 순서 (Claude Code)
1. **환경** 터미널 → `conda activate mdai` → `cd week14` → `claude` · RDKit · XGBoost · SHAP · scikit-learn · pandas 는 mdai 에 포함(`../environment.yml` · 따로 설치 없음 · 없으면 Claude Code 가 설치를 제안 → 승인) (검증 버전: RDKit 2026.09.2 · XGBoost 3.2.0 · SHAP 0.51.0 · scikit-learn 1.9.1 · pandas 3.1.1) · (선택) Colab 이면 노트북 첫 셀의 `pip install` 주석을 푼다
2. **01** 덱 지시(P14-1 · P14-2) 또는 「`@notebooks/01_features_xgb.ipynb` 를 실행하고 결과를 요약해」 → Claude Code 가 week14 폴더에서 `python ../run_nb.py notebooks/01_features_xgb.ipynb` 실행(승인 · 출력이 노트북에 저장) · 기술자(32분자) → 바인더 9행 → 학습 표 672행 → XGBoost 4표적 · 특징 세트 3 · Ridge · 무작위 ↔ 그룹 · 격자 60회
3. **02** 같은 방식으로 `notebooks/02_shap_refine.ipynb` · TreeSHAP 4표적 · 워터폴 5행 · 부분의존도 2개 · 재정련 R0 → R3
4. 한 번에(터미널 · Claude Code 안에서는 앞에 `!`): `python3 scripts/run_all.py` (격자 생략 = `--fast` · 87 s · 이전 `hparam_grid.json` 이 있으면 그 값을 재사용)
5. **확인** (Claude Code 가 `out/` 과 `expected_output/` 을 비교해 보고) `out/features_log.json` 의 rows 672 · groups 54 · `out/train_metrics.json` 의 밀도 T+binder+additive R² 0.975 · `out/refine_rounds.json` 의 final 6개
6. **제출** `features.csv` · `train_metrics.json` · `shap_summary.json` · `refine_rounds.json` · P14-1~3 결과
7. **바꿔 보기** `scripts/common.py` 의 `PARAMS`(깊이 · η · 나무 수) · `refine_features.py` 의 상위 k(6 → 4) → `scripts/` 는 고치지 않고 Claude Code 가 `out/` 아래 변형 스크립트를 만들어 돌린 뒤 결과를 다른 이름으로 저장해 강좌 결과와 비교 · `data/sara_molecules.csv` 끝에 내 분자 SMILES 1행(P14-1)

패키지가 없으면: `expected_output/` 의 같은 이름 파일로 W15 진행(W15 기준선 = `train_metrics.json` 의 4표적 값 · 덱 26장).

## 스크립트
| 파일 | 역할 |
|---|---|
| `scripts/descriptors.py` | `data/sara_molecules.csv`(13분자 × 노화 변이 = 32분자) → RDKit 기술자 14열 · MMFF 3D(seed 7) Rg · 종횡비(PMI₃/PMI₁) · ECFP4 1024 비트 → `out/mol_descriptors.csv` · `mol_fingerprints.json` |
| `scripts/binder_features.py` | Li & Greenfield 2014 개수(`binder_compositions_LG2014.json`)로 개수 가중 평균 → 바인더 9행 · core672 정제(CED < 0 · K > 10 GPa) · 노화 라벨 복구 · 첨가제 특성 6열 결합 → `out/features.csv` · `features_log.json` |
| `scripts/common.py` | 특징 세트(T · BINDER 10 · ADD 6) · 한국어 이름표 · XGBoost 파라미터 · 그룹 5-fold `cv()`(학습 폴드 μ · σ 표준화) |
| `scripts/train_xgb.py` | 4표적 × 특징 세트 3 + Ridge · 무작위 seed 3개 ↔ 그룹 · 부스팅 라운드 시연(AAA1 무첨가 94행 · 깊이 1 · η 0.3) · 격자 60회 → `train_metrics.json` · `boosting_rounds.json` · `hparam_grid.json` · `oof_density.csv` |
| `scripts/shap_report.py` | 전체 데이터 학습 → TreeSHAP mean \|SHAP\| · 방향(Spearman 부호) · 워터폴 5행 · 부분의존도(온도 · 첨가제 밀도 45점) → `shap_summary.json` · `shap_waterfall.json` · `shap_values_density.csv` · `pdp_density.json` |
| `scripts/refine_features.py` | R1 기여 < 최대의 1 % 제거 · R2 \|r\| > 0.95 쌍에서 기여 작은 쪽 제거 · R3 상위 6 유지 → 라운드마다 그룹 5-fold 재평가 → `refine_rounds.json` |
| `scripts/export_deck_data.py` | 위 결과를 `out/deck_data.json` 으로 묶고 덱의 `W14` 데이터 블록을 교체(덱 갱신 전용 · `../week11/out/mol2d.json` 이나 격자 결과가 없으면 건너뜀) |
| `scripts/run_all.py` | 위 6개를 순서대로 실행 |

## 데이터
| 파일 | 내용 · 출처 |
|---|---|
| `data/comid_core672_dataset.csv` | COMID MD 672행(바인더 3 × 첨가제 6 × 노화 3 × 온도 12 · 밀도 · CED · 체적탄성률 · E_inter) |
| `data/sara_molecules.csv` | W11 13분자 SMILES + 노화 변이(산소 추가) |
| `data/binder_compositions_LG2014.json` | Li & Greenfield (2014) 표 1 분자 개수 counts_X1 · AAA1 72 · AAK1 60 · AAM1 90 |
| `data/aging_recovered.csv` | CNT · SBS 행의 노화 라벨 복구(COMID final_feature_dataset material_id) · 614행 |
| `data/additive_properties.csv` | 첨가제 6종 밀도 · 무기 · 고분자 · 종횡비 · 강성 · 나노 · 문헌 대표값(원본 09주차 #9 · #13) |

## 실행 결과 (이 저장소에서 측정 · mdai · 1코어 · 2026-11-08 · 같은 seed 로 다시 돌려 모든 결과 파일 일치 확인)
그룹 5-fold R² (54그룹 · 폴드 밖 예측 합산)

| 표적 | n | 온도만 | + 바인더 | + 첨가제 (17) | Ridge (17) | RMSE (17) |
|---|---|---|---|---|---|---|
| 밀도 | 670 | 0.583 | 0.876 | **0.975** | 0.967 | 0.0078 g/cm³ |
| CED | 613 | 0.603 | 0.788 | **0.979** | 0.940 | 5.92 MJ/m³ |
| 체적탄성률 | 576 | 0.800 | 0.769 | 0.727 | **0.822** | 0.52 GPa |
| E_inter | 576 | 0.420 | 0.737 | 0.849 | **0.879** | 94.9 kcal/mol |

- 정제: CED 음수 48행 · 체적탄성률 > 10 GPa 50행 제거 · 중복 47행 · 그룹 54(원본 09주차 42 → 노화 라벨 복구)
- 무작위 5-fold seed 0 · 1 · 2 = 0.9892 · 0.9878 · 0.9892 ↔ 그룹 0.9752 (밀도 · 17특징)
- 부스팅 시연 학습 RMSE: 나무 0 → 10 → 100 = 0.0466 → 0.0150 → 0.0055 g/cm³
- 격자 60회(나무 50 ~ 800 × 깊이 2 · 3 · 4 · 6 × η 0.03 · 0.1 · 0.3): 최고 800 · 2 · 0.03 → 0.9858 · 최저 50 · 2 · 0.03 → 0.729
- SHAP 1순위 = 4표적 모두 온도. 밀도 기준값 1.0108 · 온도 0.0333(−) · logP 0.0152(−) · O 분율 0.0075(+) · 첨가제 밀도 0.0072(+). 워터폴 5행 |예측 − MD| ≤ 0.0012
- 부분의존도 변화폭: 온도 0.115 g/cm³(COMID 0.1154 와 일치) · 첨가제 밀도 0.030
- 재정련: R0 17 → R1 12 → R2 9 → R3 6 · 밀도 0.9752 → 0.9764 · CED 0.9792 → 0.9770 · 최종 6 = 온도 · logP · 첨가제 고분자 · 첨가제 밀도 · 바인더 방향족 분율 · 첨가제 종횡비

## W18 폐루프와의 연결 (2026-11-14 · 18주 과정)
- 이번 주 데이터(`data/comid_core672_dataset.csv`) = **참고 사례 데이터(연구 플랫폼 결과)** · 숫자 그대로. 같은 종류의 내 데이터는 W17 · W18 에서 MD 워크플로우(`../mdworkflow/`)로 직접 만든다.
- 폐루프의 대리모델은 학습자가 고른다(덱 26장 아래 카드 · 지시문 L-4 · `../loop/prompts.md`): 조건 = 예측과 함께 불확실성 σ 를 내는 모델 · 후보 = GP(W15) · 랜덤 포레스트(W13) · XGBoost 앙상블(이번 주 · 시드만 바꾼 여러 모델의 예측 흩어짐 = σ).
- 비교: `python scripts/surrogate.py compare`(`../loop/` 에서) · 단일 제외 교차검증(leave-one-out) RMSE 와 1σ 포함 비율(|오차| ≤ σ 인 비율) · 결과 = `loop/ws/<이름>/model_compare.json` · 설정 `config/loop.yaml` 의 `model`. 루프의 숫자는 W18 에서 본다.

## 숫자의 출처 · 주의
- 덱 수치는 모두 위 실행값(`out/deck_data.json` → 덱 데이터 블록). 원본 09주차의 COMID 보고서 수치(LightGBM · RF · 42그룹)는 `docs/model_notes.md` 에 원문 보존 · 차이 설명 §0
- 체적탄성률 · E_inter 는 Ridge 가 XGBoost 를 앞선다 → W15 기준선은 표적마다 이긴 모델(덱 26장)
- CED – 첨가제 고분자 방향(−)은 첨가제가 SBS · 리그닌 2종뿐이고 특성이 문헌값이라 「확인 필요」(덱 20장)
- R2 가 O 분율 대신 logP 를 남겼다 · logP 는 계산값이므로 측정 가능성 기준으로 사람이 O 분율로 되돌려 다시 잴 것(덱 25장 · P14-3 ②)
- 원본 부록 수퍼그래프 사례 5장 = `docs/case_supergraph.md` · 덱 27장 요약
- 점도(58행 · 3그룹)는 그룹 5-fold 가 성립하지 않아 표적에서 뺐다(`docs/model_notes.md` §17)
