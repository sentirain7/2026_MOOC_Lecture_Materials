# week10 Claude Code 지시문 · 덱 「만들어 보기」 장의 원문

사용 환경 · 순서 · 규칙: `../docs/prompt_setup.md` · `../docs/claude_code_quickstart.md` (W01 12장). 터미널 → `conda activate mdai` → `cd week10` → `claude` → 아래 블록을 붙여 넣고 [ ] 안만 바꾼다. 파일은 Claude Code 가 직접 읽는다(붙여 넣지 않음). LAMMPS · Packmol 실행은 승인 창에서 확인한다(인장 1건 ≈ 40초). 결과 파일 = `out/P10-n_result.md`. 수치의 「확인 필요」 · 「미정」 표시는 지우지 않는다.

## P10-1 · 분리일 검산 · 보고 한 줄 (덱 14장) → `out/P10-1_result.md`
지시문이 실행하는 명령: `python3 scripts/pull_test.py --water 0 --tag dry --build` → `python3 scripts/work_of_separation.py out/dry/pull.csv` → `out/dry/wsep.json` (같은 계산 = `python ../run_nb.py notebooks/01_pull_test.ipynb`).
```text
scripts/pull_test.py --water 0 --tag dry --build → work_of_separation.py out/dry/pull.csv 를 실행하고 @out/dry/wsep.json 을 읽어라(단면적 A · 그립 속도 · 스텝 수 포함). ① 응력 환산(1 kcal/mol/Å ÷ A Å² → MPa)과 면적 환산(1 MPa·Å = 0.1 mJ/m²)이 맞는지 식으로 검산하고 ② W_mech(면적)와 W_E(에너지 차)가 왜 다른지 · 열 요동 sd, 미분리, 규약 · 세 줄로 설명하고 ③ 보고 한 줄 「W_sep = 값 ± (불확실) mJ/m² · 규약 · A · 속도 · 시드 수」를 써라. 시드가 1개면 ± 는 「미정(n = 1)」 으로 두고 지어내지 마라. 내 재료 [석영 / 톨루엔 → SBS 개질 바인더]로 바꿀 때 어느 인수를 바꿔야 하는지 한 줄 덧붙여라.

W_mech 를 expected_output/dry/wsep.json 과 비교하고 out/P10-1_result.md 로 저장해라.
```
확인: 69.4786 / 627.1 × 100 = 11.08 MPa per kcal/mol/Å · W_mech = 0.1 × 사다리꼴 적분 · 「n = 1 · ± 미정」 이 그대로 남아 있는가.

## P10-2 · 건조 · 습윤 비교표 · ER 정의 (덱 21장) → `out/P10-2_result.md`
지시문이 실행하는 명령(습윤 셀): `python3 scripts/pull_test.py --water 10 --tag wet` (셀 = `data/wet_final.data` · 저장소 제공 · 없거나 새로 만들려면 `--build`) → `work_of_separation.py out/wet/pull.csv` → `fracture_mode.py out/wet/pull.dump` (건조도 `fracture_mode.py out/dry/pull.dump` 까지).
```text
습윤 셀(--water 10 --tag wet)로 scripts/pull_test.py → work_of_separation.py → fracture_mode.py 를 실행하고(건조 dry 도 fracture_mode 까지) out/dry · out/wet 의 wsep.json · fracture.json 4개를 읽어라. ① 비교표(열: 조건 · 원자 수 · σ_peak MPa · W_mech mJ/m² · 파괴 모드 · 노출률 e · 규약 · 속도 · 시드 수)를 만들고 ② 에너지비를 정의 ② 보존비 W_wet/W_dry 로 계산하되 정의 ①(W_adh/W_deb)은 W_deb 가 없으니 「미정」으로 두고 ③ 시드가 1개씩이므로 「유의한 차이」라는 말을 쓰지 말고 다음 실행에 필요한 시드 수를 25장 기준(스크리닝 3 · 확정 5)으로 적어라. 수치는 파일에 있는 값만 쓴다.

W_mech 를 expected_output 과 비교하고 out/P10-2_result.md 로 저장해라.
```
확인: 규약 · 속도 · 시드 수 열이 있는가 · ER 정의 ① 이 「미정」 인가 · 「유의한 차이」 표현이 없는가.

## P10-3 · 파괴 모드 판정 · 보고 문단 (덱 26장) → `out/P10-3_result.md`
```text
python3 scripts/fracture_mode.py 를 out/dry/pull.dump · out/wet/pull.dump 에 차례로 실행하고, 건조 · 습윤의 분리일(@out/dry/wsep.json · @out/wet/wsep.json)과 파괴 모드 판정(fracture.json)을 읽어라. 25장의 보고 형식으로 한 문단을 써라: ① 조건마다 「W_sep = 값 ± CI (n) · 규약 · 단면 · 속도 · 힘장 · 평형/생산 길이」 한 줄씩 · 시드가 1개면 CI 를 「미정(n = 1)」 으로 ② 파괴 모드를 e · t_res · 임계(50 % · z1)로 설명 ③ 두 조건의 차이는 「유의성 미정」 으로 적고 ④ 다음 실행 계획(시드 3개 · 속도 10배 낮춤 · 석영 표면 수산화 적용)을 세 줄로 써라. 파일에 없는 수치는 쓰지 마라.

mode 를 expected_output/{dry,wet}/fracture.json 과 비교하고 out/P10-3_result.md 로 저장해라.
```
확인: 모드 설명이 fracture.json 의 rule 과 같은가 · CI 에 지어낸 숫자가 없는가 · 프로토콜 5항목(규약 · A · 속도 · 힘장 · 길이)이 모두 있는가.
