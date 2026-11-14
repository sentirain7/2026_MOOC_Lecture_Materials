# ReaxFF 수식 9장 전문 (참조 덱 「ReaxFF Cement Review」 Part I 14~22장 이식 · 덱 W12 에는 2장만)

출처: Baba & Yun, *ReaxFF-Based Reactive MD of Cementitious Materials: A Review* §2.2 · 함수형은 van Duin 외 (2001) · Chenoweth 외 (2008). 덱 W12 11장(결합 차수 · 결합 에너지) · 12장(전하 평형)이 이 중 2개를 그림 위 기호로 표시한다. 유도는 하지 않는다.

1. **전체 에너지 12항 · 2그룹**: E_system = E_bond + E_over + E_under + E_lp + E_val + E_pen + E_coa + E_tor + E_conj + E_vdW + E_Coul + E_Hbond. 결합 그룹(결합차수 BO 의 함수) · 비결합 그룹(모든 원자쌍 · 차폐 · 타퍼).
2. **결합 차수**: BO′_ij = exp[p_bo1 (r_ij/r₀^σ)^p_bo2] + exp[p_bo3 (r_ij/r₀^π)^p_bo4] + exp[p_bo5 (r_ij/r₀^ππ)^p_bo6]. 거리 하나로 σ · π · ππ 세 항 · r 증가 시 연속 0 → 결합 파괴에 불연속 없음.
3. **보정과 배위 항**: BO_ij = BO′_ij · f₁(Δ′_i, Δ′_j) · f₄ · f₅ · Δ_i = Σ_j BO_ij − Val_i (O: 2 · Si: 4) · E_over ∝ Δ_i /(1 + exp(λΔ_i)) · E_lp = p_lp2 Δ_i^lp /(1 + exp(−75 Δ_i^lp)).
4. **결합 에너지**: E_bond = −D_e^σ BO^σ exp[p_be1 (1 − (BO^σ)^p_be2)] − D_e^π BO^π − D_e^ππ BO^ππ · BO → 0 ⇒ E_bond → 0 · D_e · p_be 는 DFT 해리 스캔으로 피팅.
5. **각도 항**: E_val = f₇(BO_ij) f₇(BO_jk) f₈(Δ_j) p_val1 {1 − exp[−p_val2 (Θ₀ − Θ_ijk)²]} · f₇(BO) = 1 − exp(−p_val3 BO^p_val4) · E_pen · E_coa(3체 공액).
6. **비틀림 · 4체 공액**: E_tor = f₁₀(BO_ij, BO_jk, BO_kl) sinΘ_ijk sinΘ_jkl [½V₁(1 + cos ω) + ½V₂ exp{p_tor1 (BO^π_jk − 1 + f₁₁)²}(1 − cos 2ω) + ½V₃(1 + cos 3ω)] · E_conj = f₁₂(BO) p_cot1 [1 + (cos²ω − 1) sinΘ sinΘ].
7. **비결합 항**: E_vdW = Tap(r) D_ij {exp[α(1 − f₁₃(r)/r_vdW)] − 2 exp[½α(1 − f₁₃(r)/r_vdW)]}(차폐 Morse) · E_Coul = Tap(r) C q_i q_j [r_ij³ + γ_ij⁻³]^(−1/3) · Tap(r) = Σ_{k=0}^{7} Tap_k r^k → 0 at R_cut ≈ 10 Å.
8. **수소결합**: E_Hbond = p_hb1 [1 − exp(p_hb2 BO_XH)] exp[−p_hb3 (r⁰_hb/r_HZ + r_HZ/r⁰_hb − 2)] sin⁸(Θ_XHZ/2) · X–H···Z (X, Z = O, N) · 각도 선택성 강함 · C-S-H 층간수 · 수산화 표면의 수소결합 개수가 이 정의에 의존.
9. **전하 평형 EEM/QEq**: E_Q = Σ_i (χ_i q_i + ½η_i q_i²) + Σ_{i<j} k_c q_i q_j [r_ij³ + γ_ij⁻³]^(−1/3) · ∂E_Q/∂q_i = μ · Σq_i = 0 · 매 스텝 풀이. 한계: 전하 재분배만 · O–H 해리의 전자 이동 미표현 · pH 부여 없음.

이 저장소 `data/ffield.reax.cement` 의 결합 파라미터(원본 08주차 15장 노트): O–H r₀^σ 0.9215 · p_bo1 −0.0920 · p_bo2 4.2790 / Ca–O r₀^σ 1.9052 · p_bo1 −0.0515 · p_bo2 8.9041(π 없음) / Si–O r₀^σ 1.7073 · p_bo1 −0.1130 · p_bo2 8.4790 · r₀^π 1.2375 · p_bo3 −0.2572 · p_bo4 28.8153. 사례연구 1 의 결합 판정 거리 Ca–O_w 2.8 Å · Si–O_w 2.2 Å 에서 BO′ ≈ 0.2~0.4.

## 덱에서 옮긴 식 (2026-11-14 · STYLE_ADDENDUM 규칙 16 · 덱 W12 는 식 없이 곡선 · 막대 그림만)

### 덱 10장 「결합 차수」에 있던 식 · 기호표

- E = Σ_k E_k(BO_ij) ,  BO′_ij = exp[p_bo1 (r_ij / r_0^σ)^p_bo2] + exp[p_bo3 (r_ij / r_0^π)^p_bo4]

| 기호 | 뜻 · 단위 |
|---|---|
| r_ij | 원자 i–j 거리 · Å |
| r_0^σ · r_0^π | σ · π 결합 기준 거리 · Å |
| p_bo1~4 | 원소쌍 파라미터 · ffield |
| E_k | 결합 · 각 · 비틀림 · vdW · 쿨롱 등 9항 |

- 덱 표기: 「결합 차수 BO′(r) = 거리의 연속 함수」 → 「결합 차수 = 거리에 따라 서서히 끊어지는 결합」

### 덱 11장 「전하 평형(QEq)」에 있던 식 · 기호표

- E_Q = Σ_i (χ_i q_i + ½ η_i q_i²) + Σ_{i<j} k_c q_i q_j [r_ij³ + γ_ij^−3]^−1/3 ,  ∂E_Q/∂q_i = μ ,  Σq_i = 0 · 매 스텝 풀이 (QEq/EEM)

| 기호 | 뜻 · 단위 |
|---|---|
| χ_i | 전기음성도 · eV |
| η_i | 경도(자기 쿨롱) · eV |
| γ_ij | 차폐 파라미터 · Å⁻¹ |
| μ | 공통 화학 퍼텐셜 · Σq = 0 조건 |

### 덱 15장 「온도 가속」에 있던 식 · 계산

- Arrhenius: k(T)/k(300) = exp[(Ea/R)(1/300 − 1/T)] · R = 8.314 J/(mol·K)
- 논문(Shimelis 외 2026 §2.3)의 「1300 K 에서 약 6자릿수 가속」 역산 → Ea ≈ 45 kJ/mol(계산값)
- 연습: Ea 를 35 · 55 kJ/mol 로 바꿔 배율 자릿수 확인 · 절대 시간 환산은 보고서에 기재 금지 · 상 간 순서만
