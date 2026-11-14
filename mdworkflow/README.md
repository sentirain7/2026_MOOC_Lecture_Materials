# MD 워크플로우 (mdwf) · 강좌용 간이 분자동역학 파이프라인

분자 하나의 SMILES 에서 출발해 **분자 → 힘장 → 셀 → 계산 → 물성 → 결과 표** 를 한 줄로 잇는다.
연구 플랫폼이 하는 일을 교육용으로 줄인 것이며, 모든 중간 결과가 파일로 남아 열어 볼 수 있다.

- 환경: `conda activate mdai` (RDKit · AmberTools · Packmol · LAMMPS · `../environment.yml`)
- 명령 하나: `python mdwf.py <단계> …` · 단계 = mol · ff · build · run · analyze · store · all
- 작업 폴더: 기본 `ws/` (mol · ff · cells · runs · db) · 폐루프는 `../loop/ws/<이름>` 을 쓴다
- Claude Code 지시문: `prompts.md` (M-1 ~ M-6)
- 범위: 유기 분자 한 종류를 채운 상자(단분자 상자) · 광물 · 물 계면(W08 · W10) · ReaxFF(W12)는 각 주차 자료

## 여섯 단계

| 단계 | 넣는 것 → 나오는 것 | 틀리기 쉬운 곳 | 확인(자동) | 처음 배우는 주차 |
|---|---|---|---|---|
| ① `mol` (molecule.py) | SMILES → `ws/mol/<이름>.mol · .pdb · .json` · RDKit 수소 추가 · ETKDG 3D(seed 7) · MMFF94 정리 | 수소 누락 · 입체(@/@@) 뒤바뀜 · 형식전하 | 원자 수 · 입체 중심 수 유지 · MMFF 수렴 | W04 |
| ② `ff` (forcefield.py) | `.mol` → `ws/ff/<이름>_gaff2.json` · antechamber(GAFF2 타입 · AM1-BCC 전하) → parmchk2(빠진 매개변수) → tleap(prmtop) → parmed(JSON) | 형식전하 틀림 · parmchk2 가 빌린 값(ATTN)을 그대로 믿음 · 이면각 위상 · 1-4 축소 변환 | 전하 합 = 형식전하 · 타입 빠짐 없음 · ATTN 개수 · 결합 · 각 개수 = prmtop | W04 |
| ③ `build` (builder.py) | `이름=개수` → `ws/cells/<id>/system.data` · 초기 밀도 ρ0(기본 0.5)로 상자 한 변 역산 → Packmol(tolerance 2 Å · seed) → 품질 게이트 → LAMMPS data | ρ0 를 너무 높게(Packmol 실패) · 같은 타입 이름에 다른 수치 | Packmol 성공 · 분자간 최소 거리 ≥ 0.9 × tolerance · 원자 수 · 전하 합 ≈ 0 | W06 |
| ④ `run` (runner.py) | `system.data` → `ws/runs/<id>/log.lammps · prod.lammpstrj · status.json` · 표준 프로토콜(`templates/in.protocol`) | 짧은 실행 = 수렴 전 값 · 코어 수가 바뀌면 궤적이 비트 단위로 달라짐 | 종료 코드 · 실패 규칙 R1(원자 잃음 → Δt 절반 1회) · R2(그 밖 → 멈춤) | W07 |
| ⑤ `analyze` (analyze.py) | 생산 구간 → `props.json` · 밀도(블록 5개 표준오차) · CED = −⟨E_inter⟩/⟨V⟩ · δ = √CED | 평형 전 구간 포함 · 프레임 부족 · 경계에서 잘린 분자 | 전반 · 후반 밀도 차 < 1 % · 분자 크기 < 전하 절단 | W09 |
| ⑥ `store` (store.py) | → `ws/db/results.csv` 한 줄(조성 · 물성 ± · 조건 · 힘장 · seed · 근거) | 같은 id 두 번 · 실패 기록을 지움 | 같은 id 거부 · 실패도 ok=False 로 남김 | W09 · W13 |

### 표준 프로토콜 (④ · 시간 간격 1 fs · 합계 130 ps)
최소화 → A 섞기 NVT 500 K 10 ps → B 압축 NPT 500 K · 1000 atm 20 ps → C 이완 NPT 500 K · 1 atm 20 ps → D 냉각 500 → 298 K 20 ps → E 평형 NPT 298 K 20 ps → **P 생산 NPT 298 K 40 ps**(물성은 이 구간만 · 앞 20 % 버림)
- 1,500 원자 · 4코어(OpenMP) 약 5분(단독) · 짧은 교육용 프로토콜 → 값은 「수렴 전 형태」이며 연구용은 ns 단위

### CED 계산 (⑤)
E_inter = E_벌크(PPPM 장거리 전하 · LJ 꼬리 보정 포함) − Σ E_분자 하나(같은 좌표). 분자 하나의 에너지는 생산 프레임마다 분자를 120 Å 간격 격자로 떼어 놓고 LAMMPS rerun 한 번으로 구한다(`templates/in.intra` · 전하 직접 합 절단 55 Å · LJ 12 Å). W09 Method A 와 같은 정의.

## 힘장 검증 사례 (2026-11-14 · mdai · 4코어)
| 분자(개수) | MD 밀도 g/cm³ | 실측(NIST 298 K) | MD CED MJ/m³ | 실측 CED = (ΔvapH − RT)/Vm |
|---|---|---|---|---|
| 톨루엔(100) | 0.8703 ± 0.0024 | 0.86238 | 352.3 ± 2.2 | 332.5 |
| n-데칸(47) | 0.734 ± 0.0014 | 0.72664 | 303.0 ± 2.0 | 249.7 |
- 밀도 +1 % 안 · CED 방향족 +6 % · 포화 +21 % → GAFF2 의 응집 과대(특히 알케인)를 알고 결과를 읽는다
- 출처: NIST Chemistry WebBook (톨루엔 C108883 · n-데칸 C124185 · 밀도 = Lemmon & Span 2006 상태식 · ΔvapH = Majer–Svoboda 식 298.15 K)
- 톨루엔 GAFF2 타입 · 전하 · 결합 매개변수는 W04 참고 결과(`week04/data/Toluene_gaff2.json`)와 같다

## 같은 계산을 다시 돌리면 (반복 흔들림 · 톨루엔 100 · 같은 seed)
| 실행 | 코어 | 밀도 g/cm³ | CED MJ/m³ |
|---|---|---|---|
| 1회 | 4 | 0.8703 ± 0.0024 | 352.3 ± 2.2 |
| 2회 | 4 | 0.8724 ± 0.0036 | 357.1 ± 3.3 |
| 3회 | 2 | 0.8801 ± 0.0013 | 362.6 ± 4.9 |
- 같은 코어 수 · 같은 seed 라도 OpenMP 합산 순서가 달라 궤적이 비트 단위로 같지 않다 → 값은 「흔들림」 안에서 같다
- 실행 사이 흔들림(밀도 약 ±0.005 · CED 약 ±5)이 한 실행 안의 블록 표준오차보다 크다 → 짧은 실행의 오차 막대는 작게 나온다(W05)
- 「같은 결과」 판정 폭: 밀도 ±0.015 g/cm³ · CED ±15 MJ/m³ (흔들림의 약 1.5배)

## 확장 (강의 밖 · 선택)
- `build --sara S,A,R,As` : Li & Greenfield 12분자 혼합 셀(약 3,000 원자). 강의의 LAMMPS 사례는 단분자 상자만 쓴다. 12분자 SMILES 중 AS-Phenol 은 산소가 없는 구조(C42H54)로 들어 있어 원전 확인이 필요하다.
