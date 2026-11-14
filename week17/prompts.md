# week17 Claude Code 지시 · 덱 「만들어 보기」 장의 원문 (M-1 ~ M-6)

사용 환경 · 순서 · 규칙: `../docs/prompt_setup.md` (W01 12장). 터미널 → `conda activate mdai` → `cd 2026_MOOC_Lecture_Materials/week17` → `claude` → 아래 블록을 붙여 넣고 [ ] 안만 바꾼다. 지시 1개 = 대화 1개(주제가 바뀌면 `/clear`). 명령 실행은 승인 창에서 확인한다. 결과 파일 = `out/M-n_result.md`.
기준 원문 = `../mdworkflow/prompts.md` (mdworkflow 폴더에서 실행하는 판) · 이 파일은 week17 폴더에서 실행하도록 경로를 옮긴 판이다: 명령 = `python ../mdworkflow/mdwf.py …` · 작업 폴더 = `--ws out/ws`.
역할 나눔: 계산은 `../mdworkflow/mdwf/` 의 강좌 코드가 한다(고치지 않음) · Claude Code 는 실행 · 파일 읽기 · 표 · 판정 근거 · 비교 · 파일에 없는 값은 쓰지 않는다.

## M-1 · 분자 3D (덱 13장) → `out/M-1_result.md`
```text
python ../mdworkflow/mdwf.py mol [Toluene] --ws out/ws 를 실행해라(목록에 없는 분자 = [이름] --smiles [SMILES]). out/ws/mol/<이름>.json 의 원자 수 · 분자식 · 분자량 · 형식전하 · 입체 중심 수 · MMFF 수렴을 표로 적고, 수소 추가 전후 원자 수 차이의 이유를 한 줄로 써라. → out/M-1_result.md
```
확인: 톨루엔 원자 15(무거운 원자 7 + 수소 8) · 분자량 92.141 · 형식전하 0.

## M-2 · 힘장 만들기와 검사 (덱 13장) → `out/M-2_result.md`
```text
python ../mdworkflow/mdwf.py ff [Toluene] --ws out/ws 를 실행해라. out/ws/ff/<이름>_gaff2.json 과 로그를 읽어 ① 원자별 GAFF2 타입 · 전하 ② 전하 합 ③ 빌린 값(ATTN) 개수 ④ 결합 · 각 · 이면각 개수를 표로 적고, 톨루엔이면 @../week04/data/Toluene_gaff2.json 과 타입 · 전하를 비교해라. ../mdworkflow/mdwf/ 는 고치지 마라. → out/M-2_result.md
```
확인: checks 4값(전하 합 −0.000001 · DU 0 · ATTN 0 · 결합 15 · 각 24 = prmtop)이 `expected_output/Toluene_gaff2.json` 과 같은가 · W04 대조에서 타입 · 전하 차 0 · 원자 순서만 다름.

## M-3 · 단분자 상자 (덱 19장) → `out/M-3_result.md`
```text
python ../mdworkflow/mdwf.py build --id [tol100] --comp [Toluene=100] --ws out/ws 를 실행해라. cell.json 의 분자 수 · 원자 수 · ρ0 · 한 변 L · Packmol 시도 · 분자간 최소 거리 · 전하 합을 표로 적고, L = (N·M/(ρ0·N_A))^(1/3) 손계산 값과 비교해라. → out/M-3_result.md
```
확인: L 31.278 Å · 원자 1,500 · 시도 1 · 최소 거리 2.166 Å (기준 1.8 Å) · Σq −0.0001 (`expected_output/tol100/cell.json`). M-2 를 건너뛰었으면 먼저 `expected_output/Toluene_gaff2.json` 을 `out/ws/ff/` 로 복사.

## M-4 · 실행과 판독 (덱 19장) → `out/M-4_result.md`
```text
python ../mdworkflow/mdwf.py run [tol100] --threads [4] --seed 4928460 --ws out/ws 를 실행해라(약 5분). status.json · log.lammps 를 읽어 구간 A ~ P 의 끝 온도 · 압력 · 밀도와 벽시계 · 코어 수 · 실패 규칙 사용 여부를 표로 적어라. 오류면 마지막 ERROR 줄과 R1 · R2 판정만 쓰고 멈춰라. → out/M-4_result.md
```
확인: attempts 1개 · ok true · exit 0 · 프레임 21 · 벽시계 404.6 s(기준 = 3개 동시 실행 · 단독이면 약 5분) · 아니면 R1 · R2 중 어느 쪽인가.

## M-5 · 밀도 · CED 판정 (덱 25장) → `out/M-5_result.md`
```text
python ../mdworkflow/mdwf.py analyze [tol100] --ws out/ws 를 실행해라. props.json · ced_frames.csv 의 밀도 ± · 전반/후반 차 · CED ± · δ 를 적고, expected_output/[tol100]/props.json 과의 차를 판정 폭(밀도 ±0.015 · CED ±15)으로, NIST 실측(0.86238 g/cm³ · 332.5 MJ/m³)과의 차를 % 로 적어라. 차이의 이유 두 줄. → out/M-5_result.md
```
확인: 기준 0.8703 ± 0.0024 · 352.3 ± 2.2 · δ 18.77 · 실측 대비 +0.9 % · +6 % · 내 값 − 기준 값이 판정 폭 안 · 밖이면 코어 수 · seed · 프로토콜부터 확인. M-4 를 못 돌렸으면 `expected_output/tol100/props.json` · `ced_frames.csv` 를 읽어 같은 표만 만든다.

## M-6 · 결과 표 (덱 25장) → `out/M-6_result.md`
```text
python ../mdworkflow/mdwf.py store [tol100] --source [nist_toluene] --ws out/ws 를 실행하고 out/ws/db/results.csv 를 표로 보여 줘라. expected_output/validation_results.csv 의 같은 id 줄과 비교하고, 같은 id 재기록 거부 · 실패 기록 보존의 이유를 한 줄씩 써라. → out/M-6_result.md
```
확인: 열 24개 · n_atoms 1500 · seed 4928460 · ok True · source nist_toluene · 같은 명령 재실행 → 거부 메시지 → 새 id 로 기록.

## 한 번에 (③ ~ ⑥ · 선택)
```text
python ../mdworkflow/mdwf.py all --id [dec47] --comp [Decane=47] --threads [4] --ws out/ws 를 실행하고(mol · ff 는 먼저 · Decane 은 --smiles CCCCCCCCCC), 끝나면 M-5 와 같은 표를 만들어라. 기준 = expected_output/[dec47]/props.json · NIST 실측 0.72664 g/cm³ · 249.7 MJ/m³.
```
