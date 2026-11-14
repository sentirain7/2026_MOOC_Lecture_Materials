# week02 지시문 · 덱 「만들어 보기」 장의 Claude Code 지시 원문

사용 환경 · 순서 · 규칙: `../docs/prompt_setup.md` · `../docs/claude_code_quickstart.md`. week02 폴더에서 `claude` 를 열고, 지시 1개 = 대화 1개(주제가 바뀌면 `/clear`). [ ] 안만 바꾼다. 결과 파일 = `out/P2-n_….md` (Claude Code 가 저장 · 강좌 규칙 `../CLAUDE.md`).

## P2-1 · 내 주제의 검색식 (덱 7장) → `out/P2-1_result.md`
```text
내 연구 주제는 [아스팔트 바인더의 수분 손상을 분자동역학으로 다루는 연구]다. 문헌 검색식을 만들어라. ① 개념 블록 4개(재료 · 방법 · 성분/조건 · 물성)로 나누고, 블록 안은 동의어를 OR 로, 블록 사이는 AND 로 묶어라. ② 배제할 유형(리뷰 · 특허 등)은 NOT 으로 한 줄. ③ 연도 하한을 넣어라. ④ 같은 식을 Scopus 문법과 Crossref API 질의 문자열 두 가지로 써라. ⑤ 마지막에 기록 표(검색식 · 실행 날짜 · DB · 결과 건수 · 한계)의 빈 칸을 만들어라. 검색은 아직 실행하지 말고, P2-1 결과로 out/P2-1_result.md 에 저장해라.
```
확인: 블록 사이 AND 만 · 블록 안 OR 동의어 2개 이상 · 기록 표 5칸. 덱 16장 조립기에서 같은 구조로 편수 변화 확인.

## P2-2 · 노트북 실행 · 오류 조치 (덱 12장) → `out/P2-2_result.md`
```text
@notebooks/02_dedup_doi.ipynb 를 실행해라. 내 환경은 [Ubuntu / macOS / Windows WSL2]다. 오류가 나면 ① 어느 셀 · 어느 줄에서 멈췄는지 ② 원인 한 줄 ③ 조치(명령) ④ 다시 확인하는 방법을 표로 보고하고, 조치는 내 승인을 받은 뒤 실행해라. 노트북과 scripts/ 는 고치지 말고 환경 · 경로 · 입력 파일 쪽에서 해결해라. 성공하면 out/dedup_report.json 의 records · unique · duplicates 를 expected_output/ 과 비교해 P2-2 결과로 out/P2-2_result.md 에 저장해라.
```
확인: 승인 창의 명령이 `python ../run_nb.py notebooks/02_dedup_doi.ipynb` 인지 보고 승인 → `out/dedup_report.json` 의 `"unique": 267` · `"duplicates": 267` 이 `expected_output/` 과 일치. 오류 조치도 승인한 뒤에만 실행된다. 그래도 안 되면 `expected_output/dedup_report.json` 을 `out/` 에 복사하고 W03.

## P2-3 · DOI + 초록 → 논문 노트 → 강좌 볼트 (덱 26장) → `../loop/vault/papers/<citekey>.md` · `out/P2-3_result.md`
```text
아래 논문의 노트를 @../loop/vault/templates/논문노트.md 템플릿 그대로 작성해라(제목 · 연도 · 학술지 = @data/md_corpus_267.csv 의 같은 DOI 행). 보고 물성 = 물성 · 값 · 단위 · 조건 · 근거 다섯 칸 · 연결 = 템플릿 링크 3개 + 관련 개념 [[ ]] 2개. citekey = 첫 저자 성 + 연도 + 제목 첫 단어(소문자). 초록에 없는 값은 「미기재」로 두고 지어내지 마라. loop_role 은 none(표적 여부는 W18). ../loop/vault/papers/<citekey>.md 로 저장하고(같은 이름이 있으면 먼저 알려라), python ../loop/scripts/lit_extract.py 로 표적이 그대로인지 확인해 out/P2-3_result.md 에 요약해라.

DOI: [10.1016/j.cis.2021.102565]
초록: [Zotero 에서 복사한 초록 또는 본문 일부]
```
확인: 보고 물성의 모든 값에 조건 · 근거 또는 「미기재」 · citekey 가 Better BibTeX 규칙과 일치 · `lit_extract.py` 표적이 밀도 1.018 g/cm³ · CED 354.2 MJ/m³ 그대로(새 노트 loop_role: none). Obsidian 에서 `loop/vault` 를 열면 그래프에 점 1개 · 선 5개(템플릿 링크 3 + 개념 2).
폐루프 ① 문헌 단계 설명 · 이전 판 지시(out/ 저장 · W02 템플릿) = `docs/zotero_obsidian_loop.md`.

## (선택) 채팅형 LLM 으로 쓸 때
Claude Code 를 쓸 수 없으면 위 지시를 브라우저 채팅창에 붙여 넣는다. `@경로` 자리에는 그 파일 내용을 붙여 넣고, 받은 결과는 직접 `out/P2-n_….md` 로 저장한다(`../docs/prompt_setup.md` §5).
