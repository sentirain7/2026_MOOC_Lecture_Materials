# 13주차 — 자율 탐색 파이프라인 (2) — 다목적 최적화·LLM 에이전트와 통합 사례·검증

**학습목표**: 다목적 최적화 기반 역설계와 LLM 에이전트 오케스트레이션을 이해하고, 전체 자율 탐색 파이프라인을 아스팔트·시멘트·바이오 역설계 사례로 통합 적용하며 실험으로 검증한다.

| 차시 | 주제 | 내용 | 분 |
|---|---|---|---|
| 13-1 | 다목적 최적화 | 탐색 vs 활용, Pareto front, 베이지안 최적화. | 14 |
| 13-2 | LLM 에이전트 오케스트레이션 | 제안자–비평자 구조를 활용한 LLM 에이전트 기반 오케스트레이션. | 10 |
| 13-3 | 특징 재정련 루프 | 대리모델 특징 재정련과 탐색의 반복 개선. | 6 |
| 13-4 | 통합 사례연구: 아스팔트·시멘트·바이오 | 아스팔트 첨가제·시멘트 소재에 더해 바이오소재(바이오폴리머·바이오 바인더)의 역설계 통합 사례를 다룬다. | 12 |
| 13-5 | 실험 검증과 재현성 | 아스팔트 DSR·BBR, 시멘트 강도시험, 밀도·유리전이온도(Tg) 등 실험치와 시뮬레이션·예측 결과를 대조하고 재현성을 확보한다. | 8 |

## 자료

### 발표용_PDF
발표용 덱 PDF — 강의 · 촬영용(보존용 부록을 뺀 판)

- [13주차_강의_자율 탐색 파이프라인 (2) - 다목적 최적화·LLM 에이전트·검증.pdf](%EB%B0%9C%ED%91%9C%EC%9A%A9_PDF/13%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98_%EC%9E%90%EC%9C%A8%20%ED%83%90%EC%83%89%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%20%282%29%20-%20%EB%8B%A4%EB%AA%A9%EC%A0%81%20%EC%B5%9C%EC%A0%81%ED%99%94%C2%B7LLM%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%C2%B7%EA%B2%80%EC%A6%9D.pdf)
- [13주차_보충A_플랫폼 통합과 최종 프로젝트.pdf](%EB%B0%9C%ED%91%9C%EC%9A%A9_PDF/13%EC%A3%BC%EC%B0%A8_%EB%B3%B4%EC%B6%A9A_%ED%94%8C%EB%9E%AB%ED%8F%BC%20%ED%86%B5%ED%95%A9%EA%B3%BC%20%EC%B5%9C%EC%A2%85%20%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8.pdf)

### 원본덱_PDF
원본 덱 PDF — 수정 전 문구를 부록에 남긴 판(수정 이력 확인용)

- [13주차_강의_자율 탐색 파이프라인 (2) - 다목적 최적화·LLM 에이전트·검증.pdf](%EC%9B%90%EB%B3%B8%EB%8D%B1_PDF/13%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98_%EC%9E%90%EC%9C%A8%20%ED%83%90%EC%83%89%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%20%282%29%20-%20%EB%8B%A4%EB%AA%A9%EC%A0%81%20%EC%B5%9C%EC%A0%81%ED%99%94%C2%B7LLM%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%C2%B7%EA%B2%80%EC%A6%9D.pdf)
- [13주차_보충A_플랫폼 통합과 최종 프로젝트.pdf](%EC%9B%90%EB%B3%B8%EB%8D%B1_PDF/13%EC%A3%BC%EC%B0%A8_%EB%B3%B4%EC%B6%A9A_%ED%94%8C%EB%9E%AB%ED%8F%BC%20%ED%86%B5%ED%95%A9%EA%B3%BC%20%EC%B5%9C%EC%A2%85%20%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8.pdf)

### 강의덱_HTML
강의 덱 HTML 단독 파일판 — 더블클릭하면 열림(서버 · 인터넷 불필요), 「라이브」 슬라이드 조작 가능

- [13주차_강의_자율 탐색 파이프라인 (2) - 다목적 최적화·LLM 에이전트·검증.html](%EA%B0%95%EC%9D%98%EB%8D%B1_HTML/13%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98_%EC%9E%90%EC%9C%A8%20%ED%83%90%EC%83%89%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%20%282%29%20-%20%EB%8B%A4%EB%AA%A9%EC%A0%81%20%EC%B5%9C%EC%A0%81%ED%99%94%C2%B7LLM%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%C2%B7%EA%B2%80%EC%A6%9D.html)
- [13주차_보충A_플랫폼 통합과 최종 프로젝트.html](%EA%B0%95%EC%9D%98%EB%8D%B1_HTML/13%EC%A3%BC%EC%B0%A8_%EB%B3%B4%EC%B6%A9A_%ED%94%8C%EB%9E%AB%ED%8F%BC%20%ED%86%B5%ED%95%A9%EA%B3%BC%20%EC%B5%9C%EC%A2%85%20%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8.html)

### 강의스크립트
강의 스크립트 — Word(편집용) · PDF(읽기 · 인쇄용) · JSON(원본 데이터)

- [13주차_강의스크립트_자율 탐색 파이프라인 (2).docx](%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8/13%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8_%EC%9E%90%EC%9C%A8%20%ED%83%90%EC%83%89%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%20%282%29.docx)
- [13주차_강의스크립트_자율 탐색 파이프라인 (2).pdf](%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8/13%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8_%EC%9E%90%EC%9C%A8%20%ED%83%90%EC%83%89%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%20%282%29.pdf)
- [w13.json](%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8/w13.json)

### 평가문항
평가문항 — JSON(원본) · MD(읽기용, 정답 · 해설 포함)

- [13주차_평가문항.md](%ED%8F%89%EA%B0%80%EB%AC%B8%ED%95%AD/13%EC%A3%BC%EC%B0%A8_%ED%8F%89%EA%B0%80%EB%AC%B8%ED%95%AD.md)
- [q13.json](%ED%8F%89%EA%B0%80%EB%AC%B8%ED%95%AD/q13.json)
