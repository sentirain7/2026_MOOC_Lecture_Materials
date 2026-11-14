# week16 Claude Code 지시 · 덱 「만들어 보기」 장의 원문

사용 환경 · 순서 · 규칙: `../docs/prompt_setup.md` (W01 12장). week16 폴더에서 `claude` 를 열고 붙여 넣은 뒤 [ ] 안만 바꾼다. 지시 1개 = 대화 1개(주제가 바뀌면 `/clear`). 결과 파일 = `out/P16-n_result.md`.
역할 나눔: 저장소 스크립트가 기준이고 선택(큐레이션 · EHVI 추천)도 스크립트가 한다 · Claude Code 는 스크립트 실행 · 정리 · 판정 근거 · 보고 문장 · 사람은 승인 창에서 결정 지점(제외 규칙 변경 · 추천 → MD 재검증 · 제출 폴더 수정)을 승인. JSON 에 없는 값은 쓰지 않는다. 내 프로젝트 전체를 돌리는 방법 = `docs/final_project.md` 「Claude Code 로 내 파이프라인 돌리기」.

## P16-1 · curation.json → 깔때기 단계표 · 큐레이션 보고 (덱 7장) → `out/P16-1_result.md`
```text
week16 에서 scripts/curate.py data/core672.csv --out out/curation.json --csv out/curated612.csv 를 실행하고 큐레이션 기록 out/curation.json 을 읽어라. ① 단계표(열: 단계 · 남은 행 · 표시 · 제외 · 이유)를 만들고 ② 「지운 행」과 「뺀 행」과 「복원한 행」을 구분해 세 줄로 설명하고 ③ 이상치가 값이 아니라 계산 조건(점도 런 · NPT 없음)에서 나왔다는 근거를 기록에서 찾아 적어라. ④ 같은 규칙을 내 결과 표 [../week09/out/results.csv]에 적용할 때 바꿀 인수 하나를 적어라(제안만 · 실행은 내 승인 뒤). 행 수는 expected_output/curation.json 과 비교하고, 기록에 없는 수치는 쓰지 마라. 결과는 out/P16-1_result.md 로 저장해라.
```
확인: 행 수가 672 → 614 → 612 로 이어지는가 · 보고 문단에 「삭제」 대신 「표시 · 제외 · 복원」이 쓰였는가.

## P16-2 · ehvi.json → 추천 3건 보고서 (덱 14장) → `out/P16-2_result.md`
```text
week16 에서 scripts/ehvi_select.py data/features614.csv out/curated612.csv --obs 400 --batch 3 --out out/ehvi.json 을 실행하고(약 17초 · 수렴 경고 5건은 오류 아님) out/ehvi.json 의 picks · hv_* 항목을 읽어라. ① 추천 3건을 보고 형식(조건 · 예측 K ± σ · 예측 CED ± σ · 제약 충족 · 적용 영역 · 검증 계산 제안) 표로 만들고 ② 실제값 공개 열로 HV 증가를 무작위 3개 평균과 비교해 한 문장으로 쓰고 ③ 세 후보가 모두 SiO₂ 인 점을 다양성 관점에서 평가하고 다음 배치의 규칙(예: 첨가제당 1개)을 제안해라. ④ 내 표적 [점도 범위 · 분리일 ↑]으로 바꿀 때 필요한 열을 적어라. 추천 3건은 스크립트 결과 그대로 두고, 파일에 없는 값은 쓰지 마라. 결과는 out/P16-2_result.md 로 저장해라.
```
확인: 예측마다 σ 가 붙어 있고 무작위 기준선(+0.09 · 1.5 %)과 비교했는가 · 다양성 규칙을 다음 배치 조건으로 적었는가.

## P16-3 · checklist.json → 보완 목록 · 발표 10장 계획 · problem.json (덱 24장) → `out/P16-3_result.md`
```text
week16 에서 scripts/final_project_check.py [out/my_project] --out out/checklist.json 을 실행하고 out/checklist.json 을 읽어라(폴더가 없으면 expected_output/example_project 복사를 제안하고 승인받아라). ① ✗ 항목마다 보완할 파일과 필드를 적고 ② 발표 10장 계획(장 번호 · 제목 · 평가 항목 · 근거 파일)을 표로 만들어라 · 실패한 시도와 원인 장을 반드시 넣고 ③ 내 주제 [아스팔트 바인더 첨가제 · 분리일과 점도]에서 표적 2개 · 제약 · 성공 기준을 problem.json 형식 초안으로 보여라. 내 폴더의 파일은 승인 전에 고치지 마라. 수치는 내 파일에 있는 값만 쓰고 없으면 「확인 필요」로 둔다. 결과는 out/P16-3_result.md 로 저장해라.
```
확인: 발표 계획에 「실패한 시도와 원인」 장이 있는가 · 모든 수치에 근거 파일(JSON · CSV)이 붙어 있는가 · 없는 값은 「확인 필요」로 남겼는가.
