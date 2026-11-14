# week04 · 힘장 (모듈 M1 · MD 기초)

| 항목 | 내용 |
|---|---|
| 덱 | `slides/W04_힘장.html` (v3 · 26장 · 54.5분 · 4차시 · 4-1 힘장 계보 · 4-2 전하 · 조합 규칙 · 4-3 경계조건 · 장거리 · 4-4 만들어 보기) · v1 28장은 `decks/v1/` |
| 학습목표 | ① 힘장 상수(k · ε · σ · q)가 QM 과 실험 중 무엇으로 정해지는지 항별로 말한다 ② Class I/II · LJ 12-6/9-6 · GAFF2 · OPLS-AA · COMPASS · ClayFF · ReaxFF 를 용도로 구분한다 ③ 분자 준비 4단계(SMILES → 3D → 원자 타입 → AM1-BCC)를 톨루엔으로 설명한다 ④ 세 조합 규칙으로 이종쌍 ε · σ 를 계산한다 ⑤ 주기경계 · 컷오프 · 꼬리 보정 · PPPM · 이웃 목록의 역할과 LAMMPS 명령 세 줄을 읽는다 |
| 선수 지식 | W03 U 5항 식 · LJ 곡선 · 산술 · 기하 평균 |
| 소요 시간 | 강의 50분 + 실습 20분 |
| 새 용어 (7) | 원자 타입 · 조합 규칙 · 부분전하 · 1-4 축소 · 주기경계조건 · 컷오프 · 이웃 목록 → `../GLOSSARY.md` |

## Claude Code 지시문 (덱 「만들어 보기」 장)
`prompts.md` · P4-1 내 분자의 GAFF2 타입 · AM1-BCC 전하 직접 생성(15장 · MD 워크플로우 mol · ff) · P4-2 노트북 실행 → 컷오프 스캔 결과 읽기(22장) · P4-3 내 재료의 힘장 설정 표 · in 파일 네 줄(23장). 결과 = `out/P4-n_result.md` (Claude Code 가 저장). 사용 환경 = 이 폴더에서 연 Claude Code (`../docs/claude_code_quickstart.md` · `../docs/prompt_setup.md`).

## 보충 표
`docs/forcefield_tables.md` · v1 덱의 표 7장(힘장 8종 · 전하 방법 7종 · 네 힘장 비교 · 계 크기 · 이웃 목록 인수 · Ewald 세부) 전문.

## 실습 순서
**시작**: 터미널 → `conda activate mdai` → `cd week04` → `claude`. 노트북은 「`@notebooks/01_mixing_rules.ipynb` 를 실행하고 결과를 요약해」 처럼 지시한다 → 승인 → Claude Code 가 주차 폴더에서 `python ../run_nb.py notebooks/<이름>.ipynb` 로 실행하고 `out/` 결과를 `expected_output/` 과 비교해 보고한다. 그림을 직접 보려면 `jupyter lab` 으로 연다.

1. **01** `notebooks/01_mixing_rules.ipynb` · GAFF2 32타입 + ClayFF 4원소 → 세 규칙 이종쌍 표 666쌍 · 멱평균 부등식 확인 · ca–hc 곡선 (8분)
2. **02** `notebooks/02_pbc_cutoff.ipynb` · LJ 유체 216입자 · 최소 이미지 · 컷오프 6/8/10/12 Å · 꼬리 보정 → `out/cutoff_scan.json` (10분 · 계산 30초)
3. **확인** 꼬리 보정 후 8 Å 의 오차 < 1 % · 12 Å < 0.01 %
4. **제출** `mixing_table.csv` · `cutoff_scan.json`
5. **선택** `live/mixing_rules.ipynb` · 덱 12장 조작형과 같은 계산

스크립트로 한 번에: `python3 scripts/ff_tools.py` (week04 폴더 · mdai) → `out/` 에 3개 파일 (노트북 01 · 02 와 같은 계산).

(선택) Colab 에서 열 때: 노트북 첫 셀의 `google.colab` 분기가 저장소를 받아 week04 로 이동한다. 이 강좌의 기본 경로는 위의 Claude Code.

P4-1 은 MD 워크플로우(`../mdworkflow` · 지시문 M-1 · M-2)의 `python ../mdworkflow/mdwf.py mol` · `ff` 로 톨루엔의 GAFF2 타입 · AM1-BCC 전하를 직접 만든다. AmberTools(antechamber · parmchk2 · sqm)는 `mdai` 환경에 들어 있다. 만든 톨루엔은 `data/Toluene_gaff2.json`(참고 사례 · 연구 플랫폼 결과)과 타입 · 전하 · 결합 매개변수가 같다(원자 번호 순서만 다름). 결과 파일 `../mdworkflow/ws/ff/Toluene_gaff2.json` 은 W06 의 MD 워크플로우 ③ build 에서 쓴다.

## 숫자의 출처
- GAFF2 타입별 ε · σ · 톨루엔 AM1-BCC 전하 · 결합 상수: 참고 사례(연구 플랫폼 결과) `data/forcefield_artifacts/organic_gaff2/*.json` (→ `data/`)
- ClayFF σ · ε · 전하: 연구 플랫폼 `data/forcefields/mineral_lj_catalog.yaml` · `mineral_charge_catalog.yaml` (Cygan 2004)
- 1-4 축소 lj 0.5 / coul 0.833333 · `pair_modify mix arithmetic` · `pair_style lj/cut/coul/long 12.0` · `kspace_style pppm 1.0e-4` · `kspace_modify slab 3.0`: 연구 플랫폼 `src/forcefield/ff_stack.py` · `src/protocols/lammps_force_field.py`
- 12 Å 정규화 값(0.0002 · 0.25) · erfc(3) ≈ 2.2e−5 · neighbor 2.0 bin · 계 크기 권장: 원본 02주차 덱 #24~#27
- 불일치 기록: 원본 02주차 #16 노트의 「GAFF2 ca–ca K 478.4 · r₀ 1.387」은 GAFF 1세대 값. GAFF2 아티팩트(`data/Toluene_gaff2.json`)는 K 354.25 · r₀ 1.3986.

## 기대 결과 (`expected_output/`)
| 파일 | 내용 |
|---|---|
| `mixing_table.csv` | 36타입 × 3규칙 = 666쌍 |
| `mixing_examples.json` | ca–hc: LB σ 2.958 ε 0.0453 · geo 2.936 · WH 3.058 ε 0.0355 / ca–Si(ClayFF) ε 4.3e−4 |
| `cutoff_scan.json` | N 216 · L 26.2 Å · 절단만 6 Å 30 % → 12 Å 3.9 % · 꼬리 보정 후 8 Å −0.10 % · 12 Å −0.003 % |

## 체크리스트
- [ ] 노트북 01 의 「부등식 위반 0」
- [ ] 노트북 02 의 꼬리 보정 후 8 Å 오차 절댓값 < 1 %
- [ ] W03 상자에서 rc 10 · 12 Å 가 `valid_rc_le_L2 = False`
- [ ] 퀴즈 5문항 (`quiz.md`)

## 못 끝냈다면
`expected_output/` 을 받고 W05 로 간다. W05 노트북은 이 파일을 읽지 않는다.

## 폴더
```
week04/
  README.md
  slides/W04_힘장.html
  notebooks/01_mixing_rules.ipynb   02_pbc_cutoff.ipynb
  live/mixing_rules.ipynb           덱 12장 조작형과 같은 계산
  prompts.md                        P4-1 · P4-2 · P4-3 Claude Code 지시문 원문
  docs/forcefield_tables.md         v1 표 7장 전문
  scripts/ff_tools.py               노트북 01 · 02 와 같은 계산
  data/gaff2_atom_types.csv  clayff_lj.csv  Toluene_gaff2.json  README.md
  expected_output/mixing_table.csv  mixing_examples.json  cutoff_scan.json
  out/                              실행 결과 (git 제외)
  quiz.md
```
