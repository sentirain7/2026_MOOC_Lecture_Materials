# week02 · 계산 환경과 문헌 도구 (도구 주차)

| 항목 | 내용 |
|---|---|
| 덱 | `slides/W02_계산환경과문헌도구.html` (27장 · 50분 · 4차시 · v2) |
| 학습목표 | ① Claude Code 를 설치 · 로그인하고 주차 폴더에서 노트북 실행을 지시 · 승인한 뒤 `out/` 과 `expected_output/` 을 비교한다 (권한 모드 · CLAUDE.md · `!` · `@` · Esc · `/clear`) ② 셸 명령 6개(pwd · ls · cd · mkdir · cp · python3)를 쓴다 ③ Python 5요소(변수 · 리스트 · 반복 · 함수 · import)로 짧은 스크립트를 읽는다 ④ 저장소를 clone · pull 하고 주차 폴더 순서(README → notebooks → out → expected_output)를 따른다 ⑤ 불리언 검색식을 짜고 DOI 정규화로 중복을 제거한다 ⑥ Zotero 인용키와 Obsidian 위키링크의 역할을 안다 |
| 선수 지식 | W01 실습 완료 (mdai 환경 · `setup_report.json` ok) |
| 소요 시간 | 강의 50분 + 실습 20분 (+ 선택 10분) |
| 새 용어 (8) | 셸 · 가상환경 · Git · 저장소 · 불리언 검색식 · 인용키 · 위키링크 · Claude Code(CLAUDE.md · 권한 승인) → `../GLOSSARY.md` |
| 준비물 | Claude 유료 요금제(Pro 이상) 또는 Console(API) 계정 · conda `mdai` · Zotero · Obsidian(설치 지시 I-3 · I-4 = `../docs/install_prompts.md`) · GitHub 계정 |

## 만들어 보기 (덱 7 · 12 · 26장 · Claude Code)
지시문 원문 = `prompts.md` · 사용법 = `../docs/prompt_setup.md`. 지시 1개 = 대화 1개(주제가 바뀌면 `/clear`) · 결과는 Claude Code 가 `out/P2-n_….md` 로 저장.
1. **P2-1** 내 주제의 검색식 → `out/P2-1_result.md` → 덱 16장 조립기에서 블록 구조 재현
2. **P2-2** `@notebooks/02_dedup_doi.ipynb` 실행 지시 → 승인 → `out/dedup_report.json` (unique 267) · 오류는 Claude Code 가 원인 · 조치 표 보고 → 승인 후 실행
3. **P2-3** DOI + 초록 → 논문 노트 1장 → 강좌 볼트 `../loop/vault/papers/<citekey>.md` (템플릿 `../loop/vault/templates/논문노트.md` · loop_role: none) → `lit_extract.py` 로 표적(밀도 1.018 · CED 354.2) 불변 확인 → `out/P2-3_result.md`. Zotero · Obsidian = 폐루프 ① 문헌 단계 (`docs/zotero_obsidian_loop.md`)
바꿔 보기: 「첫 셀 `YEAR_MIN` 을 2023 으로 바꿔 다시 실행」 → unique 177. 설명서: `../docs/claude_code_quickstart.md` · `../docs/git_quickstart.md` · `../docs/prompt_setup.md` (Colab 을 쓸 때만: `../docs/colab_quickstart.md`).

## 실습 순서
0. **준비 (처음 1회)** Claude Code 설치 → `claude --version` · `claude doctor` → `git clone https://github.com/sentirain7/2026_MOOC_Lecture_Materials.git` → `conda env create -f environment.yml` (설치 명령 · 요구 사양: `../docs/claude_code_quickstart.md` §1 · §2)
   매번: 터미널 → `conda activate mdai` → `cd 2026_MOOC_Lecture_Materials/week02` → `claude` (처음이면 로그인)
   노트북 실행 = 「`@notebooks/<이름>.ipynb` 를 실행하고 결과를 요약해」 → 승인 창에서 `python ../run_nb.py notebooks/<이름>.ipynb` 확인 · 승인
1. **01** `notebooks/01_colab_shell_python.ipynb` · 셸 명령 6개 · Python 5요소 · CSV 267행 읽기 (10분)
2. **02** `notebooks/02_dedup_doi.ipynb` · `norm_doi()` 작성 → 서지 파일 2개 합치기(534행) → 중복 제거 → 267편 (10분)
3. **확인** `out/dedup_report.json` 의 `"unique": 267`
4. **제출** `dedup_report.json` 1개
5. **선택** Zotero 「식별자로 항목 추가」에 `data/md_corpus_267.csv` 의 DOI 10개 붙여넣기 → Better BibTeX 인용키 확인 · `live/cooccurrence.ipynb` 로 슬라이드 20 재현

직접 실행(터미널 · week02 폴더): `python ../run_nb.py notebooks/02_dedup_doi.ipynb` 또는 스크립트만 `python3 scripts/norm_doi.py data/md_corpus_267.csv data/md_asphalt_literature_2021_2026.csv`. Claude Code 안에서는 앞에 `!` 를 붙인다.

## 체크리스트
- [ ] `claude --version` 이 버전을 보여 주고, week02 에서 `claude` 가 열린다
- [ ] Claude Code 안에서 `!ls data` 가 CSV 파일을 보여 준다
- [ ] `out/dedup_report.json` 의 `unique = 267`, `duplicates = 267`
- [ ] 퀴즈 5문항 (`quiz.md`)
- [ ] (선택) Zotero 라이브러리에 항목 10개 · 인용키 표시

## 못 끝냈다면
`expected_output/dedup_report.json` 을 `out/` 에 복사하고 W03 으로 간다. W03 노트북도 같은 3단계(`week03` 에서 `claude` → 실행 지시 → 승인)로 실행된다.

## 폴더
```
week02/
  README.md
  slides/W02_계산환경과문헌도구.html
  notebooks/01_colab_shell_python.ipynb   02_dedup_doi.ipynb
  live/cooccurrence.ipynb                  슬라이드 20 과 같은 계산 (주제 동시출현)
  scripts/norm_doi.py                      노트북 02 와 같은 계산
  data/md_corpus_267.csv  md_asphalt_literature_2021_2026.csv  md_construction_literature_2021_2026.csv  comid_unified_bibliography.csv
  docs/literature_map.md                   문헌맵 · 기관 분포 · 공백 분석 · 노벨티 판정 (원본 11주차 #9 · #11 · #12 · #13 · #18)
  docs/scraping_and_extraction.md          자동 수집 · 코퍼스 색인 · 전문 확보 · LLM 추출 · 후보 등록 (원본 11주차 #20 · #22 ~ #27)
  docs/obsidian_template.md                논문 노트 템플릿 (W02 판 · 폐루프 판 = ../loop/vault/templates/논문노트.md)
  docs/zotero_obsidian_loop.md             폐루프 ① 문헌: Zotero → library.bib → 볼트 → 표적 2개 · 덱 24 ~ 26장에서 옮긴 내용
  expected_output/dedup_report.json
  quiz.md
```
