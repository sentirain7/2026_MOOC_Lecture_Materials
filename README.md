https://github.com/sentirain7/2026_MOOC_Lecture_Materials

# 2026 MOOC 강의자료 · 건설소재 역설계 도구 개발을 위한 AI와 분자동역학 활용

> 수강생은 이 README 와 [사용자 가이드](사용자_가이드.md)부터 읽는다.

*AI and Molecular Dynamics for Developing Inverse-Design Tools for Construction Materials*

한국건설기술연구원 윤태영(Taeyoung Yun) · **18주 강좌**(주당 약 50분) · 2026

문헌에서 목표값을 뽑고, 분자동역학(MD)으로 계산하고, 인공지능 대리모델로 다음 계산을 고르는 **역설계 폐루프**를 내 컴퓨터에서 직접 한 바퀴 돌린다. 모든 실습은 터미널의 **Claude Code** 에 강의 덱의 지시문을 붙여 넣는 방식으로 한다.

## 바로 시작
```bash
git clone https://github.com/sentirain7/2026_MOOC_Lecture_Materials.git
cd 2026_MOOC_Lecture_Materials
```
1. **Claude Code 설치**(W01 · 사람이 직접 설치하는 유일한 프로그램) → `docs/claude_code_quickstart.md`
2. **나머지 설치**는 Claude Code 에 지시문을 붙여 넣는다 → `docs/install_prompts.md` (I-1 conda · I-2 강좌 환경 `mdai` · I-3 Zotero · I-4 Obsidian · I-5 전체 점검)
3. **매주**: `conda activate mdai` → `cd 2026_MOOC_Lecture_Materials/weekNN` → `claude` → 덱의 지시문 붙여 넣기 → 결과 `out/` ↔ 기준 `expected_output/`
- **수강생 사용자 가이드**: [`사용자_가이드.md`](사용자_가이드.md) — 준비물 · 덱 보는 법 · 설치 · 매주 실습 · 주차별 할 일 · 평가 · 막힐 때
- `강의자/` 폴더 = 강의자 전용(비공개 저장소 연결 · 작성자만 열 수 있다 · 수강생은 필요 없다)

## 폴더
| 폴더 | 내용 |
|---|---|
| `강의덱/` | W01 ~ W18 슬라이드(HTML · Chrome 으로 연다 · 옆의 `common/` 과 함께) · 「한국어 \| EN」 버튼(L 키) |
| `week01/` ~ `week18/` | 주차별 실습: README · 지시문 `prompts.md` · notebooks · scripts · data · 기준 결과 `expected_output/` · 평가문항 문제지 |
| `mdworkflow/` | MD 워크플로우(W17): 분자 → 힘장(GAFF2 · AM1-BCC) → 상자(Packmol) → LAMMPS → 밀도 · CED → 결과 표 |
| `loop/` | 폐루프(W18): Obsidian 볼트 문헌 노트 → 표적 → 평균 분자 후보 168 → 대리모델 → 체비셰프 EI → 볼트 환류 · 기준 사례 |
| `docs/` | 설치 지시문 · Claude Code 시작 · 지시문 사용법 · Git |
| `강의자/` | 강의자 전용(비공개 · 서브모듈) · `git clone` 하면 빈 폴더로 받아진다 |
| `CLAUDE.md` | Claude Code 가 자동으로 읽는 강좌 규칙 |
| `environment.yml` · `environment.lock.txt` | 강좌 환경 `mdai`(Python 3.12 · RDKit · scikit-learn · XGBoost · SHAP · LAMMPS · AmberTools · Packmol) |
| `weekNN/평가문항/` | 주차별 평가문항 6개(객관식 3 · OX 2 · 단답형 1) 문제지 · 정답 · 해설은 강의자가 따로 안내 |
| `GLOSSARY.md` | 용어집 |

## 주차
| 모듈 | 주차 |
|---|---|
| M0 도구 | W01 과정 개요 · W02 계산 환경과 문헌 도구 |
| M1 MD 기초 | W03 원자 세계와 운동방정식 · W04 힘장 · W05 앙상블 · 평형화 · 오차 |
| M2 LAMMPS | W06 LAMMPS 입력과 구조 생성 · W07 Python 으로 MD 자동화 · W08 다층 구조와 다중 힘장 스택 |
| M3 물성 · 소재 | W09 물성 산출 · W10 계면과 부착 · W11 아스팔트 · W12 시멘트 |
| M4 기계학습 | W13 기계학습 기초 · W14 표현자와 대리모델 · W15 신경망 · 그래프 · 불확실성 |
| M5 자율 탐색 | W16 자율 탐색 파이프라인과 검증 · W17 MD 워크플로우 조립 · W18 폐루프 통합 실습 · 최종 프로젝트 |

## 요구 사항
Claude 유료 요금제(Pro 이상) 또는 Claude Console(API) · Ubuntu / macOS / Windows(WSL2) · 4코어 이상 권장 · 디스크 여유 10 GB 이상. 설치 검증은 Ubuntu(WSL2 포함)에서 했다.
