# week08 · 다층 구조와 다중 힘장 스택 (모듈 M2 · LAMMPS)

| 항목 | 내용 |
|---|---|
| 덱 | `slides/W08_다층구조와다중힘장스택.html` (v3 · 25장 · 51.0분 · 3차시: 8-1 계면 셀 3층 · 8-2 FF-neutral 토폴로지와 라우팅 · 8-3 혼용 규칙과 스택) |
| 학습목표 | ① 광물 | 물 | 바인더 3층 셀의 구성(고정 슬래브 · 진공 ≥ 30 Å · p p f · slab 보정)을 말하고 조립 명령 5줄을 읽는다 ② FF-neutral 토폴로지(원소 · 좌표 · 결합 · 분자 ID)와 힘장 라우팅(organic → GAFF2 · mineral → ClayFF · water → SPC/E · unknown → blocked)을 구분한다 ③ 혼용 조건 4(함수 형태 · 조합 규칙 · 전하 척도 · 1-4 축소)로 힘장 짝을 가능 · 조건부 · 불가로 판정한다 ④ 스택 이름(clayff_gaff2_v1)과 검증 수준(validated · research_only · blocked)을 결과에 기록한다 |
| 선수 지식 | W04 이종쌍 · 조합 규칙 · PPPM · W06 data 파일 · Packmol · W07 템플릿 |
| 소요 시간 | 강의 50분 + 실습 25분 |
| 새 용어 (5) | FF-neutral 토폴로지 · 힘장 라우팅 · 힘장 스택 · slab 보정 · 분리일 → `../GLOSSARY.md` |

## Claude Code 지시 (덱 「만들어 보기」 장)
`prompts.md`: P8-1 내 재료의 3층 셀 설계표(15장) · P8-2 토폴로지 → 힘장별 타입 표(16장) · P8-3 in 파일 혼용 위험 점검(24장). 결과 = `out/P8-n_result.md`(Claude Code 가 저장). 사용 환경 = `../docs/claude_code_quickstart.md` · `../docs/prompt_setup.md`.

## 실습 순서 (Claude Code)
0. **열기** 터미널 → `conda activate mdai` → `cd week08` → `claude` · 노트북 실행 = 「`@notebooks/01_stack_cell.ipynb` 를 실행하고 결과를 요약해」(= `python ../run_nb.py notebooks/<이름>.ipynb` · 강좌 실행기 · 직접 보려면 JupyterLab)
1. **01** `notebooks/01_stack_cell.ipynb`: 석영 슬래브(540) | 물 209분자 | 톨루엔 20분자 → `out/stack.data` · `in.stack` → LAMMPS 500 스텝 → 측면 뷰 (10분 · 계산 4초)
2. **02** `notebooks/02_route_and_check.ipynb`: 토폴로지 3개 → 힘장 라우팅 → 혼용 점검 5규칙 (8분)
3. **확인** `stack_summary.json` 변/2rc ≥ 1 · 슬래브 전하 합 0 · 층 z 범위 분리 · `routed_toluene.json` 아티팩트 일치 · `check_mix_stack.json` 5 ✓
4. **제출** `stack_summary.json` · `routed_toluene.json` · `check_mix_stack.json`
5. **바꿔 보기** `python3 scripts/stack_cell.py --slab off --tag stack_noslab` (p p p · slab 보정 없음) → `log.stack_noslab` 의 E_long · PotEng 비교(덱 21장) · `--water 0` 건조 계면

스크립트를 직접 실행할 때: `python3 scripts/stack_cell.py --packmol packmol --lmp lmp` (week08 폴더에서 · numpy · packmol · lmp 는 `mdai` 에 포함 · Claude Code 안에서는 앞에 `!`). (선택) Colab 은 노트북 01 첫 셀의 clone 분기 사용.

## 스크립트
| 파일 | 역할 |
|---|---|
| `scripts/stack_cell.py` | 석영 보정 단위셀 → 직교 초격자(p·a × q·√3·a) 슬래브 · Packmol 로 물 · 톨루엔 층 · 진공 → data + in (COMID clayff_gaff2_v1 설정) · `--lmp` 로 실행 · 측면 뷰 JSON |
| `scripts/make_topology.py` | FF-neutral 토폴로지 JSON 3개(톨루엔 · 석영 셀 · 물) · 구조 해시 |
| `scripts/route_ff.py` | 토폴로지 → GAFF2(규칙 타이핑 + 아티팩트 전하) · ClayFF · SPC/E · COMPASS(blocked) · ReaxFF(원소만) |
| `scripts/check_mix.py` | in 파일 혼용 위험 5규칙 ✓/✗ (R1 함수 형태 · R2 조합 규칙 · R3 전하 척도 · R4 special_bonds · R5 층상 셀) |
| `data/in_bad_mix.example` | 다섯 규칙을 전부 깨는 교육용 in 파일 |

## 숫자의 출처
- α-quartz 보정 단위셀(a 4.913 · c 5.405 · 9원자 · Levien 1980) · 직교 초격자 변환 A1 = p·a1 · A2 = q·(a1 + 2a2) · 물 0.0334 분자/Å³ · 슬래브 전체 고정 레인: COMID `src/builder/crystal_builder.py` · `crystal_std_termination.py` · `layer_builder.py`
- ClayFF Si +2.1 · O −1.05 · σ · ε: COMID `inorganic_profiles.yaml`(silica) · `week04/data/clayff_lj.csv`(Cygan 2004) · 주의: COMID 프로파일의 Si ε 는 4.0e−4, Cygan 원표는 1.84e−6 (이 강좌는 week04 표 값 사용 · 「확인 필요」 기록)
- SPC/E O −0.8476 · H +0.4238 · ε_O 0.1553 · σ_O 3.166 · O–H 1.0 Å · 109.47°: Berendsen 1987(원본 03주차 물 모델 표 · W04 8장)
- 톨루엔 GAFF2 + AM1-BCC · ρ0 0.2: `week06/data/Toluene_gaff2.json` · W06 규칙
- 진공 ≥ 30 Å · boundary p p f · change_box · add append offset · shift · kspace_modify slab 3.0 · fix setforce · npt x y: 원본 04주차 #39 · #41 · 플랫폼 셀 23,124원자 · AAA1 216분자: 원본 04#40(paper10 Fig. 2)
- FF-neutral 토폴로지 · 메틸페놀 타입 대응(ca/c3a · oh/o2h · ho/h1o · c3/c4) · 라우팅 표 · 스택 레지스트리 · 라벨 사고: 원본 05주차 #22~#28 · COMID `src/forcefield/ff_stack.py` · `FF_AUDIT_REPORT_20260715.md`
- 혼용 조건 4 · 관계도 · 이종쌍 수치 예(σ_CO 3.283 · ε_CO 0.116 · 3.080/3.042 → 1.16 · 12-6 vs 9-6 r_min) · 재정의 4 · 검증 5: 원본 03주차 #31~#34
- 실행 결과(이 저장소에서 측정): 1,467원자 · 500 스텝 · T 298 → 307 K · PE −135,374 → −135,408 kcal/mol · 층 z 범위 0~10.2 / 10.7~25.1 / 25.1~49.7 Å · slab 보정 유 · 무 PE −130,670 vs −135,251(Δ 4,582) · E_long −32,049 vs −37,685
- 덱에서 옮긴 식 · hybrid/overlay 입력 예시(규칙 16 · 2026-11-14) → `docs/forcefield_stack_notes.md`

## 기대 결과 (`expected_output/`)
| 파일 | 내용 |
|---|---|
| `stack_summary.json` · `stack_sideview.json` | 셀 24.565 × 25.529 × 82.2 Å · 540 / 627 / 300 원자 · 층 z 범위 |
| `in.stack` · `log.stack` · `in.stack_noslab` · `log.stack_noslab` | 조립 in 파일 · 500 스텝 로그(slab 보정 유 · 무) |
| `routed_toluene.json` · `routed_quartz.json` · `routed_water.json` | 힘장 라우팅 결과(아티팩트 일치) |
| `check_mix_stack.json` · `check_mix_bad_mix.json` | 5 ✓ · 5 ✗ |

## 체크리스트
- [ ] `stack_summary.json` 의 `min_edge_over_2rc ≥ 1` · `slab.charge_sum = 0` · `packmol.success`
- [ ] 500 스텝 뒤 세 층의 z 범위가 겹치지 않음(측면 뷰)
- [ ] `routed_toluene.json` 의 `artifact_check.all_match = true`
- [ ] `check_mix_stack.json` 5 ✓ · `in_bad_mix.example` 의 ✗ 5개를 줄과 대응시킬 수 있음
- [ ] P8-1 ~ P8-3 결과 파일 3개 · 퀴즈 5문항
