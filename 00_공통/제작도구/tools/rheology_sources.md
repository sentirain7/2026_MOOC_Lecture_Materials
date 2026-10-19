# 레올로지 실측 · TTS · 마스터커브 원천 목록 (2026-09-22 조사)

약칭
- `LA` = `/home/tyun/mounted_directory/sdd/Claude_Code/LAMMPS_Asphalt`
- `ARB` = `LA/docs/papers/analysis_review_build`
- `SYN` = `/home/tyun/SynologyDrive/Research Data`

기준 바인더는 **S64-22 (= AAA1, README 확정)**이다. 모든 파일은 읽기 전용으로 다루고, 쓴 그림·수치는 발표자 노트에 경로를 적는다.

## BBR (굽힘보 레오미터, Bending Beam Rheometer) — 측정값
- `LA/data/experimental/S64-22_physical_20260728/S6422.xlsx` BBR 시트(−6/−12/−18/−24 °C, 240 s 하중 시계열)
  - **주의**: 시트 머리글의 시료명이 −12 °C만 `S6422NA`이고 나머지는 `S6422LA`로 적혀 있다. 노화 상태가 섞였을 수 있다.
- `ARB/data/an57_expt.json` (스크립트 `ARB/scripts/an57_expt_shift.py`)
  - S(60 s) = 162 / 332 / 1100 / 2105 MPa, m = 0.419 / 0.432 / 0.346 / 0.369
  - Arrhenius Ea: BBR 186 kJ/mol, 점도 71 kJ/mol
  - PG 판정은 없다.
- `ARB/figures/AN59_bbr_master.png` (1721×693): 4온도 S(t)와 저온 크리프 마스터커브(기준 −12 °C). 그림 안 글자가 한국어다.
- `SYN/8. Life Cycle Assessemnt/20231023/최종평가-2/바인더 물리실험 결과/BBR/BBR_Orig. RTFO.XLSX`: 8종 × Original/RTFO × −6/−12/−18 °C 원시 시계열

## DSR (동적전단 레오미터, Dynamic Shear Rheometer) — 측정값
- `S6422.xlsx`의 `DSR_Original`/`RTFO`/`PAV1`/`PAV2` 시트: 58–88 °C, 10 rad/s, 12 %, MCR302
  - Original의 G*/sinδ: 58 °C 3.42 kPa(δ 86.4°), 64 °C 1.50, 70 °C 0.70, 76 °C 0.34, 82 °C 0.18 kPa
- `LA/data/experimental/S64-22_physical_20260728/Asphalt_Sweep_Test_Original.xlsx`: 주파수 스윕 13–90 °C × 6.28–62.8 rad/s, 0.1 %, 8종(사용 시트는 `S6422NA`)
- `SYN/…/최종평가-2/바인더 물리실험 결과/DSR Sweep/Asphalt Sweep Test_{Original,RTFO,PAV}.xlsx`: 8종 × 3노화상태 주파수 스윕
- MSCR(다중 응력 크리프 회복, Multiple Stress Creep Recovery)
  - 원시 자료: `LA/data/experimental/S64-22_physical_20260728/Asphalt_MSCR.xlsx`(64 °C, 8종 × NA/SA/LA)
  - 가공값 · 그림: `ARB/data/an56_mscr.json`, `ARB/figures/AN56_mscr_vstar.png`
  - S64-22 Jnr: NA 5.35 → 5.75, SA 2.82 → 3.06, LA 0.125 → 0.132 kPa⁻¹

## TTS (시간-온도 중첩, time–temperature superposition) · 마스터커브
- **`ARB/figures/AN79_cam_master.png`** (1687×823): DSR+BBR+RV 138점 CAM 동시 적합, WLF C1 = 12.8, C2 = 110 K(기준 20 °C). 데이터는 `ARB/data/an79_cam.json`. **강의용 우선.**
- `ARB/figures/AN76_sweep_clock.png`: 스윕만으로 만든 마스터커브, WLF 16.1 / 159 K. 데이터 `an76_sweep_clock.json`. (c) 패널은 MD 파손 비교라 잘라서 쓴다.
- `ARB/figures/AN77_full_mastercurve.png`: 3기기 통합 |G*|. BBR 변환은 G ≈ S/3, ω ≈ 1/t 근사.
- `ARB/figures/AN78_sigmoid_master.png`: 시그모이드 동시 적합, WLF 13.4 / 113
- MD와 실험 대조: `ARB/figures/AN116_md_exp_master.png`(두 시계 간격 Δ = 4.7 ± 0.4 decade), `AN117_unified_equation.png`
- MD G(t): `LA/docs/plans/FIG_GT_FAMILY_MASTER_20260809.png`, `LA/docs/papers/MASTERCURVE_DATA_20260809.xlsx`
- 이론: `LA/docs/theory/tts-material-clock-theory_20260805.md`
- 원데이터 표: `LA/docs/papers/analysis_review_data_20260727.xlsx` (AN56/57/59/76–79/116/117 시트)
- 2012년 노화 5단계 마스터커브: `SYN/8. Life Cycle Assessemnt/20231023/최종평가-2/DSR-BBR Gstar Mastercurve (20231023).xlsx` (AP5 등, log aT와 시그모이드 계수)

## 기타 실측
- 회전점도: `LA/data/experimental/S64-22_physical_20260728/Viscosity20230407.xlsx`
  - S64-22: 100 °C 4125 cP, 120 °C 1112 cP, 150 °C 275 cP
- SARA 실측: `SYN/…/바인더 물리실험 결과/TLC-FID/SARA 분석 자료.xlsx`
- **PG 최종 판정표는 없다.**
