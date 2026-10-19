# 08주차 — 시멘트 소재 — 콘크리트 활용·특성과 수화 MD(C-S-H·ReaxFF·ML 힘장)

**학습목표**: 시멘트 콘크리트의 활용·특성을 이해하고, 클링커 수화 반응을 ReaxFF로 모델링하여 C-S-H 구조·물성을 해석하며, 기계학습 기반 힘장으로의 대체를 이해한다.

| 차시 | 주제 | 내용 | 분 |
|---|---|---|---|
| 8-1 | 시멘트 콘크리트와 클링커 모델 | 시멘트 콘크리트의 활용·특성(강도·내구성)과 클링커 4상(C3S·C2S·C3A·C4AF) 모델링. | 16 |
| 8-2 | ReaxFF 수화 시뮬레이션 | 반응성 힘장 ReaxFF로 클링커 수화 반응을 시뮬레이션. | 14 |
| 8-3 | C-S-H 구조·물성 | 6주 물성 후처리 방법으로 C-S-H의 구조와 역학물성을 해석한다. | 10 |
| 8-4 | ML 힘장 대체 | 고비용 ReaxFF를 기계학습 원자간 퍼텐셜(ML 퍼텐셜)로 대체한다. | 10 |

## 자료

### 발표용_PDF
발표용 덱 PDF — 강의 · 촬영용(보존용 부록을 뺀 판)

- [08주차_강의_시멘트 소재 - 콘크리트 특성과 수화 MD.pdf](%EB%B0%9C%ED%91%9C%EC%9A%A9_PDF/08%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98_%EC%8B%9C%EB%A9%98%ED%8A%B8%20%EC%86%8C%EC%9E%AC%20-%20%EC%BD%98%ED%81%AC%EB%A6%AC%ED%8A%B8%20%ED%8A%B9%EC%84%B1%EA%B3%BC%20%EC%88%98%ED%99%94%20MD.pdf)

### 원본덱_PDF
원본 덱 PDF — 수정 전 문구를 부록에 남긴 판(수정 이력 확인용)

- [08주차_강의_시멘트 소재 - 콘크리트 특성과 수화 MD.pdf](%EC%9B%90%EB%B3%B8%EB%8D%B1_PDF/08%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98_%EC%8B%9C%EB%A9%98%ED%8A%B8%20%EC%86%8C%EC%9E%AC%20-%20%EC%BD%98%ED%81%AC%EB%A6%AC%ED%8A%B8%20%ED%8A%B9%EC%84%B1%EA%B3%BC%20%EC%88%98%ED%99%94%20MD.pdf)

### 강의덱_HTML
강의 덱 HTML 단독 파일판 — 더블클릭하면 열림(서버 · 인터넷 불필요), 「라이브」 슬라이드 조작 가능

- [08주차_강의_시멘트 소재 - 콘크리트 특성과 수화 MD.html](%EA%B0%95%EC%9D%98%EB%8D%B1_HTML/08%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98_%EC%8B%9C%EB%A9%98%ED%8A%B8%20%EC%86%8C%EC%9E%AC%20-%20%EC%BD%98%ED%81%AC%EB%A6%AC%ED%8A%B8%20%ED%8A%B9%EC%84%B1%EA%B3%BC%20%EC%88%98%ED%99%94%20MD.html)

### 강의스크립트
강의 스크립트 — Word(편집용) · PDF(읽기 · 인쇄용) · JSON(원본 데이터)

- [08주차_강의스크립트_시멘트 소재.docx](%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8/08%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8_%EC%8B%9C%EB%A9%98%ED%8A%B8%20%EC%86%8C%EC%9E%AC.docx)
- [08주차_강의스크립트_시멘트 소재.pdf](%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8/08%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8_%EC%8B%9C%EB%A9%98%ED%8A%B8%20%EC%86%8C%EC%9E%AC.pdf)
- [w08.json](%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8/w08.json)

### 평가문항
평가문항 — JSON(원본) · MD(읽기용, 정답 · 해설 포함)

- [08주차_평가문항.md](%ED%8F%89%EA%B0%80%EB%AC%B8%ED%95%AD/08%EC%A3%BC%EC%B0%A8_%ED%8F%89%EA%B0%80%EB%AC%B8%ED%95%AD.md)
- [q08.json](%ED%8F%89%EA%B0%80%EB%AC%B8%ED%95%AD/q08.json)
