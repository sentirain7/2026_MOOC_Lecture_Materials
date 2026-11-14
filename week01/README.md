# week01 · 과정 개요: 배합 설계의 한계에서 역설계까지

| 항목 | 내용 |
|---|---|
| 덱 | `slides/W01_과정개요.html` (26장 · 50분 · 4차시 · v2: 그림 · 애니 · 만들어 보기 중심) |
| 학습목표 | ① 배합 설계의 세 가지 한계 설명 ② 순방향 설계와 역설계의 차이를 그림으로 설명 ③ 표적 물성이 갖춰야 할 네 요소(수치 · 단위 · 산출 방법 · 방향) 이해 ④ 네 스케일에서 분자동역학과 대리모델의 위치 이해 ⑤ 자율 탐색 파이프라인 6단계와 18주 지도 연결 (W17 MD 워크플로우 조립 · W18 폐루프 통합 실습 · 최종 프로젝트) |
| 선수 지식 | 배합 설계 경험 · 응력–변형률 · 스프레드시트. 이 셋이면 된다 |
| 소요 시간 | 강의 50분 + 실습 10분 (+ 선택 15분) |
| 새 용어 (7) | 역설계 · 표적 물성 · 분자동역학 · 힘장 · 대리모델 · 디지털 트윈 · 능동학습 → `../GLOSSARY.md` |

## 만들어 보기 (덱 13 · 25장 · Claude Code)
1. **P1-1** `prompts.md` 의 지시를 Claude Code 에 붙여 넣어 내 재료의 조성 변수 4개 · 표적 물성 2개 표 → 수준 수의 곱 = 조합 수 → `out/P1-1_result.md` → 덱 6장 계산기 · `live/combination_space.ipynb` 로 자릿수 차 확인
2. **P1-2** 환경 점검: Claude Code 가 노트북 실행 → `out/setup_report.json` · `claude --version` · `lmp` · conda 환경 표 → 조치 필요 항목은 원인 · 조치 표 → 승인 후 실행 → `out/P1-2_result.md`

## 준비물
| 항목 | 내용 |
|---|---|
| Claude Code | 유료 요금제(Pro 이상) 또는 Console(API) 계정 · 무료 요금제 불가 · 설치 · 로그인: `../docs/claude_code_quickstart.md` |
| 터미널 · conda | 강좌 환경 `mdai` (`../environment.yml`) · 손으로 설치하는 것은 Claude Code 하나 · conda · mdai 는 설치 지시 I-1 · I-2 · 전체 점검 I-5 (`../docs/install_prompts.md` · 덱 24장) |
| 운영체제 | macOS · Linux · Windows 는 WSL2 Ubuntu 권장 |

## 실습 순서 (Claude Code)
1. **열기** · 터미널 → `conda activate mdai` → `cd week01` → `claude` (처음이면 로그인). 저장소 맨 위 `CLAUDE.md`(강좌 규칙)를 Claude Code 가 자동으로 읽는다.
2. **지시** · `prompts.md` 의 P1-2 를 붙여 넣는다. Claude Code 가 week01 폴더에서 `python ../run_nb.py notebooks/00_setup_check.ipynb` 로 노트북을 실행해 `out/setup_report.json` · `out/papers_by_year.png` 를 만든 뒤 `claude --version` · `lmp` · conda 환경을 표로 보고한다. 파이썬 · 패키지 버전 확인 → 공개 데이터 101행 읽기 → 그림 1장.
3. **승인 · 확인** · 명령 · 설치 승인 창을 읽고 승인한다. `out/setup_report.json` 의 ok · data_rows 를 `expected_output/` 과 비교한 보고를 읽는다. 예상 소요 10분.
4. **제출** · `setup_report.json` 하나 (보고 `out/P1-2_result.md` 는 함께 보관).
5. **선택** · `live/combination_space.ipynb` 로 덱 6장(조합 공간 계산기)과 같은 계산을 코드로 해 본다.

Claude Code 없이 확인할 때: mdai 환경의 week01 폴더에서 `python3 scripts/setup_check.py` · 노트북을 직접 보려면 `jupyter lab`. (선택 경로) Colab: `../docs/colab_quickstart.md`.
`run_nb.py` 는 주차 폴더 기준으로 실행해 결과가 `week01/out/` 에 생긴다(`jupyter nbconvert --execute` 는 notebooks/ 에서 실행되어 경로가 어긋나므로 쓰지 않는다).

## 체크리스트
- [ ] `claude --version` 이 출력되고 `conda activate mdai` 이 된다
- [ ] `out/setup_report.json` 의 `"ok": true`
- [ ] `out/papers_by_year.png` 가 만들어졌다
- [ ] 퀴즈 5문항 (`quiz.md`) 을 풀고 해설을 읽었다
- [ ] (W01 끝) 설치 지시 I-5 전체 점검 → 저장소 맨 위 `out/I-5_result.md`
- [ ] 다음 주 준비: GitHub 계정 · Zotero · Obsidian 은 W02 에서 설치 지시 I-3 · I-4

## 못 끝냈다면
`expected_output/setup_report.json` 을 받아 W02 로 간다. 환경 문제는 W02 1차시에서 함께 해결한다.

## 폴더
```
week01/
  README.md                     이 문서
  prompts.md                    Claude Code 지시 원문 (P1-1 · P1-2)
  slides/W01_과정개요.html       덱 (파일 하나 · 글꼴 · 스타일 내장)
  notebooks/00_setup_check.ipynb  환경 점검 (10분)
  live/combination_space.ipynb    덱 6장과 같은 계산
  scripts/setup_check.py          노트북과 같은 일을 하는 스크립트
  data/asphalt_ml_101.csv         공개 데이터 · 아스팔트 × 기계학습 논문 101편 서지 (22 KB)
  expected_output/setup_report.json  정답 산출물
  quiz.md                         5문항 + 해설
```
