# 09주차 — 기계학습 (1) — 분자 표현자와 대리모델(XGBoost+SHAP)

**학습목표**: 분자 표현자 설계와 XGBoost+SHAP 대리모델, 모델 해석·검증을 이해한다.

| 차시 | 주제 | 내용 | 분 |
|---|---|---|---|
| 9-1 | 표현자와 feature library | 분자 표현자(RDKit·SMILES·fingerprint)와 feature library 구축. | 18 |
| 9-2 | XGBoost 대리모델 | 적절한 데이터 분할로 XGBoost 대리모델을 학습·검증한다. | 16 |
| 9-3 | SHAP 해석 | SHAP으로 모델 예측을 해석하고 특징을 재정련한다. | 16 |

## 자료

### 발표용_PDF
발표용 덱 PDF — 강의 · 촬영용(보존용 부록을 뺀 판)

- [09주차_강의_기계학습 (1) - 분자 표현자와 대리모델.pdf](%EB%B0%9C%ED%91%9C%EC%9A%A9_PDF/09%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98_%EA%B8%B0%EA%B3%84%ED%95%99%EC%8A%B5%20%281%29%20-%20%EB%B6%84%EC%9E%90%20%ED%91%9C%ED%98%84%EC%9E%90%EC%99%80%20%EB%8C%80%EB%A6%AC%EB%AA%A8%EB%8D%B8.pdf)

### 원본덱_PDF
원본 덱 PDF — 수정 전 문구를 부록에 남긴 판(수정 이력 확인용)

- [09주차_강의_기계학습 (1) - 분자 표현자와 대리모델.pdf](%EC%9B%90%EB%B3%B8%EB%8D%B1_PDF/09%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98_%EA%B8%B0%EA%B3%84%ED%95%99%EC%8A%B5%20%281%29%20-%20%EB%B6%84%EC%9E%90%20%ED%91%9C%ED%98%84%EC%9E%90%EC%99%80%20%EB%8C%80%EB%A6%AC%EB%AA%A8%EB%8D%B8.pdf)

### 강의덱_HTML
강의 덱 HTML 단독 파일판 — 더블클릭하면 열림(서버 · 인터넷 불필요), 「라이브」 슬라이드 조작 가능

- [09주차_강의_기계학습 (1) - 분자 표현자와 대리모델.html](%EA%B0%95%EC%9D%98%EB%8D%B1_HTML/09%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98_%EA%B8%B0%EA%B3%84%ED%95%99%EC%8A%B5%20%281%29%20-%20%EB%B6%84%EC%9E%90%20%ED%91%9C%ED%98%84%EC%9E%90%EC%99%80%20%EB%8C%80%EB%A6%AC%EB%AA%A8%EB%8D%B8.html)

### 강의스크립트
강의 스크립트 — Word(편집용) · PDF(읽기 · 인쇄용) · JSON(원본 데이터)

- [09주차_강의스크립트_기계학습 (1).docx](%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8/09%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8_%EA%B8%B0%EA%B3%84%ED%95%99%EC%8A%B5%20%281%29.docx)
- [09주차_강의스크립트_기계학습 (1).pdf](%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8/09%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8_%EA%B8%B0%EA%B3%84%ED%95%99%EC%8A%B5%20%281%29.pdf)
- [w09.json](%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8/w09.json)

### 평가문항
평가문항 — JSON(원본) · MD(읽기용, 정답 · 해설 포함)

- [09주차_평가문항.md](%ED%8F%89%EA%B0%80%EB%AC%B8%ED%95%AD/09%EC%A3%BC%EC%B0%A8_%ED%8F%89%EA%B0%80%EB%AC%B8%ED%95%AD.md)
- [q09.json](%ED%8F%89%EA%B0%80%EB%AC%B8%ED%95%AD/q09.json)
