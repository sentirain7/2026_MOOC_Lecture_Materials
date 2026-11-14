# week09 보충 · 원본 06주차에서 덱에 넣지 않은 식 · 표 · 도구 (내용 보존)

## 1. 부피 분포와 수렴 (원본 #8 · #9)
- P(V) ∝ Ω(V) e^{−(U+PV)/k_BT} · Ω: 배치 수(엔트로피) · U: 포텐셜 · PV: 외부 압력의 일 · k_BT: 열에너지(폭).
- 압력 되먹임 dV/dt ∝ (P_int − P_ext) · V(t) = V_∞ + ΔV e^{−t/τ} · τ 는 P_damp.
- 평형 뒤 요동 ⟨δV²⟩ = k_BT V κ_T · δV/V ∝ 1/√N.
- 온도 T ↑ → 분포 폭 ↑ · 압력 P ↑ · N ↑ → 봉우리 왼쪽 · 폭 ↓.

## 2. 열팽창 · Tg (원본 #10 · #11)
- α = (1/V)(∂V/∂T)_P · ρ–T 직선 기울기에서. 온도 최소 3점 · 같은 시드 · 같은 프로토콜.
- Tg: 고온에서 단계적 냉각 → 각 온도 평형 부피 → 두 직선 적합 → 교점. MD 냉각률은 실험보다 10^10 배 빠름 → 수십 K 높게 산출 · 상대 비교 · 여러 냉각률 외삽.

## 3. 부착 · 인장 (원본 #12 → W10 에서 다룸)
- W_sep = (E_slab + E_binder − E_interface)/A · mJ/m² · 건조 · 습윤 차이 = 수분 민감도.
- 응력–변위 σ(d) → σ_max(인장강도) · ∫σ dd(파괴에너지) · 속도 의존 · 파괴 모드 3(계면 박리 · 응집 · 혼합).

## 4. CED 두 분자 예시 (원본 #15)
- ΔE_coh = ⟨E_gas⟩ − ⟨E_bulk⟩ = −⟨E_AB⟩ · E_AB = Σ_i∈A Σ_j∈B [4ε_ij((σ/r)^12 − (σ/r)^6) + q_iq_j/4πε₀r_ij].
- ⟨E_AB⟩ = −12.4 kcal/mol = 8.62×10⁻²⁰ J · V 1.2 nm³ → CED 71.8 MJ/m³ · δ 8.5 MPa^0.5.

## 5. Method A 의 LAMMPS 설정 (원본 #16)
```
compute inter all pair lj/cut/coul/long
compute_modify ... exclude intra     # 분자 안 쌍 제외 → 분자 사이 vdW · Coulomb 만
```
이 저장소는 교육용으로 「벌크 좌표 고정 분자 50개 run 0」 로 A 를 구현(분리 설정 민감성을 피하기 위해). 결과 비교 = ced.json.

## 6. 숫자 예 (원본 #18)
E_bulk −43,490 · E_gas −17,820 kcal/mol → ΔE 25,670 = 1.074×10⁸ J/mol · V 482,000 Å³ → CED ≈ 370 MJ/m³ · δ ≈ 19.2.

## 7. 상용성 (원본 #19)
χ ≈ (V_ref/RT)(δ₁ − δ₂)² · |Δδ| < 2 혼합 · 2~5 부분 상용(RDF 로 국소 뭉침) · > 5 상 분리 · 극성은 Hansen 3성분(δ_d · δ_p · δ_h) 또는 혼합 엔탈피.

## 8. Green–Kubo · NEMD (원본 #21 · #22)
```
variable pxy equal pxy
variable pxz equal pxz
variable pyz equal pyz
fix ss all ave/correlate 5 20000 100000 v_pxy v_pxz v_pyz type auto file profile.stress ave running
run 10000000     # 10 ns · NVT 298 K
```
NEMD(SLLOD): η = τ/γ̇ · 고전단 → 저전단 외삽. 상온 바인더는 고온 계산 후 Arrhenius 외삽. 연구 플랫폼은 RNEMD(Müller-Plathe) 도 운용 · src/metrics/viscosity.py (_GK_TO_MPAS ≈ 7.436e−10 · _REAL_TO_MPAS ≈ 16.61).

## 9. MSD · 확산 (원본 #23)
MSD(t) = ⟨|r(t) − r(0)|²⟩ · D = lim MSD/6t · 탄도 → 케이지 → 확산(log–log 기울기 ≈ 1 에서만 적합) · SARA 분류별 MSD → 아스팔텐 정체.

## 10. OVITO · MDAnalysis (원본 #25 · #26)
- OVITO: 궤적 시각화 · 공통 이웃 분석 · 클러스터 · 보이드 · 계면 단면 · GUI 파이프라인을 ovito 파이썬 모듈로 재실행 · 파괴 모드 판정 측면도.
- MDAnalysis: 원자 선택 → MSD · RDF · 밀도 프로파일 · 수소결합 → numpy · pandas.
```python
u = mda.Universe("final.data", "prod.lammpstrj", format="LAMMPSDUMP")
msd = einstein_msd(u, select="all"); D = slope(msd, t0=200, t1=2000) / 6
rho, rho_err = block_average(log["Density"])
row = dict(exp_id=exp_id, rho=rho, rho_err=rho_err, D=D, ced=ced, delta=delta, eta=eta); append_csv("results.csv", row)
```
규칙 5: 입력 = 실험 ID 폴더 · 구간은 인수 · 평균 + 오차 · CSV 한 줄 · OVITO PNG 함께 보관 · 스크립트도 입력 해시에.

## 11. 오차 · 예산 (원본 #27 · #28)
| seed | ρ (g/cm³) | CED (MJ/m³) | 비고 |
|---|---|---|---|
| 01 | 1.019 | 368 | 기준 |
| 02 | 1.022 | 373 | 초기 배치 변경 |
| 03 | 1.018 | 366 | 속도 시드 변경 |
| 평균 ± SE | 1.020 ± 0.001 | 369 ± 2 | 보고 형식 |

| 물성 | 권장 궤적 | 전형적 오차 | 수렴 진단 |
|---|---|---|---|
| 밀도 | 2 ns | < 0.5 % | 블록 평균 겹침 |
| D | 20~50 ns | 10~30 % | log–log 기울기 ≈ 1 구간 |
| η | 10~100 ns | 20~50 % | 적분 평탄 · 시드 일치 |
| Tg | 8점 × 1 ns | ± 10 K | 적합 구간 바꿔도 교점 안정 |
짧게 여러 번 > 길게 한 번 · 고온 후 외삽 · 선별(짧은 다수) / 검증(긴 소수).

## 12. 이번 주 실행 조건 (이 저장소)
톨루엔 50분자(W06 final.data · 750원자) · GAFF2 + AM1-BCC · lj/cut/coul/long 12 Å · pppm 1e−4 · tail yes · NPT 298 K 1 atm 30 ps → NVT 20 ps(응력 5 fs) · Tg 4점(100 · 175 · 250 · 325 K) × 8 ps · 기상 100 Å 상자 lj/cut/coul/cut 12 Å · mdai LAMMPS 22 Jul 2025 · 1 코어. 모든 값은 「수렴 전 · 형태만」.

## 13. 덱에서 옮긴 식 (2026-11-14 · STYLE_ADDENDUM 규칙 16 · 덱 = 말 식 · 비유 · 숫자 그대로)

덱 W09 는 핵심 식 1개(「CED = 떼어 놓는 에너지 ÷ 부피」)만 남기고, 아래 식 · 기호표 · 환산 상수를 이곳으로 옮겼다. 값은 덱에 있던 그대로다.

| 덱 장 | 옮긴 식 · 값 | 덱에 남은 말 |
|---|---|---|
| 6 수렴 | 부피 분포 P(V) ∝ Ω(V) e^{−(U+PV)/k_BT} · 압력 되먹임 dV/dt ∝ (P_int − P_ext) · V(t) = V_∞ + ΔV e^{−t/τ} · 소요 시간 τ_total ≈ max(τ_baro, τ_struct) · 잔여 부피 요동 ⟨δV²⟩ = k_BT V κ_T | 한 봉우리 주변 흔들림 · 압력 차만큼 상자 조정 · 느린 쪽이 전체 시간 결정 |
| 5 밀도 | ρ = M / ⟨V⟩ | 질량 고정 · 흔들리는 것은 부피뿐 |
| 7 Tg | 열팽창계수 α = (1/V)(∂V/∂T) | 온도에 따른 부피 증가 비율 |
| 10 CED | CED = (⟨E_gas⟩ − ⟨E_bulk⟩) / ⟨V⟩ = −⟨E_AB⟩ / ⟨V⟩ [MJ/m³] · δ = √CED [MPa^0.5] · E_AB = Σ [LJ + q_i q_j / 4πε₀r] · 기호: ⟨E_gas⟩ = 분자를 하나씩 떼어 놓은 상태의 평균 전위에너지(kcal/mol) · ⟨E_bulk⟩ = 응집 상태(벌크 셀)의 평균 전위에너지 · ⟨V⟩ = 평형 구간 평균 부피(Å³) · E_AB = 분자 A–B 사이 원자쌍 에너지 합(LJ + 쿨롱) | 떼어 놓는 에너지 ÷ 부피 · δ = 그 제곱근 |
| 11 두 경로 | E_inter = E_bulk − Σ E_single(fixed) · CED_A = −E_inter / V · CED_B = (50⟨E_gas⟩ − ⟨E_bulk⟩) / ⟨V⟩ | 분자 사이 에너지 = 벌크 − 분자별 합 · (기상 50분자 − 벌크) ÷ 부피 |
| 12 숫자 | 환산 상수 kcal/mol/Å³ → MJ/m³ = 4184 / N_A / 1e−30 / 1e6 = **6.9477** · 1 kcal = 4184 J · 1 Å³ = 10⁻³⁰ m³ · N_A 로 나눠 분자당 | × 단위 환산(스크립트 몫) |
| 13 상용성 | χ ≈ (V_ref / RT)(δ₁ − δ₂)² | 용해도 파라미터 차가 작을수록 잘 섞임 |
| 16 점도 | η = (V / k_BT) ∫₀^∞ ⟨P_αβ(0) P_αβ(t)⟩ dt · αβ = xy · xz · yz · 기호: P_αβ = 비대각 응력 성분(atm) · ⟨P(0)P(t)⟩ = 응력 자기상관(여러 시간 원점 평균) · V 부피 Å³ · T 온도 K · η 점도 mPa·s · 단위 환산 η[mPa·s] = **7.436 × 10⁻¹⁰** × V/T × ∫⟨PP⟩dt (V Å³ · T K · P atm · t fs · 연구 플랫폼과 같은 환산 상수) · 대안 NEMD: SLLOD 전단 → η = τ / γ̇(고전단 → 저전단 외삽) · 연구 플랫폼 RNEMD(Müller-Plathe) 병행 · 고온 계산 → Arrhenius 외삽 | 흔들림의 기억 시간 · 꿀 vs 물 · 곡선 아래 면적 = 점도 |
| 19 MSD | MSD(t) = ⟨\|r(t) − r(0)\|²⟩ · D = MSD(t) / 6t (t → ∞) · 탄도 구간 ∝ t² | 이동 거리 제곱 평균의 증가 속도 = 확산 계수 |
| 23 오차 | 블록 평균 SE = σ_block / √N_block · 시드 반복 SE = σ_seed / √N_seed | 블록 평균들의 흩어짐 · 시드별 결과의 흩어짐 |

덱 16장에 있던 LAMMPS 명령(원래 그대로):

```
# LAMMPS · Green–Kubo (NPT 로 부피 → 그 부피에서 NVT 약한 조절기)
variable pxy equal pxy   # pxz · pyz 도 같게
fix ss all ave/correlate 5 20000 100000 &
    v_pxy v_pxz v_pyz type auto file profile.stress ave running
run 10000000             # 10 ns · NVT 298 K
# 이 저장소(교육용): fix ave/time 1 1 5 … stress.txt · 20 ps → 형태만
```
