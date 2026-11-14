# week10 · 계면과 부착 (모듈 M3 · 물성 · 소재)

| 항목 | 내용 |
|---|---|
| 덱 | `slides/W10_계면과부착.html` (v3 · 27장 · 54.0분 · 4차시 · 10-1 계면 인장 프로토콜 · 10-2 분리일 · 10-3 수분 손상 · 10-4 파괴 모드와 보고) |
| 학습목표 | ① 계면 계 규칙 4(격자 정합 · 슬랩 두께 ≥ 2 rc · p p f + slab · 힘장 조합)를 말하고 인장 설정 5줄을 읽는다 ② 분리일을 두 경로(힘–거리 적분 · 같은 좌표 에너지 차)로 계산하고 흔한 실수 3을 피한다 ③ 건조 · 습윤 셀을 같은 조건에서 비교하고 에너지비 정의 둘을 구분한다 ④ 노출률 e · 잔류 두께 t_res 로 파괴 모드를 판정하고 값 ± CI (n · 프로토콜) 형식으로 보고한다 |
| 선수 지식 | W08 3층 셀(stack_cell.py) · W05 시드 · 블록 평균 · W04 GAFF2 + ClayFF 조합 |
| 소요 시간 | 강의 50분 + 실습 25분(실행 약 3분) |
| 새 용어 (5) | 분리일 · 견인력–분리 관계 · 에너지비 · 파괴 모드 · 노출률 → `../GLOSSARY.md` |

## Claude Code 지시문 (덱 「만들어 보기」 장)
`prompts.md`: P10-1 분리일 검산 · 보고 한 줄(14장) · P10-2 건조 · 습윤 비교표 · ER 정의(21장) · P10-3 파괴 모드 판정 · 보고 문단(26장). 결과 = `out/P10-n_result.md`. 사용 환경 = `../docs/prompt_setup.md`.

## 실행 환경 · Claude Code (기본)
터미널 → `conda activate mdai` → `cd 2026_MOOC_Lecture_Materials/week10` → `claude` (설치 · 조작 = `../docs/claude_code_quickstart.md` · 강좌 규칙 = `../CLAUDE.md` 자동 적용). 덱 지시 상자(= `prompts.md`)를 붙여 넣고 [ ] 안만 바꾼다 → LAMMPS · Packmol 명령은 승인 창에서 확인 → `out/` 결과와 `expected_output/` 비교 보고를 읽는다. lmp · packmol = mdai(`../environment.yml`).

## 실습 순서
1. **01** P10-1 · P10-2 지시(덱 14 · 21장) · 같은 계산 = `python ../run_nb.py notebooks/01_pull_test.ipynb`: W08 빌더로 인장용 셀(톨루엔 60분자 · 0.6 g/cm³)을 건조 · 습윤 두 벌 만들고 그립 정속 당김 4,000 스텝 → `out/{dry,wet}/pull.csv` (각 40초)
2. **02** P10-3 지시(덱 26장) · 같은 계산 = `python ../run_nb.py notebooks/02_wsep_fracture.ipynb`: `work_of_separation.py`(분리일 2경로) · `fracture_mode.py`(e · t_res · 모드) → `wsep.json` · `fracture.json`
3. **확인** 건조 = 계면 박리(e > 0.5) · 습윤 = 바인더 쪽 파단 · W_mech 가 pull.csv 직접 적분과 일치 · 에너지 경로는 sd ≫ ΔE 로 「신뢰 불가」
4. **제출** `out/{dry,wet}/wsep.json` · `fracture.json` · P10-1~3 결과
5. **바꿔 보기** `--v 0.005 --steps 2000`(속도 2배 · `out/*_fast`) · `--water 0 ↔ 10`

Claude Code 없이 터미널에서 직접(week10 폴더): `python3 scripts/pull_test.py --water 0 --tag dry --build --packmol packmol --lmp lmp` (mdai · numpy · packmol · lmp = W06 SETUP.md). Colab 은 선택 경로(노트북 첫 셀 주석).

## 스크립트
| 파일 | 역할 |
|---|---|
| `scripts/pull_test.py` | W08 `stack_cell.py` 호출(--ntol 60 --rho0 0.6) → `in.pull`(슬랩 고정 · 그립 = 바인더 상단 6 Å · fix move linear v · 반력 fix ave/time 20) → LAMMPS 실행 → `pull.csv`(변위 · 반력 · σ MPa · PE · 평균 z) · `pull_summary.json` |
| `scripts/work_of_separation.py` | σ(d) 평활(15점) · W_mech = ∫σ dd(1 MPa·Å = 0.1 mJ/m²) · W_E = (E_sep − E_int)/A × 694.77 · 피크 · 분리점(피크의 10 %) → `wsep.json` |
| `scripts/fracture_mode.py` | 마지막 덤프 → 노출률 e(2 Å 격자 · 5 Å 안 원자) · t_res(12 Å 안 바인더 z 90 백분위) → e > 0.5 계면 박리 · t_res ≥ z1 응집 · 사이 박층 → `fracture.json` |

## 숫자의 출처
- 실행(이 저장소 · mdai lmp 22 Jul 2025 · 1코어): `expected_output/{dry,wet,dry_fast,wet_fast}/`: 셀 요약 · in.pull · pull.csv · wsep.json · fracture.json · 로그 머리. 건조 1,440원자(석영 540 · 톨루엔 900) · 습윤 2,067원자(+ 물 627) · 단면 627.1 Å² · v 0.0025 Å/fs(≈ 10¹¹ s⁻¹) · 4,000 스텝. **교육용 축소 실행**: 속도가 캠페인(10⁸~10¹⁰)의 10~1,000배 · 석영 표면 수산화 미적용 · 시드 1 → 값은 모양 확인용 · 정량은 W16.
- 셀 밀도 변경 이유: W08 기본 톨루엔 20분자 · 0.2 g/cm³ 는 기체처럼 성겨 당기면 그냥 흩어진다 → 같은 빌더에 `--ntol 60 --rho0 0.6`(두께 24.4 Å 유지).
- 프로토콜 · 규칙: 원본 06주차 보충A #6~#10(계면 계 규칙 · 인장 설정 · 속도 환산) · #12~#17(분리일 · 같은 좌표 규약 · 견인력–분리 · Weibull 피크) · #19~#22(수분 · ER · 수산화) · #24~#37(파괴 모드 · 변동 · 시드 · 보고) · 07주차 #29~#35(702런 결과 · 스냅샷 · 곡선 · 속도 의존) · 연구 플랫폼 `docs/theory/interface-adhesion-energy.md` §1~§3
- 캠페인 수치(MD 계산값 · 실험값 아님): 연구 플랫폼 `docs/papers/paper13_standard_dry_hydro/data/agg_dry_vs_oh_20260920.csv` · `agg_failure_mode_20260920.csv` · `agg_sio2_hydroxylation_by_T_20260920.csv`(광물 · 표면당 n 117 · 702런) · Weibull 피크 150/185/248 vs 원시 163/199/307 MPa · 요인 효과 45.2/24.2/15.0/11.6 MPa · 시드 CI 표 = 선행 연구 R6
- 덱에서 뺀 원본 내용(전단 식 · 셀 크기 의존성 · 시간 상관 · 조건 격자 · 측면도 · 평면도 규칙 · 결정면 선택) · 덱에서 옮긴 식(분리일 기호식 · 단위 환산 · 에너지비 식 · 2026-11-14) → `docs/interface_notes.md`
