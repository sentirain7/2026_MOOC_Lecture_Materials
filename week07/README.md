# week07 · Python 으로 MD 자동화 (모듈 M2 · 도구 주차)

| 항목 | 내용 |
|---|---|
| 덱 | `slides/W07_Python으로MD자동화.html` (23장 · 48분 · 3차시 · v3) |
| 학습목표 | ① 매개변수 표 + 템플릿에서 입력 파일 세트를 생성한다 ② 반복 실행의 실패를 로그 규칙 4개로 감지하고 재시도 1회를 자동화한다 ③ 로그의 thermo 블록을 표로 바꾸고 요약한다 ④ 생성기에 규칙을 더할 때의 상한 · 결정론적 실패를 구분한다 |
| 선수 지식 | W02 셸 6 · 저장소 순서 · W06 in · data 파일 (toluene_box.data · in.toluene 이름만) |
| 소요 시간 | 강의 48분 + 실습 15분 |
| 새 용어 (5) | 템플릿 · 자리표시 · 매개변수 표 · 배치 실행 · 입력 해시 → `../GLOSSARY.md` |
| 도구 주차 | 새 물리 없음 · 다음 주차(W08 다층 구조 · W09~ 물성)에서 쓰는 생성 · 실행 · 파싱만 |

## 만들어 보기 · Claude Code 지시 (덱 8 · 14 · 22장 · `prompts.md`)
- **P7-1** 매개변수 표에 열 추가 → `out/P7-1_result.md`
- **P7-2** 실패 로그에서 원인 · 조치 → `out/P7-2_result.md`
- **P7-3** 생성기에 규칙 추가(시드 변경 재시도) → `out/P7-3_result.md`

## 실습 순서 (Claude Code · `../docs/claude_code_quickstart.md`)
1. **열기**: 터미널 → `conda activate mdai` → `cd week07` → `claude` (LAMMPS 는 `mdai` 에 포함 · `../environment.yml`).
2. **실행**: 덱의 지시 P7-1 · P7-2 를 붙여 넣으면 Claude Code 가 승인 후 `render_inputs.py`(표 6줄 → in 6개) → `run_batch.py`(7회 실행 · 1건 재시도) → `parse_log.py`(CSV 7 + summary.json) 를 실행한다. 그림까지 만들려면 「`@notebooks/01_automation.ipynb` 를 실행하고 결과를 요약해」(= `python ../run_nb.py notebooks/01_automation.ipynb` · 강좌 실행기). 전체 약 10초.
3. **확인**: `out/runs/status.csv` 에 `ok` 6 · `lost_atoms` 1 · 재시도 `ok` / `summary.json` 의 `temp_mean` 이 목표 T ±2 %.
4. **제출**: `status.csv` · `summary.json` · `temperature_6runs.png`.
5. **바꿔 보기**: `data/params.csv` 에 한 줄 추가 → 스크립트 3개 다시 실행(노트북이면 2) 부터).

직접 실행할 때(터미널 · Claude Code 안에서는 앞에 `!`) week07 폴더에서:
```
python3 scripts/render_inputs.py && python3 scripts/run_batch.py --lmp lmp && python3 scripts/parse_log.py
```
대화 없이 지시 1개만 실행하고 끝내기: `claude -p "out/runs/status.csv 를 요약해"` (배치 스크립트 안에서 부를 수 있는 형태 · W16 자동화와 연결).

MD 워크플로우 연결(`../mdworkflow` · ④ run · 지시문 M-4 · 덱 11장 아래 줄): 같은 실패 규칙의 축소판. R1 = 원자 잃음 계열(Lost atoms · Bond atoms missing · Out of range atoms) → Δt 절반 · 스텝 2배(같은 물리 시간)로 1회 재실행 · R2 = 그 밖의 오류 → 멈추고 마지막 ERROR 줄 보고. 실행 기록 = `ws/runs/<id>/status.json`(attempts · rule). 이 주차 `run_batch.py` 는 실패 종류와 무관하게 1회 재시도(③ ④ 분기는 P7-3).

(선택) Colab: 노트북 0) · 1) 셀의 주석대로 저장소 clone · LAMMPS 설치 후 위에서부터 실행.

## 숫자의 출처
- 실행 결과(status · T̄ · 벽시계 초) = 이 폴더의 스크립트를 2026-11-08 에 LAMMPS 22 Jul 2025 (conda env mdai · CPU) 로 실제 실행한 값 → `expected_output/`
- 실패 감지 규칙 · Δt 절반 · 재시도 상한 · 결정론적 실패: 원본 05주차 #17 · #18 · COMID `src/orchestrator/lammps_runner.py`(ERROR 줄 추출) · `src/parsers/log_parser.py`(thermo 블록 규칙)
- 사례 2건(진공 40 → 60 Å · 실패 38 % · fix momentum 필름 높이 표): 원본 05주차 #19 · #20
- 명세 = 유일한 기준 · 입력 해시 6자리 · 멱등성: 원본 05주차 #8 · #9 · #15

## 기대 결과 (`expected_output/`)
| 파일 | 내용 |
|---|---|
| `inputs/in.*` + `manifest.json` | 입력 6개 · 해시 6자리 |
| `runs/status.csv` | 7행: ok ×5 · T12_s22 시도 1 `lost_atoms`(Δt 0.03) · 시도 2 `ok`(Δt 0.015) · 벽시계 0.11 ~ 0.54 s |
| `runs/*/log.lammps` | 로그 7개 (실패 로그 포함) |
| `thermo/*.csv` · `summary.json` | thermo 21행 × 6 · T̄ 0.799 / 0.810 / 1.005 / 1.012 / 1.207 / 1.203 |

## 못 끝냈다면
`expected_output/` 을 받고 W08 로 간다. 환경 · LAMMPS 설치는 `../environment.yml` · `../docs/claude_code_quickstart.md`.
