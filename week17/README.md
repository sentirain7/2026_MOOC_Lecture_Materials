# week17 · MD 워크플로우 조립: 분자에서 물성까지 (모듈 M5 · 파이프라인)

| 항목 | 내용 |
|---|---|
| 덱 | `slides/W17_MD워크플로우조립.html` (v3 · 27장 · 54분 · 4차시: 17-1 왜 워크플로우인가 · 17-2 분자와 힘장 · 17-3 상자와 실행 · 17-4 물성 · 검증 · 다음 주) |
| 학습목표 | ① MD 워크플로우 6단계(mol → ff → build → run → analyze → store)의 넣는 것 · 나오는 것 파일과 자동 확인 항목을 말한다 ② SMILES 한 줄에서 GAFF2 · AM1-BCC 힘장 JSON 을 만들고 자동 검사 4(전하 합 · 타입 빠짐 · 빌린 값 · 개수)로 판정한다 ③ 초기 밀도에서 상자 한 변을 역산하고 표준 프로토콜 130 ps 와 실패 규칙 R1 · R2 를 설명한다 ④ 밀도(블록 표준오차) · CED(벌크 − 분자 하나씩 · 재계산)를 구해 NIST 실측 · 반복 흔들림 판정 폭으로 판정한다 ⑤ 후보 8개 시험 결과에서 두 표적을 동시에 맞추는 일이 왜 W18 폐루프로 넘어가는지 말한다 |
| 선수 지식 | W04 원자 타입 · 부분전하 · W05 블록 평균 · NPT · W06 Packmol 상자 · W07 실패 감지 · W09 CED 정의(Method A) |
| 소요 시간 | 강의 54분 + 실습 약 30분(LAMMPS 실행 약 5분 · 4코어) |
| 새 용어 (6) | 워크플로우 · 부분전하 할당 · 빌린 매개변수(ATTN) · 생산 구간 · 재계산(rerun) · 반복 흔들림 → `../GLOSSARY.md` |

## 실행 환경 · Claude Code (기본)
터미널 → `conda activate mdai` → `cd 2026_MOOC_Lecture_Materials/week17` → `claude` (설치 · 조작 = `../docs/claude_code_quickstart.md` · 강좌 규칙 = `../CLAUDE.md` 자동 적용 · 설치 지시문 I-2 = `../docs/install_prompts.md`). 이 주차의 도구는 저장소 맨 위의 `../mdworkflow/` 이다(설명 = `../mdworkflow/README.md`). 모든 명령은 week17 폴더에서 `python ../mdworkflow/mdwf.py <단계> … --ws out/ws` 로 실행하고, 결과는 `out/ws/` (mol · ff · cells · runs · db) 에 남는다. `../mdworkflow/mdwf/` 의 강좌 코드는 고치지 않는다.

필요한 실행 파일(mdai 에 포함): RDKit · AmberTools(antechamber · parmchk2 · tleap · sqm · packmol) · parmed · LAMMPS(`lmp`, OpenMP). 확인: `which antechamber packmol lmp`.

## Claude Code 지시문 (덱 「만들어 보기」 장)
`prompts.md`: M-1 분자 3D · M-2 힘장 만들기와 검사(13장) · M-3 단분자 상자 · M-4 실행과 판독(19장) · M-5 밀도 · CED 판정 · M-6 결과 표(25장). 결과 = `out/M-n_result.md`. 기준 원문 = `../mdworkflow/prompts.md` (week17 경로로 옮긴 판). 사용 환경 = `../docs/prompt_setup.md`.

## 실습 순서
1. **분자 · 힘장** (17-2 · 약 5분) M-1 · M-2 → `out/ws/mol/Toluene.json` · `out/ws/ff/Toluene_gaff2.json` · AM1-BCC 0.2 s. 결과를 `expected_output/Toluene_gaff2.json` 과 `../week04/data/Toluene_gaff2.json` 에 대조.
2. **상자** (17-3) M-3 → `out/ws/cells/tol100/` (Toluene 100분자 · 1,500 원자 · ρ0 0.5 → L 31.278 Å). M-2 를 건너뛰었으면 `expected_output/Toluene_gaff2.json` 을 `out/ws/ff/` 로 복사한 뒤 진행.
3. **실행** (17-3 · 약 5분 · 4코어) M-4 → `out/ws/runs/tol100/` (log.lammps · prod.lammpstrj · status.json). seed 4928460 = 기준 결과와 같은 값.
4. **물성 · 기록** (17-4) M-5 · M-6 → `props.json` · `ced_frames.csv` · `out/ws/db/results.csv` 한 줄. LAMMPS 를 돌리지 못했으면 `expected_output/tol100/props.json` 으로 M-5 의 판정 표만 만든다.
5. **선택** 같은 순서를 n-데칸(`Decane --smiles CCCCCCCCCC` · 47분자) 으로 반복해 덱 23장의 +21 % 를 재현. 한 번에: `python ../mdworkflow/mdwf.py all --id dec47 --comp Decane=47 --threads 4 --ws out/ws` (mol · ff 는 먼저).

Claude Code 없이 터미널에서 직접(week17 폴더 · mdai): `python ../mdworkflow/mdwf.py mol Toluene --ws out/ws` → `ff Toluene` → `build --id tol100 --comp Toluene=100` → `run tol100 --threads 4 --seed 4928460` → `analyze tol100` → `store tol100 --source nist_toluene` (모두 `--ws out/ws`).

## 확인
- 힘장: `checks.pass` true · 전하 합 −0.000001 · ATTN 0 · 결합 15 · 각 24 · 이면각 30 · 비정규 6 · W04 참고 결과와 타입 · 전하 · 결합 값 같음(원자 순서만 다름)
- 상자: Packmol 게이트 1번째 시도 통과 · 분자간 최소 거리 ≥ 1.8 Å (기준 2.166 Å) · 전하 합 |Σq| < 0.01
- 실행: `status.json` 의 attempts 1개 · ok true · 프레임 21
- 물성: 내 값 − 기준 값(`expected_output/tol100/props.json` 0.8703 · 352.3) 이 판정 폭 밀도 ±0.015 g/cm³ · CED ±15 MJ/m³ 안 · 전반/후반 밀도 차 < 1 %
- 기록: `results.csv` 의 열 24개 · 같은 id 재기록 거부

## 제출
`out/ws/ff/Toluene_gaff2.json` · `out/ws/cells/tol100/cell.json` · `out/ws/runs/tol100/status.json` · `props.json` · `out/ws/db/results.csv` · `out/M-1_result.md` ~ `out/M-6_result.md` · 퀴즈 `quiz.md` 답

## 못 끝냈다면
`expected_output/` 의 JSON · CSV 로 W18 진행 가능(W18 재생 모드 = 기준 MD 값 사용 · `../loop/README.md`).

## 숫자의 출처
- 모든 실행값: `expected_output/` (2026-11-14 · mdai · LAMMPS 22 Jul 2025 - Update 6 · OpenMP 4코어 · 표준 프로토콜 130 ps · seed 4928460) · 각 파일 설명 = `expected_output/README.md`
- 힘장 검증표 · 반복 흔들림 · 판정 폭: `../mdworkflow/README.md` (톨루엔 · n-데칸 NIST 298 K · 밀도 = Lemmon & Span 2006 상태식 · ΔvapH = Majer–Svoboda 식 · NIST Chemistry WebBook)
- 단독 실행 속도 455 스텝/s(약 5분) · 동시 실행 벽시계(검증 3개 405 ~ 454 s · 후보 8개 431 ~ 509 s) · 환경 버전: 0단계 사전 검증 기록
- 표적(밀도 1.018 g/cm³ · CED 354.2 MJ/m³ · 폭 ±0.02 · ±20) · 후보 표(168개 · 원자 15 ~ 96): `../loop/README.md` · `../loop/config/loop.yaml`
- 후보 8개 이름 = 핵-사슬 수 x 사슬 탄소 수 (naph = naphthalene · phen = phenanthrene · dbt = dibenzothiophene · bt = benzothiophene · quin = quinoline · tet = tetralin) · SMILES 규칙 = `../loop/scripts/library.py`
- 덱의 W04 대조: `../week04/data/Toluene_gaff2.json` ↔ `expected_output/Toluene_gaff2.json`
