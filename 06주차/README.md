# 06주차 — 물성 계산·후처리 — 역학·부착·점도·응집에너지밀도(CED) 산출

**학습목표**: MD 궤적에서 역학·열물성과 다층 소재 부착력·인장강도, 점도, 응집에너지밀도를 산출하는 자동 후처리 파이프라인을 이해한다.

| 차시 | 주제 | 내용 | 분 |
|---|---|---|---|
| 6-1 | 후처리 개요와 부착·인장 | 역학·열물성 개요와 다층 소재의 부착력·인장강도 평가. | 12 |
| 6-2 | 응집에너지밀도(CED) | CED 개념과 계산법(분자간 상호작용 에너지 직접 산출 방식 vs 간접 차감 방식, Method A vs B). | 14 |
| 6-3 | CED·용해도 파라미터 산출 | 두 지표를 정의·산출한다 — ① 응집에너지밀도(CED): 분자간 상호작용 에너지를 부피로 나눈 값, ② Hildebrand 용해도 파라미터: CED의 제곱근 δ=√CED로 혼화성·용해도 예측. | 10 |
| 6-4 | 점도 산출 | Green–Kubo 및 비평형 MD 방법으로 점도를 산출한다. | 8 |
| 6-5 | 궤적 분석 자동화 | OVITO·MDAnalysis를 이용한 궤적 분석 자동화. | 6 |

## 자료

### 발표용_PDF
발표용 덱 PDF — 강의 · 촬영용(보존용 부록을 뺀 판)

- [06주차_강의_물성 계산·후처리 - 역학·부착·점도·CED.pdf](%EB%B0%9C%ED%91%9C%EC%9A%A9_PDF/06%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98_%EB%AC%BC%EC%84%B1%20%EA%B3%84%EC%82%B0%C2%B7%ED%9B%84%EC%B2%98%EB%A6%AC%20-%20%EC%97%AD%ED%95%99%C2%B7%EB%B6%80%EC%B0%A9%C2%B7%EC%A0%90%EB%8F%84%C2%B7CED.pdf)
- [06주차_보충A_계면 부착 물성.pdf](%EB%B0%9C%ED%91%9C%EC%9A%A9_PDF/06%EC%A3%BC%EC%B0%A8_%EB%B3%B4%EC%B6%A9A_%EA%B3%84%EB%A9%B4%20%EB%B6%80%EC%B0%A9%20%EB%AC%BC%EC%84%B1.pdf)

### 원본덱_PDF
원본 덱 PDF — 수정 전 문구를 부록에 남긴 판(수정 이력 확인용)

- [06주차_강의_물성 계산·후처리 - 역학·부착·점도·CED.pdf](%EC%9B%90%EB%B3%B8%EB%8D%B1_PDF/06%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98_%EB%AC%BC%EC%84%B1%20%EA%B3%84%EC%82%B0%C2%B7%ED%9B%84%EC%B2%98%EB%A6%AC%20-%20%EC%97%AD%ED%95%99%C2%B7%EB%B6%80%EC%B0%A9%C2%B7%EC%A0%90%EB%8F%84%C2%B7CED.pdf)
- [06주차_보충A_계면 부착 물성.pdf](%EC%9B%90%EB%B3%B8%EB%8D%B1_PDF/06%EC%A3%BC%EC%B0%A8_%EB%B3%B4%EC%B6%A9A_%EA%B3%84%EB%A9%B4%20%EB%B6%80%EC%B0%A9%20%EB%AC%BC%EC%84%B1.pdf)

### 강의덱_HTML
강의 덱 HTML 단독 파일판 — 더블클릭하면 열림(서버 · 인터넷 불필요), 「라이브」 슬라이드 조작 가능

- [06주차_강의_물성 계산·후처리 - 역학·부착·점도·CED.html](%EA%B0%95%EC%9D%98%EB%8D%B1_HTML/06%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98_%EB%AC%BC%EC%84%B1%20%EA%B3%84%EC%82%B0%C2%B7%ED%9B%84%EC%B2%98%EB%A6%AC%20-%20%EC%97%AD%ED%95%99%C2%B7%EB%B6%80%EC%B0%A9%C2%B7%EC%A0%90%EB%8F%84%C2%B7CED.html)
- [06주차_보충A_계면 부착 물성.html](%EA%B0%95%EC%9D%98%EB%8D%B1_HTML/06%EC%A3%BC%EC%B0%A8_%EB%B3%B4%EC%B6%A9A_%EA%B3%84%EB%A9%B4%20%EB%B6%80%EC%B0%A9%20%EB%AC%BC%EC%84%B1.html)

### 강의스크립트
강의 스크립트 — Word(편집용) · PDF(읽기 · 인쇄용) · JSON(원본 데이터)

- [06주차_강의스크립트_물성 계산·후처리.docx](%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8/06%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8_%EB%AC%BC%EC%84%B1%20%EA%B3%84%EC%82%B0%C2%B7%ED%9B%84%EC%B2%98%EB%A6%AC.docx)
- [06주차_강의스크립트_물성 계산·후처리.pdf](%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8/06%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8_%EB%AC%BC%EC%84%B1%20%EA%B3%84%EC%82%B0%C2%B7%ED%9B%84%EC%B2%98%EB%A6%AC.pdf)
- [w06.json](%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8/w06.json)

### 평가문항
평가문항 — JSON(원본) · MD(읽기용, 정답 · 해설 포함)

- [06주차_평가문항.md](%ED%8F%89%EA%B0%80%EB%AC%B8%ED%95%AD/06%EC%A3%BC%EC%B0%A8_%ED%8F%89%EA%B0%80%EB%AC%B8%ED%95%AD.md)
- [q06.json](%ED%8F%89%EA%B0%80%EB%AC%B8%ED%95%AD/q06.json)
