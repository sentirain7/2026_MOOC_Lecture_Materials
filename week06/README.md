# week06 · LAMMPS 입력과 구조 생성 (모듈 M2 · LAMMPS)

| 항목 | 내용 |
|---|---|
| 덱 | `slides/W06_LAMMPS입력과구조생성.html` (v3 · 26장 · 53분 · 4차시: 6-1 LAMMPS 와 설치 · 6-2 입력 스크립트 · 6-3 프로토콜 · data · 힘장 파일 · 6-4 Packmol 과 벌크 셀) · v1 28장은 `decks/v1/` |
| 학습목표 | ① in 스크립트를 5구간(초기화 · 원자 정의 · 힘장 · 실행 설정 · 출력 · 실행)으로 읽는다 ② data 파일의 6절과 타입 번호 ↔ 계수 대응을 말한다 ③ 4단계 프로토콜(최소화 · 어닐링 · 평형화 · 생산)의 조건과 판정을 말한다 ④ 분자 수 · 분자량 · 초기 밀도에서 상자 한 변을 역산한다 ⑤ Packmol 품질 게이트 3(수렴 보고 · 거리 검사 · 시드 변경)을 적용한다 |
| 선수 지식 | W05 실무 순서 5단계 · W02 셸 명령 6 · W04 pair_style · kspace · special_bonds 네 줄 |
| 소요 시간 | 강의 50분 + 실습 25분 |
| 새 용어 (6) | 입력 스크립트 · data 파일 · 패키지 · 초기 구조 · 허용 거리 · 고리 관통 → `../GLOSSARY.md` |

## Claude Code 지시 (덱 「만들어 보기」 장)
`prompts.md`: P6-1 LJ 유체 실행 · LAMMPS log 읽기(7장) · P6-2 톨루엔 상자 실행 · 내 분자의 Packmol 입력 · in 수정 포인트(19장). 결과 = Claude Code 가 `out/P6-n_result.md` 로 저장. 사용법 = `../docs/prompt_setup.md` · `../docs/claude_code_quickstart.md` (W01 12장).

## 실습 순서
0. **시작** 터미널 → `conda activate mdai` → `cd week06` → `claude` · LAMMPS(`lmp`) · Packmol 은 mdai 에 포함(`../environment.yml`) · 확인 `lmp -h` · Claude Code 가 `lmp -in …` 을 승인 후 실행하고 log 를 읽어 보고 · 노트북은 `python ../run_nb.py notebooks/<이름>.ipynb`(week06 폴더 기준 경로)
1. **01** `notebooks/01_lammps_first_run.ipynb`: W03 LJ 유체 64원자 → `lj.data` · `in.lj` → `lmp -in in.lj` → thermo 표 읽기 (5분 · 계산 1초)
2. **02** `notebooks/02_packmol_box.ipynb`: Toluene.mol → Packmol(ρ0 0.2 · 3.0 Å) → 게이트 → `toluene_box.data` → `in.toluene` → 최소화 + NPT 6 ps (10분 · 계산 30초)
3. **확인** 게이트 pass · 원자 750 · |Σq| < 1e−4 · log.toluene 의 Density 가 0.2 → 약 0.31
4. **제출** `build_report.json` · `log.lj` · `log.toluene` · P6-1 · P6-2 결과
5. **선택** `live/box_calculator.ipynb`: 덱 12 · 22장과 같은 계산

노트북 없이 직접(week06 폴더 · mdai): `python3 scripts/build_lj_lammps.py --run lmp` · `python3 scripts/build_toluene_box.py --run-lammps lmp`. 덱 지시 P6-1 · P6-2 는 이 스크립트와 `lmp -in` 을 Claude Code 가 실행하게 한다. 노트북이 멈추면 이 명령으로 대신한다.

MD 워크플로우 연결(`../mdworkflow` · ③ build · 지시문 M-3): 같은 식 L = (N·M / (ρ0·N_A))^(1/3) 으로 한 변을 역산하고 한 종류 분자만 채운 단분자 상자 → 같은 품질 게이트(분자간 최소 거리 ≥ 0.9 × tolerance · 시드 바꿔 3회) → LAMMPS data. `python ../mdworkflow/mdwf.py build --id tol50 --comp Toluene=50 --rho0 0.2 --tol 3.0` → L 33.69 Å(이 주차와 같은 조건). build 의 기본값은 ρ0 0.5 · tolerance 2.0 Å 이므로 이 주차 권장 조건은 옵션으로 준다. 힘장 파일은 W04 P4-1(M-2)에서 만든 `../mdworkflow/ws/ff/Toluene_gaff2.json` 을 쓴다.

(선택) Colab 을 쓸 때: 노트북 01 · 02 의 첫 셀이 Colab 에서만 저장소를 받고 LAMMPS · Packmol 을 설치한다(약 3분 · `docs/checklist_and_commands.md` §7 · `../docs/colab_quickstart.md`).

## 숫자의 출처
- 톨루엔 셀: `data/Toluene.mol` · `data/Toluene_gaff2.json` (GAFF2 + AM1-BCC 공개 파라미터) → N 50 · ρ0 0.2 → L 33.69 Å · Packmol 최소 분자간 거리 3.283 Å · 750/750/1200/1500 · Σq −5e−5 (`out/build_report.json`)
- 실제 실행(mdai · LAMMPS 22 Jul 2025 Update 6 · 1코어): 최소화 973스텝 E 993 → −276 kcal/mol · NPT 6 ps 밀도 0.200 → 0.309 g/cm³ · 6,000스텝 15.2 s(1 ns ≈ 39 분) · LJ 64원자 1,000스텝 0.021 s (`expected_output/log.toluene` · `log.lj`)
- 스타일 선언 순서: `pair_style` 등이 `read_data` 보다 뒤에 있으면 `ERROR: Must define pair_style before Pair Coeffs` (1차 실행에서 실제 발생 → 스크립트 수정)
- in 스크립트 7단락 · 구간별 셀 밀도(M 82,950 · L 62/55/54 → 0.58/0.83/0.87) · 프로토콜 조건 · 개수 역산 예(80 Å · ρ 1.0 · M̄ 480 → 640) · 품질 게이트 스윕(25 · 58 · 92 %) · 165건 중 96건 관통: 원본 04주차 덱 #20 · #23 · #25 · #34 · #37
- 패키지 4 · 설치 명령: 원본 04#7 · #10 · `../environment.yml` · mdai `lmp -h` 출력 · 이전 버전 고정 명령 = `docs/checklist_and_commands.md` §7

## 기대 결과 (`expected_output/`)
| 파일 | 내용 |
|---|---|
| `lj.data` · `in.lj` · `log.lj` | LJ 유체 64원자 · NVE 1,000스텝 · TotEng 23.031 → 23.100 · Density 0.2394 |
| `toluene.inp` · `packmol.log` · `toluene_box.data` · `build_report.json` | Packmol 입력 · 로그 · data 750원자 · 게이트 pass |
| `in.toluene` · `log.toluene` · `density.txt` · `final.data` · `prod.lammpstrj` | 최소화 + NPT 6 ps + NVT 3 ps (단축 실행) |

## 보충
`docs/checklist_and_commands.md`: v1 덱의 표 · 체크리스트 6 · 출력 4종 · 프로토콜 표 · 메탄 data 예 · 설치 규칙 전문 · 이전 버전 고정 설치 명령. `docs/install_gpu.md`: 소스 빌드 · GPU · KOKKOS(선택).

## 체크리스트
- [ ] `log.lj` 에 `Total wall time` · Density 열 일정
- [ ] `build_report.json` `pass: true` · atoms 750
- [ ] `log.toluene` Density 0.2 → 상승
- [ ] 퀴즈 5문항 (`quiz.md`)

## 못 끝냈다면
`expected_output/` 의 data · in · log 를 받고 W07 로 간다. W07 은 `in.toluene` 을 템플릿으로 쓴다.
