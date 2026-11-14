# week01/data

| 파일 | 크기 | 내용 | 출처 | 라이선스 |
|---|---|---|---|---|
| `asphalt_ml_101.csv` | 22 KB · 101행 × 8열 | 아스팔트 × 기계학습 논문 101편의 서지(DOI · 연도 · 제목 · 피인용 · 기관 · 국가 · 초록 유무 · MD+ML 여부) | COMID 플랫폼 문헌 모듈(Claude Science 내보내기 `asphalt_ml_101.csv`, artifact 5b91edbb) · Crossref · OpenAlex 메타데이터 | 서지 메타데이터 · CC BY 4.0 로 재배포. 논문 전문은 포함하지 않는다 |

열 설명: `doi` 논문 식별자 · `year` 출판 연도 · `title` 제목 · `cites` 피인용 수(수집 시점) · `institutions` 소속 기관(`;` 구분) · `countries` 국가 코드 · `has_abstract` 초록 확보 여부 · `is_md_ml` 분자동역학과 기계학습을 함께 쓴 논문인지.

이 파일은 환경 점검(읽기 · 그림 1장)에만 쓴다. 문헌 도구는 W02, 본격적인 문헌 데이터는 `week02/data/` 에 있다.
