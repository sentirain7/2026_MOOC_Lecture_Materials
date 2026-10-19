# 04주차 — LAMMPS 활용 (1) — 환경 구축·입력 스크립트·초기 및 다층구조 생성

**학습목표**: LAMMPS 설치와 입력 스크립트 구조, 초기 구조 및 다층구조 생성 방법을 익힌다.

| 차시 | 주제 | 내용 | 분 |
|---|---|---|---|
| 4-1 | LAMMPS 개요와 설치 | LAMMPS 개요, GPU/KOKKOS 빌드와 패키지 구조를 다룬다. | 8 |
| 4-2 | 입력 스크립트 해부 | 입력 스크립트 분석: units·atom_style·pair_style·fix·run 명령. | 16 |
| 4-3 | 데이터 파일과 토폴로지 | 원자 좌표·토폴로지·힘장 파라미터로 구성되는 데이터 파일 구조. | 8 |
| 4-4 | 초기 구조 생성 | Packmol·Moltemplate·RDKit을 이용한 초기 구조 생성. | 10 |
| 4-5 | 다층구조 생성 | 부착·계면 연구를 위한 다층(계면 포함) 시스템 생성. | 8 |

## 자료

### 발표용_PDF
발표용 덱 PDF — 강의 · 촬영용(보존용 부록을 뺀 판)

- [04주차_강의_LAMMPS 활용 (1) - 환경 구축·입력 스크립트·초기 및 다층구조.pdf](%EB%B0%9C%ED%91%9C%EC%9A%A9_PDF/04%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98_LAMMPS%20%ED%99%9C%EC%9A%A9%20%281%29%20-%20%ED%99%98%EA%B2%BD%20%EA%B5%AC%EC%B6%95%C2%B7%EC%9E%85%EB%A0%A5%20%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8%C2%B7%EC%B4%88%EA%B8%B0%20%EB%B0%8F%20%EB%8B%A4%EC%B8%B5%EA%B5%AC%EC%A1%B0.pdf)

### 원본덱_PDF
원본 덱 PDF — 수정 전 문구를 부록에 남긴 판(수정 이력 확인용)

- [04주차_강의_LAMMPS 활용 (1) - 환경 구축·입력 스크립트·초기 및 다층구조.pdf](%EC%9B%90%EB%B3%B8%EB%8D%B1_PDF/04%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98_LAMMPS%20%ED%99%9C%EC%9A%A9%20%281%29%20-%20%ED%99%98%EA%B2%BD%20%EA%B5%AC%EC%B6%95%C2%B7%EC%9E%85%EB%A0%A5%20%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8%C2%B7%EC%B4%88%EA%B8%B0%20%EB%B0%8F%20%EB%8B%A4%EC%B8%B5%EA%B5%AC%EC%A1%B0.pdf)

### 강의덱_HTML
강의 덱 HTML 단독 파일판 — 더블클릭하면 열림(서버 · 인터넷 불필요), 「라이브」 슬라이드 조작 가능

- [04주차_강의_LAMMPS 활용 (1) - 환경 구축·입력 스크립트·초기 및 다층구조.html](%EA%B0%95%EC%9D%98%EB%8D%B1_HTML/04%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98_LAMMPS%20%ED%99%9C%EC%9A%A9%20%281%29%20-%20%ED%99%98%EA%B2%BD%20%EA%B5%AC%EC%B6%95%C2%B7%EC%9E%85%EB%A0%A5%20%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8%C2%B7%EC%B4%88%EA%B8%B0%20%EB%B0%8F%20%EB%8B%A4%EC%B8%B5%EA%B5%AC%EC%A1%B0.html)

### 강의스크립트
강의 스크립트 — Word(편집용) · PDF(읽기 · 인쇄용) · JSON(원본 데이터)

- [04주차_강의스크립트_LAMMPS 활용 (1).docx](%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8/04%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8_LAMMPS%20%ED%99%9C%EC%9A%A9%20%281%29.docx)
- [04주차_강의스크립트_LAMMPS 활용 (1).pdf](%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8/04%EC%A3%BC%EC%B0%A8_%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8_LAMMPS%20%ED%99%9C%EC%9A%A9%20%281%29.pdf)
- [w04.json](%EA%B0%95%EC%9D%98%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8/w04.json)

### 평가문항
평가문항 — JSON(원본) · MD(읽기용, 정답 · 해설 포함)

- [04주차_평가문항.md](%ED%8F%89%EA%B0%80%EB%AC%B8%ED%95%AD/04%EC%A3%BC%EC%B0%A8_%ED%8F%89%EA%B0%80%EB%AC%B8%ED%95%AD.md)
- [q04.json](%ED%8F%89%EA%B0%80%EB%AC%B8%ED%95%AD/q04.json)
