# week15 Claude Code 지시 · 덱 「만들어 보기」 장의 원문

사용 환경 · 순서 · 규칙: `../docs/prompt_setup.md` (W01 12장). week15 폴더에서 `claude` 를 열고 붙여 넣은 뒤 [ ] 안만 바꾼다. 지시 1개 = 대화 1개(주제가 바뀌면 `/clear`). 명령 실행 · 파일 수정은 승인 창에서 확인한다. 결과 파일 = `out/P15-n_result.md`.

## P15-1 · 내 분자 그래프 → 3층 순전파 해석 (덱 9장) → `out/P15-1_result.md`
```text
week15 에서 scripts/mol_graph.py --smiles "[내 SMILES]" 와 scripts/mpnn_forward.py --graph out/graph_mine.json --layers 3 을 차례로 실행하고 out/mpnn_forward.json 을 읽어라. ① 노드 수 · 엣지 수 · 방향족 노드 수를 표로 정리해라. ② reach_from_node0 을 읽고 「3층이면 노드 0 에서 몇 결합 거리 · 몇 개 원자까지 정보가 닿는가」를 graph_distance 로 설명해라. ③ 방향족 · 결합 차수 엣지 특징이 없으면 구분하지 못하는 분자쌍 예를 하나 들어라. ④ readout_y_permuted 와 readout_y 가 같은 이유를 한 줄로 써라. 노드 · 엣지 수는 mol_graph.py 출력과 대조하고, JSON 에 없는 값은 「확인 필요」로 표시해라. 결과는 out/P15-1_result.md 로 저장해라.
```
확인: 노드 · 엣지 수가 mol_graph.py 출력과 같은가 · 「3층 = 3결합 거리」를 graph_distance 로 확인했는가.

## P15-2 · 보정 판정 · σ 배율 s (덱 21장) → `out/P15-2_result.md`
```text
week15 에서 scripts/gp_demo.py 와 scripts/calibration.py 를 차례로 실행하고 out/calibration.json(명목 신뢰 수준 p 와 실제 포함률 · 참고 사례(연구 플랫폼 결과) 4물성 커버리지 · r · s)을 읽어라. ① 물성 · 모델별로 68 % · 95 % 명목 대 실제 포함률 표를 만들어라. ② 각각 「양호 · 약한 과신 · 과신 · 과소신」으로 판정하고 기준(대각선과의 차)을 한 줄로 써라. ③ 과신인 경우 σ 에 곱할 배율 s 와, 그 대신 커널 잡음항을 키우는 방법의 차이를 두 줄로 써라. ④ [내 물성]의 GP 를 획득함수에 쓰기 전에 확인할 항목 3개를 적어라. 포함률은 expected_output/calibration.json 과 비교하고, JSON 에 없는 값은 「확인 필요」로 표시해라. 결과는 out/P15-2_result.md 로 저장해라.
```
확인: 68 · 95 % 두 수준을 모두 썼는가 · 과신일 때 s 가 1 보다 큰가.

## P15-3 · 획득함수 5종 비교 → κ 선택 (덱 26장) → `out/P15-3_result.md`
```text
week15 에서 scripts/acquisition.py --kappa 2 --rounds 5 를 실행하고 out/acquisition.json(같은 시작 3점에서 UCB κ 2 · κ 0 · κ 0.1 · EI · 최대 분산을 5라운드씩 돌린 결과)을 읽어라. ① 방법별로 다음 계산 점 순서 · 같은 점 반복 수 · 찾은 최고 참값을 표로 정리해라. ② 내 역설계는 [초기 탐색 / 목표 근접 / 모델 개선] 단계다 · 이 단계에 맞는 획득함수와 κ 를 고르고 근거를 표의 숫자로 두 줄 써라. ③ 참고 사례(연구 플랫폼 결과)의 기본값 κ 0.1 이 맞는 상황을 한 줄로 써라. ④ 이 결과가 가정 함수 하나에서 나왔다는 한계를 결론에 적어라. 표는 expected_output/acquisition.json 과 비교하고, JSON 에 없는 값은 「확인 필요」로 표시해라. 결과는 out/P15-3_result.md 로 저장해라.
```
확인: 최고 참값과 반복 점 수를 함께 비교했는가 · 결론에 「가정 함수 하나」의 한계가 있는가.
