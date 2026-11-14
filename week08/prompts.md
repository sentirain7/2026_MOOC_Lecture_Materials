# week08 Claude Code 지시문: 덱 「만들어 보기」 장의 원문

사용 환경 · 순서 · 규칙: `../docs/prompt_setup.md` · `../docs/claude_code_quickstart.md` (W01 12장). 터미널에서 `conda activate mdai` → `cd week08` → `claude` 를 열고 아래 지시를 붙여 넣는다 · [ ] 안만 바꾼다. 파일은 붙여 넣지 않는다(`@경로` 로 Claude Code 가 직접 읽음). 노트북 · 스크립트 실행은 승인 창에서 확인한다. 결과 파일 = `out/P8-n_result.md`(Claude Code 가 저장). `scripts/` 는 고치지 않는다. 수치의 「확인 필요」 표시는 지우지 않는다.

## P8-1 · 내 재료의 3층 셀 설계표 (덱 15장) → `out/P8-1_result.md`
지시가 `python ../run_nb.py notebooks/01_stack_cell.ipynb` 로 노트북을 실행한다(같은 계산: `python3 scripts/stack_cell.py --packmol packmol --lmp lmp`) → `out/stack_summary.json`.
```text
`python ../run_nb.py notebooks/01_stack_cell.ipynb` 로 노트북을 실행하고, 생성된 out/stack_summary.json(3층 계면 셀 요약)을 expected_output 과 비교해라. 이 요약으로 내 재료 [광물: 석영 / 바인더: SBS 개질 아스팔트 / 물 층: 있음] 에 맞춰 ① 층별 설계표(열: 층 · 재료 · 힘장 · 전하 방법 · 두께 Å · 원자 수 · 고정 여부)를 쓰고 ② 셀 한 변이 2 × 컷오프(24 Å) 이상인지, 진공이 30 Å 이상인지, 슬래브 전하 합이 0 인지 판정하고 ③ 바인더를 톨루엔에서 내 재료 분자로 바꿀 때 stack_cell.py 의 어느 인수 · 어느 입력 파일을 바꿔야 하는지 적어 out/P8-1_result.md 에 저장해라. scripts/ 는 고치지 말고, 요약에 없는 값은 「확인 필요」로 표시해라.
```
기대 답(기본값): Lx 24.565 · Ly 25.529 → 변/2rc 1.024 ≥ 1 · 진공 30 Å · 슬래브 540원자 전하 합 0 · 물 209분자(10 Å) · 톨루엔 20분자(24.4 Å · ρ0 0.2) · 총 1,467원자. 확인: 「슬래브 고정 = fix setforce」 · 「물 = SPC/E(ClayFF 짝)」 이 표에 있는가.

## P8-2 · FF-neutral 토폴로지 → 힘장별 타입 표 (덱 16장) → `out/P8-2_result.md`
```text
`python ../run_nb.py notebooks/02_route_and_check.ipynb` 로 노트북을 실행해라. 이어서 `@data/topology_toluene.json`(톨루엔 FF-neutral 토폴로지 · 원소 · 좌표 · 결합 차수 · 분자 ID, 타입 · 전하 없음)의 atoms · bonds 만 보고 ① 원자마다 GAFF2 타입(ca · c3 · ha · hc 규칙: 방향족 C = ca · sp³ C = c3 · 방향족 C 의 H = ha · sp³ C 의 H = hc)과 COMPASS 타입(ca→c3a · c3→c4 · ha/hc→h1)을 표로 붙여라(열: id · 원소 · GAFF2 · COMPASS · ReaxFF). ② 타입 수를 세어라. ③ GAFF2 와 COMPASS 를 한 셀에 섞을 수 없는 이유를 함수 형태 · 조합 규칙 · 1-4 축소 세 줄로 써라. 전하 · ε · σ 는 토폴로지에 없으니 쓰지 말고 「라우팅에서 붙임」이라고 적어라. 표를 다 만든 뒤에만 out/routed_toluene.json 과 비교하고 out/P8-2_result.md 에 저장해라.
```
기대 답: ca 6 · c3 1 · ha 5 · hc 3 (= `out/routed_toluene.json` · 아티팩트 일치). 확인: ReaxFF 열이 원소만(C · H)인가 · 전하를 지어내지 않았는가.

## P8-3 · 내 in 파일의 혼용 위험 점검 (덱 24장) → `out/P8-3_result.md`
지시가 `python3 scripts/check_mix.py <in 파일> <요약 JSON>` 을 두 번 실행한다 → `out/check_mix_*.json` · [ ] 를 내 in 파일로 바꾸면 내 입력 점검.
```text
`scripts/check_mix.py` 를 [out/in.stack + out/stack_summary.json] 과 [data/in_bad_mix.example + out/bad_summary.json] 으로 한 번씩 실행해라. 각 in 파일과 판정 out/check_mix_*.json(5규칙 ✓/✗)을 읽고 ✗ 인 규칙마다 ① 어느 줄이 원인인지 ② 왜 물리적으로 문제인지(함수 형태 · 조합 규칙 · 전하 척도 · 1-4 축소 · 층상 셀 중 하나로) ③ 고치는 한 줄(또는 「한 셀에 둘 수 없음 · 영역 분할」)을 표로 써라. 모든 규칙이 ✓ 이면 「혼용 없음」 한 줄과 남은 검증 항목(단성분 밀도 · 혼합 밀도 · 계면 RDF · 분리일 · 전이성)을 써라. 결과는 out/P8-3_result.md 에 저장하고 판정을 expected_output 과 비교해라.
```
기대 답: `in.stack` → 5 ✓ · `data/in_bad_mix.example` → 5 ✗(12-6 + 9-6 + buck hybrid · mix 2개 · QEq 동거 · special_bonds 2줄 · slab 없음 · 진공 12 Å). 확인: 고치는 줄이 「한 셀 안 힘장 하나 · 전하 방법 하나 · special_bonds 하나」(W04 25장) 를 지키는가.

---
(선택) 채팅형 LLM 으로 할 때: 지시의 `@경로` · 결과 파일 내용을 지시 끝에 붙여 넣고, 받은 표를 같은 이름의 결과 파일로 저장한다(`../docs/prompt_setup.md` §5).
