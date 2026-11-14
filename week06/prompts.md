# week06 Claude Code 지시: 덱 「만들어 보기」 장의 원문

사용 환경 · 순서 · 규칙: `../docs/prompt_setup.md` · `../docs/claude_code_quickstart.md` (W01 12장). 시작: 터미널 → `conda activate mdai` → `cd week06` → `claude`. LAMMPS(`lmp`) · Packmol 은 mdai 에 포함(`../environment.yml`). 지시 1개 = 대화 1개(주제가 바뀌면 `/clear`). 대괄호 [ ] 안만 바꾼다. 로그 · 입력 파일은 붙여 넣지 않는다(Claude Code 가 `out/` 에서 직접 읽음). 명령 실행 · 파일 생성은 승인 창에서 읽고 승인한다. 결과 = Claude Code 가 `out/P6-n_result.md` 로 저장. 수치의 「확인 필요」 표시는 지우지 않는다.

## P6-1 · LJ 유체 실행 · LAMMPS log 읽기 (덱 7장) → `out/P6-1_result.md`
Claude Code 가 실행하는 명령: `python3 scripts/build_lj_lammps.py` → `out/lj.data` · `in.lj`, 그 다음 `cd out && lmp -in in.lj` → `log.lj` (1초 안).
```text
scripts/build_lj_lammps.py 로 out/lj.data · out/in.lj 를 만들고 out 폴더에서 lmp -in in.lj 를 실행해라. 그다음 out/log.lj 의 thermo 표와 마지막 줄을 읽고 ① 열(Step · Temp · PotEng · KinEng · TotEng · Press · Density)마다 뜻과 units real 에서의 단위를 표로 써라. ② TotEng 의 처음과 끝 값으로 에너지 보존 오차(%)를 계산하고, NVE 에서 이 값이 뜻하는 바를 한 줄로 써라. ③ Density 가 변하지 않는 이유를 앙상블로 설명해라. ④ Loop time 과 스텝 수로 1 ns 를 돌리는 데 걸릴 시간을 추정해라. 숫자는 expected_output/log.lj 와 비교하고, 로그에 없는 값은 「확인 필요」로 표시해라. lmp 를 찾지 못하면 원인과 조치를 먼저 보고하고 내 승인 뒤 실행해라.
```
기대 답(`expected_output/log.lj`): TotEng 23.031 → 23.100 kcal/mol (0.3 %) · Density 0.2394 g/cm³ 고정(NVE · 상자 불변) · Loop time 0.021 s / 1,000 스텝 → 1 ns ≈ 21 s. 확인: 「Total wall time」 줄이 있는가 · 로그에 없는 압력 단위 환산 등을 지어내면 「확인 필요」. 흔한 오류: mdai 을 켜지 않아 `lmp` 없음 → Claude Code 가 원인 · 조치를 먼저 보고.

## P6-2 · 톨루엔 상자 실행 · 내 분자의 Packmol 입력과 in 파일 수정 포인트 (덱 19장) → `out/P6-2_result.md`
Claude Code 가 실행하는 명령: `python3 scripts/build_toluene_box.py --run-lammps lmp` → `out/toluene_box.data` · `in.toluene` · `build_report.json` · `log.toluene` (약 30초).
```text
python3 scripts/build_toluene_box.py --run-lammps lmp 를 실행하고 out/build_report.json · log.toluene 을 expected_output/ 과 비교해라. 그다음 내 재료 분자 [톨루엔 · SMILES Cc1ccccc1 · 분자량 92.14 g/mol] 을 [50] 개 넣어 초기 밀도 0.2 g/cm³ 의 정육면체 상자를 만들려 한다. ① 상자 한 변 L 을 N·M/(ρ·N_A) 의 세제곱근으로 계산해라(Å · 소수 둘째 자리). ② Packmol 입력 파일(tolerance 3.0 · seed 기록 · inside box 는 경계 2 Å 안쪽)을 out/ 에 새 파일로 써라. ③ out/in.toluene 에서 내 분자로 바꿀 때 고쳐야 할 줄 3개와 고치지 말아야 할 줄 3개를 표로 써라. scripts/ 는 고치지 말고, 근거 없는 수치는 「확인 필요」로 표시해라.
```
순서: 톨루엔 그대로 먼저 → L 33.69 Å(`build_report.json` 의 L_A)과 비교 → `[분자 · SMILES · 분자량]` · `[개수]` 를 내 재료로 바꿔 같은 대화에서 다시 지시.
기대 답: L = (50 × 92.14 / (0.2 × 6.022e23) × 1e24)^(1/3) = 33.69 Å · 고치는 줄 = read_data 파일 이름 · velocity 온도 · 시드 · run 스텝 수 / 고치지 않는 줄 = units · atom_style · boundary · pair_style · kspace · special_bonds · minimize 인수. 확인: 보고의 L 이 33.69 와 다르면 단위 환산(1 cm³ = 10²⁴ Å³)을 다시 확인하게 한다 · special_bonds 를 바꾸라고 하면 「확인 필요」(W04 23장) · 새 Packmol 입력이 `out/` 에 있고 `scripts/` 는 그대로인가(`git status`).

## (선택) 채팅형 LLM 으로 쓸 때 · 이전 원문
Claude Code 를 쓸 수 없으면 아래 이전 원문을 채팅창에 붙여 넣고, 대괄호 자리에 파일 내용을 붙인다(`../docs/prompt_setup.md` §5).

P6-1 이전 원문:
```text
아래는 LAMMPS 가 만든 log.lj 의 thermo 표와 마지막 줄이다. ① 열(Step · Temp · PotEng · KinEng · TotEng · Press · Density)마다 뜻과 units real 에서의 단위를 표로 써라. ② TotEng 의 처음과 끝 값으로 에너지 보존 오차(%)를 계산하고, NVE 에서 이 값이 뜻하는 바를 한 줄로 써라. ③ Density 가 변하지 않는 이유를 앙상블로 설명해라. ④ Loop time 과 스텝 수로 1 ns 를 돌리는 데 걸릴 시간을 추정해라. 로그에 없는 값은 「확인 필요」로 표시해라.

[여기에 log.lj 의 thermo 표(Step 줄부터 Loop time 줄까지)를 붙여 넣는다]
```
P6-2 이전 원문:
```text
내 재료 분자 [톨루엔 · SMILES Cc1ccccc1 · 분자량 92.14 g/mol] 을 [50] 개 넣어 초기 밀도 0.2 g/cm³ 의 정육면체 상자를 만들려 한다. ① 상자 한 변 L 을 N·M/(ρ·N_A) 의 세제곱근으로 계산해라(Å · 소수 둘째 자리). ② Packmol 입력 파일(tolerance 3.0 · seed 기록 · inside box 는 경계 2 Å 안쪽)을 써라. ③ 첨부한 in.toluene 에서 내 분자로 바꿀 때 고쳐야 할 줄 3개와 고치지 말아야 할 줄 3개를 표로 써라. 근거 없는 수치는 「확인 필요」로 표시해라.

[여기에 week06/out/in.toluene 내용을 붙여 넣는다]
```
