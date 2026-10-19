# 10주차 — 기계학습 (2) — 그래프 신경망(GNN)과 능동학습

**학습목표**: 분자·결정의 그래프 표현과 GNN(Graphormer-3D) 물성 예측, 불확실성 기반 능동학습을 이해한다.

| 차시 | 주제 | 내용 | 분 |
|---|---|---|---|
| 10-1 | 분자 그래프와 message passing | 분자·결정의 그래프 표현과 메시지 전달(message passing) 메커니즘. | 12 |
| 10-2 | 등변 GNN과 Graphormer-3D | 등변(equivariant) GNN과 3D 구조 인코딩을 갖춘 Graphormer-3D. | 16 |
| 10-3 | MD 데이터 학습 | MD로 생성한 데이터로 GNN 물성 예측 모델을 학습·검증. | 10 |
| 10-4 | 불확실성과 능동학습 | 불확실성 정량화와, 자율 탐색 파이프라인의 능동학습 단계에 연계되는 샘플링 전략. | 12 |

## 자료

### 발표용_PDF
발표용 덱 PDF — 강의 · 촬영용(보존용 부록을 뺀 판)

- [10주차_강의_기계학습 (2) - 그래프 신경망과 능동학습.pdf](%EB%B0%9C%ED%91%9C%EC%9A%A9_PDF/10%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98_%EA%B8%B0%EA%B3%84%ED%95%99%EC%8A%B5%20%282%29%20-%20%EA%B7%B8%EB%9E%98%ED%94%84%20%EC%8B%A0%EA%B2%BD%EB%A7%9D%EA%B3%BC%20%EB%8A%A5%EB%8F%99%ED%95%99%EC%8A%B5.pdf)
- [10주차_보충A_대리모델 평가와 불확실성.pdf](%EB%B0%9C%ED%91%9C%EC%9A%A9_PDF/10%EC%A3%BC%EC%B0%A8_%EB%B3%B4%EC%B6%A9A_%EB%8C%80%EB%A6%AC%EB%AA%A8%EB%8D%B8%20%ED%8F%89%EA%B0%80%EC%99%80%20%EB%B6%88%ED%99%95%EC%8B%A4%EC%84%B1.pdf)
- [10주차_보충B_능동학습과 탐색 전략.pdf](%EB%B0%9C%ED%91%9C%EC%9A%A9_PDF/10%EC%A3%BC%EC%B0%A8_%EB%B3%B4%EC%B6%A9B_%EB%8A%A5%EB%8F%99%ED%95%99%EC%8A%B5%EA%B3%BC%20%ED%83%90%EC%83%89%20%EC%A0%84%EB%9E%B5.pdf)

### 원본덱_PDF
원본 덱 PDF — 수정 전 문구를 부록에 남긴 판(수정 이력 확인용)

- [10주차_강의_기계학습 (2) - 그래프 신경망과 능동학습.pdf](%EC%9B%90%EB%B3%B8%EB%8D%B1_PDF/10%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98_%EA%B8%B0%EA%B3%84%ED%95%99%EC%8A%B5%20%282%29%20-%20%EA%B7%B8%EB%9E%98%ED%94%84%20%EC%8B%A0%EA%B2%BD%EB%A7%9D%EA%B3%BC%20%EB%8A%A5%EB%8F%99%ED%95%99%EC%8A%B5.pdf)
- [10주차_보충A_대리모델 평가와 불확실성.pdf](%EC%9B%90%EB%B3%B8%EB%8D%B1_PDF/10%EC%A3%BC%EC%B0%A8_%EB%B3%B4%EC%B6%A9A_%EB%8C%80%EB%A6%AC%EB%AA%A8%EB%8D%B8%20%ED%8F%89%EA%B0%80%EC%99%80%20%EB%B6%88%ED%99%95%EC%8B%A4%EC%84%B1.pdf)
- [10주차_보충B_능동학습과 탐색 전략.pdf](%EC%9B%90%EB%B3%B8%EB%8D%B1_PDF/10%EC%A3%BC%EC%B0%A8_%EB%B3%B4%EC%B6%A9B_%EB%8A%A5%EB%8F%99%ED%95%99%EC%8A%B5%EA%B3%BC%20%ED%83%90%EC%83%89%20%EC%A0%84%EB%9E%B5.pdf)

### 강의덱_HTML
강의 덱 HTML 단독 파일판 — 더블클릭하면 열림(서버 · 인터넷 불필요), 「라이브」 슬라이드 조작 가능

- [10주차_강의_기계학습 (2) - 그래프 신경망과 능동학습.html](%EA%B0%95%EC%9D%98%EB%8D%B1_HTML/10%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98_%EA%B8%B0%EA%B3%84%ED%95%99%EC%8A%B5%20%282%29%20-%20%EA%B7%B8%EB%9E%98%ED%94%84%20%EC%8B%A0%EA%B2%BD%EB%A7%9D%EA%B3%BC%20%EB%8A%A5%EB%8F%99%ED%95%99%EC%8A%B5.html)
- [10주차_보충A_대리모델 평가와 불확실성.html](%EA%B0%95%EC%9D%98%EB%8D%B1_HTML/10%EC%A3%BC%EC%B0%A8_%EB%B3%B4%EC%B6%A9A_%EB%8C%80%EB%A6%AC%EB%AA%A8%EB%8D%B8%20%ED%8F%89%EA%B0%80%EC%99%80%20%EB%B6%88%ED%99%95%EC%8B%A4%EC%84%B1.html)
- [10주차_보충B_능동학습과 탐색 전략.html](%EA%B0%95%EC%9D%98%EB%8D%B1_HTML/10%EC%A3%BC%EC%B0%A8_%EB%B3%B4%EC%B6%A9B_%EB%8A%A5%EB%8F%99%ED%95%99%EC%8A%B5%EA%B3%BC%20%ED%83%90%EC%83%89%20%EC%A0%84%EB%9E%B5.html)

### 강의스크립트
강의 스크립트 — Word(편집용) · PDF(읽기 · 인쇄용) · JSON(원본 데이터)

- [10주차_강의스크립트_기계학습 (2).docx](%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8/10%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8_%EA%B8%B0%EA%B3%84%ED%95%99%EC%8A%B5%20%282%29.docx)
- [10주차_강의스크립트_기계학습 (2).pdf](%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8/10%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8_%EA%B8%B0%EA%B3%84%ED%95%99%EC%8A%B5%20%282%29.pdf)
- [w10.json](%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8/w10.json)

### 평가문항
평가문항 — JSON(원본) · MD(읽기용, 정답 · 해설 포함)

- [10주차_평가문항.md](%ED%8F%89%EA%B0%80%EB%AC%B8%ED%95%AD/10%EC%A3%BC%EC%B0%A8_%ED%8F%89%EA%B0%80%EB%AC%B8%ED%95%AD.md)
- [q10.json](%ED%8F%89%EA%B0%80%EB%AC%B8%ED%95%AD/q10.json)
