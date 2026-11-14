# Git · 저장소 최소 안내 (W02 v1 2차시 3장의 설명을 문서로)

## 1. 용어 2개
- **Git**: 파일의 변경 이력(누가 · 언제 · 무엇을)을 기록하고 되돌릴 수 있게 하는 도구. 기록 단위 = 커밋(commit).
- **저장소(repository)**: Git 이 이력을 관리하는 폴더 전체. GitHub 는 저장소를 올려 두는 웹 서비스. 이 강좌 저장소 = 16주 덱 · 노트북 · 데이터 · 정답(expected_output).

## 2. 학생이 쓰는 명령 2개 (+1)
```bash
git clone https://github.com/sentirain7/2026_MOOC_Lecture_Materials.git     # 처음 1회 · 전체 받기 (URL = 저장소 README 첫 줄)
git pull                  # 매주 1회 · 강사가 올린 변경분 받기
git status                # 선택 · 내가 바꾼 파일 확인 (제출 전)
```
Colab 노트북 첫 셀에 `!git clone …` 이 들어 있다. 세션 소멸 시 clone 을 다시 실행한다.

## 3. 주차 폴더 사용 순서 4
1. `weekNN/README.md` — 목표 · 순서 · 소요 시간
2. `notebooks/` — 번호 순서로 ▶
3. `out/` — 내 결과 파일
4. `expected_output/` — 정답과 파일 이름 · 값 비교 · 못 끝냈으면 이 파일을 다음 주 입력으로

## 4. 선택: GitHub 계정 · 토큰 · 올리기(push)
제출은 파일 업로드로 한다. push 는 선택 — `SETUP.md` 참조. 줄끝(CRLF) 문제는 WSL 안에서 `git config --global core.autocrlf input`.
