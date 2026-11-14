# Claude Code 시작 안내 · 이 강좌의 기본 실습 환경

이 강좌는 내 컴퓨터(또는 연구실 서버)의 터미널에서 **Claude Code** 로 실습한다. Claude Code 는 저장소 폴더 안에서 파일을 직접 읽고, 명령 · 노트북 · LAMMPS 를 실행하고, 오류를 읽고 고치는 AI 코딩 도구다. 사람은 지시하고, 바꾸려는 내용을 검토 · 승인한다.

공식 문서: https://code.claude.com/docs (설치 · 명령 · 권한 · 요금은 여기서 최신 확인)

## 1. 준비물
| 항목 | 내용 |
|---|---|
| 운영체제 | macOS 13 이상 · Ubuntu 20.04 이상 · Windows 10/11 (WSL2 Ubuntu 권장) · RAM 4 GB 이상 · 인터넷 |
| 계정 | Claude 유료 요금제(Pro 이상) 또는 Claude Console(API) 계정 · 무료 요금제로는 Claude Code 를 쓸 수 없음 · 가격은 https://claude.com/pricing |
| conda | Miniforge 또는 Anaconda · 강좌 환경 `mdai` 을 만든다 |
| 저장소 | `git clone https://github.com/sentirain7/2026_MOOC_Lecture_Materials.git` 로 받은 이 폴더 |

## 2. 설치 (처음 1회)
```bash
# Claude Code (macOS · Linux · WSL)
curl -fsSL https://claude.ai/install.sh | bash
claude --version            # 설치 확인
claude doctor               # 설정 점검

# 강좌 환경
conda env create -f environment.yml
conda activate mdai
```
Windows PowerShell 에서 직접 설치할 때: `irm https://claude.ai/install.ps1 | iex` (LAMMPS 실습은 WSL2 권장).

## 3. 매 실습의 3단계
1. **폴더 열기**: 터미널 → `conda activate mdai` → `cd 2026_MOOC_Lecture_Materials/weekNN` → `claude` (처음이면 로그인).
2. **지시하기**: 덱의 「Claude Code 지시」 상자를 복사해 붙여 넣고 [ ] 안만 바꾼다. 파일은 `@notebooks/02_dedup_doi.ipynb` 처럼 `@` 로 가리킨다.
3. **검토 · 승인 · 확인**: 명령 실행 · 파일 수정 전에 승인 창이 뜬다. 무엇을 하는지 읽고 승인한다. 끝나면 `out/` 의 결과와 `expected_output/` 을 비교한 보고를 읽는다.

## 4. 자주 쓰는 조작
| 조작 | 뜻 |
|---|---|
| `!명령` | 셸 명령을 직접 실행 (예 `!ls out`) · 출력이 대화에 들어감 |
| `@경로` | 파일을 대화에 붙임 |
| Esc | 진행 중인 작업 멈춤 · Esc 두 번 = 되돌리기 메뉴(`/rewind`) |
| Shift+Tab | 권한 모드 전환 · 기본(매번 승인) → 수정 자동 승인 → 계획 모드(읽기만 · 계획 먼저) |
| `/clear` | 새 대화 시작 (주제가 바뀔 때) |
| `/usage` (`/cost`) | 사용량 · 비용 확인 |
| `/init` · `/memory` | 프로젝트 규칙 파일 CLAUDE.md 만들기 · 고치기 |
| `claude -c` | 이 폴더의 마지막 대화 이어서 |

## 5. 노트북 · LAMMPS 실행
- 노트북: 「`@notebooks/01_xx.ipynb` 를 실행하고 결과를 요약해」 → Claude Code 가 주차 폴더에서 `python ../run_nb.py notebooks/01_xx.ipynb` 를 실행한다(저장소 맨 위의 실행기 · 경로가 주차 폴더 기준으로 맞음). 출력이 노트북에 저장되므로 JupyterLab · VS Code 로 열어 그림을 볼 수 있다.
- 직접 보고 싶으면 `jupyter lab` 으로 열어 셀을 실행해도 된다(같은 결과).
- LAMMPS: 「`in.lj` 로 LAMMPS 를 돌리고 thermo 표를 요약해」 → `lmp -in in.lj`.

## 6. 오류가 날 때
- 오류를 복사해 붙여 넣을 필요가 없다. Claude Code 가 실행 출력을 직접 읽는다.
- 지시 예: 「방금 오류의 원인을 설명하고, 강좌 스크립트는 고치지 말고 환경 · 경로 · 입력 쪽 조치를 제안해. 실행 전에 확인받아」.
- 그래도 안 되면 `expected_output/` 의 결과 파일로 다음 주차를 진행한다.

## 7. 안전 · 비용 규칙
- 처음에는 기본 모드(매번 승인)로 쓴다. 모든 권한을 건너뛰는 옵션은 쓰지 않는다.
- 큰 수정 전 `git commit` · 실수하면 Esc 두 번으로 되돌리기(셸 명령으로 바뀐 파일은 되돌리기 대상이 아님 · git 이 기준).
- API 키 · 비밀번호를 대화나 파일에 쓰지 않는다.
- 대화가 길어지면 `/clear` 로 새로 시작한다(비용 · 정확도 모두 유리).

## 8. 다른 화면
- VS Code 확장 「Claude Code」: 편집기 안 대화창 · 수정 내용 비교 화면.
- 데스크톱 앱(macOS · Windows): Code 탭.
같은 계정 · 같은 규칙(CLAUDE.md)을 쓴다.
