# DT-Lab 앱 구성 프롬프트 (P00 ~ P13)

13주 실습을 따라 하나의 앱(DT-Lab)을 쌓아 가는 구현 프롬프트다. 주차마다 모듈 · CLI · 앱 페이지 · 테스트가 하나씩 늘어난다. 구조 생성(분자 → 3층 셀 → 인장 패키지 → 캠페인)의 세부는 `PROMPTS_STRUCTURE.md`의 S 프롬프트에 있고, P 프롬프트는 해당 S 프롬프트를 불러 쓰는 방식으로 연결한다.

- 계획: `INTEGRATED_APP_PLAN.md`
- 설치 · 힘장 기준: `INSTALL_GUIDE.md`, `FF_COMPATIBILITY.md`
- 작성일: 2026-09-22

## 사용법
1. **P00**으로 저장소를 만든다. 이후 주차마다 **공통 머리말 + Pnn**을 Claude Code에 붙여 넣는다.
2. 모든 프롬프트는 앞 주차의 산출물(모듈 · 명세 · 실행 대장)이 있다는 전제로 쓰였다. 앞 주차의 완료 기준을 통과한 뒤 다음으로 넘어간다.
3. 설치 시점은 권장일 뿐이다. 처음 한 번 `bash install/create_env.sh`로 전용 가상환경 `dtlab`을 만들고, 필요한 그룹은 `bash install/install.sh <그룹>`으로 그 환경에만 설치한다(S0). 실행은 항상 `bin/dtlab …` · `bin/dtlab-app`으로 하며, 이 래퍼가 환경을 자동으로 활성화한다.
4. **완료 확인은 공통 3단계다.**
   - `bin/dtlab test NN` (환경 활성화 후 `pytest tests/test_weekNN.py`)
   - `bin/dtlab check-env --week NN`
   - `bin/dtlab-app`에서 새 페이지가 열리는지

| 프롬프트 | 주차 | 핵심 산출 | 함께 쓰는 S 프롬프트 |
|---|---|---|---|
| P00 | 준비 | 저장소 · 패키지 뼈대 · CI · 가상환경 | S0 · S0-P · S0-V |
| P01 | 1 | core · CLI · 앱 홈 · 환경 점검 | S0 |
| P02 | 2 | LJ 고체 인장 · 곡선 뷰어 | — |
| P03 | 3 | 분자 라이브러리 · 힘장 · 교차항 · 평형 판정 | S1 · S2 |
| P04 | 4 | 벌크 · 슬래브 · 물층 · 3층 · 벤치마크 · 구조 빌더 | S4 · S3 · S5 · S6 |
| P05 | 5 | 생성기 · CPU 실행기 · 자기교정 · 실행 대장 · 반복 연구 | S7 |
| P06 | 6 | 인장 지표 · CED · QC · 지표 페이지 | S10 |
| P07 | 7 | 설계 공간 · 캠페인 · 캠페인 페이지 | S8 |
| P08 | 8 | portlandite 기판 · ReaxFF · SNAP 예제 | S9 |
| P09 | 9 | 특징 · XGBoost · SHAP · 모델 페이지 | — |
| P10 | 10 | GNN · 불확실성 · 능동학습 | S7 · S8(추가 실행) |
| P11 | 11 | 문헌 수집 · 추출 · 후보 분자 · 검증 기준표 | S1(신규 분자) |
| P12 | 12 | 정식 DB · 품질 게이트 · 폴드 · 자동 루프 | S10 |
| P13 | 13 | 다목적 역설계 · 에이전트 · 검증 · 앱 완성 | S7 · S8(검증 실행) |

---

## 공통 머리말 (모든 P 프롬프트 앞에 붙임)

```text
[DT-Lab 공통 머리말 · 앱]
너는 대학원 MOOC 「건설소재 역설계 도구 개발을 위한 AI와 분자동역학 활용」의 통합 실습 앱 DT-Lab 을 만드는 개발자다.
앱 목적: 단순 분자 바인더 | 물층 | 광물(α-석영 · portlandite) 3층 셀의 CPU LAMMPS 직접인장 데이터(온도 253 · 273 · 293 K, 온도별 약 100개)를 만들고,
기계학습 대리모델과 다목적 역설계로 조성을 추천한 뒤 MD 로 다시 검증하는 폐루프.
저장소 규칙
- 패키지 dtlab/ (모듈: core toy ff build gen analyze campaign cement ml lit db opt), CLI cli.py(typer) `dtlab <그룹> <명령>`, 앱 app/(Streamlit, 페이지 파일 app/pages/NN_이름.py).
- 이번 주차 작업은 앞 주차 모듈을 import 해서 쓴다. 코드 복사 금지, 기존 공개 함수 시그니처 변경 금지(필요하면 새 함수 추가 + 기존 것 유지).
- 설정은 specs/*.yaml + pydantic 모델. 경로 · 온도 · 속도 · 코어 수를 코드에 하드코딩하지 않는다.
- 모든 계산 산출물 폴더에 manifest.json(입력 명세 · 입력 SHA-256 · 도구 버전 · seed · 부모 ID · 시각). 산출물 ID = 정규화 명세 SHA-256 앞 12자리. 멱등.
- 실행 결과는 5주차 이후 실행 대장(data/runs.sqlite)에 기록. 12주차부터 정식 DB(data/dtlab.sqlite).
- 가상환경: 모든 설치 · 실행은 전용 conda 환경 dtlab 에서(S0). 명령은 bin/dtlab, 앱은 bin/dtlab-app, 노트북은 'DT-Lab (dtlab)' 커널. 새 파이썬 진입점은 dtlab.core.env.assert_env() 를 먼저 호출. 새 의존성은 install/groups.yaml 에 추가(직접 pip install 금지).
- LAMMPS 는 CPU 전용(MPI + OpenMP). 실행 파일은 dtlab.core.env.lmp_path() 로만 얻는다.
- 수치 · 파라미터를 지어내지 말 것. 출처를 주석 · README 에 쓰고 가정값은 '가정' 으로 표시.
- 실패는 fail-closed(조용한 근사 우회 금지). 예외 메시지에 원인 · 조치 한 줄.
- 테스트: tests/test_weekNN.py (pytest, CPU 5분 이내 축소판). 앱 페이지는 데이터가 없을 때도 안내 문구와 함께 열려야 한다.
- 문서: weekNN/README.md(한국어) = 학습목표(강의계획서 차시 코드) · 이번 주에 추가된 모듈 · 실행 순서 · 결과물 체크리스트 · 한계. 전문 용어는 처음 나올 때 영어 병기.
- 참고 코드(읽기 전용, 복사 금지): /home/tyun/mounted_directory/sdd/Claude_Code/LAMMPS_Asphalt (LA). *.db 는 열지 않는다.
- 기준 문서: INSTALL_GUIDE.md(설치 · 플랫폼 · Packmol), FF_COMPATIBILITY.md(힘장 조합 · 타입 접두어 g2_ · sw_ · cf_ · 검증 V1~V9). 지원 플랫폼 Linux · macOS · Windows(WSL2 전용). 기본 프로필 laptop(MPI 없음, OpenMP).
- 모든 문서는 한국어로 쓰고, 실행이 필요한 문서에는 반드시 「실행 순서」(번호 목록: 명령 · 예상 시간 · 성공 판정 · 실패 시 조치)와 「Windows(WSL2) · macOS 주의」 절을 둔다.
- 끝나면: 변경 파일 목록, 새 CLI 명령, 테스트 결과, 남은 한계를 보고.
```

---

## P00 · 저장소 준비

```text
[P00] 공통 머리말 +
새 저장소 mooc-inverse-design/ 을 초기화하라.
1) 폴더: dtlab/{__init__,core,toy,ff,build,gen,analyze,campaign,cement,ml,lit,db,opt}/__init__.py, app/Home.py, app/pages/, specs/, library/, data/{reference,samples}/, install/, env/, tests/, week01 ~ week13/ (각 README.md 자리 표시).
2) pyproject.toml: 패키지 dtlab, 콘솔 스크립트 dtlab = cli:app, 선택 의존성 그룹 [md] [ml] [lit] [db] (S0 그룹과 일치).
3) environment.yml: S0 의 G0 만 우선. 나머지 그룹은 install/groups.yaml 로.
4) .gitignore: runs/ 의 대용량(dump, restart), *.sqlite(단, data/reference/*.sqlite 는 예외 목록), __pycache__, .ipynb_checkpoints.
   gitignore 된 것 중 재생 불가능한 것(기준 캠페인 결과)은 data/reference/ 에 두고 Git LFS 또는 릴리스 첨부로 관리한다는 규칙을 README 에(LA 교훈 22).
5) 가상환경 우선: S0 의 0) 항목(install/create_env.sh · env/activate.sh · bin/dtlab · bin/dtlab-app · assert_env)을 이 단계에서 먼저 만든다. `bin/dtlab test NN` 하위 명령(환경 활성화 후 pytest) 포함.
   README 첫 절 「시작하기」: 운영체제별 준비(Linux · macOS · Windows=WSL2, INSTALL_GUIDE §2~§4 요약과 링크) → git clone(WSL2 는 ~/ 아래) → bash install/create_env.sh --profile laptop → bash install/install.sh G0 G1 → bin/dtlab check-env → bin/dtlab selftest md → bin/dtlab-app. 'conda activate dtlab 을 잊어도 bin/ 래퍼가 활성화한다' 는 문장 포함. 단계마다 예상 시간 · 성공 판정 · 실패 시 조치.
   INSTALL_GUIDE.md · FF_COMPATIBILITY.md 를 저장소 docs/ 에 복사(원본 유지).
   .gitattributes: *.sh *.in *.inp *.j2 *.yaml *.py text eol=lf (Windows 줄끝 문제 방지).
6) README.md: 앱 개요 그림(ASCII: 분자 → 3층 → 인장 → DB → ML → 역설계 → MD 검증), 주차 ↔ 모듈 표, 설치 요약(S0), 데이터 이용 조건, 한계.
7) .github/workflows/ci.yml: 로컬과 같은 install/create_env.sh · install/install.sh G0 G1(미리 빌드판 lammps · packmol · ambertools) 로 dtlab 환경을 만든 뒤 bin/dtlab test 00 과 pytest -m "not slow". 소스 빌드는 CI 에서 하지 않는다.
8) tests/test_week00.py: 패키지 import, `bin/dtlab --help` 동작, 래퍼가 dtlab 환경의 python 을 쓰는지(sys.prefix 출력 비교).
완료 기준: 환경을 활성화하지 않은 새 터미널에서 `bin/dtlab --help` 가 dtlab 환경으로 실행, CI 파일 문법 검사(act 없으면 yaml 파싱 테스트).
```

---

## P01 · 1주차 — core · CLI · 앱 홈 · 환경 점검

```text
[P01] 공통 머리말 +
1주차(1-1 ~ 1-4) 작업. 먼저 PROMPTS_STRUCTURE.md 의 S0 을 수행해 install/ 과 `dtlab check-env` 를 만든다. 그 위에:
1) dtlab/core/ids.py: normalize(spec) → 정렬 · 부동소수 12자리 문자열화한 JSON, artifact_id(spec) → sha256[:12]. 테스트: 키 순서 · 0.1+0.2 표현 차이에도 같은 ID.
2) dtlab/core/manifest.py: write_manifest(folder, spec, inputs:list[Path], parents:list[str], seed) / read_manifest / verify_manifest(입력 파일 해시 재계산 대조).
3) dtlab/core/units.py: kcal/mol ↔ kJ/mol ↔ eV, kcal/mol/Å³ → MPa(6947.7), g/cm³ ↔ amu/Å³(1.66054), 각 변환에 테스트(왕복 오차 < 1e-12).
4) dtlab/core/config.py: DTLAB_HOME, 데이터 · 실행 폴더 경로, lmp 선택(S0 규칙) — 환경변수 > specs/local.yaml > 기본값.
5) app/Home.py: 앱 소개, 파이프라인 지도(1~13주 단계, 현재 구현된 단계는 초록 · 미구현은 회색 — dtlab 모듈 존재 여부로 자동 판정), 환경 점검 표(check-env 결과).
6) week01/README.md: 1-1 역설계 동기 · 1-2 스케일 · 1-3 디지털 트윈 · 1-4 파이프라인 흐름을 DT-Lab 의 어느 단계가 담당하는지 표로.
7) tests/test_week01.py: ids · manifest · units · check-env 표 생성.
완료 기준: 앱 홈에서 1주차 단계만 초록으로 표시, check-env --week 1 통과.
```

---

## P02 · 2주차 — LJ 고체 직접인장 · 곡선 뷰어

```text
[P02] 공통 머리말 +
2주차(2-1 원리 · 2-2 퍼텐셜 · 2-3 수치적분 · 2-4 경계조건) 작업. dtlab/toy/ 를 만든다. 모든 입력은 units lj.
1) toy/lj_templates/: (a) in.lj_nve — 덱 실습 입력(fcc 0.8442, lj/cut 2.5, velocity 1.44, timestep 0.005, NVE) (b) in.lj_tension — fcc 고체(밀도 1.0, T* 0.1 로 평형, NVT) → fix deform z erate(변수) + x · y 는 npt 로 압력 0 유지(단축 응력) → 변형률 0.5 까지.
   응력: −pzz(부호 규칙 주석), 변형률 = (Lz − Lz0)/Lz0, fix ave/time 로 파일 기록.
2) toy/run.py: 템플릿 렌더 → 실행(lmp_path, 1코어 기본) → 로그 파싱(thermo 블록 여러 개 처리, 'WARNING' 수집).
3) toy/experiments.py:
   - timestep_sweep: dt {0.002, 0.005, 0.010, 0.020} → 에너지 드리프트(etotal 선형 적합 기울기 / 원자) 표. 발산(NaN, lost atoms)은 '발산' 으로.
   - cutoff_sweep: rc {1.5, 2.5, 3.5} → 평균 pe · 압력 차이.
   - size_sweep: 격자 {5, 8, 10} → 요동 크기 ∝ 1/√N 확인.
   - tension_rate: erate {1e-3, 1e-2} (lj 단위) → σ_max 차이.
4) dtlab/analyze/curves.py(6주차 모듈의 원형): peak(x, y, window) → (x_peak, y_max) 창 평균 후 최댓값, area_under(x, y, until) → 적분. 이 두 함수는 6주차에서 그대로 재사용한다.
5) app/pages/02_곡선뷰어.py: 실험 선택 → thermo 시계열 · 드리프트 표 · 응력–변형 곡선(최대점 표시).
6) week02/notebooks/verlet_by_hand.ipynb: 2원자 LJ velocity-Verlet 한 스텝 손계산 → toy 결과와 일치 확인.
7) tests/test_week02.py: 축소판(격자 4, 1000 스텝) 실행, dt 를 키우면 드리프트가 커지는지 단조성 검사, peak · area_under 해석해(삼각형 곡선) 검사.
CLI: `dtlab toy nve`, `dtlab toy sweep --kind timestep`, `dtlab toy tension --erate 0.01`
완료 기준: 1코어에서 인장 곡선이 1분 안에 나오고 곡선 뷰어에 표시.
```

---

## P03 · 3주차 — 분자 라이브러리 · 힘장 · 교차항 · 평형 판정

```text
[P03] 공통 머리말 +
3주차(3-1 힘장 · 3-2 전하 · 3-3 앙상블 · 3-4 평형화와 다중 힘장) 작업.
1) PROMPTS_STRUCTURE.md 의 S1(분자 7종 GAFF2 · AM1-BCC · 에너지 일치 검증)과 S2(SPC/E · ClayFF · 교차항 표)를 수행한다.
2) dtlab/analyze/equil.py:
   - block_average(x, n_blocks) → 평균, SE, 블록 크기에 따른 SE 곡선(평탄 구간에서 SE 채택)
   - autocorr_time(x) → 적분 자기상관 시간
   - t_eq(x, t) → 앞부분을 잘라 가며 전반 · 후반 평균 차 < 2 SE 가 되는 최소 절단 시간
   - seeds_summary(list of arrays) → 시드별 평균, 전체 평균 ± SE(시드 간)
3) 온도 조절기 비교 실습(toy 재사용): LJ 액체 NVT 에서 Nosé–Hoover · Berendsen · Langevin 온도 분포 폭 비교 표. 수송 물성(확산) 비교에서 Langevin 이 왜곡하는지 확인.
4) app/pages/03_분자라이브러리.py: 분자 표(구조 이미지 · 화학식 · 분자량 · 전하 합 · GAFF 타입 수), 교차항 표(검색 · 정렬), 산술 · 기하 혼합 차이 상위 10쌍.
5) week03/README.md: 이종쌍(unlike pair) · 조합 규칙(combining rule) · 형식전하(formal charge) 개념과 DT-Lab 에서의 위치.
6) tests/test_week03.py: S1 · S2 테스트 + equil 함수(합성 AR(1) 시계열로 SE · 자기상관 시간 해석해 대조).
완료 기준: 분자 라이브러리 페이지에서 7종 + 물 + ClayFF 타입이 보이고, 교차항 표가 생성됨.
```

---

## P04 · 4주차 — 벌크 · 슬래브 · 물층 · 3층 · CPU 벤치마크 · 구조 빌더

```text
[P04] 공통 머리말 +
4주차(4-1 설치 · 4-2 입력 스크립트 · 4-3 데이터 파일 · 4-4 초기 구조 · 4-5 다층구조) 작업.
1) (권장) install/build_lammps.sh 로 CPU 소스 빌드(S0). 미리 빌드판과 둘 다 쓸 수 있게 lmp 선택 규칙 유지.
2) PROMPTS_STRUCTURE.md 의 S4(석영 슬래브) → S3(벌크 바인더, 기준 조성) → S5(물층 0 · 1 · 2) → S6(3층 조립)을 순서대로 수행.
   기준 조성 specs/bulk_ref.yaml: SAT 35 · ARO 35 · RES 20 · ASP 10 wt%, 첨가제 없음(가정 — 12주차 설계 공간의 중심점).
3) dtlab/gen/bench.py + `dtlab bench`: 기준 3층 셀(water 1)로 짧은 NVT(10 ps) 를 (MPI 랭크 × OpenMP 스레드) = (4×1, 8×1, 4×2, 8×2, 16×1) × dt {1, 2 fs} 조합으로 실행 → ns/day, 병렬 효율 표 → env/bench.json.
   동시에 k 개 작업을 돌렸을 때 개별 속도 저하(LA 교훈 9 · 12)를 2 · 4 · 8 동시 실행으로 측정.
   결과로 INTEGRATED_APP_PLAN §3 계산량 표를 갱신하는 스크립트(tools/update_budget.py)와, 인장 속도 · 코어 배정 권고값 출력.
4) 수동 인장 1회: S7 의 템플릿이 아직 없으므로 week04/manual/in.tension_manual(주석이 많은 교육용 입력)로 기준 셀 × 293 K 인장을 1회 실행. 5주차에 이 입력을 템플릿으로 바꾼다(4-2 입력 해부의 교재 역할).
5) app/pages/04_구조빌더.py: 조성 슬라이더(합 100 자동 정규화) · 첨가제 · 물층 선택 → '입력만 생성' 버튼(S3 → S6 --dry-run 결과: 분자 개수 · 원자 수 · 층 z 범위) → 생성된 구조가 있으면 x–z 스냅샷 표시. 계산 실행 버튼은 두지 않는다(실행은 5주차 실행기로).
6) week04/README.md: data 파일 구획(Masses · Atoms · Bonds …)과 layered.data 의 실제 예를 대응시키는 표. 타입 번호 병합 규칙.
7) tests/test_week04.py: S3 ~ S6 축소판 테스트, bench.json 스키마.
완료 기준: 3층 셀(water 0 · 1 · 2) 3개, bench.json, 첫 3층 인장 곡선 PNG.
```

---

## P05 · 5주차 — 생성기 · CPU 실행기 · 자기교정 · 실행 대장

```text
[P05] 공통 머리말 +
5주차(5-1 자동 생성 · 5-2 자기교정 · 5-3 FF-neutral 토폴로지 · 5-4 다중 힘장 스택 · 배치 실행) 작업.
1) PROMPTS_STRUCTURE.md 의 S7(인장 실행 패키지)을 수행. week04 수동 입력과 렌더 결과를 diff 로 비교하는 테스트를 둔다.
2) dtlab/gen/registry.py — 실행 대장 data/runs.sqlite (테이블 runs 하나):
   exp_id(PK) · kind(bulk|parent|child|toy) · parent_id · spec_json · campaign_tag · status(planned|queued|running|done|failed|needs_human) · attempts · fail_class · fail_msg · path · cores · started · finished · wall_s · lmp_version.
   함수: register(spec) · set_status · next_ready(의존성: 부모 done 인 자식만) · summary().
3) dtlab/gen/runner.py — 로컬 CPU 실행기:
   - `dtlab run --jobs N --cores k [--tag T]`: 대장에서 준비된 작업을 N 개 병렬(각 k 코어, OMP_NUM_THREADS 명시, mpirun -np 랭크)로 실행.
   - 하트비트: 로그 크기 · 마지막 step 을 30초마다 기록, 진행 정체 판정은 bench.json 의 예상 속도 대비 10배 이상 느릴 때만(LA 교훈 26 — 감속을 교착으로 오진하지 않기).
   - 중단(Ctrl-C) 시 running 을 queued 로 되돌리고 부분 산출물은 *.partial 로 격리(교훈 30).
4) dtlab/gen/selfcorrect.py — 실패 분류 규칙표 specs/failure_rules.yaml:
   lost_atoms · pppm_out_of_range · shake_failure · packmol_not_converged · bond_atoms_missing · nan_energy · timeout
   → 처방: seed+1 / dt 절반 / 진공 +20 Å / Packmol tolerance · 초기 밀도 조정. 재시도 최대 2회, 같은 분류로 두 번 실패하면 needs_human(교훈 2: 결정론적 실패에 시드 재시도 남발 금지 — 규칙표에 deterministic: true 표시된 분류는 재시도 없이 needs_human).
   적용 기록을 대장 attempts · fail_class 와 selfcorrect_log.jsonl 에 남긴다.
5) FF-neutral 토폴로지(5-3): dtlab/ff/neutral.py — 분자 템플릿에서 원소 · 좌표 · 결합 차수만 뽑은 중립 JSON ↔ GAFF2 템플릿 재생성 왕복 테스트. (다른 힘장 OPLS-AA 로 같은 중립 토폴로지를 타이핑하는 예시는 선택 — LigParGen 등 외부 도구 필요 시 안내만.)
6) 다중 힘장 스택(5-4) 교육 예제 week05/hybrid_overlay/: 쿨롱이 붙은 쌍 스타일을 hybrid/overlay 로 두 번 겹치면 쿨롱이 이중 계산됨을 2원자 에너지로 보이는 테스트. DT-Lab 본 계산은 세 힘장 모두 LJ 12-6 이라 단일 pair_style 로 충분하다는 설명.
7) 반복 연구 명세 specs/replicate_ref.yaml: 기준 조성 × water {0,1,2} × T {253,273,293} × seed {1,2,3} = 27 자식 → `dtlab campaign materialize`(8번 S8 전 임시 버전: 이 명세만 처리) → `dtlab run`.
8) app/pages/05_실행대장.py: 상태별 개수, 실행 중 작업 진행률, 실패 분류 · 처방 기록, 재시도 버튼(needs_human 만).
9) tests/test_week05.py: 규칙표 분류(샘플 로그 6종 → 올바른 분류), next_ready 의존성, 템플릿 하드코딩 검사, 축소판 자식 1개 실행.
완료 기준: 27 자식이 done 또는 분류된 failed/needs_human, 대장 요약 표.
```

---

## P06 · 6주차 — 인장 지표 · CED · QC · 지표 페이지

```text
[P06] 공통 머리말 +
6주차(6-1 부착 · 인장 · 6-2 CED · 6-3 δ · 6-4 점도 · 6-5 궤적 분석 자동화) 작업.
1) dtlab/analyze/tension.py:
   - load(stress_disp.dat) → disp(Å), σ(MPa) = −F_grip / A × 6947.7 (units 모듈 사용)
   - metrics(disp, σ): σ_max = curves.peak(창 1 Å 이동평균), d_peak, W_sep(mJ/m²) = ∫σ d(disp) 를 곡선 완주 지점까지 적분한 뒤 단위 환산(MPa·Å → mJ/m²: × 0.1 — LA tensile_metrics.py 식과 대조 테스트), 완주 여부.
   - failure_locus(density_profile_start, _end, groups): 최종 프로파일에서 전체 밀도가 0.05 g/cm³ 미만인 z 구간(공극)을 찾고, 그 구간 아래 · 위의 주 그룹으로 판정 → 'mineral|water' · 'water|binder' · 'mineral|binder'(water 0) · 'cohesive'(바인더 내부).
   - md_tsr(comp_id, T): σ_max(water k) / σ_max(water 0) — 같은 comp_id · T · seed 가 있으면 시드별로, 없으면 평균끼리.
2) dtlab/analyze/bulk.py: S3 bulk_props(밀도 · CED · δ) 를 읽어 특징 표로. 6-2 Method A(compute group/group 분자간 합, 축소판에서만 교육용)와 Method B 비교 노트북 week06/ced_methods.ipynb.
3) 6-4 점도: week06/viscosity/ 에 Green–Kubo 교육 예제(벌크 기준 조성, 축소판) — 앱 데이터셋에는 넣지 않는다고 README 에 명시(CPU 비용).
4) 6-5 궤적 자동화: MDAnalysis 로 dump 를 읽어 z 밀도 프로파일 재계산 → LAMMPS ave/chunk 결과와 일치 검사. OVITO 가 있으면 파괴 직전 · 직후 스냅샷.
5) PROMPTS_STRUCTURE.md 의 S10(구조 품질 게이트) 중 '인장' 항목을 구현하고 결과를 대장에 qc_flag 로 기록.
6) `dtlab analyze runs --tag <T>` → data/results/tension_metrics.csv (열: exp_id, comp_id, substrate, water_level, T, seed, rate, sigma_max_MPa, d_peak_A, wsep_mJm2, locus, complete, qc_flag, bulk_density, ced, delta). 열 이름 · 단위 · 설명을 dtlab/analyze/SCHEMA.md 에 고정(12주차 DB 와 동일).
7) 반복 연구 해석 dtlab/analyze/replicate.py: 조건별 시드 3개 → 변동계수, 두 조건 차이를 판별할 수 있는 최소 효과 크기(양측 α 0.05, 검정력 0.8 근사식, n=1·3 각각). 결과를 week06/replicate_report.md 로.
8) app/pages/06_지표.py: 실행 선택 → 응력–변위 곡선(최대점 · 적분 면적 음영) · 밀도 프로파일(시작/끝) · 파괴 위치 · 지표표 · 반복 연구 산포 그림.
9) tests/test_week06.py: 합성 곡선(사다리꼴)으로 σ_max · W_sep 해석해 대조, 합성 밀도 프로파일로 파괴 위치 판정 4종, 단위 환산.
완료 기준: 27 자식 지표표, 반복 연구 보고서(물층 효과가 시드 산포보다 큰지 첫 판단).
```

---

## P07 · 7주차 — 설계 공간 · 본 캠페인

```text
[P07] 공통 머리말 +
7주차(7-1 SARA 모델 · 7-2 첨가제 라이브러리 · 7-3 다중 힘장 적용 · 7-4 노화 · 점탄성) 작업.
1) PROMPTS_STRUCTURE.md 의 S8(설계 공간 · Sobol 12 조성 · 36 조합 · 부모 108 · 자식 324 + 반복 72, 계산량 추정, materialize · submit · slice)을 수행.
2) week07/sara_mapping.md: 4분자가 SARA 각 분획의 어떤 역할을 대신하는지와 한계(분자량 · 극성 · 상분리 · 점탄성) 표.
3) dtlab/campaign/additives.py: 첨가제 라이브러리(ADD_*) RDKit 기술자(분자량 · TPSA · logP · HBD · HBA · 방향족 원자 비율) 표 → data/results/additives.csv. 11주차 신규 분자가 들어오면 같은 함수로 확장.
4) 기준 데이터셋 적재: data/reference/ 의 강의자 기준 캠페인(tension_metrics.csv + manifest)을 campaign_tag='reference' 로 대장에 등록하는 `dtlab campaign import-reference`. 해시 검사 후 적재, 이미 있으면 건너뜀.
5) 수강생 할당분 실행: `dtlab campaign slice --student <id> --n 12` → `dtlab run --tag student-<id>` → `dtlab analyze runs --tag student-<id>` → 같은 조건의 기준 결과와 비교 표(속도가 다르므로 상대 경향만 비교한다는 경고 포함).
6) 1차 경향 분석 dtlab/analyze/trends.py: 온도별 σ_max · W_sep 상자그림, 물층 효과(MD-TSR 분포), 첨가제별 MD-TSR, 파괴 위치 비율(온도 × 물층) — 반복 연구의 판별 가능 크기 선을 그림에 표시.
7) 7-4 노화 · 점탄성은 강의 내용 유지(앱 데이터셋 밖). 선택 과제: 노화 대용 분자(케톤 · 설폭사이드 도입 변형) 1종을 S1 로 추가해 부분 캠페인 12개.
8) app/pages/07_캠페인.py: 설계 공간 3원 도표(SAT·ARO·RES+ASP), 조합 표, 계층별 진행률(벌크/부모/자식), 1차 경향 그림.
9) tests/test_week07.py: import-reference 해시 검사, slice 태그 분리, trends 함수 입력 스키마.
완료 기준: 대장에 reference 약 400행, 1차 경향 그림 4종.
```

---

## P08 · 8주차 — 시멘트 기판 · ReaxFF · ML 힘장(SNAP)

```text
[P08] 공통 머리말 +
8주차(8-1 클링커 모델 · 8-2 ReaxFF 수화 · 8-3 C-S-H · 8-4 ML 힘장) 작업.
1) PROMPTS_STRUCTURE.md 의 S9(portlandite 기판 · 확장 캠페인 36)를 수행. 벌크 바인더는 기판 x·y 에 맞춰 다시 평형화(S3, 같은 조성 · 다른 lateral_xy → 다른 bulk_id).
2) dtlab/cement/stoichiometry.py: 클링커 4상 수화 반응식(표준 교과서 반응식, 출처 기록) → 생성물 질량 계산기. 8-1 덱의 동적 도구와 같은 입력 · 출력.
3) dtlab/cement/reaxff_demo/ (앱 데이터셋 밖, 교육용): C₃S 슬래브(COD CIF, 표면 절단) + 물 약 1,000원자, pair_style reaxff + fix qeq/reaxff, dt 0.25 fs, NVT 온도 가속 수십 ps(CPU).
   ffield 는 원 논문 인용과 배포 조건 확인 후 내려받기 안내만(저장소에 넣지 않음). 분석: Ca–O_w 배위수 · 이온 용출 시계열.
4) dtlab/cement/snap_demo/ (G4 설치 필요): reaxff_demo 궤적에서 프레임 추출 → FitSNAP 학습 입력(에너지 · 힘) → SNAP 계수 → LAMMPS pair_style snap 으로 같은 계를 돌려 에너지 · 힘 오차(검증 프레임), 속도(ns/day) 비교. CPU 축소판(작은 twojmax).
   한계: 참조 데이터가 ReaxFF 이므로 SNAP 는 ReaxFF 를 흉내 낼 뿐 DFT 정확도를 갖지 않음 — README 에 명시.
5) 기판 비교 분석: 같은 12 조합 × water 3 × 293 K 에서 석영 vs portlandite 의 σ_max · MD-TSR · 파괴 위치 비교 그림.
6) app/pages/04_구조빌더.py 에 기판 선택 추가, app/pages/08_시멘트.py: 화학량론 계산기, 기판 비교 그림, ReaxFF · SNAP 데모 결과(있을 때).
7) tests/test_week08.py: 화학량론 질량 보존, portlandite 전하 합 0, SNAP 데모 입력 파일 생성(학습은 slow 마크).
완료 기준: portlandite 36 자식 지표, 기판 비교 그림.
```

---

## P09 · 9주차 — 특징 · XGBoost · SHAP

```text
[P09] 공통 머리말 +
9주차(9-1 표현자 · feature library · 9-2 XGBoost · 9-3 SHAP) 작업.
1) dtlab/ml/dataset.py: 대장(qc 통과 행만) + tension_metrics.csv → 학습 표. 목표 변수: sigma_max_MPa, wsep_mJm2 (자식 행 단위), md_tsr(comp_id · T · water>0 단위 집계 표). 제외 행과 사유 통계 출력.
2) dtlab/ml/features.py — feature library v1:
   - 분자별 RDKit 기술자(분자량 · TPSA · logP · HBD · HBA · 방향족 원자 비율 · 회전 결합 수 · S · N · O 원자 수) → 조성 질량분율 가중 평균
   - 조성 자체(4분율 + 첨가제 one-hot + 첨가제 wt%)
   - 조건: T, water_level(또는 분자/nm²), substrate one-hot
   - 벌크 특징: bulk_density, ced, delta
   - 메타데이터(features_meta.json): RDKit 버전, 열 목록 · 순서, 생성 해시. 버전이 다르면 학습 거부.
   - 중복 · 상수 열 검사(13주차 특징 재정련의 사전 점검).
3) dtlab/ml/xgb.py: GroupKFold(groups = comp_id, 5-fold, 고정 순서 저장). 표준화는 폴드 안: mu = X[tr].mean(axis=0), sd = X[tr].std(axis=0), 검증 폴드에 같은 mu · sd 적용.
   모델: 선형(Ridge), RF, XGBoost(작은 데이터 권장 범위: max_depth 2~4, learning_rate 0.05, n_estimators 조기 종료, reg_lambda ≥ 1). 폴드 평균 ± 표준편차의 RMSE · MAE · R².
   시드 산포 하한: 반복 연구 · 반복 72개로 추정한 조건 내 표준편차를 '도달 가능한 RMSE 하한' 으로 같이 보고.
   추가 평가: 온도 외삽(293 · 273 학습 → 253 예측) 성능.
4) dtlab/ml/shap_report.py: TreeExplainer SHAP 요약 · 의존 그림(T, water_level, 첨가제 wt%), 물리 점검표(water↑ → σ_max↓, T↓ → σ_max↑ 예상 방향과 부호 일치 여부).
5) 모델 저장: models/xgb/<target>/<hash>/ (모델 · 폴드 · mu/sd · features_meta · 성능표 · manifest).
6) app/pages/09_모델.py: 목표 선택 → 모델별 성능표 · 예측–실측 산점도(폴드 색) · SHAP 요약 · 물리 점검표 · 하한 비교.
7) week09/notebooks/: 트리 분할 SSE, 부스팅 잔차, 무작위 vs 그룹 분할 누수 비교, SHAP 합 = 예측 확인(덱 동적 도구와 같은 실험을 DT-Lab 데이터로).
8) tests/test_week09.py: 폴드 누수 검사(검증 comp_id 가 학습에 없음), 표준화가 폴드 안에서만 계산되는지(모의 데이터), features_meta 버전 거부.
완료 기준: 목표 3개 성능표, SHAP 물리 점검표.
```

---

## P10 · 10주차 — GNN · 불확실성 · 능동학습 1회

```text
[P10] 공통 머리말 +
10주차(10-1 분자 그래프 · 10-2 등변 GNN · Graphormer-3D · 10-3 MD 데이터 학습 · 10-4 불확실성 · 능동학습) 작업. PyTorch CPU.
1) dtlab/ml/graphs.py: 분자별 그래프(노드: 원자 번호 · 혼성 · 방향족 · 형식전하 · H 수, 엣지: 결합 차수 · 공액 · 고리) → 시료 = 분자 그래프 집합 + 질량분율 가중치 + 조건 벡터(T · water · substrate) + 벌크 특징.
2) dtlab/ml/gnn.py:
   - MPNN(3층 GINE 또는 NNConv) → 분자 임베딩 → 조성 가중 풀링 → 조건 벡터 결합 → MLP → 물성.
   - Graphormer3D-lite(4층 · 4헤드, 원자 쌍 거리 가우스 기저 → 어텐션 편향, S1 의 3D 좌표 사용). CPU 에서 1 epoch < 1분 크기.
   - 스칼라 출력은 회전 · 병진 불변(거리만 사용) — 주석으로 불변성(invariance) · 등변성(equivariance) 구분.
3) dtlab/ml/train_gnn.py: P09 와 같은 폴드 파일 재사용, 조기 종료, 학습 곡선 CSV, 체크포인트, config.yaml. 성능을 XGBoost · 선형과 같은 표에.
4) dtlab/ml/uncertainty.py: 시드 5개 앙상블(XGBoost 는 부트스트랩 5개) → 평균 · 표준편차, 보정 곡선(명목 68 · 95 % 대비 실제 포함률), 필요하면 σ 배율 보정(검증 폴드에서 추정).
5) dtlab/ml/active.py: 후보 풀 = 설계 공간 Sobol 1,000점 × 조건(물층 · 온도) 중 미계산 조건 → 획득함수 UCB(κ 명세) · EI → 상위 10 조합 선택(서로 너무 가까운 후보는 조성 거리 임계로 제외) → 각 조합 × T 3 × water 1 = 30 자식 명세(specs/active_round1.yaml) → S8 materialize → 실행기 큐 등록(사람 승인 후).
   라운드 기록: data/active/round1.json (선택 이유: 예측 · σ · 획득값).
6) 재학습 비교: 30개가 끝나면 P09 · P10 모델을 다시 학습해 라운드 전후 RMSE 와 선택 영역 근처 예측 σ 변화 보고.
7) app/pages/10_불확실성.py: 보정 곡선, 후보 풀 산점도(예측 vs σ, 선택점 강조), '라운드 제출' 버튼(승인 체크박스 필수), 라운드 전후 비교.
8) tests/test_week10.py: 그래프 변환(피렌 노드 · 엣지 수), 회전 불변성(좌표 회전 후 출력 동일), 획득함수 단조성, 후보 중복 제거.
완료 기준: GNN · XGB · 선형 비교표, 보정 곡선, 능동학습 1라운드 30 자식 완료 · 재학습 비교.
```

---

## P11 · 11주차 — 문헌 · 검증 기준 · 후보 분자 확장

```text
[P11] 공통 머리말 +
11주차(11-1 검색 전략 · 11-2 Obsidian · 11-3 자동 스크래핑 · 11-4 Zotero) 작업. 문헌 전문(PDF · XML)은 저장소에 넣지 않는다(TDM 약관).
1) dtlab/lit/harvest.py: OpenAlex(pyalex, mailto 설정) · Crossref(habanero) 검색. 검색식 3종(명세 specs/lit_queries.yaml):
   ("asphalt" OR "bitumen") AND ("aggregate" OR "silica" OR "quartz" OR "calcite") AND ("molecular dynamics") AND ("moisture" OR "water")
   ("anti-stripping" OR "adhesion promoter" OR "amine additive") AND ("asphalt" OR "bitumen")
   ("asphalt" OR "bitumen") AND ("molecular dynamics") AND ("tension" OR "pull-off" OR "separation" OR "debonding")
   기간 최근 10년, 각 최대 200건. 로그: 검색식 · 실행 시각 · 결과 수 · API 응답 해시.
2) dtlab/lit/dedupe.py: DOI 정규화(https://doi.org/ · doi: 접두 · 대소문자 · 공백 제거) + 제목 정규화 유사도(rapidfuzz ≥ 95) → 선별 흐름도 건수(수집 → 중복 제거 → 초록 선별 → 추출 대상).
3) dtlab/lit/extract.py: 초록 → JSON 스키마(binder_model · additive · mineral · water_condition · force_field · pull_rate · temperature · reported_quantity · value · unit · trend_statement).
   LLM 은 교체 가능한 인터페이스(Extractor 프로토콜): AnthropicExtractor(선택, API 키 환경변수) · MockExtractor(고정 응답, 오프라인 · CI 용). 30건 사람 채점 시트(CSV) 생성 → 필드별 정확도 → 정확도 < 0.8 필드는 자동 추출 대상에서 제외.
4) dtlab/lit/benchmarks.py → data/lit/validation_table.csv: 문헌 경향 · 범위 기준표(물 → 부착 감소, 알칼리성 광물 > 산성 광물, 온도 효과, 첨가제 효과). 각 행에 DOI · 원문 위치(표/그림 번호) · 추출 방식(사람/LLM) · 비교 가능 조건. 13주차 검증에서 사용.
5) dtlab/lit/candidates.py: 추출된 첨가제명 → PubChem(pubchempy) SMILES · CID → 실패 목록 분리 → library/molecules.yaml 후보 구역(status: candidate)에 추가. 사람이 status: active 로 바꾼 분자만 S1 파라미터화 대상.
   최소 2종을 active 로 올려 S1 을 다시 돌리고(dtlab ff build-library --only <id>) P07 additives 표를 갱신.
6) week11/vault_template/: 폴더(00_Inbox · 10_Papers · 20_Concepts · 30_Claims · 90_Templates), 논문 노트 템플릿(citekey · DOI · 모델 · 힘장 · 물 조건 · 결과 · DT-Lab 관련 링크), Dataview 질의 예시. harvest 결과에서 논문 노트 초안을 만드는 `dtlab lit notes`.
   week11/zotero.md: Better BibTeX 인용키 · Keep updated 내보내기 · Obsidian Zotero Integration 설정 안내.
7) app/pages/11_문헌.py: 흐름도 건수, 기준표(필터), 후보 분자(상태 · 출처 DOI · SMILES 구조 이미지).
8) tests/test_week11.py: DOI 정규화 케이스 8개, 중복 제거, MockExtractor 스키마 검증, candidates 상태 전이.
완료 기준: 기준표 1개(10행 이상), 신규 첨가제 2종 파라미터화 완료.
```

---

## P12 · 12주차 — 정식 DB · 품질 게이트 · 폴드 · 자동 루프

```text
[P12] 공통 머리말 +
12주차(12-1 파이프라인 구조 · 12-2 후보 생성 · 12-3 데이터 큐레이션 · 12-4 이상치 · 재현성) 작업.
1) dtlab/db/schema_sqlite.sql (+ schema_postgres.sql 같은 설계):
   composition(comp_id PK, fractions_json, additive_id, additive_wt, created) — CHECK: 분율 합 100 ± 0.01, additive_wt 0~10
   run(exp_id PK, comp_id FK, kind, parent_id, substrate, water_level, temperature_K, seed, pull_rate_Aps, campaign_tag, status, qc_flag, manifest_sha, lmp_version, wall_s) — CHECK: temperature_K IN (…명세), water_level IN (0,1,2)
   property(exp_id FK, name, value, unit, method, PRIMARY KEY(exp_id, name)) — 긴 형식(long format), name · unit 은 등록 사전 property_dict 에 있는 것만(외래 키)
   property_dict(name PK, unit, description)
2) dtlab/db/migrate.py: runs.sqlite + tension_metrics.csv + bulk_props → dtlab.sqlite. fail-closed 적재 계약: 미등록 물성 이름 · 다른 단위 · 제약 위반 행은 거부하고 거부 사유 표(data/db/rejects.csv).
   `dtlab db migrate --backend sqlite|postgres` (postgres 는 선택, 접속 정보 환경변수).
3) dtlab/db/qc.py: S10 게이트 결과 + 통계 이상치(조건 내 로버스트 z > 4) → qc_flag. 학습 뷰 v_train(qc 통과 · status done) 생성. 제외 사유 통계.
4) dtlab/db/splits.py: comp_id GroupKFold 5-fold 인덱스와 폴드별 mu · sd 를 테이블 split(fold, comp_id, role) · scaler(fold, feature, mu, sd) 로 저장. P09 · P10 은 이 테이블을 읽도록 수정(기존 파일 경로 방식은 호환 유지).
5) 12-2 후보 생성: dtlab/campaign/candidates.py — 라이브러리 active 분자 + 생성 규칙(첨가제 wt% 격자, 4분율 Sobol) → 후보 풀 테이블 candidate(cand_id, spec_json, source: sobol|rule|literature). P10 active 와 P13 opt 가 이 풀을 사용.
6) dtlab/db/loop.py — `dtlab loop --rounds 1 --acq ucb --n 10`:
   ① v_train 으로 앙상블 재학습 ② 후보 풀 평가 · 선택 ③ 사람 승인 게이트(CLI 확인 또는 앱 버튼, 승인 기록) ④ S8 materialize ⑤ 실행기 ⑥ analyze ⑦ migrate · qc ⑧ 재학습 · 전후 비교.
   각 단계 결과를 loop_log 테이블에, 전체를 run_manifest.json(코드 git 해시 · DB 스냅샷 해시 · 모델 해시 · 명세 해시)로 고정.
7) 재현성 점검 `dtlab repro check <run_manifest>`: 같은 manifest 로 학습을 다시 해 성능이 같은지(결정론 설정: 스레드 · 시드), 입력 해시가 같은지.
8) app/pages/12_DB_QC.py: 테이블 행 수, 거부 · 제외 사유, 물성 분포(qc 전후), 루프 이력 · 승인 기록.
9) tests/test_week12.py: 제약 위반 삽입이 거부되는지(분율 합 · 미등록 물성 · 온도), migrate 멱등, split 누수 없음, loop 단계 모의 실행(실행기 mock).
완료 기준: dtlab.sqlite 에서 P09 성능표가 같은 값으로 재현, loop 1회 완주(능동학습 2라운드에 해당).
```

---

## P13 · 13주차 — 다목적 역설계 · 에이전트 · 검증 · 앱 완성

```text
[P13] 공통 머리말 +
13주차(13-1 다목적 최적화 · 13-2 LLM 에이전트 · 13-3 특징 재정련 · 13-4 통합 사례 · 13-5 실험 검증과 재현성) 작업.
1) dtlab/opt/problem.py — 명세 specs/opt_main.yaml:
   목적 f1 = W_sep(253 K, water 0) 최대(저온 부착), f2 = MD-TSR(293 K, water 2) 최대(수분 저항)
   제약: 첨가제 wt% ≤ 4, 예측 bulk_density 가 기준 조성 ± 5 % 안, 학습 분포 안(LOF 점수 임계 — 사용성 게이트), 4분율 설계 공간 제약.
   설계 변수: 4분율(단체 → 3차원 로그비 변환으로 연속화) + 첨가제 범주(범주별로 따로 최적화 후 합침) + wt%.
2) dtlab/opt/moo.py: 대리모델(P10 앙상블, 두 목적 각각) → BoTorch qEHVI(CPU), 참조점 = 현재 데이터 두 목적의 하위 10 % 값(근거 주석), 배치 3, 라운드 수 명세.
   출력: 파레토 전선(관측 · 예측), 라운드별 HV 곡선, 추천 표(조성 · 예측 ± σ · 제약 충족 · LOF).
3) dtlab/opt/agent.py (선택): Proposer(LLM 또는 규칙) → Critic(LLM 또는 규칙) → 결정론적 점수(EHVI 값 · 제약 · LOF) → 사람 승인. LLM 은 P11 과 같은 교체 가능 인터페이스, MockAgent 로 오프라인 동작.
   README: 운영 플랫폼이 토론형 다중 에이전트 대신 함수 호출 + 결정론적 점수로 바꾼 이유(LA 문서 참고)와, 여기서도 최종 결정은 점수 · 사람 승인으로 한다는 원칙.
4) dtlab/opt/refine.py (13-3): 특징 재정련 — 상관 |r| > 0.95 쌍, 조성 그룹 안에서 상수인 열, 다른 열의 선형 결합인 열을 찾아 제거 후보 → 제거 전후 GroupKFold 성능 비교 → features v2 (features_meta 버전 올림).
5) 검증(13-5): 추천 상위 3조성 × T 3 × water {0, 2} = 18 자식 → S8 materialize → 실행 → analyze → 예측 구간(95 %) 포함 여부 표, MD-TSR 개선이 반복 연구의 판별 가능 크기보다 큰지 판정.
   문헌 대조: P11 validation_table 의 경향 행과 방향이 같은지 점검표(예: 물층 → σ_max 감소, 아민계 첨가제 → MD-TSR 증가 여부는 '검증 대상'으로 기록, 결과를 그대로 보고).
6) 통합 사례(13-4): week13/case_study.ipynb — 목표 입력부터 추천 · 검증 · 한계까지 한 흐름. 시멘트 기판(portlandite) 조건으로 같은 문제를 푼 결과를 부록으로.
7) 앱 완성:
   app/pages/13_역설계.py: 목표 · 제약 입력 → 최적화 실행(백그라운드, 진행 표시) → 파레토 그림 · 추천 표 → '검증 실행 제출'(승인 필수) → 검증 결과 대조.
   app/Home.py 파이프라인 지도 전 단계 초록, 각 단계에서 해당 페이지로 이동하는 링크.
   `dtlab demo --quick`: 기준 데이터셋만으로 학습 → 역설계 → (검증은 기존 결과 사용) 5분 안에 끝나는 시연 경로.
8) 최종 보고서 템플릿 week13/final_report.md: 데이터셋 요약(조건 · 행 수 · 제외 사유), 모델 성능과 하한, 역설계 결과, 검증, 한계(단순 분자 · 인장 속도 · 작은 셀 · 결정 고정 · 데이터 수).
9) tests/test_week13.py: 제약 함수(경계값), 참조점 계산, refine 가 합성 중복 열을 찾는지, demo --quick 이 기준 표본 데이터(data/samples)로 끝까지 도는지.
완료 기준: 추천 표 · 파레토 · HV 곡선, 검증 18 자식 결과, `dtlab demo --quick` 5분 이내 완주, 앱 전 페이지 연결.
```

---

## 부록 · 프롬프트 사용 시 점검표
- [ ] 앞 주차 완료 기준 통과
- [ ] 이번 주 설치 그룹 확인(`dtlab check-env --week NN`)
- [ ] 새 모듈이 앞 모듈을 import하는지(코드 복사 없음)
- [ ] 명세 · 결과 열 이름이 `dtlab/analyze/SCHEMA.md` · DB 스키마와 일치
- [ ] 실행 대장 · DB에 캠페인 태그 구분(reference · student · active · validation)
- [ ] 앱 새 페이지가 데이터 없이도 열리는지
- [ ] `weekNN/README.md` 결과물 체크리스트가 덱 실습 안내와 일치(덱 수정 전이면 차이를 README에 기록)
