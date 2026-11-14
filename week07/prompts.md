# week07 Claude Code 지시문: 덱 「만들어 보기」 장의 원문

사용 환경 · 순서 · 규칙: `../docs/prompt_setup.md` · `../docs/claude_code_quickstart.md` (W01 12장). 터미널에서 `conda activate mdai` → `cd week07` → `claude` 를 열고 아래 지시를 붙여 넣는다 · [ ] 안만 바꾼다. 파일은 붙여 넣지 않는다(`@경로` 로 Claude Code 가 직접 읽음). 명령 실행 · 파일 수정은 승인 창에서 확인한다. 결과 파일 = `out/P7-n_result.md`(Claude Code 가 저장). 저장소 스크립트(`scripts/`)가 기준 · 변형은 `out/` 아래 새 파일로만.

## P7-1 · 내 매개변수 표에 열 추가 (덱 8장) → `out/P7-1_result.md`
```text
`python3 scripts/render_inputs.py` 를 실행하고 out/inputs/manifest.json 의 해시 6개를 expected_output 과 비교해라. 이어서 `@data/in.lj.template` 와 `@data/params.csv` 를 읽고, 표에 열 [rho](격자 밀도 · 0.6 ~ 0.9) 를 추가해 템플릿의 `lattice fcc 0.8` 이 `lattice fcc {rho}` 가 되도록 ① 템플릿에서 바뀌는 줄 ② 표의 새 열과 6행의 값(T 3 × 시드 2 는 그대로) ③ render_inputs.py 는 고치지 않아도 되는 이유(str.format 이 열 이름을 자리표시로 쓴다) 를 표로 정리해 out/P7-1_result.md 에 저장해라. data/ · scripts/ 는 고치지 말고, 값을 지어내지 말고 범위 밖이면 「확인 필요」로 표시해라.
```
확인: `manifest.json` 해시 6개 = `expected_output/inputs/manifest.json` · 템플릿에서 바뀐 줄이 1줄뿐인가 · 표의 새 열 이름이 템플릿 자리표시와 글자까지 같은가 (다르면 KeyError).

## P7-2 · 7회 실행 · 실패 로그에서 원인 · 조치 찾기 (덱 14장) → `out/P7-2_result.md`
```text
`python3 scripts/run_batch.py --lmp lmp` 와 `python3 scripts/parse_log.py` 를 차례로 실행하고 out/runs/status.csv 를 expected_output 과 비교해라. 이어서 실패한 실행의 log.lammps 끝 40줄을 읽고, run_batch.py 의 실패 감지 규칙 4개(ERROR 줄 · Lost atoms · nan/inf · 종료 코드 ≠ 0) 기준으로 ① 어느 규칙에 걸렸는지 ② 멈춘 스텝과 그때의 thermo 값 ③ 원인 후보 2개(물리적 · 설정) ④ 자동 조치(Δt 절반 1회)가 맞는 처방인지, 아니면 사람이 봐야 하는지를 표로 정리해 out/P7-2_result.md 에 저장해라. 로그에 없는 값은 지어내지 마라.
```
확인: `status.csv` 7행 · ok 6 · lost_atoms 1 · 재시도 Δt 0.015 · 멈춘 스텝 · 값이 로그와 글자까지 같은가 · 「사람이 봐야 한다」 는 판정이 있으면 근거가 적혀 있는가.
대화 없이 한 번 실행: `claude -p "[out/runs/status.csv 를 요약해]"` → 결과 출력 후 종료.

## P7-3 · 간단 생성기에 규칙 추가 (덱 22장) → `out/P7-3_result.md`
```text
`@scripts/run_batch.py` 는 실패하면 Δt 를 절반으로 한 번 재시도한다. 규칙을 하나 추가하려 한다: [재시도 뒤에도 실패하면 시드를 바꿔 한 번 더] . ① 바꿔야 할 함수와 줄 ② 추가될 status.csv 의 행 형태(시도 번호 3) ③ 무한 반복을 막는 상한을 어디에 두는지 ④ 이 규칙이 통하는 실패 유형과 통하지 않는 유형(결정론적 실패)을 표로 써서 out/P7-3_result.md 에 저장해라. scripts/ 는 고치지 말고, 코드 전체를 다시 쓰지 말고 바뀌는 부분만 보여라.
```
확인: 재시도 상한이 명시되어 있는가 · 「결정론적 실패에는 시드 변경이 소용없다」 가 들어 있는가 (원본 05주차 #18) · `scripts/run_batch.py` 가 바뀌지 않았는가(`git status`).

---
(선택) 채팅형 LLM 으로 할 때: 지시의 `@경로` 파일 내용을 지시 끝에 붙여 넣고, 받은 표를 같은 이름의 결과 파일로 저장한다(`../docs/prompt_setup.md` §5).
