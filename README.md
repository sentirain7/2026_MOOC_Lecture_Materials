https://github.com/sentirain7/2026_MOOC_Lecture_Materials

# 2026 MOOC 강의자료 · 건설소재 역설계 도구 개발을 위한 AI와 분자동역학 활용

> 수강생은 이 README 와 [사용자 가이드](사용자_가이드.md)부터 읽는다.
>
> English version: [below](#english)

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
- **온라인 슬라이드(설치 없이 · 주차별 링크)**: https://sentirain7.github.io/Self_Driving_Lab_Instruction/lectures/mooc/
- `강의자/` 폴더 = 강의자 전용(비공개 저장소 연결 · 작성자만 열 수 있다 · 수강생은 필요 없다)

## 폴더
| 폴더 | 내용 |
|---|---|
| `week01/` ~ `week18/` | 주차별 한 묶음: 강의 덱 `slides/WNN_….html`(Chrome 으로 연다 · 「한국어 \| EN」 L 키) · README · 지시문 `prompts.md` · notebooks · scripts · data · 기준 결과 `expected_output/` · 평가문항 문제지 |
| `common/` | 덱이 함께 쓰는 글꼴 · 스타일 · 스크립트(덱을 다른 곳으로 옮길 때 같은 상대 위치에 둔다) |
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
- 계정: Claude 유료 요금제(Pro 이상) 또는 Claude Console(API)
- 운영체제: Ubuntu · macOS · Windows(WSL2)
- 컴퓨터: 4코어 이상 권장 · 디스크 여유 10 GB 이상
- 설치 검증: Ubuntu(WSL2 포함)

---

<a id="english"></a>

# 2026 MOOC Course Materials (English) · AI and Molecular Dynamics for Developing Inverse-Design Tools for Construction Materials

> Students: start with this README and the [User Guide](사용자_가이드.md) (Korean).

Taeyoung Yun, Korea Institute of Civil Engineering and Building Technology (KICT) · **18-week course** (about 50 min per week) · 2026

You extract target values from the literature, compute them with molecular dynamics (MD), and let an AI surrogate model choose the next calculation. In this way you run one full **inverse-design closed loop** on your own computer. Every exercise works the same way: paste the prompt from the lecture deck into **Claude Code** in your terminal.

## Quick start
```bash
git clone https://github.com/sentirain7/2026_MOOC_Lecture_Materials.git
cd 2026_MOOC_Lecture_Materials
```
1. **Install Claude Code** (W01 · the only program you install by hand) → `docs/claude_code_quickstart.md`
2. **Install everything else** by pasting prompts into Claude Code → `docs/install_prompts.md` (I-1 conda · I-2 course environment `mdai` · I-3 Zotero · I-4 Obsidian · I-5 full check)
3. **Every week**: `conda activate mdai` → `cd 2026_MOOC_Lecture_Materials/weekNN` → `claude` → paste the deck prompt → compare your results in `out/` with the reference in `expected_output/`
- **Student user guide**: [`사용자_가이드.md`](사용자_가이드.md) — what you need · how to view the decks · installation · weekly exercises · weekly tasks · assessment · troubleshooting
- **Online slides (no install · one link per week)**: https://sentirain7.github.io/Self_Driving_Lab_Instruction/lectures/mooc/
- `강의자/` folder = instructor only (linked private repository · only the author can open it · students do not need it)

## Folders
| Folder | Contents |
|---|---|
| `week01/` ~ `week18/` | One bundle per week: lecture deck `slides/WNN_….html` (open in Chrome · 「한국어 \| EN」 button or L key) · README · prompts `prompts.md` · notebooks · scripts · data · reference results `expected_output/` · assessment question sheet |
| `common/` | Fonts, styles and scripts shared by the decks (keep the same relative location if you move a deck) |
| `mdworkflow/` | MD workflow (W17): molecule → force field (GAFF2 · AM1-BCC) → box (Packmol) → LAMMPS → density · CED → results table |
| `loop/` | Closed loop (W18): Obsidian vault literature notes → targets → 168 average-molecule candidates → surrogate model → Chebyshev EI → write-back to the vault · reference case |
| `docs/` | Install prompts · getting started with Claude Code · how to use prompts · Git |
| `강의자/` | Instructor only (private · submodule) · `git clone` gives an empty folder |
| `CLAUDE.md` | Course rules that Claude Code reads automatically |
| `environment.yml` · `environment.lock.txt` | Course environment `mdai` (Python 3.12 · RDKit · scikit-learn · XGBoost · SHAP · LAMMPS · AmberTools · Packmol) |
| `weekNN/평가문항/` | Weekly assessment, 6 items (3 multiple choice · 2 true/false · 1 short answer) · answers and explanations are given separately by the instructor |
| `GLOSSARY.md` | Glossary |

## Weeks
| Module | Weeks |
|---|---|
| M0 Tools | W01 Course overview · W02 Computing environment and literature tools |
| M1 MD basics | W03 The atomic world and equations of motion · W04 Force fields · W05 Ensembles · equilibration · error |
| M2 LAMMPS | W06 LAMMPS input and structure building · W07 Automating MD with Python · W08 Multilayer structures and multi-force-field stacks |
| M3 Properties · materials | W09 Property calculation · W10 Interfaces and adhesion · W11 Asphalt · W12 Cement |
| M4 Machine learning | W13 Machine-learning basics · W14 Descriptors and surrogate models · W15 Neural networks · graphs · uncertainty |
| M5 Autonomous exploration | W16 Autonomous exploration pipeline and validation · W17 Assembling the MD workflow · W18 Closed-loop integration lab · final project |

## Requirements
- Account: paid Claude plan (Pro or higher) or Claude Console (API)
- Operating system: Ubuntu · macOS · Windows (WSL2)
- Computer: 4 or more cores recommended · at least 10 GB free disk space
- Installation verified on: Ubuntu (including WSL2)
