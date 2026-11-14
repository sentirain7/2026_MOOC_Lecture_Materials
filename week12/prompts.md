# week12 Claude Code 지시문 · 덱 「만들어 보기」 장의 원문

사용 환경 · 순서 · 규칙: `../docs/claude_code_quickstart.md` · `../docs/prompt_setup.md` (W01 12장).
순서: 터미널 → `conda activate mdai` → `cd week12` → `claude` → 아래 지시를 붙여 넣고 [ ] 안만 바꾼다 → 명령 실행 · 파일 저장 승인 창을 읽고 승인.
파일은 붙여 넣지 않는다(지시의 경로 · `@경로` 로 Claude Code 가 직접 읽음). 결과 파일 = `out/P12-n_result.md`(Claude Code 가 저장). 수치의 「확인 필요」 표시는 지우지 않는다.

## P12-1 · 내 시멘트 조성의 수화 생성물 표 (덱 8장) → `out/P12-1_result.md`
Claude Code 가 실행하는 명령(승인 후): `python3 scripts/clinker_phases.py --c3s [55] --c2s [18] --c3a [10] --c4af [8] --json out/hydration_products.json`.
```text
scripts/clinker_phases.py 를 내 시멘트 조성 [C₃S 55 · C₂S 18 · C₃A 10 · C₄AF 8 wt%] 로 실행해 out/hydration_products.json(클링커 100 g 완전 수화 시 생성물 · 소요 질량)을 만들고 읽어라. ① 생성물 4종과 소요 석고 · 결합수를 표(열: 항목 · 질량 g · 반응식 · 비고)로 정리하고 ② 결합수/클링커 비가 실무 w/c 0.4~0.5 보다 작은 이유를 두 줄로 쓰고 ③ C₃A 를 5 % 올린 조성으로 다시 실행해(출력은 out/ 의 새 파일) 어느 항목이 가장 크게 변하는지 보고해라. 계산 가정(석고 충분 · C-S-H = C₃S₂H₃ 이상화 · 완전 수화)을 표 아래에 그대로 옮기고, 가정 밖의 값은 「확인 필요」로 표시해라. 기본 조성은 @expected_output/hydration_products.json 과 비교하고, 결과는 out/P12-1_result.md 로 저장해라.
```
기대 답(55 · 18 · 10 · 8): C-S-H 59.1 g · CH 28.2 g · 에트린자이트 46.5 g · C₃AH₆ + C₃FH₆ 13.4 g · 석고 19.1 g · 결합수 37.1 g · 결합수/클링커 0.371. 확인: 반응식 4개가 표에 있는가 · 「완전 수화 · 이상화」 가정이 적혀 있는가.

## P12-2 · ReaxFF 실행 결과 읽기 · 결합 차수 · 전하 (덱 13장) → `out/P12-2_result.md`
Claude Code 가 실행하는 명령(승인 후 · mdai LAMMPS REAXFF · 1코어 약 40초): `python3 scripts/reaxff_input.py --packmol packmol --lmp lmp --steps 2000` → `out/reaxff_summary.json`. 노트북 `notebooks/01_reaxff_portlandite.ipynb` 와 같은 계산.
```text
scripts/reaxff_input.py 를 --steps [2000] --packmol packmol --lmp lmp 로 실행해라(포틀란다이트 Ca(OH)₂ 슬래브 + 물 71분자 · 373원자 · ReaxFF · Δt 0.25 fs). 끝나면 out/reaxff_summary.json 을 읽고 ① 프레임별 Ca–O_w 결합 수(BO ≥ 0.3)와 물 O 의 H 개수 분포를 표로 옮기고 해리(H 1개 또는 3개인 O)가 있었는지 판정해라. ② 종류별 평균 전하(Ca · O · H · 슬래브/물)의 처음과 끝을 표로 쓰고, 고전 힘장의 고정 전하(SPC/E O −0.8476 · ClayFF Ca +1.05)와 무엇이 다른지 두 줄로 써라. ③ 이 시간(총 [0.5] ps)에 수화 반응이 보이지 않는 이유를 시간 규모로 설명하고, 사례연구 1 이 왜 1300 K · 300 ps 가속을 썼는지 연결해라. 요약에 없는 값은 「확인 필요」로 표시하고, @expected_output/reaxff_summary.json 과 비교해 out/P12-2_result.md 로 저장해라.
```
기대 답: 결합 수 · 전하 표 2개 · 「전하가 매 스텝 변한다(QEq)」 · 「100 fs~ps 로는 반응 0 → 가속 또는 긴 시간」. 확인: 해리 판정을 표의 H 개수 분포로 했는가 · 지어낸 반응을 적지 않았는가.

## P12-3 · C-S-H 층 모델 Ca/Si 바꾸기 (덱 20장) → `out/P12-3_result.md`
Claude Code 가 실행하는 명령(승인 후): `python3 scripts/csh_layer_model.py --ca-si [1.0] --json out/csh_1.0.json` · `--ca-si [1.7] --json out/csh_1.7.json` (층간 물 기본 `--water 2`).
```text
scripts/csh_layer_model.py 를 Ca/Si [1.0] 과 [1.7] 로 한 번씩 실행해(--ca-si · --json out/csh_1.0.json · out/csh_1.7.json) C-S-H 층상 개념 모델 요약을 읽어라. 두 경우에 대해 ① 가교 사면체 제거 수 · 평균 사슬 길이 · 층간 Ca · 층간 물 수를 비교 표로 쓰고 ② Ca/Si 와 층간 물이 탄성계수에 미치는 방향(증가/감소)을 토버모라이트 → C-S-H 문헌(원본 08주차 25장 · 나노압입 대조)에 근거해 한 줄씩 쓰되, 수치 예측은 하지 말고 「W09 탄성 상수 계산으로 확인」이라고 적어라. ③ 이 모델이 결정 좌표가 아니라 구성 단위 수 모델이라는 한계를 한 줄로 써라. @expected_output/csh_model_1.0.json · csh_model_1.7.json 과 비교하고, 결과는 out/P12-3_result.md 로 저장해라.
```
기대 답: 표 1개(두 열) · 방향 2줄 · 한계 1줄. 확인: 탄성계수 수치를 지어내지 않았는가 · 「확인 필요」 가 유지되는가.
