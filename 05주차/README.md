# 05주차 — LAMMPS 활용 (2) — 자동 스크립트 생성·자기교정과 다중 힘장 스택

**학습목표**: 자동 스크립트 생성·자기교정 워크플로우와 FF-neutral 토폴로지 기반 다중 힘장 스택 운용을 익힌다.

| 차시 | 주제 | 내용 | 분 |
|---|---|---|---|
| 5-1 | 자동 스크립트 생성 | LAMMPS 입력 스크립트를 자동 생성하는 워크플로우. | 12 |
| 5-2 | 오류 자기교정 루프 | 스크립트·실행 오류를 자동 탐지·교정하는 반복 루프. | 12 |
| 5-3 | FF-neutral 토폴로지 설계 | OPLS-AA·GAFF2·ReaxFF에 재사용 가능한 힘장 중립 토폴로지 설계. | 14 |
| 5-4 | 다중 힘장 스택 운용 | 다중 힘장(multi-FF) 스택 운용, 배치 실행과 재현성 확보. | 12 |

## 자료

### 발표용_PDF
발표용 덱 PDF — 강의 · 촬영용(보존용 부록을 뺀 판)

- [05주차_강의_LAMMPS 활용 (2) - 자동 스크립트·자기교정·다중 힘장 스택.pdf](%EB%B0%9C%ED%91%9C%EC%9A%A9_PDF/05%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98_LAMMPS%20%ED%99%9C%EC%9A%A9%20%282%29%20-%20%EC%9E%90%EB%8F%99%20%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8%C2%B7%EC%9E%90%EA%B8%B0%EA%B5%90%EC%A0%95%C2%B7%EB%8B%A4%EC%A4%91%20%ED%9E%98%EC%9E%A5%20%EC%8A%A4%ED%83%9D.pdf)

### 원본덱_PDF
원본 덱 PDF — 수정 전 문구를 부록에 남긴 판(수정 이력 확인용)

- [05주차_강의_LAMMPS 활용 (2) - 자동 스크립트·자기교정·다중 힘장 스택.pdf](%EC%9B%90%EB%B3%B8%EB%8D%B1_PDF/05%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98_LAMMPS%20%ED%99%9C%EC%9A%A9%20%282%29%20-%20%EC%9E%90%EB%8F%99%20%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8%C2%B7%EC%9E%90%EA%B8%B0%EA%B5%90%EC%A0%95%C2%B7%EB%8B%A4%EC%A4%91%20%ED%9E%98%EC%9E%A5%20%EC%8A%A4%ED%83%9D.pdf)

### 강의덱_HTML
강의 덱 HTML 단독 파일판 — 더블클릭하면 열림(서버 · 인터넷 불필요), 「라이브」 슬라이드 조작 가능

- [05주차_강의_LAMMPS 활용 (2) - 자동 스크립트·자기교정·다중 힘장 스택.html](%EA%B0%95%EC%9D%98%EB%8D%B1_HTML/05%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98_LAMMPS%20%ED%99%9C%EC%9A%A9%20%282%29%20-%20%EC%9E%90%EB%8F%99%20%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8%C2%B7%EC%9E%90%EA%B8%B0%EA%B5%90%EC%A0%95%C2%B7%EB%8B%A4%EC%A4%91%20%ED%9E%98%EC%9E%A5%20%EC%8A%A4%ED%83%9D.html)

### 강의스크립트
강의 스크립트 — Word(편집용) · PDF(읽기 · 인쇄용) · JSON(원본 데이터)

- [05주차_강의스크립트_LAMMPS 활용 (2).docx](%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8/05%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8_LAMMPS%20%ED%99%9C%EC%9A%A9%20%282%29.docx)
- [05주차_강의스크립트_LAMMPS 활용 (2).pdf](%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8/05%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8_LAMMPS%20%ED%99%9C%EC%9A%A9%20%282%29.pdf)
- [w05.json](%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8/w05.json)

### 평가문항
평가문항 — JSON(원본) · MD(읽기용, 정답 · 해설 포함)

- [05주차_평가문항.md](%ED%8F%89%EA%B0%80%EB%AC%B8%ED%95%AD/05%EC%A3%BC%EC%B0%A8_%ED%8F%89%EA%B0%80%EB%AC%B8%ED%95%AD.md)
- [q05.json](%ED%8F%89%EA%B0%80%EB%AC%B8%ED%95%AD/q05.json)
