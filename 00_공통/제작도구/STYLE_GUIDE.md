# 강의 덱 스타일 가이드

「건설소재 역설계 도구 개발을 위한 AI와 분자동역학 활용」 MOOC 강의 덱(`*.dc.html`) 17개에 공통으로 적용하는 번호 규칙과 디자인 규격이다.

- **디자인 기준**: 2·3주차 덱. 두 덱에서 실제 쓰인 값을 집계해 가장 많이 쓰인 값을 규격으로 삼았다. 1주차도 이 규격에 맞춘다.
- **번호 기준**: 강의계획서 `uploads/강의계획서_건설소재역설계_MOOC.hwp`. 추출본은 `tools/syllabus.json`이다.
- **디자인 토큰**: `_ds/nacmid-design-system-…/tokens/`(NACMID).
- **기계 점검**: `tools/check_style.py`. 이 문서와 점검 도구의 규격 상수는 항상 같게 유지한다.

---

## 1. 파일과 덱 매핑

덱과 주차의 대응은 `tools/decks.json`에 정의한다.

**파일명 규칙**(2026-09-22 정리): `NN주차_강의_<계획서 주차명>.dc.html`, `NN주차_보충A_<제목>.dc.html`.
- 두 자리 주차 번호(`01`…`13`)로 정렬 순서를 맞춘다.
- `_강의_`가 `_보충A_`보다 먼저 정렬되어, 같은 주차 안에서 본강의가 앞에 온다.
- 이전 이름은 `decks.json`의 `orig`에 남아 있다. 과거 커밋을 조회할 때 쓴다.

| 파일 | 주차 | 구분 | 차시 코드 |
|---|---|---|---|
| 1–9주차 본강의 | 1–9 | 본강의 | 계획서 그대로 (`1-1`…) |
| 6주차 보충 · 계면 부착 물성 | 6 | 보충 A | `6-S1`~`6-S4` |
| 10주차 · 기계학습 (2) GNN과 능동학습 | 10 | 본강의 | `10-1`~`10-4` |
| 10주차 보충 · 대리모델 평가와 불확실성 | 10 | 보충 A | `10-S1`~`10-S4` |
| 10주차 보충 · 능동학습과 탐색 전략 | 10 | 보충 B | `10-S5`~`10-S8` |
| 11·12·13주차 본강의 | 11–13 | 본강의 | 계획서 그대로 |
| 13주차 보충 · 플랫폼 통합과 최종 프로젝트 | 13 | 보충 A | `13-S1`~`13-S4` |

---

## 2. 번호 규칙

### 2.1 본강의

| 위치 | 형식 | 예 |
|---|---|---|
| 표지 상단 라벨 | `WEEK NN · 차시 N-1 ~ N-k · 총분` | `WEEK 03 · 차시 3-1 ~ 3-4 · 50분` |
| 지난 주차 상단 라벨 | `RECAP · WEEK NN` (직전 주차) | `RECAP · WEEK 02` |
| 학습목표·구성·정리 제목 | `N주차 학습목표` / `N주차 구성` / `N주차 정리` | `3주차 구성` |
| 구성 슬라이드 행 | 차시 코드 · 계획서 차시명 · 계획서 시간 | `3-1 · 힘장 개관 · 16분` |
| 구분 슬라이드 | `data-label="[N-k] 섹션"`, 큰 번호 `N-k`, 부제 첫머리 `M분 ·` | `[3-1] 섹션` · `16분 · …` |
| 본문 상단 라벨 | `N-k · KEYWORD` (영문 대문자 키워드) | `3-1 · TERMS` |
| `data-screen-label` | 덱 안 순번, 두 자리 (`01`, `02`, …) | 29번째 슬라이드 → `29` |

- 표지의 총 시간과 차시별 시간은 강의계획서 값을 쓴다. 현재 계획서는 모든 주차가 50분이다.
- 발표자 노트(`data-speaker-notes`)와 본문 속 "N주차" 언급도 같은 번호 체계를 따른다. 점검 도구는 이 부분을 검사하지 않으므로 사람이 확인한다.
- 계획서에 없는 차시를 덱에 추가하면 계획서 쪽을 먼저 고친다. 덱이 계획서보다 앞서가지 않게 한다.

### 2.2 보충 강의

| 위치 | 형식 | 예 |
|---|---|---|
| 표지 상단 라벨 | `WEEK NN · 보충 A · 차시 N-S1 ~ N-S4 · 총분` | `WEEK 10 · 보충 B · 차시 10-S5 ~ 10-S8 · 45분` |
| 지난 주차 슬라이드 | `RECAP · WEEK NN` — 같은 주차 본강의(보충 B는 보충 A)를 가리킨다 | `RECAP · WEEK 10` |
| 학습목표·구성·정리 제목 | `N주차 보충 A 학습목표` 등 | `10주차 보충 B 구성` |
| 차시 코드 | `N-S번호`. 한 주에 보충이 둘이면 번호를 이어 쓴다 (A: S1~S4, B: S5~S8) | `10-S5 · ACQUISITION` |

보충 강의의 시간은 계획서에 없으므로 덱에 적힌 값을 유지한다.

---

### 2.3 내용 보존 · 부록 · 주차 간 공유

**기존 슬라이드의 내용은 삭제하지 않는다.** 글자 크기, 여백, 번호, 문구 다듬기 같은 수정은 할 수 있다.

1. **맞지 않는 슬라이드는 맨 뒤로 옮긴다.** 순서나 구성상 해당 주차 계획서 차시에 맞지 않는 슬라이드는 덱 맨 뒤의 부록 구간으로 옮긴다. 빈 자리에는 계획서에 맞는 슬라이드를 새로 추가한다.
2. **부록 구간 형식**
   - 정리 슬라이드 뒤에 부록 구분 슬라이드를 하나 둔다. `data-label="부록"`, 큰 번호 자리에 `APPX`, 제목 `부록 · 참고 자료`를 쓴다.
   - 부록 슬라이드는 `data-label`을 `부록 · 원래 라벨`로 바꾼다.
   - 상단 라벨은 `APPENDIX · KEYWORD`로 바꾼다.
   - 발표자 노트 맨 앞에 `[부록] 원래 위치: N-k, #원래순번.`을 적는다.
3. **주차 간 공유**
   - 다른 주차 덱에 이 주차에 맞는 슬라이드가 있으면, 그 슬라이드를 이 주차 덱의 알맞은 차시 위치로 **복사**한다.
   - 복사본은 이 주차의 차시 코드와 번호 체계를 따른다. 발표자 노트 맨 앞에 `[공유] 출처: M주차 덱 #순번.`을 적는다.
   - 원본 덱의 슬라이드는 그대로 둔다. 원본 주차에도 맞지 않으면 원본 덱에서는 부록으로 옮긴다.
4. **이동·복사 기록**: 모든 이동과 복사는 `tools/moves.md`에 한 줄씩 남긴다. 형식은 `날짜 · 출발 덱 #순번 → 도착 덱 #순번 · 이동/복사 · 사유`이다.

---

## 3. 서체

| 서체 | 스택 | 용도 |
|---|---|---|
| **Pretendard** (sans) | `'Pretendard Variable',Pretendard,'Noto Sans KR',sans-serif` | 기본. `<section>`에 지정하고 하위 요소는 상속 |
| **JetBrains Mono** (mono) | `'JetBrains Mono',monospace` | 상단 라벨, 번호, 카드 라벨, 코드, 표지 메타 정보, 배지 |
| **STIX Two Text** (math) | `'STIX Two Text','Cambria Math',serif` + `word-spacing:0.14em;font-feature-settings:'ss04';letter-spacing:0.01em` | 수식. 변수는 `<i>`로 감싼다 |

수식을 쓰는 덱은 `<helmet>` 안에 다음 링크를 추가한다(2·3주차와 같은 줄).

```html
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=STIX+Two+Text:ital,wght@0,400..700;1,400..700&display=swap">
```

---

## 4. 글자 크기 (타입 스케일)

**최소 크기는 24px이다.** 아래 표에 없는 크기는 쓰지 않는다. `<svg>` 내부 글자는 viewBox 좌표라 이 규칙에서 제외한다.

### 4.1 Pretendard (sans)

| 크기 | 굵기 · 줄간격 · 자간 | 역할 |
|---|---|---|
| 88 | 700 · 1.08 · −0.03em | 표지 제목 `<h1>` |
| 68 | 700 · 1.1 · −0.02em | 구분 슬라이드 제목 `<h2>` |
| 52 | 700 · 1.1 · −0.02em | 본문·구조 슬라이드 제목 `<h2>` |
| 40 | 400 · 1.4 | 표지 부제 (`#94a3b8`) |
| 38 | 400–600 · 1.45 | 구성 행 차시명(600), 정리 항목(400) |
| 36 | 400 · 1.45 | 학습목표 항목 |
| 32 | 400 · 1.45 | 지난 주차 카드 본문, 한 줄 강조 문장 |
| 30 | 400 · 1.4 | 구분 슬라이드 부제 (`#94a3b8`), 큰 본문 |
| 28 | 400–600 · 1.4 | 강조 본문, 카드 핵심 문장 |
| 26 | 400 · 1.4 | 기본 본문 |
| 24 | 400 · 1.4 | 보조 설명, 캡션, 출처 (`#94a3b8` 또는 `#64748b`) |

### 4.2 JetBrains Mono (mono)

| 크기 | 역할 |
|---|---|
| 120 | 구분 슬라이드 큰 번호 (`#1f2937`, 700, 줄간격 1) |
| 44 | 큰 지표 숫자 |
| 34 | 구성·정리 목록 번호 (`3-1`, `01`) |
| 32 | 학습목표 목록 번호 |
| 28 | 표지 라벨·메타 정보, 배지, 실습 단계 번호, 구성 행 시간(`#64748b`) |
| 26 | 본문 상단 라벨(자간 0.14em, `#599eff`), 코드 블록, 카드 머리 라벨 |
| 24 | 카드 라벨(자간 0.06em), 표 머리, 인라인 코드 |

### 4.3 STIX Two Text (math)

36(중심 수식) · 32 · 30 · 28 · 26 · 24(본문 속 짧은 식). 수식 색은 `#8ec0ff`.

### 4.4 규격 밖 값의 정규화

기존 덱을 고칠 때 아래 순서로 가장 가까운 허용값에 맞춘다. 맞춘 뒤 넘침 여부를 반드시 확인한다(§8).

| 현재 값 | 바꿀 값 |
|---|---|
| 20–23 | 24 |
| 25 | 보조색(`#94a3b8`/`#64748b`)이면 24, 아니면 26 |
| 27 | 굵기 600 이상이면 28, 아니면 26 |
| 29 | 28 |
| 31 · 33 · 34 (sans) | 32 |
| 35 | 36 |
| 42–48 (sans, 제목 아님) | 40 |
| mono 25 · 27 | 상단 라벨이면 26, 아니면 24 · 28 |
| mono 29 · 30 | 28 |
| mono 31 · 33 | 32 · 34 |
| 본문 `<h2>` 44–72 | 52 |
| 구분 `<h2>` 60–72 | 68 |

---

## 5. 슬라이드 유형

모든 `<section>`은 `color:#f1f5f9`, Pretendard 스택, `display:flex;flex-direction:column`을 갖는다.

| 유형 | `data-label` | 배경 | padding | gap |
|---|---|---|---|---|
| 표지 | `표지` | `#0c1222` | `100px 100px 80px` | `justify-content:space-between` |
| 지난 주차 | `지난 주차` | `#0c1222` | `56px 90px 44px` | 26px |
| 학습목표 | `학습목표` | `#111827` | `56px 90px 44px` | 26px |
| 구성 | `N주차 구성` | `#0c1222` | `56px 90px 44px` | 26px |
| 구분 | `[N-k] 섹션` | `#111827` | `100px` | 40px · `justify-content:center` |
| 본문 | 자유 (짧은 한국어 명사구) | `#0c1222` / `#111827` 교대 | 기본 `56px 90px 44px` · 조밀 `40px 80px 28px` · 최조밀 `34px 80px 22px` | 16–26px |
| 실습 안내 | `실습 안내` | `#111827` | `56px 90px 44px` | 26px |
| 정리 | `N주차 정리` | `linear-gradient(135deg,#111827,#0c1222)` | `56px 90px 44px` | 26px |

- 본문 슬라이드 여백은 기본값을 먼저 쓴다. 내용이 넘칠 때만 조밀 → 최조밀 순으로 내린다. 그래도 넘치면 글자를 줄이지 말고 슬라이드를 나눈다.
- 슬라이드 크기는 1920×1080이며, 덱은 `<x-import component-from-global-scope="deck-stage" …>` 안에 `<section>`을 나열한다.

### 5.1 표지

```html
<section data-label="표지" data-screen-label="01" data-speaker-notes="…" style="background:#0c1222;color:#f1f5f9;font-family:'Pretendard Variable',Pretendard,'Noto Sans KR',sans-serif;padding:100px 100px 80px;display:flex;flex-direction:column;justify-content:space-between;">
  <div style="display:flex;align-items:center;gap:28px;">
    <div style="width:64px;height:64px;border-radius:14px;background:linear-gradient(135deg,#3377ff,#8b5cf6);"></div>
    <div style="font-family:'JetBrains Mono',monospace;font-size:28px;letter-spacing:0.16em;color:#94a3b8;">COMID</div>
  </div>
  <div style="display:flex;flex-direction:column;gap:40px;max-width:1500px;">
    <div style="font-family:'JetBrains Mono',monospace;font-size:28px;letter-spacing:0.14em;color:#599eff;">WEEK 03 · 차시 3-1 ~ 3-4 · 50분</div>
    <h1 style="font-size:88px;font-weight:700;letter-spacing:-0.03em;line-height:1.08;margin:0;">주차명</h1>
    <p style="font-size:40px;color:#94a3b8;margin:0;line-height:1.4;">차시 주제 · 차시 주제 · …</p>
  </div>
  <div style="display:flex;gap:56px;font-size:28px;color:#64748b;font-family:'JetBrains Mono',monospace;">
    <span>윤태영 (Taeyoung Yun)</span><span>실습 · 도구</span><span>퀴즈 3주차</span>
  </div>
</section>
```

### 5.2 본문 슬라이드 머리

```html
<section data-label="힘장의 구성" data-screen-label="06" data-speaker-notes="…" style="background:#0c1222;color:#f1f5f9;font-family:'Pretendard Variable',Pretendard,'Noto Sans KR',sans-serif;padding:56px 90px 44px;display:flex;flex-direction:column;gap:20px;">
  <div style="font-family:'JetBrains Mono',monospace;font-size:26px;letter-spacing:0.14em;color:#599eff;">3-1 · TERMS</div>
  <h2 style="font-size:52px;font-weight:700;letter-spacing:-0.02em;line-height:1.1;margin:0;">제목은 한 줄 결론형 문장</h2>
  <!-- 본문 -->
</section>
```

### 5.3 구분 슬라이드

```html
<section data-label="[3-1] 섹션" data-screen-label="05" data-speaker-notes="…" style="background:#111827;color:#f1f5f9;font-family:'Pretendard Variable',Pretendard,'Noto Sans KR',sans-serif;padding:100px;display:flex;flex-direction:column;justify-content:center;gap:40px;">
  <div style="width:200px;height:6px;background:linear-gradient(135deg,#3377ff,#8b5cf6);border-radius:999px;"></div>
  <div style="font-family:'JetBrains Mono',monospace;font-size:120px;color:#1f2937;font-weight:700;line-height:1;">3-1</div>
  <h2 style="font-size:68px;font-weight:700;letter-spacing:-0.02em;margin:0;line-height:1.1;">계획서 차시명</h2>
  <p style="font-size:30px;color:#94a3b8;margin:0;">16분 · 다루는 내용 · 다루는 내용</p>
</section>
```

### 5.4 구성 행 · 목록 행 · 정리 하단

```html
<!-- 구성 행 -->
<div style="display:flex;align-items:center;gap:40px;background:#111827;border:1px solid #1f2937;border-radius:12px;padding:32px 40px;">
  <div style="font-family:'JetBrains Mono',monospace;font-size:34px;color:#599eff;width:120px;">3-1</div>
  <div style="font-size:38px;font-weight:600;flex:1;">계획서 차시명</div>
  <div style="font-family:'JetBrains Mono',monospace;font-size:28px;color:#64748b;">16분</div>
</div>

<!-- 학습목표 행 (정리 행은 번호 34px · 본문 38px) -->
<div style="display:flex;gap:36px;align-items:baseline;">
  <div style="font-family:'JetBrains Mono',monospace;font-size:32px;color:#599eff;width:80px;">01</div>
  <div style="font-size:36px;line-height:1.45;flex:1;">목표 문장</div>
</div>

<!-- 정리 하단 -->
<div style="margin-top:auto;display:flex;gap:40px;align-items:center;border-top:1px solid #1f2937;padding-top:36px;">
  <span style="font-size:28px;padding:14px 28px;border-radius:999px;background:rgba(59,130,246,0.20);color:#60a5fa;border:1px solid rgba(59,130,246,0.30);font-family:'JetBrains Mono',monospace;">퀴즈 3주차</span>
  <span style="font-size:32px;color:#94a3b8;">다음 주차 — 다음 주차명</span>
</div>
```

목록 번호 색은 위에서부터 `#599eff` → `#8ec0ff` → `#a5b4fc` → `#a78bfa` 순으로 쓴다.

---

## 6. 구성 요소

| 요소 | 규격 |
|---|---|
| 기본 카드 | `background:#111827;border:1px solid #1f2937;border-radius:12px;padding:22px 30px` (여유 있으면 `40px`) |
| 강조 카드 | 기본 카드 + `border:1px solid #2d3748` 또는 `border-left:3px solid <강조색>` |
| 이번 주차 카드(지난 주차 슬라이드) | 강조 카드 + `box-shadow:0 0 20px rgba(59,130,246,0.15)` |
| 카드 머리 라벨 | mono 24px, 자간 0.06em, 강조색(`#60a5fa`, `#a78bfa`, `#4ade80` …) |
| 코드 블록 | 카드 배경 `#0c1222` 안에 `<pre>` mono 26px, 줄간격 1.7, `#8ec0ff`, `white-space:pre-wrap` |
| 배지 | mono 28px, `padding:14px 28px;border-radius:999px`, 배경·테두리는 강조색 rgba 0.20/0.30 |
| 구분선 | `1px solid #1f2937` |
| 모서리 | 카드 12px · 작은 칩 8px · 배지 999px · 로고 14px |

---

## 7. 색상

`tokens/colors.css`의 NACMID 토큰만 쓴다. 토큰에 없는 색 중에서는 `#6366f1`, `#cbd5e1`, `#e2e8f0`, `#f8fafc`만 허용한다.

| 역할 | 값 |
|---|---|
| 배경 | `#0c1222` (canvas) · `#111827` (secondary, 카드) · `#1f2937` (tertiary) |
| 테두리 | `#1f2937` 기본 · `#2d3748` 강조 · `#374151` 밝음 |
| 글자 | `#f1f5f9` 기본 · `#94a3b8` 보조 · `#64748b` 메타 · `#475569` 흐림 |
| 브랜드 파랑 | `#3377ff` · `#599eff` (상단 라벨, 번호) · `#60a5fa` · `#8ec0ff` (강조어, 수식) |
| 브랜드 보라 | `#8b5cf6` · `#a78bfa` · `#a5b4fc` |
| 의미색 | 성공 `#4ade80`/`#34d399` · 경고 `#facc15`/`#f59e0b` · 오류 `#f87171` · 주황 `#fb923c` |

본문 속 강조어는 `<span style="color:#8ec0ff;">`로 표시한다.

---

## 8. 작성 규칙

- **용어**: 자주 쓰이지 않는 전문 용어가 처음 나올 때는 영어를 함께 적는다. `이종쌍(unlike pair)` 또는 `이종쌍 · unlike pair` 형식이다(`CLAUDE.md`).
- **그림**: 새 그림은 `assets/`에 두고 상대경로(`assets/…`)로 참조한다. 보충 내용은 `LAMMPS_Asphalt` 저장소의 캠페인 결과물과 논문 그림을 먼저 활용한다.
- **넘침**: 글자 크기를 바꾼 슬라이드는 `tools/check_overflow.js`로 넘침을 확인한다. 넘치면 여백 단계를 내리고, 그래도 넘치면 슬라이드를 나눈다. 24px 아래로 줄이지 않는다.
- **가시성 우선 · 슬라이드 분할**: 넘치지 않더라도 한 장에 내용이 너무 많아 읽기 어려우면 슬라이드를 나눈다. 기준은 한 장에 핵심 메시지 하나다. 나눈 슬라이드는 같은 `data-label`에 `(1/2)`, `(2/2)`를 붙이고, 상단 라벨 키워드도 `· 1 / 2` 형식으로 맞춘다. 분할은 내용 삭제가 아니므로 §2.3과 충돌하지 않는다.
- **전체 흐름 정리**: 표준화 도중이나 마지막에 덱마다 한 번씩 흐름을 점검한다. 슬라이드 순서가 계획서 차시 흐름을 따르는지, 각 차시가 "왜 → 무엇 → 어떻게 → 확인" 순으로 이해되는지, 앞뒤 주차 연결 문장이 맞는지를 본다.

---

## 9. 점검 도구

```bash
python3 tools/check_style.py                  # 17개 덱 요약표 (규칙별 위반 건수)
python3 tools/check_style.py 3                # 3주차 덱 상세 목록
python3 tools/check_style.py --rules numbering,minutes 10
python3 tools/check_style.py --json > report.json
```

| 규칙 | 등급 | 검사 내용 |
|---|---|---|
| `font-size` | ERROR | 24px 미만, 서체별 허용 크기(§4) 밖 |
| `heading` | ERROR | 표지 h1 88 · 구분 h2 68 · 본문 h2 52 |
| `padding` | ERROR | 슬라이드 유형별 여백(§5) |
| `screen-label` | ERROR | `data-screen-label`이 순번(두 자리)과 불일치 |
| `numbering` | ERROR | 표지 WEEK, 지난 주차, 제목의 N주차, 구분·구성·상단 라벨의 차시 코드 |
| `minutes` | ERROR | 표지 총 시간, 구성 행·구분 슬라이드 시간 ↔ 계획서 |
| `color` | WARN | 팔레트(§7) 밖 색상 |
| `background` | WARN | 슬라이드 배경(§5) |

ERROR가 하나라도 있으면 종료 코드 1을 돌려준다. 발표자 노트, 본문 속 주차 언급, 넘침은 검사하지 않는다.

---

## 10. 문체 · 표현 규칙 (2026-09-22 추가)

### 10.1 개조식
슬라이드 화면의 모든 문장은 개조식으로 쓴다. 발표자 노트는 말로 하는 설명이라 서술형을 허용한다.

| 쓰지 않음 (서술형) | 씀 (개조식) |
|---|---|
| 자르지 않고 나눠서 더한다 | 자르지 않고 분할 후 합산 |
| 밀도는 궤적 평균으로 계산한다 | 밀도 = 궤적 평균 |
| 시드를 바꿔 다시 실행해야 한다 | 시드 변경 후 재실행 필요 |
| 계산 비용이 크게 줄어든다 | 계산 비용 대폭 감소 |
| 이 방법은 층상 셀에만 쓸 수 있다 | 층상 셀에만 적용 가능 |
| 원인은 이웃 목록 갱신 누락이다 | 원인: 이웃 목록 갱신 누락 |

- 문장 끝은 명사형(「…함」「…됨」「…임」), 명사구, 「→」·「:」·「=」 표기로 맺는다. 「…다」「…한다」「…이다」「…합니다」로 끝내지 않는다.
- 한 항목에는 한 가지 사실만 쓴다. 항목이 길면 「·」로 끊거나 항목을 나눈다.
- 제목(h2)도 명사구 또는 개조식으로 쓴다(예: 「세 개의 테이블로 나눈다」 → 「조성 · 실행 · 물성 세 테이블 분리」).

### 10.2 영어 병기
- 덱마다 전문 용어가 **처음** 나올 때 영어를 함께 적는다. 형식은 `한국어(English)` 또는 `한국어 · English`다.
  - 예: 크리프 강성(creep stiffness), 동적전단 레오미터(DSR, Dynamic Shear Rheometer)
- 각 덱은 따로 강의되므로, 앞 주차에서 병기한 용어도 그 덱에서 처음 나오면 다시 병기한다.
- 약어는 처음 나올 때 풀어 쓴다(예: 시간-온도 중첩(TTS, time–temperature superposition)).

### 10.3 직설 표현
- 은유 · 비유 · 의인화를 쓰지 않는다. 대상과 관계를 직접 쓴다.

| 쓰지 않음 | 씀 |
|---|---|
| 데이터베이스의 뼈대 | 데이터베이스의 기본 구조 |
| 능동학습의 연료 | 능동학습의 입력 |
| 순열 불변성이 공짜로 따라옴 | 순열 불변성이 구조상 자동 보장 |
| 두 단계 사이에 다리를 놓는 주차 | 두 단계를 연결하는 주차 |
| 모델의 무지 | 학습 데이터 부족에서 오는 불확실성 |

---

## 11. 그림 · 배치 규칙 (2026-09-22 추가)

- **겹침 금지**: 글자가 선 · 화살표 · 도형 테두리 · 그림 · 다른 글자와 겹치지 않게 한다.
  - 화살표 라벨은 선의 위나 아래로 충분히 띄운다(선과 8px 이상 간격).
  - 상자 안 글자는 테두리 안쪽 여백을 12px 이상 둔다.
- **그림 속 글자 크기**: SVG 안 글자의 실제 화면 크기(설계 px, viewBox 배율 반영)는 18–28px로 쓰고, 32px를 넘기지 않는다. 본문(24–28px)보다 크게 쓰지 않는다.
- **점검 도구**:
  - `tools/check_layout.js`: hit-test 방식으로 선 겹침, 글자 겹침, 그림 속 큰 글자를 본다.
  - `tools/check_overlap_px.js` + `tools/check_overlap_px.py`: 픽셀 방식으로 화살촉 · 이미지 위 글자까지 본다.
  - 두 도구 모두 0건이어야 한다.

## 12. 동적 설명도구 (인터랙티브 슬라이드)

덱마다 `<script type="text/x-dc" data-dc-script …>class Component extends DCLogic { … }</script>` 하나가 들어 있다(비어 있는 덱도 있다). 동적 설명도구는 이 컴포넌트에 추가한다. 예시는 2주차 부록 「라이브 · NVE ⇄ NVT」이다.

- **상태와 핸들러**: `state = {…}`에 상태를 두고, `renderVals()`가 돌려주는 객체의 함수를 슬라이드 HTML에서 `onClick="{{ 이름 }}"`으로 연결한다.
- **화면 갱신**: `document.getElementById(id)`로 SVG 요소의 속성(`points`, `x`, `y2` 등)이나 `textContent`를 직접 바꾼다. 상태를 바꾼 뒤에는 `setTimeout(() => this.draw(), 0)`으로 다시 그린다.
- **한 덱에 도구가 여러 개**: id와 핸들러 이름에 도구별 접두어를 붙인다(예: `tts_`, `bbr_`). 그리는 함수는 `componentDidMount`에서 모두 호출한다.
- **정리**: 타이머를 쓰면 `componentWillUnmount`에서 해제한다.
- **예약 문법**: 화면 글자에 `{{`, `}}`를 쓰지 않는다(템플릿 문법으로 처리됨).
- **camelCase 변환**: 본문 글자에 `camelCase=` 형태가 있으면 런타임이 `sc-camel-…`로 바꿔 버린다. `=`를 `&#61;`로 쓴다(예: `randomSeed&#61;42`).
- **표시 기준**: 조작 버튼은 24px 이상 글자, 38px 이상 높이로 만든다. 조작 결과로 바뀌는 값(수치 · 곡선)을 화면에 함께 보인다.
- **근거**: 도구에 쓰는 식과 계수는 원천 자료(측정 데이터, 논문, 표준식)에서 가져오고, 발표자 노트에 출처를 적는다.
