# week04 Claude Code 지시문 · 덱 「만들어 보기」 장의 원문

사용 환경: 터미널 → `conda activate mdai` → `cd week04` → `claude` (`../docs/claude_code_quickstart.md`) · 순서 · 규칙: `../docs/prompt_setup.md`. 지시문 1개 = 대화 1개(주제가 바뀌면 `/clear`). 대괄호 [ ] 안만 바꾼다. 파일은 붙여 넣지 않고 `@경로` 로 가리킨다. 결과 파일 = `out/P4-n_result.md` (Claude Code 가 저장 · 저장소 `CLAUDE.md` 규칙). 수치의 「확인 필요」 표시는 지우지 않는다.

## P4-1 · 내 분자의 GAFF2 타입 · AM1-BCC 전하 직접 생성 (덱 15장) → `out/P4-1_result.md`
MD 워크플로우(`../mdworkflow` · 지시문 M-1 · M-2)의 ① mol · ② ff 를 week04 폴더에서 실행한다. AmberTools(antechamber · parmchk2 · sqm)는 `mdai` 환경에 들어 있다(`../environment.yml`).
```text
MD 워크플로우(../mdworkflow · M-1 · M-2)로 분자 [Toluene] 의 힘장을 직접 만들어라(목록 밖 분자 = --smiles [SMILES] 와 이름). ① python ../mdworkflow/mdwf.py mol [Toluene] ② python ../mdworkflow/mdwf.py ff [Toluene] ③ ../mdworkflow/ws/ff/<이름>_gaff2.json 으로 원자별 표(번호 · 원소 · GAFF2 타입 · q · ε · σ) · 전하 합과 형식전하 · ATTN(parmchk2 가 빌린 값) 개수 · 결합 · 각 · 이면각 종류 수 ④ 톨루엔이면 @data/Toluene_gaff2.json 과 타입 · 전하 · 결합 매개변수 비교(번호 순서 무관 · 타입별). mdwf/ 는 고치지 말고, 오류가 나면 마지막 오류 줄과 원인을 보고하고 멈춰라.
```
순서: 톨루엔 그대로 먼저 지시 → `data/Toluene_gaff2.json`(참고 사례 · 연구 플랫폼 결과)과 비교 → 같은 대화에서 `[Toluene]` 을 내 재료 분자(`--smiles` 와 이름)로 바꿔 다시 지시.
기대 결과: MD 워크플로우로 만든 톨루엔 = 참고 사례와 타입 · 전하 · 결합 매개변수가 같다(ca 6 · c3 1 · ha 5 · hc 3 · Σq = −1e−6 ≈ 0 · ca q −0.077 · −0.127~−0.135 · c3 −0.054 · ha +0.130 · hc +0.044 · ca–ca K 354.25 · r₀ 1.3986 · 결합 4종 · 각 5종 · 이면각 6종 · ATTN 0). 원자 번호 순서는 다르다(MD 워크플로우는 메틸 C 가 1번) → 타입 · 전하 묶음으로 비교.
확인: Σq = 형식전하 · 15원자 전부 타입 있음. 값이 소수 셋째 자리까지 같지 않아도 된다(AM1-BCC 버전 차이). 내 재료 분자에 ATTN(parmchk2 가 빌린 값)이 남으면 그 원자 환경을 적어 두고 W06 라이브러리와 비교. 생성된 `ws/ff/<이름>_gaff2.json` 은 W06 의 MD 워크플로우 ③ build(M-3)에서 그대로 쓴다.

## P4-2 · 노트북 실행 → 컷오프 스캔 결과 읽기 (덱 22장) → `out/P4-2_result.md`
Claude Code 가 승인 후 `python ../run_nb.py notebooks/01_mixing_rules.ipynb notebooks/02_pbc_cutoff.ipynb` 로 실행(같은 계산 = `python3 scripts/ff_tools.py`) → `out/cutoff_scan.json`.
```text
@notebooks/01_mixing_rules.ipynb 와 @notebooks/02_pbc_cutoff.ipynb 를 차례로 실행하고, 생긴 out/cutoff_scan.json 을 읽어라. ① 컷오프별 절단 오차(rel_diff_vs_ref_pct)와 꼬리 보정 후 오차(rel_diff_with_tail_pct)를 표로 정리해라. ② 셀 한 변 L_A 와 2 × 컷오프 조건으로 이 상자에서 쓸 수 있는 최대 컷오프를 답해라. ③ 꼬리 보정 후 오차가 1 % 이내인 가장 작은 컷오프를 답하고 근거 행을 인용해라. 파일에 없는 값은 계산하지 말고 「확인 필요」로 표시해라. 끝나면 out/ 의 세 파일을 expected_output/ 과 비교해라.
```
기대 답: 최대 컷오프 12 Å(2 r_c 24 < L 26.207) · 1 % 이내 최소 8 Å(−0.101 %). 확인: `mixing_table.csv` 「부등식 위반 0」 · Claude Code 답이 파일의 L_A 가 아닌 다른 L 을 쓰면 「확인 필요」. 못 끝냈다면 `expected_output/cutoff_scan.json`.

## P4-3 · 내 재료의 힘장 설정 표 · in 파일 네 줄 (덱 23장) → `out/P4-3_result.md`
```text
내 재료 [SBS 개질 아스팔트 바인더]의 분자 목록 [아스팔텐 · 수지 · 방향족 · 포화분 대표 분자 + SBS 단량체]에 대해 ① 힘장(GAFF2) · 전하 방법(AM1-BCC) · 조합 규칙 · 1-4 축소 · 컷오프 · kspace 를 한 표로 ② LAMMPS in 파일의 pair_style · pair_modify · kspace_style · special_bonds 네 줄 ③ 다른 계열 힘장(ClayFF · COMPASS)이나 다른 전하 방법을 한 셀에 섞을 때 생기는 위험 3가지를 써라. 수치는 GAFF2 기본값을 쓰고 근거가 없으면 「확인 필요」로 표시해라. 컷오프 근거는 out/cutoff_scan.json(없으면 @expected_output/cutoff_scan.json)의 행을 인용해라.
```
기대 결과(참고 사례 · 연구 플랫폼 `src/forcefield/ff_stack.py` 기본 설정 · MD 워크플로우 `../mdworkflow/templates/in.protocol` 도 같은 네 줄 · special_bonds amber = lj 0 0 0.5 coul 0 0 0.833333):
```
pair_style    lj/cut/coul/long 12.0
pair_modify   mix arithmetic
kspace_style  pppm 1.0e-4
special_bonds lj 0 0 0.5 coul 0 0 0.833333
```
확인: 네 줄이 위와 같은가 · special_bonds 가 계 전체 한 줄인가 · 위험 3가지에 「접촉 거리 변화 · 응집 균형 붕괴 · 학습 편향」이 들어 있는가. 광물이 섞이면 ClayFF + 짝 물 모델(SPC/E) · 전하 척도 통일(W08 · W10).
