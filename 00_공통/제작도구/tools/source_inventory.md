# 보충 자료 원천 목록 (LAMMPS_Asphalt)

2026-09-22에 조사했다(읽기 전용, DB는 열지 않음). 경로는 모두 `/home/tyun/mounted_directory/sdd/Claude_Code/LAMMPS_Asphalt/` 기준이다. 5단계(내용 보완)에서 새 예시·그림을 만들기 전에 이 목록부터 본다. 가져다 쓴 그림은 `assets/`로 복사하고 발표자 노트에 출처 경로를 적는다.

## 구조 메모
- e55·e61·e63·e64·e65는 층상 인장 캠페인의 **사고·복구 번호**다. 결과 캠페인 이름이 아니다. tr1~tr5는 변형률 속도 트랙이다.
- 논문 폴더는 `docs/papers/paper{N}_*/`(목록은 `docs/papers/README.md`)에 있다. 역설계 ML 논문(paper3)의 원본은 `paper_exports/`, Claude Science 산출물은 `claude_science_export/`(`CATALOG.md`)에 있다.
- `paper_exports/comid_paper_v3.md`와 v2는 함량확장 재실행 **전** 수치다. 인용할 때 주의한다.

## 주차별

| 주차 | 자료 | 종류 |
|---|---|---|
| 4 | `docs/figures/fig5_layered.png` — 층상 계면 구조 개념도 | 그림 |
| 4 | `docs/papers/paper10_beta_unified/figures/GEO_layered_cell.png` — 층상 인장 셀 기하 | 그림 |
| 4 | `docs/papers/paper13_reproducibility_reporting/analysis/fig_sandwich_pilot_20260921/` — 샌드위치 셀 뷰, 응력-변위 | 그림 5 |
| 4 | `docs/architecture/packmol-structure-generation-quality.md` — Packmol 품질, 고리 관통 게이트 | 보고서 |
| 4 | `docs/workflows/crystal-slab-hydroxylation-procedure.md` — 결정 슬래브·수산화 7단계와 시행착오 | 보고서 |
| 5 | `docs/figures/fig3_ff_workflow.png` — 힘장 결정론적 라우팅 | 그림 |
| 5 | `docs/SoftwareX/figures/fig_workflow_paper.png` — 플랫폼 파이프라인 | 그림 |
| 5 | `docs/architecture/ff-standard-reference-20260906.md` (+xlsx) — 전하·LJ·물·이온 모델, 결정 D1~D15 | 보고서·표 |
| 5 | `docs/architecture/FF_INTEGRATED_TABLE_20260906.xlsx` — 문헌 335편 힘장 통합표 | 표 |
| 5 | `docs/theory/clayff-gaff2-mixing-theory.md` — ClayFF+GAFF2 혼합 정당성·한계 | 보고서 |
| 5 | `docs/DECISION_RULES.md` — 실패 복구(change_seed, reduce_dt), tier 승급 | 보고서 |
| 5 | `docs/ops/EVENT_LOG_LAYERED_CAMPAIGN.md` — 사고·복구 로그 E1~E65 (자기교정 사례) | 보고서 |
| 5 | `docs/ops/E63_RESUME_PLAN_20260914.md`, `E64_RESUME_20260916.md`, `E65_RESUME_RUNBOOK_20260917.md` | 런북 |
| 6 | `docs/theory/ced-calculation-methods.md` — CED 계산법 | 보고서 |
| 6 | `docs/theory/interface-adhesion-energy.md` — 부착일·CED·인장 기하, 참고문헌 35+ | 보고서 |
| 6 | `docs/figures/fig_exampleB_ced_pipeline.png` — CED 산출 파이프라인 | 그림 |
| 6 | `paper_exports/figures/fig_ced_solubility_validation.png` (+csv) — δ 검증 | 그림·표 |
| 6 | `paper_exports/tensile_curves_20260716.png`, `force_displacement_20260716.png`, `debonding_sideview_20260716.png` (+csv/xlsx) | 그림·표 |
| 6 | `paper_exports/adhesion_energy_20260716.xlsx` — 부착에너지 | 표 |
| 6 | `claude_science_export/fig_viscosity_diagnostic.png`, `fig_viscosity_literature.png` — NEMD 점도 | 그림 |
| 6·12 | `docs/HANDOFF_bulk_ced_guard.md` — 전단 런 bulk/CED 발산 진단 (후처리 함정, 이상치 사례) | 보고서 |
| 7 | `docs/papers/paper7_spectroscopy_molecular_model/drafts/Manuscript_KR_v8.md` — 분광 기반 바인더 분자모형 역설계 | 원고 |
| 7 | `docs/papers/paper7_spectroscopy_molecular_model/reproduction_20260720/figures/` — SARA, FTIR·NMR·GPC, 레이더, 노화 연산자 (~34장) | 그림 |
| 7 | `docs/workflows/aged-binder-bulk-procedure.md` (+ledger xlsx) — 노화 분자 32종 | 보고서·표 |
| 7 | `docs/theory/tts-material-clock-theory_20260805.md` — 시간-온도 중첩 | 보고서 |
| 7 | `docs/papers/GT_RUNS_PRELIM_ARTIFACT.html`, `docs/plans/FIG_GT_FAMILY_MASTER_20260809.png` — G(t) 마스터커브 | 보고서·그림 |
| 7 | `docs/papers/paper10_beta_unified/drafts/BETA_UNIFIED_DRAFT_v3_20260803.md` — 이완·손상 분해 | 원고 |
| 7 | `claude_science_export/fig_aging_tg.png`, `fig_aging_band_resolution.png` | 그림 |
| 8 | `claude_science_export/literature_map_report.md` (+csv) — 아스팔트·시멘트 MD 문헌지도 | 보고서 (**C-S-H·ReaxFF·ML 힘장 결과물 없음**) |
| 9 | `paper_exports/comid_paper_v3.md` (+docx) — 표현자 기반 역설계 본원고 | 원고 |
| 9 | `paper_exports/figures/` — `fig_shap_pdp`, `fig_model_comparison`, `fig_interaction_2dpdp` 등 22장 | 그림 |
| 9 | `claude_science_export/comid_shap_pdp_analysis.md`, `fig_rf_vs_xgb.png`, `comid_modeling_report.md` | 보고서·그림 |
| 9·13 | `claude_science_export/comid_feature_correction.md` — additive_wt 제거, 분자특성 전환 | 보고서 |
| 9 | `claude_science_export/comid_core672_dataset.csv`, `paper_exports/ML_features_paper3.xlsx` | 데이터 |
| 10 | `claude_science_export/comid_W1_uncertainty_plan.md`, `comid_W1_stageBCD_results.md` — 불확실도 정량 | 보고서 |
| 10 | `claude_science_export/fig_reliability.png`, `fig_holdout_validation.png`, `fig_offgrid_validation.png` | 그림 |
| 10 | `docs/plans/STRUCTURAL_ML_NODE_SYSTEM_FEATURES_PLAN.md` — Graphormer 계열 피처 계획 | 계획서 (**GNN 학습 결과 없음**) |
| 10 | `docs/plans/ONGRID_OFFGRID_ML_VALIDATION_PLAN.md` — 검증 프로토콜 8종 | 계획서 |
| 11 | `docs/corpus/CORPUS_INDEX_20260904.md` (+xlsx/csv) — 전문 코퍼스 색인 | 표 |
| 11 | `claude_science_export/comid_fulltext_download_README.md` — Elsevier API 전문 수집 | 보고서 |
| 11 | `claude_science_export/fig1_topic_landscape.png`, `fig2_cooccurrence.png`, `fig_gap_coverage.png` — 문헌맵 267편 | 그림 |
| 11 | `docs/papers/CITATION_MAP_BY_TOPIC_20260726.md`, `NOVELTY_ASSESSMENT_20260726.md` | 보고서 |
| 12 | `docs/figures/fig1_architecture.png`, `fig2_workflow.png`, `fig4_mps_scheduling.png`, `fig7_db_erd.png` | 그림 |
| 12 | `scripts/dashboard/work/proj_dashboard.html`, `sandwich_dashboard.html` — 캠페인 대시보드 | 대시보드 |
| 12 | `docs/ops/FIG_throughput_power_vs_jobs_20260908.png` — GPU당 잡 수 대비 처리율 | 그림 |
| 12 | `docs/architecture/db-ml-ssot-contract.md` — DB→ML SSOT 계약 | 보고서 (**운영 DB는 SQLite, PostgreSQL 산출물 없음**) |
| 12 | `claude_science_export/comid_data_quality_eda.md` — 정제·이상치 감사 | 보고서 |
| 13 | `paper_exports/figures/fig_inverse_design.png`, `fig_design_insights.png`, `fig_compromise_combined.png` (+csv) — 베이지안 역설계, Pareto | 그림·표 |
| 13 | `paper_exports/figures/fig_experimental_validation.png`, `fig_tg_validation.png`, `fig_triangulation.png` — 실험 대조 | 그림 |
| 13 | `docs/plans/INVERSE_DESIGN_AUTOMATION_PLAN.md`, `docs/archive/LLM_AGENT_IMPLEMENTATION_PLAN.md` | 계획서 |
| 13 | `docs/papers/IJPE_Conference_2026/` — 대량 시뮬레이션 에이전트 원고 2편 (통합 사례) | 원고 |
| 13 | `docs/SoftwareX/SOFTWAREX_MANUSCRIPT.md` — NACMID 플랫폼 논문 | 원고 |
| 6·7·12 | `docs/papers/analysis_review_build/analysis_review.html` — 인장 캠페인 통합 검토, `figures/AN*.png` 179장 | 보고서·그림 |
| 6·7 | `docs/papers/paper13_reproducibility_reporting/drafts/release_R6_20260905/` — CBM 투고 패키지 (Figure 1~9, 데이터) | 원고·그림·표 |
| 6·7 | `docs/papers/paper13_standard_dry_hydro/` — 건조 대 수산화 인장 702런 분석 | 보고서·그림·표 |

## 원천 자료가 없는 주제
- 8주차: C-S-H, ReaxFF 수화, ML 힘장 결과
- 10주차: GNN/Graphormer-3D 학습 결과, 능동학습 루프 결과
- 12주차: PostgreSQL 큐레이션 (운영은 SQLite)

이 주제들은 문헌 자료와 개념 도식으로 보완한다. 저장소 밖 `/home/tyun/mounted_directory/sdd/Claude_Code/20260712_OnOffGrid_ML/results/`에 ML 독립 검증 결과가 있으나 아직 확인하지 않았다.
