# 문헌맵 · 주제 분포 · 기관 분포 · 공백 분석 · 노벨티 판정 · 주장–문헌 지도

원본 11주차 덱 #9 · #11 · #12 · #13 · #18 의 내용을 문서로 옮긴 자료(슬라이드에서는 W02 3차시가 검색식 · 기록 · 동시출현만 다룬다). 수치는 원본 덱과 연구 플랫폼의 Claude Science 내보내기(`claude_science_export/`)에서 가져왔다. 플랫폼 DB 원자료는 열지 않았다.

## 1. 주제별 분포 (267편 · 2021~2026)
문헌맵 보고서(`literature_map_report.md`) 규칙으로 분류한 편수. 한 논문에 주제가 여러 개 붙으므로 합은 267 을 넘는다. 데이터: `data/md_construction_literature_2021_2026.csv` 의 `topics` 열.

| 주제 | 편수 | 주제 | 편수 |
|---|---|---|---|
| 아스팔트 · 역청 | 191 | 노화 · 산화 | 36 |
| 골재 상호작용 | 127 | 콘크리트 · 지오폴리머 | 26 |
| 수분 · 부착 · 계면 | 124 | 나노 첨가제 | 25 |
| 시멘트 · C-S-H | 93 | 다중스케일 | 18 |
| 역학 · 유변 | 81 | ReaxFF · 반응성 | 13 |
| 재생제 · RAP | 81 | 기계학습 | 5 |
| 열 · 확산 | 58 | | |

- 집중 영역: 결합재–골재 계면 (아스팔트 191 · 계면 · 수분 124).
- 상승 주제: 재생 · 재생제(RAP) · 2021년 9편 → 2025년 23편.
- 공백: 기계학습 5편 · 다중스케일 18편.
- 2026년은 연중 수치.

## 2. 기관 분포 (8편 이상 16곳)
데이터: `data/md_corpus_267.csv` 의 `institutions` · `primary_country` 열. 한 논문에 기관이 여럿이면 기관마다 1회.

Chang'an University 37 · Southeast University 16 · Changsha Univ. of Sci. & Tech. 14 · Wuhan University of Technology 13 · Dalian University of Technology 13 · Qingdao University of Technology 13 · Harbin Institute of Technology 13 · RWTH Aachen University 12 · Tongji University 11 · Delft University of Technology 10 · Henan University of Technology 10 · Rutgers University 9 · Chongqing Jiaotong University 9 · Michigan Tech. Univ. 8 · Beijing University of Technology 8 · Hohai University 8

제1 기관 국가: 중국 203 · 미국 19 · 네덜란드 6 · 독일 4 · 미기재 12.

> 주의: `literature_map_report.md` 본문은 소속을 수집하지 않았다고 적고 있어, 이 기관 열이 어느 단계(예: OpenAlex 보강)에서 추가됐는지 원천 기록이 없다. 인용 전 사람 확인 필요.

## 3. 공백 분석 · 문헌 × 플랫폼 보유 데이터
같은 267편을 `md_corpus_267.csv` 에서 더 넓은 어휘로 다시 분류한 값(주제 분포 표와 규칙이 다르다): 아스팔트 · 역청 193 · 수분 · 부착 · 계면 136 · 나노 첨가제 51 · 유변 · 역학 81 · 열 · 확산 62 · 다중스케일 36 · ML · 데이터 기반 5.

연구 플랫폼의 완료 MD 실험 765건에서 지표가 계산된 물성별 건수(원 그림 `fig_gap_coverage.png` 판독값): 밀도 763 · 체적탄성률 716 · CED 694 · RDF 첫 피크 692 · MSD 확산계수 645 · 점도 57 · Tg 45.

→ 문헌에 적은 것(ML · 데이터 기반 5편)과 플랫폼이 많이 가진 것(밀도 · CED 약 700건)을 겹치면 **MD 데이터로 학습한 물성 대리모델**(W13 ~ W15)이 연구 질문이 된다.

두 분류의 차이 예: 제목에 nano 가 들어간 29편은 넓은 규칙에서 모두 나노 첨가제(좁은 규칙 9편), coarse-grained 10편 중 9편이 다중스케일(좁은 규칙 0편).

## 4. 노벨티 판정 (코퍼스 342편 전수조사)
출처: `docs/papers/NOVELTY_ASSESSMENT_20260726.md` 부록 A. 계면 파괴 원고의 주장을 전수조사로 다시 판정해 3항목 상향 · 2항목 하향.

| 판정 | 주장 | 근거 |
|---|---|---|
| ▲ | TTS 붕괴 · 계면 파괴의 노벨티 | Khabaz & Khare (2018) 인용 8편 역추적 · 계면 · 파괴 맥락 인용 0건 |
| ▲ | CED 벌크 검증 | MD 계산 3.26–3.29 × 10⁸ J/m³ ↔ 문헌 최소 7편과 정합 |
| ▲ | 평행 배향 · 약한 결합 | Cao 외 (2023) CBM 364:129970 · 직접 선행 |
| ▼ | MD ↔ 실험 정량 대조 | 선행 3편 확인 → 노벨티 항목에서 제외 |
| ▼ | 강도 – 파괴 모드 탈동조 | 정면 반례 Zhou 외 (2026) CBM 513:145469 → 적용 범위를 건조 · 산화물 · 단결정으로 한정 |

원칙: 원문 미확보 문헌은 판정 근거에서 제외 · 반대 실측은 선제 인용 · “처음 수행” 표현은 선행 0건 확인 후에만.

## 5. 주장–문헌 지도 (citation map)
출처: `docs/papers/CITATION_MAP_BY_TOPIC_20260726.md` (주제 1–15, §Z 검증 불가 총괄). 주제마다 우리 결과 · 동의 문헌 · 부동의 문헌 · 근거 없음 · 원문 확인 지점(표 · 절 번호)을 한 표에 둔다.

예 · 주제 3 계면 조성 → 파괴 모드: 우리 결과 r = −0.79 (계면 0–4 Å 포화분 ↔ 노출률) · 동의: 직접 대응 없음(인접 Huang2023 · CuiWang2024) · 부동의: JinH2026 (CBM 509:145179, BBS 실측) · 판정: 주장 수위 “관찰” · 반대 실측 병기.

규칙: 원문 문장 전재 금지(표 · 절 번호만) · 검증 불가 문헌은 별도 절에 모아 ① 원문 확보 ② 서술 완화 ③ 삭제 순 · 원문 확보 후 인용 계획이 정정된 사례 3건(Wang2015 · Cui2020 · Yao2016).

Obsidian 대응: 주제 = 주장 노트 · 문헌 = 논문 노트 · 동의 · 부동의 = 링크 섹션 → 백링크로 “이 논문이 어느 주장에 쓰였는가” 역조회. (플랫폼은 Obsidian 이 아닌 마크다운 문서로 관리했으며, Obsidian 대응은 수업용 해석이다.)
