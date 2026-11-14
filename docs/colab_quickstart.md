# (선택 경로) Colab · 셸 · Python 최소 안내 (W02 v1 1차시 5장의 설명을 문서로)

> 2026-11-14 부터 이 강좌의 기본 실습 환경은 **Claude Code + 내 컴퓨터(conda mdai)** 이다 · `docs/claude_code_quickstart.md`. 이 문서는 Colab 으로 노트북만 열어 보려는 경우를 위한 참고로 남긴다. 셸 명령 6개 · 오류 읽기 · Python 5요소 설명은 터미널에서도 그대로 쓴다(앞의 `!` · `%cd` 만 빼고).

덱은 「노트북 ▶ 한 번」만 보여 준다. 막히거나 더 알고 싶을 때 이 문서를 본다.

## 1. Colab 구조 4 단어
| 단어 | 뜻 | 할 일 |
|---|---|---|
| 셀 | 코드 또는 글 한 칸 · Shift+Enter 로 실행 · 위에서 아래 순서 | 보통은 런타임 ▸ 모두 실행 |
| 런타임 | 구글 서버의 임시 컴퓨터 · 파이썬 · 기본 패키지 설치됨 | 끊기면 런타임 ▸ 다시 시작 후 첫 셀부터 |
| 파일 탭 | 런타임의 디스크 · 노트북이 만든 파일이 보이는 곳 (왼쪽 📁) | `weekNN/out/` 의 결과를 내려받기 |
| 세션 소멸 | 일정 시간 뒤 런타임 삭제 · 디스크도 지워진다 | 결과 파일은 반드시 내려받기 |

## 2. 셸 명령 6개 (Colab 셀에서는 앞에 `!`, 폴더 이동은 `%cd`)
| 명령 | 뜻 | 예 |
|---|---|---|
| `pwd` | 지금 어느 폴더인가 | `!pwd` → `/content/…/week02` |
| `ls` | 폴더 안 목록 | `!ls data` |
| `cd` | 폴더 이동 | `%cd week03` |
| `mkdir` | 폴더 만들기 | `!mkdir -p out` |
| `cp` | 파일 복사 | `!cp out/dedup_report.json mine.json` |
| `python3` | 스크립트 실행 | `!python3 scripts/norm_doi.py data/md_corpus_267.csv` |

W06 부터 LAMMPS 도 같은 자리: `!lmp -in in.lj`. 경로 규칙: `data/` 입력 · `out/` 출력 · 공백 · 한글 없는 파일 이름.

## 3. 오류 메시지 읽기
| 메시지 | 뜻 | 조치 |
|---|---|---|
| `FileNotFoundError: data/…` | 지금 폴더가 주차 폴더가 아님 | `%cd …/weekNN` 뒤 다시 |
| `ModuleNotFoundError: No module named 'x'` | 패키지 없음 | `!pip install x` (세션마다 다시) |
| `NameError: name 'df' is not defined` | 앞 셀을 건너뜀 | 런타임 ▸ 모두 실행 |
| 런타임 연결 끊김 | 세션 소멸 | 다시 연결 → 첫 셀(clone)부터 |
막히면 덱의 P2-2 프롬프트에 오류 출력을 붙여 넣는다.

## 4. Python 최소 5요소 (노트북을 읽을 때만)
```python
import numpy as np            # ⑤ import: numpy(배열) · pandas(표) · matplotlib(그림)
dt = 1.0                      # ① 변수 (fs)
temps = [253, 273, 293]       # ② 리스트 (K)
def kinetic(m, v):            # ④ 함수: 계산을 이름으로 묶기
    return 0.5 * m * v**2
for T in temps:               # ③ 반복: 목록의 값마다 같은 일
    print(T, kinetic(1.0, np.sqrt(T)))
```
노트북의 첫 셀에 있는 매개변수(변수)만 바꾸면 된다. 함수 본문은 저장소 스크립트가 기준.

## 5. 설치 경로 3 (선택)
| 경로 | 대상 | 비고 |
|---|---|---|
| Colab (기본) | 모든 주차 | 설치 없음 · `!pip install` 로 추가 · 세션마다 재설치 |
| conda 가상환경 `mdai` | 내 컴퓨터 · W06 이후 LAMMPS | `SETUP.md` · 강좌 전용 환경 1개 |
| Docker | LAMMPS 포함 이미지 | `SETUP.md` 선택 |
