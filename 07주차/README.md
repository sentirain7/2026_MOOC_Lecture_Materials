# 07주차 — 아스팔트 소재 — 혼합물 활용·특성과 바인더 MD(SARA·첨가제·다중 힘장)

**학습목표**: 아스팔트 혼합물의 활용·특성을 이해하고, 바인더 분자 모델·첨가제 시스템과 다중 힘장 스택 시뮬레이션을 익힌다.

| 차시 | 주제 | 내용 | 분 |
|---|---|---|---|
| 7-1 | 아스팔트 혼합물과 SARA 모델 | 아스팔트 혼합물의 활용·특성(점탄성·노화·PG 등급)과 SARA 4성분 분자 모델 구성을 다룬다. | 16 |
| 7-2 | 첨가제 분자 라이브러리 | SMILES·RDKit 기술자로 표현한 21종 첨가제 분자 라이브러리. | 12 |
| 7-3 | 다중 힘장 적용 | 아스팔트 바인더 시스템에 OPLS-AA·GAFF2·ReaxFF 스택을 적용. | 12 |
| 7-4 | 노화·점탄성 분석 | 6주 물성 후처리 방법을 활용해 바인더의 노화·점착·점탄성 거동을 분석한다. | 10 |

## 자료

### 발표용_PDF
발표용 덱 PDF — 강의 · 촬영용(보존용 부록을 뺀 판)

- [07주차_강의_아스팔트 소재 - 혼합물 특성과 바인더 MD.pdf](%EB%B0%9C%ED%91%9C%EC%9A%A9_PDF/07%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98_%EC%95%84%EC%8A%A4%ED%8C%94%ED%8A%B8%20%EC%86%8C%EC%9E%AC%20-%20%ED%98%BC%ED%95%A9%EB%AC%BC%20%ED%8A%B9%EC%84%B1%EA%B3%BC%20%EB%B0%94%EC%9D%B8%EB%8D%94%20MD.pdf)

### 원본덱_PDF
원본 덱 PDF — 수정 전 문구를 부록에 남긴 판(수정 이력 확인용)

- [07주차_강의_아스팔트 소재 - 혼합물 특성과 바인더 MD.pdf](%EC%9B%90%EB%B3%B8%EB%8D%B1_PDF/07%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98_%EC%95%84%EC%8A%A4%ED%8C%94%ED%8A%B8%20%EC%86%8C%EC%9E%AC%20-%20%ED%98%BC%ED%95%A9%EB%AC%BC%20%ED%8A%B9%EC%84%B1%EA%B3%BC%20%EB%B0%94%EC%9D%B8%EB%8D%94%20MD.pdf)

### 강의덱_HTML
강의 덱 HTML 단독 파일판 — 더블클릭하면 열림(서버 · 인터넷 불필요), 「라이브」 슬라이드 조작 가능

- [07주차_강의_아스팔트 소재 - 혼합물 특성과 바인더 MD.html](%EA%B0%95%EC%9D%98%EB%8D%B1_HTML/07%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98_%EC%95%84%EC%8A%A4%ED%8C%94%ED%8A%B8%20%EC%86%8C%EC%9E%AC%20-%20%ED%98%BC%ED%95%A9%EB%AC%BC%20%ED%8A%B9%EC%84%B1%EA%B3%BC%20%EB%B0%94%EC%9D%B8%EB%8D%94%20MD.html)

### 강의스크립트
강의 스크립트 — Word(편집용) · PDF(읽기 · 인쇄용) · JSON(원본 데이터)

- [07주차_강의스크립트_아스팔트 소재.docx](%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8/07%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8_%EC%95%84%EC%8A%A4%ED%8C%94%ED%8A%B8%20%EC%86%8C%EC%9E%AC.docx)
- [07주차_강의스크립트_아스팔트 소재.pdf](%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8/07%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8_%EC%95%84%EC%8A%A4%ED%8C%94%ED%8A%B8%20%EC%86%8C%EC%9E%AC.pdf)
- [w07.json](%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8/w07.json)

### 평가문항
평가문항 — JSON(원본) · MD(읽기용, 정답 · 해설 포함)

- [07주차_평가문항.md](%ED%8F%89%EA%B0%80%EB%AC%B8%ED%95%AD/07%EC%A3%BC%EC%B0%A8_%ED%8F%89%EA%B0%80%EB%AC%B8%ED%95%AD.md)
- [q07.json](%ED%8F%89%EA%B0%80%EB%AC%B8%ED%95%AD/q07.json)
