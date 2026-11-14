# 폐루프 ① 문헌: Zotero → library.bib → Obsidian 볼트 → 표적 2개 (W02 2-4차시 보충)

덱 24 ~ 26장(2-4차시)의 본문 설명. 덱에는 그림 · 지시 상자만 두고, 순서 · 규칙 · 표는 이 문서에 둔다.
Zotero · Obsidian 은 따로 쓰는 문헌 정리 도구가 아니라 **폐루프의 첫 칸(문헌 → 표적)** 이다(`../../loop/README.md`).

```
Zotero(서지 · 인용키)  ──Better BibTeX 자동 내보내기──▶  loop/lit/library.bib
        │ 인용키 = citekey
        ▼
Obsidian 볼트 loop/vault/papers/<citekey>.md (논문 노트 · 「보고 물성」 표 · loop_role)
        │ python loop/scripts/lit_extract.py
        ▼
lit_values.csv (값 · 단위 · 조건 · citekey) → lit_targets.json = 표적 2개 (밀도 · CED)
        │
        ▼
② 후보 → ③ MD 워크플로우 → ④ 대리모델 → ⑤ EHVI → ⑥ 실행 노트 vault/runs · vault/rounds (근거 [[citekey]] 링크) → W18
```

## 1. 설치 (사람이 직접 하는 것은 Claude Code 하나 · 나머지는 지시문)
| 지시 | 무엇 | 사람이 누를 곳 |
|---|---|---|
| I-3 | Zotero 7 + Better BibTeX `.xpi` 내려받기 | ① 도구 → 플러그인 → 파일에서 설치 ② 컬렉션 내보내기 → Better BibTeX · 「Keep updated」 · 저장 위치 = `loop/lit/library.bib` |
| I-4 | Obsidian · 강좌 볼트 | ① 「폴더를 보관함으로 열기」 → `loop/vault` ② 핵심 플러그인 템플릿 · 템플릿 폴더 = `templates` |
- 전문 · OS 별 명령 · 검증 범위: `../../docs/install_prompts.md` (Ubuntu · WSL2 검증 · macOS · Windows 미검증)
- 강좌 저장소에는 사례 서지 `loop/lit/library.bib`(15편 · Better BibTeX 형식)가 미리 들어 있다 → Zotero 없이도 폐루프는 돈다
- 자동 내보내기를 켜면 이 파일이 내 라이브러리로 바뀐다. `lit_extract.py` 는 .bib 이 아니라 볼트의 노트를 읽으므로 표적은 그대로이고, 강좌 제공 판은 `git checkout loop/lit/library.bib` 으로 되돌린다

## 2. 논문 노트 형식 (`loop/vault/templates/논문노트.md`)
- W02 템플릿(`obsidian_template.md`)에 `loop_role` 한 칸을 더한 판: `target` = 표적에 쓰는 값 · `validation` = 결과 대조용 · `none` = 읽기만
- 「## 보고 물성」 표 = `| 물성 | 값 | 단위 | 조건 | 근거 |` · 값은 숫자만 · 근거 없는 값 기재 금지(없으면 「미기재」)
- 연결: `[[00_루프지도]] · [[밀도]] · [[CED]]` (템플릿에 들어 있음) + 관련 개념

## 3. lit_extract.py 가 읽는 규칙
- 물성 이름: 밀도 → density(g/cm³) · CED → ced(MJ/m³) · 용해도 매개변수 δ(MPa^0.5) → ced = δ²
- 조건 칸에 「25 °C」 또는 「298 K」 가 있는 행만 표적 계산에 쓴다 · 근거 칸에 「표적 아님」 이면 기록만
- 표적 = loop_role 이 target 인 행들의 **중앙값**(튀는 값에 덜 흔들림 · 평균도 함께 기록) · 근거 citekey 목록을 남긴다(실행 노트가 링크)

## 4. 강좌 볼트의 논문 노트 15편 → 표적 (2026-11-14 · `python scripts/lit_extract.py` 결과)
노트 15편 → 값 30행 → 밀도 표적 **1.018 g/cm³** (11편 · 무첨가 바인더 25 °C 실측 22개 중앙값 · 평균 1.0208 · 폭 ±0.02) · CED 표적 **354.2 MJ/m³** (7개 중앙값 · 폭 ±20)

| 노트 (citekey) | 밀도 g/cm³ (표적에 씀) | CED MJ/m³ (표적에 씀) | 표적에서 뺀 행 |
|---|---|---|---|
| ai2024properties | 1.016 · 1.005 · 1.038 | · | · |
| assaf2024predicting | 1.019 · 1.042 · 1.041 · 1.051 · 1.07 | · | · |
| cui2022study | 1.01 · 1.04 | · | · |
| gao2022molecular | · | 382.1 · 354.2 · 353.3 · 354.6 | · |
| jiang2026atomistic | 1.0126 | · | · |
| jiao2022evaluating | 1.012 | · | · |
| li2022investigation | 1.002 | · | · |
| liu2021molecular | 0.95 · 1.08 | · | · |
| liu2025study | · | δ 17.96 MPa^0.5 (CED = δ²) | · |
| ren2022insight | 1.017 | · | · |
| rouidi2024molecular | · | 305.0 | 밀도 0.947 g/cm³ (MD 값(실측 아님) → 표적 아님) |
| yan2022molecular | 0.94 | · | · |
| zhang2021molecular | 1.012 | · | · |
| zhu2019use | · | δ 19.15 MPa^0.5 (CED = δ²) | · |
| zou2024adhesion | 1.01 · 1.02 · 1.03 · 1.04 | · | · |

- 바인더는 증발하지 않아 CED 를 직접 잴 수 없다 → 용해도 시험값(Hansen δt)과 MD 문헌값을 함께 썼다(`../../loop/README.md` 표적 절)

## 5. P2-3 과 표적
- P2-3 의 새 노트는 `loop_role: none` 으로 둔다 → `lit_extract.py` 를 다시 돌려도 표적은 밀도 1.018 · CED 354.2 그대로 · 폐루프 재생 모드의 기준 경로(`loop/expected_output/`)도 그대로
- 새 노트를 표적에 넣으려면(W18 · 내 문제로 바꾸기): 실측값 · 조건(25 °C 또는 298 K) · 근거(표 · 쪽)를 확인한 뒤 `loop_role: target` → `lit_extract.py` → 바뀐 표적으로 루프를 처음부터

---

## 덱에서 옮긴 내용 (2026-11-14 · 폐루프 반영으로 24 ~ 26장 화면을 바꾸며 보존)

### 24장 (이전 제목) Zotero 4단계 → 인용키 1개 = 서지 · 노트 · 원고 · 데이터 출처
- 부제: 이름 하나를 네 곳이 공유 → 「어느 논문의 값인가」 끝까지 추적
- ④ .bib 자동 내보내기: LaTeX · Pandoc · Obsidian 공유
- 출처 줄: Zotero · Better BibTeX 설정 = repo/week02/docs/obsidian_template.md

### 25장 (이전 제목) Obsidian 최소 = 볼트 · 위키링크 · 백링크 · 노트 템플릿 → 그래프
- 부제: 볼트 = 폴더 1개 · 노트 = 평문 .md · [[이름]] 한 번 = 선 하나 · 템플릿 필드가 W11 자동 추출 · W16 주장–문헌 지도의 열
- 노트 예시 `yao2022discussion.md · 논문 노트 템플릿`:
```
---
citekey: yao2022discussion
doi: 10.1016/j.cis.2021.102565
year: 2022   tags: [review, force-field]   status: 읽음
---
## 한 줄 요약
## 계 · 힘장 · 앙상블
## 보고 물성   # 값 · 단위 · 조건 · 근거(표 · 쪽)
## 연결   [[GAFF2]]  [[CED]]  [[부착일]]
```
- 노트 아래 줄: YAML 속성 4 + 본문 4 · W11 자동 추출 스키마와 같은 필드 · 볼트 = 폴더 1개 · git 으로 관리 가능
- 그래프 그림: 가운데 yao2022 → GAFF2 · CED · 부착일 · li2014 (선 4) + GAFF2–CED · 부착일–GAFF2 · 「그래프 뷰 = 링크 누적 · 없는 이름 클릭 = 새 노트」
- 결론 띠: 보고 물성은 **값 · 단위 · 조건 · 근거(표 · 쪽)** 네 칸 · 근거 없는 값 기재 금지
- 강의 노트에서 옮긴 설명: 링크를 받은 노트에는 백링크가 자동으로 생겨 이 논문을 인용한 노트를 거꾸로 찾는다 · yao2022 노트가 GAFF2 · CED · 부착일에 연결되고 li2014 노트도 같은 개념에 연결되면 두 논문이 개념을 통해 이어진다 · 아직 없는 이름을 클릭하면 새 노트가 만들어진다 · 보고 물성 필드가 W11 LLM 추출 스키마와 같은 것은 사람이 쓴 노트와 LLM 이 추출한 값을 같은 표로 나란히 대조하기 위해서

### 26장 P2-3 이전 판 (W02 템플릿 · out/ 저장)
```text
아래 논문의 노트를 @docs/obsidian_template.md 의 템플릿으로 작성해라. 제목 · 연도 · 학술지는 @data/md_corpus_267.csv 의 같은 DOI 행에서 읽어라. 형식: YAML(citekey · doi · year · tags · status) → ## 한 줄 요약 → ## 계 · 힘장 · 앙상블 → ## 보고 물성(값 · 단위 · 조건 · 근거(표 · 쪽) 네 칸의 표) → ## 연결(관련 개념을 [[ ]] 위키링크로 3개). citekey 는 첫 저자 성 + 연도 + 제목 첫 단어(소문자). 초록에 없는 값은 「미기재」로 두고 지어내지 마라. P2-3 결과로 out/P2-3_<citekey>.md 에 저장해라.

DOI: [10.1016/j.cis.2021.102565]
초록: [Zotero 에서 복사한 초록 또는 본문 일부]
```
- 명령 줄: 2. 노트 → out/P2-3_<citekey>.md (자동 저장) · 3. Obsidian 볼트 폴더에 복사 → 그래프에 점 1개
- 기대 결과 `out/P2-3_yao2022discussion.md`: citekey yao2022discussion · year 2022 · status 읽음 · tags [review, asphalt, MD] · 보고 물성 | 밀도 | g/cm³ | 298 K | 미기재(리뷰) | · 연결 [[GAFF2]] [[CED]] [[SARA 모델]]
- 캡션: 「미기재」 칸 = 지어낸 값 없음의 표시 · 볼트에 넣으면 [[ ]] 3개 → 선 3개 · 지도에 점 1개 추가
- 확인: citekey 가 Zotero 의 Better BibTeX 규칙과 같은가 (yao2022discussion) · 연결 위키링크 2개 이상
