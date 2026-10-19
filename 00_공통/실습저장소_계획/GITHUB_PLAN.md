# 강의 실습 저장소 구성안과 생성 프롬프트

「건설소재 역설계 도구 개발을 위한 AI와 분자동역학 활용」 13주 강의의 실습 코드 저장소(GitHub) 구성안이다. 강의계획서 「학습자료」 칸의 GitHub 항목과 각 주차 덱의 「실습 안내」 결과물(DELIVERABLE)을 기준으로 정리했다. 주차마다 **저장할 내용**과 이를 만드는 **프롬프트**(Claude Code에 그대로 붙여 넣는 형식)를 둔다.

- **기준 문서**: 강의계획서(`uploads/강의계획서_건설소재역설계_MOOC.hwp` → `tools/syllabus.json`), 발표용 덱의 실습 안내 슬라이드
- **참고 코드(읽기 전용)**: `/home/tyun/mounted_directory/sdd/Claude_Code/LAMMPS_Asphalt` (이하 `LA`)
- **작성일**: 2026-09-22

> **이 문서의 위치**: 강의계획서 GitHub 항목과 주차별 저장 내용의 **첫 버전(원안)**이다. 실제 저장소는 통합 앱 계획(`INTEGRATED_APP_PLAN.md`)과 프롬프트(`PROMPTS_APP.md` · `PROMPTS_STRUCTURE.md`)로 만든다. 설치는 `INSTALL_GUIDE.md`, 힘장 조합은 `FF_COMPATIBILITY.md`를 따른다. 내용이 충돌하면 그 문서들이 우선한다. 읽는 순서는 `README.md`를 본다.

---

## 1. 강의계획서의 GitHub 항목

| 주차 | 강의계획서 학습자료 | 실습 안내 결과물 (덱) |
|---|---|---|
| 1 | PDF (GitHub 항목 없음) | 실습 환경 설치 (LAMMPS · Python 3.11 · PyTorch · PyG · RDKit · Optuna) |
| 2 | PDF (GitHub 항목 없음) | LJ 유체 NVE: 에너지 드리프트 · 시간 간격 · 컷오프 · 계 크기 실험 |
| 3 | **힘장 파라미터 · 예제 입력** | NVT/NPT 평형화 · 온도 조절기 비교 · t_eq 판정 |
| 4 | **LAMMPS 예제 입력 · 다층구조 모델** | 바인더 셀 평형화 (입력 · log · thermo CSV · restart · 평형 판정 그래프) |
| 5 | **LAMMPS 자동 생성기 · 다중 힘장 예제** | spec.yaml → in · data · ff 생성기, 자기교정 규칙표, 두 힘장 입력 비교 |
| 6 | **CED 계산 파이프라인** | 밀도 · CED(Method A · B) · δ · 점도 · 확산 물성표, postprocess.py |
| 7 | **아스팔트 분자구조(SARA · 첨가제) · 모델 빌드 · 다중 힘장 입력** | 기준 · 첨가제 · 노화 바인더 물성 비교, RDF · 적층 해석 |
| 8 | **시멘트 ReaxFF 모델 · ML 힘장 예제** | C-S-H(Ca/Si 1.5 · 1.7) 탄성 상수, 층간 물 함량 영향 |
| 9 | **XGBoost+SHAP 모델** | GroupKFold 대리모델 성능표, SHAP 요약 그림 · 해석 메모 |
| 10 | **GNN(Graphormer-3D) 학습 코드** | PyG 변환, MPNN · 조성 가중 풀링, 학습 곡선 · 예측 함수 |
| 11 | **Obsidian vault 템플릿 · 스크래핑 스크립트** | 문헌 200건 수집 · 중복 제거 · LLM 추출 채점 · Zotero · Obsidian 연결 |
| 12 | **자율 탐색 파이프라인 예제** | 후보 격자 · 세 테이블 DB · 기술자 · 폴드 · 품질 검사 · run_manifest |
| 13 | **최적화 · 에이전트 오케스트레이션 · 통합 사례 · 검증** | 2목적 EHVI 루프 5회, 파레토 · HV 곡선, 추천 조성 3개 · 검증 계획 |

1 · 2주차는 강의계획서에 GitHub 항목이 없다. 1주차 덱이 「실습 코드 GitHub 저장소」를 안내하고 2주차 실습 입력이 있으므로, 두 주차는 **선택(권장)** 항목으로 둔다.

---

## 2. 저장소 전체 구조

주차별 폴더를 둔 **단일 저장소**를 권장한다. 뒤 주차가 앞 주차의 산출물을 입력으로 쓰기 때문이다. 흐름은 다음과 같다.
- 5주차 생성기 → 6주차 이후 모든 계산의 입력
- 6주차 CSV 열 이름 → 12주차 DB 스키마
- 9주차 성능 → 10주차 기준선

```
mooc-inverse-design/
├── README.md                  # 강좌 개요 · 주차 목차 · 실행 환경 · 데이터 이용 조건
├── environment.yml            # 공통 conda 환경 (1주차)
├── common/                    # 주차 공통 유틸 (단위 변환 · 입출력 · 실험 ID · 해시)
├── data/
│   ├── README.md              # 데이터 출처 · 라이선스 · 측정/계산/문헌/가정 구분
│   └── samples/               # 공개 가능한 작은 표본만 (전체 원자료는 넣지 않음)
├── week01_setup/  week02_md_basics/  week03_forcefield/  week04_lammps/
├── week05_generator/  week06_postprocess/  week07_asphalt/  week08_cement/
├── week09_xgboost_shap/  week10_gnn/  week11_literature/  week12_pipeline/
├── week13_optimization/
└── tests/                     # 주차별 스모크 테스트 (CI에서 CPU로 5분 이내)
```

### 주차 폴더 공통 규칙
- `README.md`: 학습목표(강의계획서 차시 코드) · 실행 순서 · 예상 소요 시간 · 결과물 체크리스트(덱의 DELIVERABLE과 같은 항목)
- `inputs/` · `scripts/` · `notebooks/` · `expected/`: 기준 결과. 학생 결과를 이 값과 비교한다.
- 모든 실행은 **시드 고정 · 입력 해시 기록**을 따른다(13주차 보충 A 13-S3 재현성 규약).
- **CPU에서 끝나는 축소판**(수 분)과 **GPU 전체판**을 함께 제공한다. CI는 축소판만 돌린다.
- 주석 · README는 한국어로 쓰고, 코드 식별자는 영어로 쓴다. 전문 용어는 처음 나올 때 영어를 병기한다(강의자료와 같은 규칙).

### 데이터 · 라이선스 주의 (저장 전에 확인)
- **실측 자료**(S64-22 DSR · BBR · MSCR, SynologyDrive 원자료)와 **플랫폼 DB 추출본**(`comid_core672_dataset.csv` 등)은 공개 전에 소유 · 공동연구 · 공개 범위를 확인한다. 공개가 어려우면 작은 표본만 넣거나 형식이 같은 합성 표본을 넣고, `data/README.md`에 그렇게 밝힌다.
- **문헌 전문(PDF · XML)**은 TDM 약관상 공유 금지다. 11주차 저장소에는 서지정보 · DOI · 스크립트만 넣는다.
- **힘장 파라미터**: GAFF2는 AmberTools 배포 조건을 따르고, ClayFF · ReaxFF ffield는 원 논문 인용과 배포 가능 여부를 확인한다. 배포할 수 없으면 내려받기 스크립트와 인용만 둔다.
- 결정 구조 CIF는 COD(Crystallography Open Database) 출처를 적는다.

---

## 3. 주차별 저장 내용과 생성 프롬프트

프롬프트 앞에는 아래 **공통 머리말**을 붙여서 쓴다.

```text
[공통 머리말]
너는 대학원 MOOC 「건설소재 역설계 도구 개발을 위한 AI와 분자동역학 활용」의 실습 저장소를 만드는 개발자다.
저장소: mooc-inverse-design/ (단일 저장소, 주차별 폴더). 규칙:
- 파이썬 3.11, 의존성은 루트 environment.yml 에 추가. LAMMPS 는 2Aug2023 이후 안정판 기준(MOLECULE · KSPACE · RIGID · EXTRA-DUMP 패키지).
- 모든 스크립트는 명령행 인자와 --help, 시드 고정, 출력 폴더에 run_manifest.json(입력 파일 SHA-256 · 버전 · 시드 · 날짜) 기록.
- CPU 축소판(수 분 이내)과 GPU 전체판을 --scale small|full 로 전환.
- README.md(한국어): 학습목표(강의계획서 차시 코드) · 실행 순서 · 결과물 체크리스트 · 예상 결과(expected/) 비교 방법.
- tests/ 에 축소판 스모크 테스트(pytest) 추가.
- 참고 코드는 읽기 전용: /home/tyun/mounted_directory/sdd/Claude_Code/LAMMPS_Asphalt (LA). 복사하지 말고 필요한 부분만 교육용으로 단순화해 새로 작성.
- 수치 · 파라미터를 지어내지 말 것. 출처(논문 · 파일 경로)를 주석과 README 에 적고, 가정값은 '가정'으로 표시.
- 강의 덱(발표용/NN주차_강의_…dc.html)의 실습 안내 슬라이드와 결과물 항목이 일치해야 한다.
```

### 1주차 (선택) · `week01_setup/` — 실습 환경
**저장 내용**
- 루트 `environment.yml`: Python 3.11 · numpy · pandas · matplotlib · rdkit · pytorch · pytorch-geometric · xgboost · shap · optuna · mdanalysis · jinja2 · pyyaml
- `check_env.py`: 각 패키지 import · 버전 · GPU 확인, LAMMPS 실행 파일과 패키지 목록(`lmp -h`) 점검
- `README.md`: 설치 순서(conda · LAMMPS 빌드 요약 · 4주차 설치 슬라이드 참조), 주차 폴더 지도

```text
[1주차] 공통 머리말 +
루트 environment.yml 과 week01_setup/ 를 만들어라.
1) environment.yml: conda-forge 채널, python=3.11, numpy, pandas, matplotlib, rdkit, pytorch(CPU/GPU 선택 주석), pyg, xgboost, shap, optuna, mdanalysis, jinja2, pyyaml, pytest.
2) week01_setup/check_env.py: 패키지별 import 성공 · 버전 표, torch.cuda 사용 가능 여부, `lmp -h` 결과에서 MOLECULE · KSPACE · RIGID · EXTRA-DUMP 설치 여부를 표로 출력. 빠진 항목은 해결 방법 한 줄 안내.
3) week01_setup/README.md: 설치 순서, 저장소 폴더 지도(주차 → 강의계획서 주차명), 데이터 이용 조건 요약.
4) tests/test_week01.py: check_env.py 가 오류 없이 표를 출력하는지.
```

### 2주차 (선택) · `week02_md_basics/` — LJ 유체와 수치적분
**저장 내용**
- `inputs/in.lj_nve`: 덱 실습 입력(units lj · fcc 0.8442 · lj/cut 2.5 · NVE · run 20000)
- `scripts/sweep.py`: 시간 간격(0.005 · 0.010 · 0.020) · 컷오프(2.5σ · 1.5σ) · 계 크기(10³ · 5³ 격자) 전개
- `scripts/drift.py`: etotal 선형 적합으로 드리프트 산출, 조건별 비교표 · 그림
- `notebooks/verlet_by_hand.ipynb`: 2주차 #8 · #19 수치 예시(ε = 0.109 kcal/mol, σ = 3.40 Å)를 손으로 따라가는 계산

```text
[2주차] 공통 머리말 +
week02_md_basics/ 를 만들어라. 기준: 발표용 2주차 덱 실습 안내(#28)와 2-3 · 2-4 차시.
1) inputs/in.lj_nve: 덱 실습 입력 그대로(units lj, lattice fcc 0.8442, region 0 10, lj/cut 2.5, velocity 1.44 87287, timestep 0.005, nve, thermo 100, run 20000). thermo 를 CSV 로 남기는 fix print 또는 log 파서 사용.
2) scripts/sweep.py: timestep {0.005,0.010,0.020}, cutoff {2.5,1.5}, box {10,5} 조합을 variable 로 전개해 실행 폴더 생성 · 실행(--dry-run 지원).
3) scripts/drift.py: 각 실행의 etotal 시계열을 선형 적합해 드리프트(τ당 기울기) · 평균 pe · press 를 표(CSV)와 그림으로. 발산(NaN · lost atoms)은 '발산'으로 기록.
4) notebooks/verlet_by_hand.ipynb: LJ 원자쌍 r = 4.00 Å 에서 U · F · a 를 계산하고 velocity-Verlet 한 스텝(Δt = 1 fs)을 손으로 전개. 값은 덱 #8 · #19(U −0.102 kcal/mol, F −0.0606 kcal/mol·Å, a −2.11e−6 Å/fs²)와 일치해야 하고 테스트로 검증.
5) expected/: 축소판 기준 드리프트 표.
```

### 3주차 · `week03_forcefield/` — 힘장 파라미터 · 예제 입력
**저장 내용**
- `ff/`: GAFF2 · OPLS-AA 발췌 파라미터(교육용 몇 개 원자 타입), ClayFF 광물 파라미터 표(출처 인용), `README`에 배포 조건 명시
- `scripts/combining_rules.py`: 산술 · 기하 · 6제곱 평균(Waldman–Hagler) 비교, 이종쌍(unlike pair) 계산 예시(GAFF2 ↔ ClayFF)
- `scripts/charges.py`: RDKit Gasteiger / AM1-BCC(antechamber 있을 때) 비교, 전하 합 · 형식전하 점검
- `inputs/in.lj_nvt`, `in.lj_npt`: 덱 실습(Nosé–Hoover · Berendsen · Langevin 비교, NPT t_eq 판정)
- `scripts/equilibration.py`: 블록 평균 · 자기상관 · t_eq 판정, 시드 3개 평균 ± SE

```text
[3주차] 공통 머리말 +
week03_forcefield/ 를 만들어라. 강의계획서 GitHub 항목: 「힘장 파라미터 · 예제 입력」. 기준: 발표용 3주차 덱 3-1~3-4, 실습 안내(#35).
1) ff/: GAFF2 · OPLS-AA 의 교육용 원자 타입 몇 개(c3 · ca · hc · oh 등)의 LJ ε · σ, 결합 · 각 파라미터를 출처(gaff2.dat 버전, OPLS-AA 원 논문)와 함께 YAML 로. ClayFF(Cygan 2004) 광물 원자 타입 표. 배포 조건을 ff/README.md 에 명시하고, 원 파일은 내려받기 스크립트로만 제공.
   참고: LA/data/force_fields, LA/src/forcefield, LA/docs/architecture/ff-standard-reference-20260906.md
2) scripts/combining_rules.py: 두 원자 타입의 ε · σ 로 산술(Lorentz–Berthelot) · 기하 · 6제곱 평균 결과와 대소 관계(기하 ≤ 산술 ≤ 6제곱)를 표로. GAFF2 유기 원자 ↔ ClayFF 광물 원자의 이종쌍 예시와 LAMMPS pair_coeff 줄 출력.
3) scripts/charges.py: SMILES 입력 → RDKit Gasteiger 전하, antechamber 가 있으면 AM1-BCC 전하 비교, 분자 전하 합 · 형식전하 검사. 없으면 안내 후 건너뜀.
4) inputs/: 덱 실습 입력(LJ 8³, T 1.44, T_damp 0.5, NVT Nosé–Hoover / Berendsen / Langevin 교체안, NPT iso P 1.0 P_damp 5.0).
5) scripts/equilibration.py: 밀도 · 온도 시계열 → 블록 평균 SE, 자기상관 시간, t_eq 판정(전후반 평균 비교), 시드 3개 평균 ± SE 보고 형식.
6) expected/: 축소판 온도 요동 폭 · t_eq · 평균 밀도.
```

### 4주차 · `week04_lammps/` — LAMMPS 예제 입력 · 다층구조 모델
**저장 내용**
- `inputs/in.binder_equil`: 최소화 → 어닐링 → 298 K NPT(4-2 평형화 프로토콜), 단위 real · mix arithmetic · special_bonds amber(쿨롱 0.8333 · LJ 0.5) · pppm 1e-4
- `data/`: 교육용 소형 바인더 data 파일(원자 수 · 상자 · 밀도가 서로 맞는 것)
- `packmol/`: inp 템플릿(초기 0.2 g/cm³ · tolerance 3.0 Å), 고리 관통(ring threading) 검사 스크립트
- `layered/`: SiO₂ 등 광물 슬래브 + 바인더 층상 셀 조립 스크립트(진공 · slab 보정 포함)
- `scripts/equil_check.py`: 밀도 · 부피 시계열 판정 그림, 평형 밀도 평균 ± SE

```text
[4주차] 공통 머리말 +
week04_lammps/ 를 만들어라. 강의계획서 GitHub 항목: 「LAMMPS 예제 입력 · 다층구조 모델」. 기준: 발표용 4주차 덱 4-1~4-5, 실습 안내(#42), 결과물 = 입력 스크립트 · log · thermo CSV · 최종 구조 · restart · 평형 판정 그래프 · 평형 밀도(평균 ± SE), '다른 사람이 받아 그대로 재실행 가능'.
1) inputs/in.binder_equil: units real, atom_style full, pair_style lj/cut/coul/long 12.0, pair_modify mix arithmetic tail yes, kspace_style pppm 1.0e-4, special_bonds amber, timestep 1.0, minimize → 600 K 어닐링 → 298 K NPT(1 atm). 변수로 온도 · 시드 · 스텝 수를 받는다. 덱의 파일 구성(in · data · 힘장 include · 출력)과 같게.
2) data/: 작은 교육용 바인더 셀(예: SARA 대표 분자 몇 개)을 RDKit + Packmol 로 생성하는 스크립트와 결과 data 파일. 원자 수 · 상자 길이 · 밀도가 계산상 일치하는지 테스트로 확인(4주차 덱 binderA 수정 내역 참고).
3) packmol/: pack.inp 템플릿(초기 밀도 0.2 g/cm³, tolerance 3.0 Å, 실패 시 시드 변경 재시도), 고리 관통 검사 스크립트.
   참고: LA/docs/architecture/packmol-structure-generation-quality.md
4) layered/build_layered.py: 광물 슬래브(SiO₂ 등, COD CIF → ASE/pymatgen 절단) + 바인더 층을 z 방향으로 적층, 진공층, kspace_modify slab 3.0 적용 입력 출력.
   참고: LA/docs/workflows/crystal-slab-hydroxylation-procedure.md, LA/docs/papers/paper10_beta_unified/figures/GEO_layered_cell.png
5) scripts/equil_check.py: log → thermo CSV, 밀도 · 부피 시계열 그림, t_eq 판정, 평형 밀도 평균 ± 블록 SE.
6) run_manifest 와 함께 '재실행 체크리스트'를 README 에.
```

### 5주차 · `week05_generator/` — LAMMPS 자동 생성기 · 다중 힘장 예제
**저장 내용**
- `generator/`: `spec.yaml` → 조성 개수 환산 → 구조 충전 → 타이핑 → `in.*` · `data.*` · `ff.inc` 렌더링(Jinja2)
- `templates/in.equil.j2`: 값은 자리 표시로만, 분기 · 반복은 템플릿에서(하드코딩 금지)
- `topology/`: FF-neutral 토폴로지(원소 · 좌표 · 결합 차수) JSON과 힘장별 타입 대응
- `selfcorrect/`: 실패 분류 → 처방 규칙표(lost atoms → 시드 변경 → Δt 절반, 재시도 2회 뒤 사람 확인)와 실행 래퍼
- `examples/hybrid_overlay/`: 쿨롱을 한 번만 두는 `lj/cut + buck + coul/long` 예시

```text
[5주차] 공통 머리말 +
week05_generator/ 를 만들어라. 강의계획서 GitHub 항목: 「LAMMPS 자동 생성기 · 다중 힘장 예제」. 기준: 발표용 5주차 덱 5-1~5-4, 실습 안내, 결과물 = 생성기 코드 · spec 예제 · 생성된 실행 패키지 목록 · 자기교정 규칙표와 적용 로그. 6주차 이후 모든 계산은 이 생성기로 만든 입력을 쓴다.
1) generator/: spec.yaml(조성 wt% · 온도 목록 · 시드 목록 · 티어 · 힘장 스택) → 분자량으로 개수 환산(원자량 C 12.011 · H 1.008 · O 15.999 등, 반올림 규칙 명시) → Packmol 충전 → 타이핑 → data 파일. 온도 3 × 시드 3 조합을 전개하고 실험 ID(해시 포함)를 부여.
   참고: LA/src/builder, LA/src/templates, LA/src/contracts/schemas
2) templates/in.equil.j2: read_data · pair_style · velocity · fix · run 을 자리 표시로. pair_style hybrid/overlay 는 한 줄, 하위 스타일은 for 문으로 나열. 온도 · 스텝 · 파일명 하드코딩 금지 테스트 포함.
3) topology/: 원소 · 좌표 · 결합 차수만 담은 중립 토폴로지 JSON → GAFF2 · COMPASS(또는 OPLS-AA) 두 힘장의 타입 대응표 → 두 data 파일 생성 · 비교 스크립트.
4) selfcorrect/: 실패 로그 패턴(lost atoms, NaN, bond atoms missing, 시간 초과) → 분류 → 처방(시드 변경 → Δt 절반, 최대 2회 재시도, 이후 사람 확인)을 YAML 규칙표로 두고, 래퍼가 적용 로그를 남긴다. 실습 03 을 위해 일부러 Δt 를 크게 한 스펙 예제 포함.
   참고: LA/docs/DECISION_RULES.md, LA/src/contracts/policies/failure.py, LA/docs/ops/EVENT_LOG_LAYERED_CAMPAIGN.md
5) examples/hybrid_overlay/: 유기(lj/cut) + 광물(buck) + 쿨롱(coul/long, 모든 쌍 1회) 예시와, 쿨롱이 붙은 스타일을 겹쳤을 때 이중 계산되는 반례를 에너지 비교로 보여 주는 테스트.
```

### 6주차 · `week06_postprocess/` — CED 계산 파이프라인
**저장 내용**
- `postprocess.py`: 밀도(블록 SE) · CED Method A(분자간 직접) · Method B(E_bulk − ΣE_isolated) · δ = √CED · Green–Kubo 점도 · MSD 확산계수 → CSV 한 줄
- `inputs/`: 점도(GK) · MSD · CED 재계산용 LAMMPS 입력
- `examples/`: 작은 궤적 · log 표본과 기대값(`expected/`)
- `schema.md`: CSV 열 이름 = 12주차 DB 스키마와 동일

```text
[6주차] 공통 머리말 +
week06_postprocess/ 를 만들어라. 강의계획서 GitHub 항목: 「CED 계산 파이프라인」. 기준: 발표용 6주차 덱 6-1~6-5, 실습 안내, 결과물 = 물성표(밀도 · CED · δ · η · D, 평균 ± 오차) · 판정 근거 그래프(부피 시계열 · 점도 러닝 적분 · MSD 로그–로그) · postprocess.py 와 실행 로그. CSV 열 이름은 12주차 DB 스키마와 같게.
1) postprocess.py: log · dump · 에너지 출력 → (a) 밀도 평균 ± 블록 SE, (b) CED Method A(분자간 상호작용 에너지 직접, compute group/group) · Method B(E_bulk − Σ 고립 분자 에너지, pe 만 사용 · ke 제외), (c) δ = √CED (MPa^0.5), (d) Green–Kubo 점도(압력 텐서 자기상관 러닝 적분 · 평탄 구간 판정), (e) MSD 선형 구간 기울기 → D. 단위 변환은 common/ 에 두고 테스트.
   참고: LA/docs/theory/ced-calculation-methods.md, LA/src/metrics, LA/docs/HANDOFF_bulk_ced_guard.md (음수 CED · 발산 bulk modulus 방어)
2) 검산 테스트: 덱 6-3 예시(ΔE 25,670 kcal/mol, V 482,000 Å³ → CED ≈ 370 MJ/m³, δ ≈ 19.2 MPa^0.5)가 재현되는지.
3) inputs/: GK 점도(NVT, 압력 텐서 저장 주기), MSD, 고립 분자 에너지 계산 입력.
4) 이상치 방어: CED < 0, 체적탄성률 > 50 GPa 등은 플래그 열로 표시(12주차 품질 검사와 같은 기준).
5) schema.md: 출력 CSV 열 이름 · 단위 · 설명.
```

### 7주차 · `week07_asphalt/` — 아스팔트 분자구조 · 모델 빌드 · 다중 힘장 입력
**저장 내용**
- `molecules/sara/`: SARA 대표 13분자(Li & Greenfield 12 + 고황 HighS13) SMILES · MOL, 분자량 표(화학식에서 계산)
- `molecules/additives/`: 첨가제 라이브러리 SMILES와 RDKit 기술자(분자량 · TPSA · logP · 방향족 비율 등)
- `build/`: 조성(wt%) → 분자 개수 → 5주차 생성기 스펙 변환, 노화 모델(산화 조성 치환) 예시
- `ff_stack/`: OPLS-AA · GAFF2 바인더 + ClayFF 광물 조합의 `ff_stack.inc`(쿨롱 1회)
- `analysis/`: RDF · 아스팔텐 적층 크기 분포 스크립트
- `rheology/`(데이터 이용 확인 후): DSR · BBR · MSCR 표본과 TTS 이동 · WLF 적합 노트북

```text
[7주차] 공통 머리말 +
week07_asphalt/ 를 만들어라. 강의계획서 GitHub 항목: 「아스팔트 분자구조(SARA · 첨가제) · 모델 빌드 · 다중 힘장 입력」. 기준: 발표용 7주차 덱 7-1~7-4, 실습 안내, 결과물 = 조건별(기준 · 첨가제 3 wt% · 노화) 물성 비교표(평균 ± SE) · 구조 해석 그림(RDF · 적층 크기 분포 · 스냅샷). 이 결과는 9주차 대리모델의 첫 학습 데이터다.
1) molecules/sara/: 13분자 구성(분류별 2 · 2 · 5 · 4, HighS13 포함) SMILES 와 3D MOL. 분자량은 화학식에서 계산해 표로(덱 값과 불일치하면 원천 확인 메모).
   참고: LA/docs/papers/paper7_spectroscopy_molecular_model/drafts/Manuscript_KR_v8.md (Table 3), LA/molecules
2) molecules/additives/: 첨가제 SMILES 와 RDKit 기술자 표. 출처와 분류(고분자 · 나노 · 바이오 등)를 열로.
3) build/compose.py: 조성 wt% → 개수 → week05 generator 의 spec.yaml 생성. 노화 모델: 산화 연산자(카보닐 · 설폭사이드 치환) 적용 예시와 원소비 · 산소 함량 검사.
   참고: LA/docs/workflows/aged-binder-bulk-procedure.md
4) ff_stack/: 바인더(OPLS-AA 또는 GAFF2) + 광물(ClayFF) 교차항을 명시 지정하는 ff_stack.inc. pair_style hybrid/overlay lj/cut 12.0 buck 12.0 coul/long 12.0, pair_coeff * * coul/long(쿨롱 1회). 이중 계산 반례 테스트는 week05 것을 재사용.
5) analysis/: RDF(방향족 고리 중심 간), 아스팔텐 적층(평면 간 거리 · 각도 기준) 크기 분포, 스냅샷 렌더(OVITO 선택).
6) rheology/(선택): 데이터 공개 조건을 확인한 뒤 S64-22 DSR 온도 스윕 · BBR S(t) · MSCR 표본과 TTS 노트북(이동인자 a_T, WLF C1 · C2 적합, 마스터커브). 공개할 수 없으면 형식이 같은 합성 표본과 '가정' 표기.
   참고: tools/rheology_sources.md (강의자료 저장소), LA/docs/papers/analysis_review_build/data/an57_expt.json · an79_cam.json
```

### 8주차 · `week08_cement/` — 시멘트 ReaxFF 모델 · ML 힘장 예제
**저장 내용**
- `structures/`: 클링커 4상(C₃S · β-C₂S · C₃A · C₄AF) COD CIF 내려받기와 슈퍼셀 · 표면 절단 스크립트
- `reaxff/`: C₃S 표면 + 물 층 수화 입력(ReaxFF, QEq, Δt 0.25 fs), 결합 생성 · 이온 용출 분석
- `csh/`: 토버모라이트 기반 C-S-H(Ca/Si 1.5 · 1.7) 모델, ClayFF 평형화, ±0.5 % 변형 탄성 상수, 층간 물 함량 변화
- `mlff/`: ReaxFF 궤적 프레임 → MLIP(예: NequIP · MACE) 학습 설정과 검증(에너지 · 힘 오차, 속도 비교)
- `tools/stoichiometry.py`: 수화 화학량론 계산기(덱 동적 도구와 같은 식)

```text
[8주차] 공통 머리말 +
week08_cement/ 를 만들어라. 강의계획서 GitHub 항목: 「시멘트 ReaxFF 모델 · ML 힘장 예제」. 기준: 발표용 8주차 덱 8-1~8-4, 실습 안내, 결과물 = Ca/Si · 물 함량별 밀도와 탄성계수 표(평균 ± SE) · 응력–변형 곡선 · 구조 스냅샷, 나노압입 문헌값과 같은 자릿수인지 확인.
1) structures/: COD 에서 알라이트(M3) · β-벨라이트 · C₃A(입방) · C₄AF(브라운밀러라이트) CIF 를 내려받는 스크립트(COD ID 명시)와, 덱 8-1 의 반응면((010) · (100) · (001) · (010))으로 슬래브를 자르는 스크립트.
   참고: uploads/1-s2.0-S0950061826020581-main.pdf (Shimelis 외 2026, Table 1 · Fig. 1)
2) reaxff/: C₃S 슬래브 + 물 층, pair_style reaxff + fix qeq/reaxff, timestep 0.25 fs, NVT 온도 가속(덱 8-2). ffield 는 원 논문 인용과 배포 조건을 확인해 내려받기 안내만 둔다. 분석: Ca–O_w 결합 수 · 배위수 · 이온 용출 시계열.
3) csh/: 토버모라이트 11 Å 에서 실리케이트 사슬 결손 · Ca 조정으로 Ca/Si 1.5 · 1.7 모델 생성, ClayFF + SPC/E 로 NPT 평형화, ±0.5 % 변형으로 탄성 상수 · 체적 · 전단 탄성계수 계산, 층간 물 함량 2 수준 비교. 결과를 나노압입 문헌값 범위와 비교하는 표.
4) mlff/: reaxff/ 궤적에서 프레임 추출 → 학습 · 검증 분할 → MLIP 학습 설정 파일(에너지 · 힘 가중치) → 검증 지표(에너지 MAE · 힘 RMSE) · 같은 계 속도 비교. GPU 전체판, CPU 축소판은 작은 모델 몇 스텝.
5) tools/stoichiometry.py: 클링커 조성 → 수화 생성물 질량(Mindess · Young · Darwin 표준 반응식, 표준 몰질량), 가정(석고 충분 · C-S-H = C₃S₂H₃ 이상화) 명시.
```

### 9주차 · `week09_xgboost_shap/` — XGBoost + SHAP 모델
**저장 내용**
- `features/`: RDKit 표현자 계산 · 조성 가중 평균 · feature library(버전 · 열 목록 고정)
- `train.py`: GroupKFold(comp_id), 점도는 그룹 3개 → 3-fold, 선형 · RF · XGBoost 비교, 폴드 평균 ± 편차
- `shap_report.py`: SHAP 요약 · PDP · 2D PDP, 물리 타당성 점검표
- `notebooks/`: 트리 분할 · 부스팅 · 누수 비교 · SHAP 누적(덱 동적 도구와 같은 실험)
- `data/`: 공개 가능한 표본(또는 합성 표본)과 열 설명

```text
[9주차] 공통 머리말 +
week09_xgboost_shap/ 를 만들어라. 강의계획서 GitHub 항목: 「XGBoost+SHAP 모델」. 기준: 발표용 9주차 덱 9-1~9-3, 실습 안내, 결과물 = 물성별 RMSE · MAE · R² 표(폴드 평균 ± 편차) · SHAP 요약 그림과 해석 메모 · 재정련한 특징 목록. 이 성능이 10주차 GNN 의 기준선이다.
1) features/: SMILES → RDKit 기술자(분자량 · TPSA · logP · 방향족 비율 등) → 조성 가중 평균. feature library 는 RDKit 버전 · 비트 수 · 열 목록을 메타데이터로 고정.
2) train.py: GroupKFold(그룹 = comp_id). 표준화는 폴드 안에서 X[tr].mean(axis=0) · std(axis=0) 로 맞추고 검증 폴드에 같은 μ · σ 적용. 점도(58행 · 3그룹)는 3-fold 로 줄이고 경고 출력. 선형 회귀 · RF · XGBoost 비교.
   참고: LA/claude_science_export/comid_modeling_report.md, comid_feature_correction.md (additive_wt 제거 근거), comid_rf_vs_xgb.csv
3) shap_report.py: TreeExplainer SHAP 요약 · 의존 그림, PDP · 2D PDP, '물리적으로 말이 되는가' 점검표(부호 · 단조성).
4) notebooks/: (a) 한 특징 임계값을 옮기며 SSE 변화 (b) 깊이 1 트리 부스팅 잔차 감소 · 학습률 비교 (c) 무작위 vs 그룹 분할 R² 차이(1-NN · 부스팅) (d) SHAP 기준값 + 기여 합 = 예측 확인.
5) data/: comid_core672_dataset.csv 는 공개 조건을 확인한 뒤 표본만. 공개할 수 없으면 같은 열 구조의 합성 표본과 '가정' 표기.
```

### 10주차 · `week10_gnn/` — GNN(Graphormer-3D) 학습 코드
**저장 내용**
- `data/to_pyg.py`: 분자 그래프(노드 · 엣지 특징) · 결정 · 벌크 그래프(컷오프 · 주기 영상) → PyG Data
- `models/mpnn.py`: 3층 MPNN + 조성 가중 풀링(실습 기준 모델)
- `models/graphormer3d.py`: 3D 거리 인코딩(가우스 기저) · 어텐션 편향, 노드 · 엣지 · 시스템 특징
- `train.py`: comp_id 폴드 학습 · 학습 곡선 · 체크포인트 · 설정 파일, 선형 기준 대비 비교
- `uncertainty/`: 시드 앙상블 불확실성 · 보정 곡선, 획득함수(EI · UCB) 예시

```text
[10주차] 공통 머리말 +
week10_gnn/ 를 만들어라. 강의계획서 GitHub 항목: 「GNN(Graphormer-3D) 학습 코드」. 기준: 발표용 10주차 덱 10-1~10-4, 실습 안내, 결과물 = 학습 곡선 · 체크포인트 · 설정 파일 · 예측 스크립트(조성 입력 → 물성 출력), 선형 기준 모델 대비 성능 우위 확인.
1) data/to_pyg.py: 9주차 데이터셋 → 분자별 그래프(원자 번호 · 혼성 · 방향족 · 형식전하 노드 특징, 결합 차수 엣지 특징) + 조성 가중치 → PyG Data. 결정 · 벌크용 컷오프 반경 그래프 · 주기 영상 처리 함수도 포함.
2) models/mpnn.py: 3층 메시지 패싱 + 조성 가중 풀링 + MLP 회귀. 스칼라 출력(밀도 등)은 회전 · 병진 불변, 힘 같은 벡터 출력이 필요한 경우 등변 모델을 쓴다는 주석.
3) models/graphormer3d.py: 원자 쌍 거리의 가우스 기저 인코딩을 어텐션 편향으로 쓰는 Graphormer-3D 축소 구현(4층 · 4헤드), 시스템 특징 결합, 게이트 풀링.
   참고: /home/tyun/MDML20250630/20260612_PreTrain_Morgan_Tanimoto_Density_opt_LigninHoldOut.py (Graphormer3D · build_supergraph), LA/docs/plans/STRUCTURAL_ML_NODE_SYSTEM_FEATURES_PLAN.md
4) train.py: comp_id GroupKFold, 조기 종료, 학습 곡선 CSV · 그림, 체크포인트, config.yaml, 조성 특징 선형 모델과의 비교표. predict.py: 조성 → 물성 함수.
5) uncertainty/: 시드 5개 앙상블 평균 · 분산, 보정 곡선(68 % · 95 % 커버리지), 1차원 GP 위 EI · UCB 예시(10주차 보충 A · B 와 연결).
```

### 11주차 · `week11_literature/` — Obsidian vault 템플릿 · 스크래핑 스크립트
**저장 내용**
- `vault_template/`: 폴더 구조(00_Inbox · 10_Papers · 20_Concepts · 30_Claims · 90_Templates), 논문 노트 · 개념 노트 · 주장 노트 템플릿, Dataview 질의 예시
- `harvest/`: Crossref · OpenAlex 수집(검색식 · 실행 날짜 · 결과 건수 기록), DOI 정규화 · 제목 유사도 중복 제거, 선별 흐름도 건수
- `extract/`: LLM 스키마 추출(JSON 스키마 · 프롬프트), 사람 채점 시트, 필드별 정확도 → 자동 추출 대상 결정
- `candidates/`: 추출 첨가제 → SMILES 변환(PubChem) → 라이브러리 등록 형식(12주차 입력)
- `zotero/`: Better BibTeX 인용키 규칙 · 자동 내보내기 설정 안내, Zotero ↔ Obsidian 연결 설정

```text
[11주차] 공통 머리말 +
week11_literature/ 를 만들어라. 강의계획서 GitHub 항목: 「Obsidian vault 템플릿 · 스크래핑 스크립트」. 기준: 발표용 11주차 덱 11-1~11-4, 실습 안내, 결과물 = 검색식 · 수집 기록 · 선별 흐름도(건수) · 추출 정확도 채점표와 후보 분자 목록(출처 DOI) · 자동 내보낸 .bib 와 링크된 논문 노트 3편.
문헌 전문(PDF · XML)은 저장소에 넣지 않는다(TDM 약관). 서지정보 · DOI · 스크립트만.
1) vault_template/: 폴더 구조와 템플릿(논문 노트: citekey · DOI · 연도 · 방법 · 수치 · 한계 · 관련 개념 링크, 개념 노트, 주장 노트). Dataview 질의 예시(연도별 · 방법별 표). Templater 플러그인 없이도 쓰이는 형태.
2) harvest/harvest.py: Crossref · OpenAlex API(polite pool, mailto 파라미터), 검색식 · 실행 날짜 · 결과 건수를 JSON 로그로, 최근 5년 200건 수집. dedupe.py: DOI 정규화(URL 접두 · doi: · 대소문자 · 공백 제거) + 제목 유사도 중복 제거, 선별 흐름도 건수 출력.
   참고: LA/claude_science_export/comid_fulltext_download_README.md, LA/scripts/build_corpus_index.py (norm_doi), LA/src/llm/literature
3) extract/: 초록 → JSON 스키마(첨가제명 · 함량 · 물성 · 단위 · 시험법) 추출 프롬프트, 30건 사람 채점 시트(CSV), 필드별 정확도 집계. 정확도가 낮은 필드는 자동 추출 대상에서 제외하는 규칙.
4) candidates/: 첨가제명 → PubChem PUG-REST 로 SMILES, 실패 목록 분리, 출처 DOI 와 함께 라이브러리 CSV.
5) zotero/: Better BibTeX 인용키 형식 예시와 Keep updated 내보내기, Obsidian Zotero Integration 설정 안내(스크린샷 자리 표시). 예시 인용키는 '예시'로 표시.
```

### 12주차 · `week12_pipeline/` — 자율 탐색 파이프라인 예제
**저장 내용**
- `grid/`: 바인더 · 노화 · 첨가제 · 온도 격자 생성과 조성 제약 필터
- `db/`: 세 테이블(조성 · 실행 · 물성) 스키마 — SQLite DDL과 PostgreSQL DDL(외래 키 · CHECK · NOT NULL), 적재 스크립트
- `features/`: 분자 기술자 · 조성 가중 평균(9주차 모듈 재사용)
- `splits/`: comp_id 5-폴드 인덱스, 폴드별 μ · σ 저장
- `qc/`: 품질 검사(음수 CED · 비정상 체적탄성률 · 미수렴 · 재시도 라벨) 플래그 통계, `run_manifest`

```text
[12주차] 공통 머리말 +
week12_pipeline/ 를 만들어라. 강의계획서 GitHub 항목: 「자율 탐색 파이프라인 예제」. 기준: 발표용 12주차 덱 12-1~12-4, 실습 안내, 결과물 = 후보 격자 CSV · DB 파일과 스키마 정의 · 폴드 인덱스 · 특징 · 라벨 통계 요약. 9–10주차 학습 스크립트의 입력으로 그대로 쓰인다.
1) grid/make_grid.py: 바인더 3 × 첨가제 계열 × 함량 × 노화 3 × 온도 12 격자, 조성 제약(첨가제 wt% 상한 · SARA 합 100 %) 필터, 격자 수 보고.
2) db/schema_sqlite.sql · schema_postgres.sql: composition · run · property 세 테이블(긴 형식 물성), exp_id(해시 포함) 기본 키, 외래 키 · CHECK(단위 · 범위) · NOT NULL. load.py: week06 CSV 와 run_manifest 를 적재. 운영 플랫폼은 SQLite, PostgreSQL 은 같은 설계를 옮기는 예시라고 README 에 명시.
   참고: LA/docs/architecture/db-ml-ssot-contract.md, LA/docs/figures/fig7_db_erd.png
3) features/: week09 features 모듈 재사용.
4) splits/: comp_id GroupKFold 5-폴드 인덱스 파일, 폴드별 학습 μ · σ 저장(누수 방지).
5) qc/check.py: CED < 0, K > 50 GPa, 미수렴, retry 라벨 오염 등 플래그와 통계, run_manifest.json.
   참고: LA/docs/HANDOFF_bulk_ced_guard.md, LA/claude_science_export/comid_data_quality_eda.md
```

### 13주차 · `week13_optimization/` — 최적화 · 에이전트 오케스트레이션 · 통합 사례 · 검증
**저장 내용**
- `moo/`: 목적 2개 + 제약 정의, 앙상블 대리모델 평가, EHVI(BoTorch) 5회 루프, 파레토 · HV 곡선
- `agents/`: 제안자–비평자(proposer–critic) 최소 구현과 결정론적 점수 · 사람 승인 게이트, 운영 교훈 메모
- `refine/`: 특징 재정련 루프(누수 · 종속 특징 제거 → 재학습 비교)
- `case_study/`: 아스팔트 통합 사례 노트북(처방 3개 · 사용성 게이트)
- `validation/`: MD 예측 ↔ 실측(밀도 · Tg · DSR · BBR · MSCR) 대조 형식과 한계, 데이터 이용 조건

```text
[13주차] 공통 머리말 +
week13_optimization/ 를 만들어라. 강의계획서 GitHub 항목: 「최적화 · 에이전트 오케스트레이션 · 통합 사례 · 검증」. 기준: 발표용 13주차 덱 13-1~13-5, 실습 안내, 결과물 = 파레토 전선 도표 · 회차별 HV 곡선 · 추천 조성 표(조성 · 예측 물성 ± 불확실성 · 제약 충족 여부) · 추천 상위 3조성의 검증 계산 계획.
1) moo/: 목적 2개(예: CED ↑ · 점도 범위) + 제약(첨가제 wt% · 사용 가능 밀도 창)을 코드로 정의. week10 uncertainty 앙상블로 후보 평가, BoTorch qEHVI 로 5회 루프, 회차별 HV · 파레토 그림, 참조점 선택 근거.
   참고: LA/claude_science_export/comid_inverse_design.md, LA/docs/plans/INVERSE_DESIGN_AUTOMATION_PLAN.md
2) agents/: 제안자 LLM → 비평자 LLM → 결정론적 후보 점수 → 사람 승인 게이트의 최소 오케스트레이션(LLM 호출은 교체 가능한 인터페이스, 오프라인 모의 응답 포함). 플랫폼에서 토론 스택을 제거하고 함수 호출 + 결정론적 점수로 바꾼 교훈을 README 에.
   참고: LA/docs/archive/LLM_AGENT_IMPLEMENTATION_PLAN.md, LA/docs/papers/IJPE_Conference_2026/drafts/PAPER_I_framework_20260825.md
3) refine/: additive_wt 처럼 다른 열의 복사본인 특징을 찾는 검사(상관 · 그룹 상수) → 제거 → 재학습 성능 비교.
   참고: LA/claude_science_export/comid_feature_correction.md
4) case_study/: 목표 3종 처방과 사용성 게이트(밀도 창 · 학습 분포 LOF 판정)를 재현하는 노트북. comid_paper_v3 수치는 '함량확장 재실행 전'이라고 표시.
5) validation/: 예측 ↔ 실측 대조 표 형식(밀도 · Tg · DSR G*/sinδ · BBR S · m · MSCR Jnr), 규격 기준선은 '참고'로만, 시료명 불일치(BBR −12 °C NA) 같은 데이터 품질 주의. 실측 원자료는 공개 조건 확인 뒤 표본만.
   참고: 강의자료 저장소 tools/rheology_sources.md
```

---

## 4. 만드는 순서와 점검

1. **1주차 → 5주차**를 먼저 만든다(환경 · 생성기가 뒤 주차의 기반).
2. **6 → 7 → 8주차**: 계산 결과 CSV 형식을 6주차에서 고정한다.
3. **12주차 DB · 폴드 → 9 · 10주차 학습**: 입력 형식이 12주차에 맞춰진다.
4. **11 · 13주차**: 문헌 · 최적화.
5. 주차마다 점검한다.
   - 축소판 `pytest tests/test_weekNN.py`가 CPU에서 5분 안에 통과
   - README의 결과물 체크리스트가 덱 실습 안내의 DELIVERABLE과 일치
   - `data/README.md`에 모든 데이터의 출처 · 공개 조건 · 측정/계산/문헌/가정 구분을 기록
