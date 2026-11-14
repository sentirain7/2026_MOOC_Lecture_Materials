# week11 Claude Code 지시문 · 덱 「만들어 보기」 장의 원문

사용 환경 · 순서 · 규칙: `../docs/claude_code_quickstart.md` · `../docs/prompt_setup.md` (W01 12장).
순서: 터미널 → `conda activate mdai` → `cd week11` → `claude` → 아래 지시를 붙여 넣고 [ ] 안만 바꾼다 → 명령 실행 · 파일 저장 승인 창을 읽고 승인.
파일은 붙여 넣지 않는다(지시의 경로 · `@경로` 로 Claude Code 가 직접 읽음). 결과 파일 = `out/P11-n_result.md`(Claude Code 가 저장). 수치의 「확인 필요」 표시는 지우지 않는다.

## P11-1 · 내 바인더의 성능 표적 표 (덱 8장) → `out/P11-1_result.md`
```text
나는 [PG 64-22 등급의 도로 포장용 아스팔트 바인더]를 다룬다. ① 성능 요구 3가지(고온 소성변형 · 저온 균열 · 수분 손상/노화)마다 실험 지표(DSR 의 G*/sinδ · G*·sinδ · BBR 의 S · m-value 등)와 대응하는 MD 산출량(점도 η(T) · 완화 탄성률 G(t) · Tg · CED · 계면 분리일 중)을 표로 써라(열: 성능 · 실험 지표 · 시험 온도 · MD 산출량 · 방향 최대/최소). ② 내 기후([연평균 최고 60 °C · 최저 −20 °C])에서 PG 고온 · 저온 등급 숫자를 정하고 이유 한 줄. ③ 표적마다 W09 · W10 어느 주차에서 계산하는지 적어라. 수치 기준값은 주지 않았으니 「확인 필요」로 표시하고, 결과는 out/P11-1_result.md 로 저장해라.
```
확인: 표적마다 방향(최대/최소)이 있는가 · PG 숫자 두 개가 기후와 맞는가 · 기준값에 「확인 필요」가 붙어 있는가.

## P11-2 · 측정 SARA → 13분자 개수표 검토 (덱 15장) → `out/P11-2_result.md`
Claude Code 가 실행하는 명령(승인 후): `python3 scripts/composition_to_counts.py --sara [11,38,31,20] --atoms 3000 --tag mine` → `out/composition_report_mine.json` · `out/mine.pdb`.
```text
scripts/composition_to_counts.py 를 내 SARA 측정값 --sara [11,38,31,20] (S · A · R · As wt%) --atoms 3000 --tag mine 으로 실행하고 out/composition_report_mine.json(13분자 개수표)을 읽어라. ① 분획별 목표 wt% 와 실제 wt% · 오차를 표로 정리하고 오차가 1 % 를 넘는 분획이 있으면 어느 분자의 개수를 ±1 바꾸면 줄어드는지 제안해라. ② H/C · S/C 를 reference_tables 의 AAA-1 · AAK-1 · AAM-1 과 비교해 내 조성이 어느 참조 바인더에 가까운지 한 줄로. ③ 상자 길이 L 과 원자 수가 W06 규칙(L/2 > 12 Å · 수천 원자)에 맞는지 판정해라. 개수표 · 스크립트는 고치지 말고 제안만 써라. 항목은 @expected_output/composition_report_mix.json 과 대조하고, 결과는 out/P11-2_result.md 로 저장해라.
```
기대 답(15/45/25/15 예시): 40분자 · 3,220원자 · 오차 −0.2/0.0/−0.6/+0.8 · H/C 1.423 · S/C 0.0114 → AAM-1(1.452)과 AAA-1(1.373) 사이 · L 53.4 Å → L/2 26.7 > 12. 확인: 제안이 「분자 1개 ±1」 수준인가 · 참조 바인더 비교에 근거(H/C 숫자)가 있는가.

## P11-3 · 내 첨가제 SMILES → 기술자 · 힘장 · 함량 표 (덱 20장) → `out/P11-3_result.md`
`out/additive_library.csv`(23종)가 없으면 Claude Code 가 `python3 scripts/additive_library.py` 를 먼저 실행한다(승인 후).
```text
@out/additive_library.csv 의 열 이름과 앞 3행을 읽어라(없으면 scripts/additive_library.py 를 먼저 실행). 내 첨가제 [이름: 폴리인산 PPA / SMILES: OP(=O)(O)OP(=O)(O)O] 를 같은 형식의 1행으로 만들어라 · 열: additive_id · name · group(고분자 개질제 / 계면 · 부착 증진 / 왁스 · 상변화 / 나노 · 무기 중) · formula · MW · logP · TPSA · aromatic_C_frac · polar_atoms · ff(gaff2 / clayff / 확인 필요) · wt_range(실무 배합 범위 · 출처 없으면 「확인 필요」). 기술자 값은 RDKit 으로 계산해야 하니 네가 추정한 값에는 「추정」을 붙이고, 다시 계산할 명령 한 줄을 끝에 써라. 결과는 out/P11-3_result.md 로 저장하고, data/ 파일 수정은 내 승인 뒤에만 해라.
```
확인: ff 열이 비어 있지 않은가(무기 = clayff · 유기 = gaff2) · 「추정」 · 「확인 필요」 표시가 있는가 · 다시 계산할 명령이 `additive_library.py` 를 가리키는가.
