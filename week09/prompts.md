# week09 Claude Code 지시문 · 덱 「만들어 보기」 장의 원문

사용 환경 · 순서 · 규칙: `../docs/prompt_setup.md` · `../docs/claude_code_quickstart.md` (W01 12장). 터미널 → `conda activate mdai` → `cd week09` → `claude` → 아래 블록을 붙여 넣고 [ ] 안만 바꾼다. 파일은 지시문의 `@경로` 로 Claude Code 가 직접 읽는다(붙여 넣지 않음). 명령 실행 · 파일 복사는 승인 창에서 확인한다. 결과 파일 = `out/P9-n_result.md`. 저장소 스크립트가 기준 · Claude Code 는 스크립트 실행 · 인수 선택 · 판정 근거 · 보고 문장에 쓰고 `scripts/` 는 고치지 않는다. JSON 에 없는 값은 쓰지 않는다.

## P9-1 · 로그 → density.json → 보고 문장 (덱 8장) → `out/P9-1_result.md`
```text
python3 scripts/density_from_log.py out/prod/log.prod 를 실행하고(로그가 없으면 expected_output/prod/log.prod 를 out/prod/ 로 복사) @out/density.json 과 로그의 thermo 머리줄(Step 줄)을 읽어라. ① 내 로그의 밀도 열 이름이 [Density] 와 다르면 --col 인수를 무엇으로 줘야 하는지 ② 전반 · 후반 차(half_diff_pct)와 블록 SE 로 수렴 여부를 판정한 근거 ③ 보고 문장 1개(「ρ = 평균 ± SE g/cm³ · n 스텝 중 뒤 70 % · 수렴 여부」) ④ 수렴 전이면 다음 실행 길이 제안(2 ns 기준)을 표로 써라. JSON 에 없는 값은 지어내지 마라.

mean · block_se 를 expected_output/density.json 과 비교하고 out/P9-1_result.md 로 저장해라.
```
확인: JSON 의 mean · block_se · half_diff_pct · converged 네 값이 문장에 글자까지 같게 들어갔는가.

## P9-2 · ced.json → 두 경로 차이 점검 표 (덱 14장) → `out/P9-2_result.md`
```text
python3 scripts/ced_method_ab.py out/prod/nvt_final.data out/prod/log.prod --lmp lmp --gas-steps 20000 을 실행하고 @out/ced.json 을 읽어라(Method A 직접 · Method B 간접 차감 · δ · 차이 %). lmp 가 없으면 실행하지 말고 expected_output/ced.json 을 읽어라. ① 두 값의 차이가 10 % 를 넘는지 ② 넘는다면 원인 후보를 점검 순서대로(분자 안/사이 분리 설정 · 기상 표본 수 · 기상 상자 크기 대 컷오프 · 꼬리 보정 · PPPM 유무 · 밀도 수렴 여부) 표로 ③ 데이터셋 전체에서 어느 방식을 고정할지와 그 이유 1줄 ④ 보고 문장(「CED_B = … MJ/m³ · δ = … · 수렴 여부」)을 써라. JSON 에 없는 값은 지어내지 마라.

diff_pct 를 expected_output/ced.json 과 비교하고 out/P9-2_result.md 로 저장해라.
```
확인: diff_pct 와 고정 방식(B)이 함께 적혔는가 · 기상 상자 100 Å ≥ 2 × 컷오프 12 Å 인지 언급했는가.

## P9-3 · results.csv 열 ↔ 내 폴더 파일 대응표 (덱 26장) → `out/P9-3_result.md`
```text
python3 scripts/postprocess_all.py --exp-id toluene50_w09 --lmp lmp 를 실행하고(lmp 가 없으면 expected_output/prod 를 out/prod 로 복사한 뒤 --skip-md) @out/results.csv 머리줄(열 이름)과 내 실험 폴더 [out/prod] 의 파일 목록을 읽어라. ① 내 파일(로그 · 응력 · data) 이 체인의 어느 입력에 대응하는지 표(체인 입력 이름 → 내 파일 이름 → 바꿔야 할 인수) ② 열마다 값의 출처 스크립트와 단위 ③ flags 열이 비려면 무엇이 충족되어야 하는지(밀도 전반 · 후반 차 · η 평탄 · Tg 온도점 수) ④ 열 이름을 바꾸면 안 되는 이유 1줄을 써라. 목록에 없는 파일은 지어내지 마라.

results.csv 를 expected_output/results.csv 와 비교하고 out/P9-3_result.md 로 저장해라.
```
확인: 열 이름이 results.csv 와 글자까지 같은가 · 「열 이름 = W16 데이터베이스 스키마」 가 이유로 적혔는가.
