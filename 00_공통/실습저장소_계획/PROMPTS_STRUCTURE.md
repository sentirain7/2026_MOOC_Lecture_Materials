# 데이터 생성용 구조 생성 프롬프트 (S0 ~ S10)

DT-Lab 데이터셋(온도별 약 100개 직접인장)을 만드는 데 필요한 구조를 처음부터 끝까지 생성하는 프롬프트 모음이다. 분자에서 출발해 벌크, 광물 슬래브, 물층, 3층 셀, 인장 실행 패키지, 캠페인 계층까지 만든다. 앱 모듈 구현 프롬프트(`PROMPTS_APP.md`)와 함께 쓰며, 여기서 만드는 코드는 `dtlab/ff`, `dtlab/build`, `dtlab/gen`, `dtlab/campaign`에 들어간다.

- 계획: `INTEGRATED_APP_PLAN.md` §2 · §3
- 설치 기준: `INSTALL_GUIDE.md` (운영체제 · 고정 버전 · Packmol · Windows 주의)
- 힘장 기준: `FF_COMPATIBILITY.md` (권장 조합 · 타입 접두어 · 검증 사다리 V1~V9)
- 작성일: 2026-09-22

## 사용법
1. Claude Code에서 저장소 루트를 연다.
2. **공통 머리말**과 해당 S 프롬프트를 이어 붙여 넣는다.
3. 실행 순서: S0 → S0-P → S0-V(V1 제외) → S1 → S2 → S4 → S3 → S5 → S6 → S7 → S8. S3는 S4 슬래브의 x · y 길이를 입력으로 받으므로 S4가 먼저다. S9(시멘트 기판)와 S10(구조 품질 게이트)은 S6 뒤 어느 때나 가능하다.
4. 각 프롬프트의 **완료 기준**이 통과해야 다음으로 넘어간다.

```
S0 설치 ─ S0-P Packmol ─ S0-V 자체검사 ─┬─ S1 분자 파라미터 ──────────────┐
         └─ S2 물 · 광물 템플릿 ─ S4 석영 슬래브 ─┴─ S3 벌크 바인더(슬래브 x·y 사용) ─┐
                                   └─ S5 물층 ──────────────────────────┴─ S6 3층 조립 ─ S7 인장 패키지 ─ S8 캠페인 계층
S9 portlandite 기판 (S4 대체 · S3 재평형화) · S10 품질 게이트 (S3~S7 검사) 는 S6 이후 언제든
```

---

## 공통 머리말 (모든 S 프롬프트 앞에 붙임)

```text
[DT-Lab 공통 머리말 · 구조 생성]
너는 교육용 통합 앱 DT-Lab(패키지 dtlab)의 구조 생성 모듈을 만드는 개발자다.
목표: 단순 분자 바인더 | 물층 | α-석영(001) 3층 셀을 만들고 CPU LAMMPS로 직접인장 데이터를 대량 생성하는 것.
규칙
- LAMMPS는 CPU 전용(MPI + OpenMP). GPU · KOKKOS 금지. units real, atom_style full.
- 파이썬 3.11, 전용 conda 가상환경 dtlab 에만 설치(S0). 의존성은 install/groups.yaml 과 environment.yml 에 추가. 모든 실행은 bin/dtlab 래퍼 또는 source env/activate.sh 뒤에 한다.
- 모든 생성 함수는 (입력 명세 dict/pydantic 모델, seed) → 출력 폴더. 같은 입력 + 같은 seed → 바이트 단위로 같은 결과(정렬 · 부동소수 형식 고정).
- 출력 폴더마다 manifest.json: 입력 명세, 입력 파일 SHA-256, 도구 버전(RDKit · AmberTools · Packmol · LAMMPS), seed, 생성 시각, 부모 산출물 ID.
- 산출물 ID = 입력 명세 정규화 JSON 의 SHA-256 앞 12자리. 이미 있으면 다시 만들지 않는다(멱등).
- 실패는 fail-closed: 파라미터 누락 · 전하 불일치 · 원자 겹침 · 타입 충돌은 예외로 중단하고 이유를 manifest 의 error 에 기록. 근사값으로 우회하지 않는다.
- 힘장 조합은 FF_COMPATIBILITY.md §1 (GAFF2 · AM1-BCC / SPC/E / ClayFF, 단일 lj/cut/coul/long, mix arithmetic)을 따른다. 바꾸려면 §2 비교표 근거와 V1~V7 재검증이 필요.
- 타입 이름은 힘장 접두어를 붙인다: g2_(GAFF2) · sw_(SPC/E) · cf_(ClayFF). 접두어가 다른 타입은 절대 병합하지 않는다(GAFF2 와 ClayFF 모두 oh · ho 이름을 씀).
- 지원 플랫폼: Linux · macOS(arm64 · x86-64) · Windows 는 WSL2 Ubuntu 안에서만. 셸 스크립트는 bash, 줄끝 LF, 경로 공백 · 한글 금지 검사.
- 생성되는 모든 README · 설치 문서는 한국어로 '실행 순서(번호 목록) · 명령 · 예상 시간 · 성공 판정 · 실패 시 조치' 를 포함한다.
- 힘장 수치는 지어내지 말 것. 출처(논문 · 파일 · 버전)를 코드 주석과 ff/SOURCES.md 에 기록. 프롬프트에 적힌 수치는 '검증 대상 기대값'이며 원 출처와 대조하는 테스트를 둔다.
- 참고 코드(읽기 전용, 복사 금지, 교육용으로 단순화해 새로 작성): /home/tyun/mounted_directory/sdd/Claude_Code/LAMMPS_Asphalt (LA). *.db 파일은 열지 않는다.
- CLI 는 cli.py 의 `dtlab <그룹> <명령>` 으로 노출, --help 필수. 각 명령은 --dry-run 지원.
- 테스트: tests/ 에 pytest. CPU 에서 5분 이내 축소판. LAMMPS 가 없으면 해당 테스트는 skip 이 아니라 '설치 필요' 로 실패.
- README · 주석은 한국어, 식별자는 영어. 전문 용어는 처음 나올 때 영어 병기.
```

---

## S0 · 종속성 설치 그룹

```text
[S0] 공통 머리말 +
install/ 에 가상환경 생성 · 설치 그룹 스크립트 · 자동 활성화 래퍼 · 점검 명령을 만들어라. 주차와 맞추면 좋지만 필수는 아니다. 그룹 단위로 언제든 설치할 수 있어야 한다.

0) 가상환경 (모든 설치 · 실행의 전제)
   - 전용 conda 환경 이름 dtlab (명세 env/env.yaml 의 name 으로 변경 가능). LAMMPS · Packmol · AmberTools 가 conda-forge 바이너리이므로 pip venv 만으로는 부족 — conda(mamba) 환경을 쓴다. 관리자 권한이 없거나 conda 가 없으면 micromamba 를 사용자 폴더에 자동 설치.
   - 프로필: --profile laptop(기본, MPI 없음 · OpenMP 만) | workstation(openmpi). 선택을 env/profile 에 기록, 실행기 · run.sh 가 읽는다.
   - 플랫폼 검사: uname 으로 Linux · Darwin 확인, WSL2 면 /proc/version 의 microsoft 표시 확인 후 (1) 저장소가 /mnt/ 아래면 중단하고 ~/ 로 옮기라고 안내 (2) git core.autocrlf 가 true 면 경고. Windows 네이티브(MSYS · Cygwin · Git Bash) 감지 시 WSL2 설치 안내 후 종료. macOS 는 uname -m 과 conda 플랫폼(osx-arm64 · osx-64) 일치 검사(Rosetta 혼용 방지).
   - install/create_env.sh: (a) mamba/conda/micromamba 탐지(없으면 micromamba 설치 여부를 묻고 설치) (b) `mamba create -n dtlab -c conda-forge python=3.11` — 이미 있으면 건너뜀 (c) 환경 안에 `pip install -e .` (d) env/activate.sh 생성.
   - env/activate.sh: 환경 활성화(conda · micromamba 둘 다 지원: shell hook 후 activate), 그리고 DTLAB_HOME · DTLAB_LMP · OMP_NUM_THREADS(기본 1, 실행기가 작업별로 덮어씀) · PYTHONNOUSERSITE=1(사용자 site-packages 차단) 설정. 스크립트는 source 로만 쓰며 직접 실행하면 사용법 안내 후 종료.
   - 모든 install/*.sh 는 첫 줄에서 env/activate.sh 를 source 하고, 활성 환경이 dtlab 이 아니면 설치를 거부한다(기본 base 환경 오염 방지). 설치 대상은 항상 `mamba install -n dtlab` · 환경 안의 pip.
   - 실행 진입점 bin/dtlab (셸 래퍼): env/activate.sh 를 source 한 뒤 `python -m dtlab.cli "$@"` 실행. 사용자가 환경을 활성화하지 않아도 항상 dtlab 환경에서 돈다. 앱은 bin/dtlab-app(= activate 후 `streamlit run app/Home.py`).
   - LAMMPS 실행 패키지의 run.sh(S7), 실행기(runner)가 띄우는 모든 하위 프로세스, 노트북 커널도 같은 환경을 쓴다: run.sh 첫 줄에서 env/activate.sh 를 source, 노트북은 `python -m ipykernel install --user --name dtlab --display-name "DT-Lab (dtlab)"` 로 커널 등록.
   - dtlab.core.env.assert_env(): 파이썬 코드 진입 시 sys.prefix 가 dtlab 환경인지 검사, 아니면 'bin/dtlab 또는 source env/activate.sh 로 실행하라' 는 메시지와 함께 종료(테스트 · CI 는 환경변수 DTLAB_ALLOW_FOREIGN_ENV=1 로만 우회).
   - 선택: .envrc(direnv) 에 `source env/activate.sh` — 저장소 폴더에 들어가면 자동 활성화.
   - 환경 재현: install/export_env.sh → env/environment.lock.yml(`conda env export --no-builds`) + env/explicit-linux-64.txt(`conda list --explicit`). install/create_env.sh --from-lock 로 같은 환경 재생성.
   - 제거 · 초기화: install/remove_env.sh (확인 질문 후 `conda env remove -n dtlab`).

1) 그룹 정의 (install/groups.yaml) — 각 그룹: 이름, 설명, 권장 시점(차시 코드), conda 패키지, pip 패키지, 소스 빌드 스크립트, 확인 명령
   G0 기본: python=3.11 numpy pandas scipy matplotlib pyyaml jinja2 pydantic psutil pytest streamlit rich typer   (권장 1-4)
   G1 MD 도구 (고정 버전, INSTALL_GUIDE §1.2 — 2026-09-22 확인값):
        lammps=2025.07.22 (빌드 문자열 고정: laptop 프로필 "cpu_py311*nompi*", workstation 프로필 "cpu_py311*mpi_openmpi*" + openmpi — CUDA 빌드 cuda129_* 설치 금지)
        packmol=21.2.1  ambertools=26.0  rdkit=2026.03.*  openmm=8.6.*  parmed=4.3.1  ase  mdanalysis=2.10.*
        (권장 2-1 · 3-2 · 4-4)
        + 소스 빌드: install/build_lammps.sh (권장 4-1)
   G2 분석 · 시각화: ovito(pip) nglview(선택)   (권장 6-5)
   G3 ML: scikit-learn xgboost shap pytorch(cpuonly) pytorch_geometric botorch gpytorch   (권장 9-1 · 10-1 · 10-4)
   G4 ML 힘장: LAMMPS ML-SNAP 재빌드 + fitsnap3 mpi4py   (권장 8-4)
   G5 문헌 · DB: pyalex habanero rapidfuzz pubchempy sqlalchemy psycopg(선택) anthropic(선택)   (권장 11-1 · 12-3)
   데스크톱 앱(스크립트 설치 안 함, 안내만): Obsidian + Dataview, Zotero + Better BibTeX
2) install/install.sh <그룹...> : dtlab 환경을 활성화한 뒤 mamba 로 그 환경에만 설치, 이미 설치된 것은 건너뜀. 끝나면 env/versions.lock 갱신(패키지 = 버전).
   install/all.sh : G0~G5 전체.
3) install/build_lammps.sh (선택 — conda 판에 필요한 패키지가 모두 있으므로 강의 4-1 실습용): 태그 stable_22Jul2025_update6 고정(--tag 로 변경 가능) 소스를 받아 CPU 빌드. -march=native 등 CPU 종속 최적화 옵션 금지(다른 컴퓨터 복사 시 Illegal instruction).
   cmake 옵션: -D BUILD_MPI=on -D BUILD_OMP=on -D LAMMPS_EXCEPTIONS=on -D FFT=FFTW3
   패키지: MOLECULE KSPACE RIGID EXTRA-MOLECULE EXTRA-FIX EXTRA-DUMP MISC MANYBODY OPENMP REAXFF (+ --with-ml 이면 ML-SNAP)
   dtlab 환경을 활성화한 상태에서 빌드하고(컴파일러 · OpenMPI · FFTW 도 conda-forge 로 같은 환경에 설치), 설치 경로 $CONDA_PREFIX/bin/lmp_dtlab. 빌드 후 `lmp_dtlab -h` 의 Installed packages 를 파싱해 요구 패키지가 모두 있는지 검사, 없으면 실패.
   git 태그 · 커밋 해시를 env/versions.lock 에 기록.
4) dtlab/core/env.py + `dtlab check-env [--group G1] [--week N]`
   - 파이썬 패키지 import · 버전, 실행 파일(lmp 또는 lmp_dtlab, packmol, antechamber, parmchk2, sqm, tleap) 존재 · 버전
   - LAMMPS 패키지 목록 대조(요구: MOLECULE KSPACE RIGID EXTRA-MOLECULE EXTRA-FIX EXTRA-DUMP MISC MANYBODY OPENMP REAXFF, G4 이면 ML-SNAP), 빌드 문자열에 cuda 가 있으면 실패, OpenMP 스레드 수 확인(OMP_NUM_THREADS 미설정이면 경고: LA 교훈 28)
   - 결과 표: 항목 · 상태(설치됨/없음/버전 낮음) · 권장 그룹 · 권장 시점. --week N 이면 N주차까지 권장된 항목만 필수로 판정.
   - 사용할 lmp 실행 파일 우선순위: 환경변수 DTLAB_LMP > lmp_dtlab > lmp. 선택 결과를 출력.
   - 첫 줄에 활성 환경 이름 · 경로 · 파이썬 경로를 표시하고, 실행 파일이 dtlab 환경 밖(예: /usr/bin/packmol)에서 잡히면 '환경 밖 도구' 경고.
5) 테스트: tests/test_env.py — groups.yaml 스키마 검사, check-env 가 오류 없이 표를 만든다(없는 도구는 '없음' 으로 표시), assert_env 가 다른 환경에서 종료하는지, activate.sh 가 source 없이 실행되면 안내 후 종료하는지.
완료 기준: 새 컴퓨터에서 `bash install/create_env.sh && bash install/install.sh G0 G1` 후, 환경을 활성화하지 않은 새 터미널에서 `bin/dtlab check-env --group G1` 이 dtlab 환경으로 실행되어 모두 설치됨. build_lammps.sh 가 요구 패키지 검사를 통과. 기본(base) 환경에는 아무것도 설치되지 않음.
```

---

## S0-P · Packmol 설치 · 판정 래퍼 (매우 주의)

```text
[S0-P] 공통 머리말 +
Packmol 은 Fortran 프로그램이라 컴파일된 실행 파일이 있어야 한다. install/build_packmol.sh 와 dtlab/build/packmol.py 를 만들어라. INSTALL_GUIDE.md §6 이 기준 문서다.
1) 설치 경로 두 가지(우선순위 순)
   (a) 기본: conda-forge packmol=21.2.1 을 dtlab 환경에 설치(G1). 컴파일 불필요.
   (b) 선택: install/build_packmol.sh --tag v21.2.3 — 다음 순서를 정확히 따른다.
       source env/activate.sh (dtlab 아니면 중단)
       mamba install -n dtlab -c conda-forge fortran-compiler cmake make   # 컴파일러도 가상환경 안에, $FC 사용
       git clone https://github.com/m3g/packmol.git build/packmol-src && git -C build/packmol-src checkout v21.2.3
       cmake -S build/packmol-src -B build/packmol-obj -DCMAKE_BUILD_TYPE=Release -DCMAKE_Fortran_COMPILER="$FC" -DCMAKE_INSTALL_PREFIX="$CONDA_PREFIX"
       cmake --build build/packmol-obj -j 4 && cmake --install build/packmol-obj
       금지: 저장소 Makefile(make) 경로 — 컴파일러가 /usr/bin/gfortran 으로 고정되어 있고 -march=native 가 들어 있어 이식성이 없다.
       금지: 시스템 gfortran · Homebrew gfortran 사용.
       빌드 로그를 build/packmol-build.log 로 저장, 실패 시 마지막 40줄과 조치 안내 출력.
   설치 후: `command -v packmol` 이 $CONDA_PREFIX/bin/packmol 인지 검사(/usr/bin/packmol 등 환경 밖 판이 잡히면 실패). 머리말의 Version 줄을 파싱해 env/versions.lock 에 (버전, 경로, 설치 방식 conda|source) 기록.
2) 판정 래퍼 dtlab/build/packmol.py: run_packmol(inp_text, workdir, expected_atoms, seed, retries=2) → PackResult
   - workdir 로 이동해 실행(구조 파일은 절대 경로로 기록), stdin 으로 입력 전달, 표준출력 전체를 packmol.log 로 저장, 시간 제한(명세, 기본 600 s).
   - 성공 판정 = 네 조건 모두: 종료 코드 0 · 로그에 'Success!' · 'Maximum violation of target distance' 값 < 0.01 · 출력 원자 수 = expected_atoms.
   - 실측 동작(2026-09-22, v21.2.3): 성공 0 / 충전 실패 173(출력 파일이 그래도 생성되고 <output>_FORCED 도 생김) / 파일 없음 172. 따라서 '출력 파일 존재' 로 성공을 판단하는 코드를 금지하고, 실패 시 출력 파일 · _FORCED 를 *.failed 로 이름을 바꿔 격리.
   - 실패 시 seed+1 로 retries 회 재시도, 이후 PackmolError(원인: 종료 코드 · 최대 위반값 · 조치: 초기 밀도 낮추기 · 상자 키우기 · tolerance 확인).
   - 입력 생성 규칙: seed 항상 명시(−1 금지), tolerance 2.0 기본, filetype pdb, 경로 공백 금지 검사, 벌크는 pbc 키워드(21.x 지원 확인됨), 슬래브 위 물층은 inside box + 가장자리 1 Å 여유.
3) 테스트 tests/test_packmol.py: (a) 물 1,000개 상자 성공 (b) 작은 상자에 물 2,000개(nloop 20) → 173 과 _FORCED 를 실패로 판정하고 격리하는지 (c) 없는 구조 파일 → 172 (d) 같은 seed 두 번 → 같은 좌표.
완료 기준: 네 테스트 통과, env/versions.lock 에 Packmol 경로 · 버전 · 설치 방식.
```

---

## S0-V · 설치 직후 자체 검사 (selftest)

```text
[S0-V] 공통 머리말 +
`bin/dtlab selftest md` 와 `bin/dtlab selftest ff --level V1..V9` 를 만들어라. 기준: INSTALL_GUIDE.md §5.2, FF_COMPATIBILITY.md §6.
1) selftest md (설치 직후, S1 이전에 실행 가능): Packmol 성공 · 실패 판정(S0-P 테스트 재사용), LAMMPS LJ 1,000스텝(1코어), SPC/E 물 216개 NVT 1 ps(PPPM · SHAKE — 데이터 파일은 dtlab 이 생성), antechamber AM1-BCC 메탄올 전하 합 0. 결과 env/selftest.json(플랫폼 · 프로필 · 버전 · 각 항목 시간).
2) selftest ff: V1~V9 를 FF_COMPATIBILITY §6 표 그대로 구현. 앞 단계 실패 시 중단. 문헌 기대값(SPC/E 밀도, 1,7-다이메틸나프탈렌 액체 밀도)은 specs/reference_values.yaml 에 출처와 함께 두고 코드에 넣지 않는다. V1 은 S1 이후, V3~V7 은 S4~S7 이후에 실행 가능하다는 의존성을 명령이 스스로 확인.
3) laptop 프로필 기준 V1~V7 합계 15분 이내가 되도록 축소판 크기를 정하고 README 에 표로.
4) 결과 요약을 한국어 표로 출력(단계 · 판정 · 측정값 · 기준 · 실패 시 조치).
완료 기준: 이 컴퓨터(Linux)에서 selftest md 통과. macOS · WSL2 결과는 강의자가 data/reference/selftest/ 에 추가.
```

---

## S1 · 분자 라이브러리와 GAFF2 파라미터

```text
[S1] 공통 머리말 +
dtlab/ff/molecules.py, dtlab/ff/gaff.py, dtlab/ff/lammps_writer.py 와 library/ 폴더를 만들어라.
목표: SMILES 목록 → 분자별 GAFF2 · AM1-BCC 파라미터 → LAMMPS 로 옮길 수 있는 검증된 분자 템플릿.

1) library/molecules.yaml (초기 7종 + 물은 S2):
   BIN_SAT  n-docosane            CCCCCCCCCCCCCCCCCCCCCC        role: saturate
   BIN_ARO  1,7-dimethylnaphthalene Cc1ccc2cccc(C)c2c1          role: aromatic
   BIN_RES  dibenzothiophene       c1ccc2c(c1)sc1ccccc12         role: resin
   BIN_ASP  pyrene                 c1cc2ccc3cccc4ccc(c1)c2c34    role: asphaltene_core
   ADD_AMN  octadecylamine         CCCCCCCCCCCCCCCCCCN           role: additive_amine
   ADD_FAC  stearic acid           CCCCCCCCCCCCCCCCCC(=O)O       role: additive_acid
   ADD_PHN  4-nonylphenol          CCCCCCCCCc1ccc(O)cc1          role: additive_phenol
   각 항목: id(7자 이내), name, smiles, role, resname(3자, 분자별 고유), source(PubChem CID 기록 칸)
   기대값 테스트(RDKit): 화학식 · 분자량 · H 포함 원자 수 = C22H46 310.61 68 / C12H12 156.23 24 / C12H8S 184.26 21 / C16H10 202.26 26 / C18H39N 269.52 58 / C18H36O2 284.48 56 / C15H24O 220.36 40
   카복실산 · 아민은 중성형으로 둔다(순전하 0). 이온화 상태는 한계로 README 에 기록.
2) 3D 구조: RDKit AddHs → ETKDGv3(randomSeed = seed) 배좌 10개 → MMFF94 최적화 → 최저 에너지 배좌 선택 → mol2(원자 이름 고유, resname 적용).
3) 파라미터화(AmberTools, CPU):
   antechamber -i x.mol2 -fi mol2 -o x_gaff2.mol2 -fo mol2 -c bcc -at gaff2 -nc 0 -rn <RES>
   parmchk2 -i x_gaff2.mol2 -f mol2 -o x.frcmod -s gaff2
   tleap: source leaprc.gaff2 → loadamberparams x.frcmod → loadmol2 → saveamberparm x.prmtop x.inpcrd
   - frcmod 에 'ATTN, need revision' 이 있으면 실패(fail-closed).
   - sqm 로그에서 수렴 실패 · 전하 합 |Σq| > 1e-4 이면 실패. 전하는 소수 6자리로 반올림 후 합이 정확히 0 이 되도록 가장 큰 |q| 원자에서 잔차 보정, 보정량을 manifest 에 기록.
4) 표준 템플릿 JSON(library/molecules/<id>/template.json): ParmEd 로 prmtop 을 읽어
   atoms[name, gaff_type, charge, mass, element, xyz], bonds[i,j,type_key], angles, dihedrals(항별 k·n·δ 목록), impropers, lj[gaff_type → ε, σ].
   변환 규칙: σ = 2·(Rmin/2)/2^(1/6). 결합 · 각 K 는 Amber 형식 그대로(LAMMPS harmonic 와 같은 형식, 1/2 인자 없음).
   이면각: LAMMPS dihedral_style fourier(여러 항), 부정각: improper_style cvff(δ=0 → d=+1, δ=180 → d=−1).
   1-4 스케일: special_bonds amber (lj 0 0 0.5, coul 0 0 0.8333333).
5) 에너지 일치 검증(tests/test_gaff_energy.py): 분자 1개를 (a) OpenMM(ParmEd 로 변환, 진공, NoCutoff) (b) LAMMPS(큰 상자, lj/cut/coul/cut 50, 템플릿 → data 로 변환)에서 계산한 결합 · 각 · 이면각 · 부정각 · 비결합 에너지가 항별 상대오차 1e-3 이내.
   이 검증이 lammps_writer 의 정답 기준이다.
6) 전역 타입 병합 규칙(dtlab/ff/typing.py): 모든 GAFF2 타입에 접두어 g2_ 를 붙인다(예: g2_ca, g2_oh, g2_ho — ClayFF oh · ho 와 충돌 방지). 여러 분자의 GAFF 타입을 합칠 때 같은 타입 이름 = 같은 LJ, 같은 결합 키(정렬한 타입 쌍) = 같은 파라미터. 다르면 실패. 결과 = 전역 타입 표(ff/gaff_types.json).
7) CLI: `dtlab ff build-library [--only BIN_SAT]`, `dtlab ff show BIN_ARO`
완료 기준: 7종 모두 template.json · manifest 생성, 에너지 일치 테스트 통과, 전역 타입 병합 충돌 0.
참고: LA/src/forcefield, LA/docs/architecture/ff-standard-reference-20260906.md
```

---

## S2 · 물(SPC/E)과 광물(ClayFF) 템플릿

```text
[S2] 공통 머리말 +
dtlab/ff/water.py, dtlab/ff/clayff.py, ff/SOURCES.md 를 만들어라.
1) SPC/E 물 템플릿(library/molecules/WAT/template.json)
   검증 대상 기대값(Berendsen 1987): O–H 1.0 Å, H–O–H 109.47°, q_O −0.8476, q_H +0.4238, O: ε 0.1553 kcal/mol, σ 3.166 Å, H: ε 0 σ 0.
   강체: LAMMPS fix shake 로 결합 · 각 고정(결합 · 각 계수는 shake 기준 길이용으로만 둠). 타입 이름 sw_OW · sw_HW (GAFF2 ow · hw 와 구분).
2) ClayFF 타입 표(ff/clayff.yaml, 타입 이름 cf_st · cf_ob · cf_oh · cf_ho · cf_cah) — Cygan et al. 2004 원 논문 표와 대조하는 테스트 필수
   검증 대상 기대값: st(사면체 Si) q +2.1, ε 1.8405e-6, σ 3.302 / ob(가교 O) q −1.05, ε 0.1554, σ 3.166 / oh(수산기 O) q −0.95, ε 0.1554, σ 3.166 / ho(수산기 H) q +0.425, ε 0, σ 0 / cah(수산화물 Ca, S9 용) q +1.05 — Ca LJ 값은 원 논문에서 옮긴다.
   결합: oh–ho 조화 결합(원 논문 k · r0), 각: st–oh–ho 또는 M–O–H 굽힘(원 논문 값). 광물 골격(st–ob)은 결합 없음(비결합 모델).
3) 혼합 규칙: 세 힘장 모두 LJ 12-6 이므로 pair_style lj/cut/coul/long 하나로 쓰고 pair_modify mix arithmetic(Lorentz–Berthelot) 적용.
   hybrid/overlay 는 쓰지 않는다(5주차 hybrid 예제와 구분). 이 선택의 근거를 SOURCES.md 에 기록: LA/docs/theory/clayff-gaff2-mixing-theory.md
4) 3자 이종쌍 표 생성기 `dtlab ff cross-table`: 전역 타입(GAFF2 + OW · HW + ClayFF) 전체의 ε_ij · σ_ij 표(CSV)와 pair_coeff 줄. 산술 · 기하 혼합 결과를 나란히 두고 차이가 큰 쌍 상위 10개를 출력(3주차 강의 연결).
5) 테스트: 전하 · LJ 값 대조, 교차항 계산 검산(수기 계산 3쌍).
완료 기준: WAT 템플릿과 ClayFF 표 생성, cross-table 출력, 출처 대조 테스트 통과.
```

---

## S3 · 벌크 바인더 생성과 평형화 (+ 벌크 물성 특징)

```text
[S3] 공통 머리말 +
dtlab/build/bulk.py 와 dtlab/gen/templates/bulk_equil.in.j2 를 만들어라.
입력 명세(BulkSpec): composition {BIN_SAT: wt%, BIN_ARO, BIN_RES, BIN_ASP}, additive {id | none, wt%}, lateral_xy (S4 슬래브의 x · y 길이, Å), target_atoms(기본 3500), seed.
1) 개수 환산: 총질량 M 을 target_atoms 에 맞춰 정하고 n_i = round(w_i · M / MW_i). 모든 성분 n_i ≥ 1(첨가제 포함).
   실제 wt% 를 다시 계산해 목표와의 차이를 보고, 성분별 |Δ| > 1.0 wt%p 이면 target_atoms 를 키워 재시도(최대 3회) 후 실패.
2) 충전: Packmol, 상자 x · y = lateral_xy(고정), z = 초기 밀도 0.3 g/cm³ 가 되는 높이. tolerance 2.0 Å, seed 전달, 구조 순서 = molecules.yaml 순서(좌표 ↔ 토폴로지 대응의 기준).
   Packmol 실패(수렴 안 됨) 시 seed+1 로 최대 2회 재시도. 이후 실패 기록.
3) data 파일: S1 템플릿 + 전역 타입 표 → LAMMPS data(Masses, Pair Coeffs 없음 — in 파일에서 지정, Bonds · Angles · Dihedrals · Impropers). 분자 ID = 분자별 고유. 이미지 플래그 0.
4) 평형화 입력(bulk_equil.in.j2): units real, atom_style full, boundary p p p,
   pair_style lj/cut/coul/long 12.0, pair_modify mix arithmetic tail yes, kspace_style pppm 1.0e-4,
   bond harmonic, angle harmonic, dihedral fourier, improper cvff, special_bonds amber,
   fix shake (X–H 결합), timestep 2.0,
   ① minimize 1e-4 1e-6 5000 50000 ② NVT 500 K 100 ps ③ NPT 500 → 293 K 냉각 200 ps(x · y 고정, z 만 barostat: fix npt ... z 1.0 1.0 1000.0) ④ NPT 293 K 1 ns 생산.
   x · y 를 고정하는 이유(주석): 뒤에서 석영 슬래브 위에 올릴 때 가로 치수를 맞추기 위해.
   thermo 1000: step temp press density pe ke etotal lz. 마지막에 write_data (unwrapped 가 아니라 image 플래그 보존) · write_restart.
5) 벌크 물성(dtlab/build/bulk_props.py): 생산 구간 후반 50 % 의 밀도 평균 ± 블록 SE, CED Method B = (Σ n_i·E_iso,i − E_bulk,inter)/V 계산을 위해
   분자별 고립 에너지 E_iso 입력(진공 단분자 NVT 293 K 200 ps 평균 pe, 분자당 1회 계산해 library 에 캐시)과 벌크 pe 평균을 사용. δ = √CED.
   결과를 bulk_props.json 에 저장(밀도, CED, δ, 각 평균 ± SE, 사용 구간).
6) CLI: `dtlab build bulk specs/bulk_ref.yaml --run --cores 8` (--run 없으면 입력만 생성).
7) 테스트: 개수 환산 · wt% 오차 검사(수치 예제), Packmol 입력 생성 문자열 검사, 축소판(target_atoms 600, 생산 20 ps) 실행 후 밀도 0.6~1.2 g/cm³ 범위(물리 타당성 거친 검사).
완료 기준: 기준 조성 벌크가 1 ns NPT 후 밀도 시계열이 평탄(전반 · 후반 평균 차 < 2 SE), bulk_props.json 생성.
참고: LA/src/builder, LA/docs/architecture/packmol-structure-generation-quality.md, LA/docs/theory/ced-calculation-methods.md
```

---

## S4 · α-석영 (001) 수산화 슬래브

```text
[S4] 공통 머리말 +
dtlab/build/quartz.py 를 만들어라. 결과는 모든 캠페인이 공유하는 기판 하나다.
1) 결정: COD 에서 α-quartz CIF 를 내려받는 함수(COD ID 를 명세에 명시하고 manifest 에 기록, 파일 SHA-256 검사). 네트워크가 없으면 library/crystals/ 의 캐시 사용.
2) 직교 초격자: 육방 셀(a = b ≈ 4.91 Å, c ≈ 5.40 Å — CIF 값 사용)을 (a, a+2b) 직교 변환 → nx × ny 반복해 x ≈ 29.5 Å, y ≈ 34.0 Å (nx=6, ny=4 기본, 명세로 조정 가능).
   z 방향 3 단위 셀(약 16 Å) 후 (001) 절단.
3) 표면 처리(위 · 아래 두 면): 배위수 부족 Si 에 OH 를 붙이고 부족 O 에 H 를 붙여 완전 수산화(fully hydroxylated) 표면을 만든다.
   목표 실라놀 밀도는 원 문헌 값으로 검증(완전 수산화 (001) 의 geminal 실라놀, 약 9.6 OH/nm² 로 알려짐 — 출처 확인 후 기대값 테스트로 고정).
   O–H 1.0 Å, Si–O–H 각 약 109.5°, H 는 표면 바깥쪽(+z 또는 −z) 향함.
4) 타입 · 전하: cf_st · cf_ob · cf_oh · cf_ho (S2 표). 슬래브 전하 합이 0 인지 검사(ClayFF 규칙상 완전 수산화 표면은 중성). 0 이 아니면 실패.
5) 출력: quartz_slab.data(원자 · 결합(oh–ho) · 각), quartz_meta.json(x · y · 두께, 위 표면 H 의 최대 z = z_top, 실라놀 밀도, 원자 수).
   모든 원자에 group 이름을 붙일 수 있게 molecule ID = 1(결정 전체), 이후 병합 시 group quartz 로 사용.
6) 검증 실행: 슬래브만 두고 진공 60 Å, 결정 원자 전체 고정(fix setforce 0 0 0), 수산기 H 만 움직이게 NVT 293 K 50 ps → O–H 길이 · 각 분포와 에너지 발산 여부 확인.
7) 테스트: 셀 치수, 원자 수 · 전하 합 · 실라놀 밀도 기대값, 원자 간 최소 거리 > 0.9 Å.
완료 기준: quartz_slab.data 1개와 검증 실행 통과.
참고: LA/docs/workflows/crystal-slab-hydroxylation-procedure.md, LA/src/builder/crystal_builder.py
```

---

## S5 · 계면 물층

```text
[S5] 공통 머리말 +
dtlab/build/water_layer.py 를 만들어라.
입력(WaterSpec): level ∈ {0, 1, 2} 또는 areal_density(분자/nm²), seed. 기본 대응: 0 → 0, 1 → 10, 2 → 20 분자/nm² (약 1 · 2 분자층; 물 밀도 33.4 분자/nm³ 기준 층 두께 약 3 Å 가정 — 값과 근거를 README 에 기록).
1) 분자 수 N_w = round(areal_density · A), A = x·y(nm²). 기판 30×34 Å 이면 level 1 ≈ 100, level 2 ≈ 200.
2) 배치 영역: z ∈ [z_top + 1.5, z_top + 1.5 + h], h = N_w / (33.4 · A) nm (Å 로 환산). Packmol inside box, tolerance 2.0 Å, x · y 는 주기 경계 가장자리 겹침을 피하려 양끝 1.0 Å 여유.
3) 출력: water_layer.xyz(+ 템플릿 참조), water_meta.json(N_w, z 범위, level). level 0 이면 빈 산출물(메타만).
4) 검증: 최소 O–O 거리 > 2.3 Å, 모든 물이 영역 안, N_w 정확.
완료 기준: level 0 · 1 · 2 산출물 3개 생성, 검증 통과.
```

---

## S6 · 3층 셀 조립

```text
[S6] 공통 머리말 +
dtlab/build/layered.py 를 만들어라. 부모 구조(parent) = (조성 조합, 물층 level, 기판) 하나. 온도 · 시드 분기는 S7/S8 에서 한다.
입력(LayeredSpec): bulk_id(S3 산출물), water_level, substrate(quartz | portlandite), gap_water_binder 2.5 Å, vacuum 60 Å, seed.
1) 층 쌓기(z 아래 → 위): 기판(z_top 까지) → 물층(S5, level 0 이면 생략) → 바인더.
   바인더: S3 평형화 최종 구조를 분자 단위로 언랩(image 플래그로 분자를 온전하게 복원)한 뒤, 분자 전체의 z 최소값이 (물층 최상단 또는 z_top) + gap 이 되도록 평행 이동.
   x · y 는 바인더 상자와 기판이 같아야 한다(S3 에서 lateral_xy 를 맞춤). 차이가 0.01 Å 넘으면 실패.
   상자 z = 바인더 최상단 + vacuum. boundary p p f, 이후 입력에서 kspace_modify slab 3.0.
2) 타입 병합: 기판(ClayFF, cf_) · 물(SPC/E, sw_) · 바인더(GAFF2, g2_) 타입을 하나의 표로 합치고(접두어가 다르면 이름이 같아도 다른 타입 — 페놀 첨가제 g2_oh 와 실라놀 cf_oh 가 분리되는지 테스트) 타입 번호를 겹치지 않게 재부여. 타입 번호 ↔ 이름 대응표를 layered_types.json 에 저장.
   결합 · 각 · 이면각 · 부정각 타입도 병합. 원래 파일의 번호를 그대로 쓰지 않는다(4주차 타입 번호 어긋남 교훈).
3) 그룹 정의 파일 groups.json: quartz(기판 원자 ID 범위), water(분자 ID 범위), binder, 그리고 binder_top5(바인더 분자 중 질량중심이 최상단 5 Å 안에 있는 분자 전체 — 인장 그립 후보).
4) 출력: layered.data, layered_types.json, groups.json, layered_meta.json(층별 z 범위, 원자 수, 총 원자 수, 순전하=0 확인).
5) 검증(FF_COMPATIBILITY V6 와 동일 기준): 순전하 |Σq| < 1e-6, 층 간 최소 거리(기판–물 > 1.5 Å, 물–바인더 > 2.0 Å), 원자 간 최소 거리 > 0.9 Å, 원자 수 = 부분합.
6) 스냅샷: matplotlib 로 x–z 투영(층별 색) PNG. OVITO 가 있으면 3D 렌더 추가.
7) CLI: `dtlab build layered --bulk <id> --water 1 --substrate quartz`
완료 기준: 기준 조성 × water 0 · 1 · 2 부모 구조 3개 생성, 검증 · 스냅샷 확인.
참고: LA/docs/papers/paper10_beta_unified/figures/GEO_layered_cell.png (층 구성 예), LA 교훈 8(진공 60 Å)
```

---

## S7 · 직접인장 실행 패키지

```text
[S7] 공통 머리말 +
dtlab/gen/templates/tension.in.j2 와 dtlab/gen/tension.py 를 만들어라. 자식 실행(child) = 부모 구조 + (온도, 시드, 인장 속도).
입력(TensionSpec): parent_id, T ∈ {253, 273, 293} K, seed, pull_velocity(Å/ps; 학습용 0.5, 기준 캠페인 0.1 — 캠페인 안에서 변경 금지), max_disp 40 Å, relax_ps 200, dt 2.0 fs.
템플릿 내용(값은 모두 변수, 하드코딩 금지):
  units real / atom_style full / boundary p p f / read_data layered.data
  pair_style lj/cut/coul/long 12.0 ; pair_modify mix arithmetic (tail 없음: 계면계)
  kspace_style pppm 1.0e-4 ; kspace_modify slab 3.0
  bond harmonic / angle harmonic / dihedral fourier / improper cvff / special_bonds amber
  groups.json 의 원자 · 분자 ID 로 group quartz · water · binder · grip 정의; group mobile subtract all quartz grip
  neigh_modify exclude group quartz quartz   (고정 결정 내부 쌍 제외 — CPU 절약, kspace 에는 적용 안 됨을 주석)
  fix freeze quartz setforce 0.0 0.0 0.0 ; velocity quartz set 0 0 0
  fix shake: mobile 그룹에만 적용(GAFF2 X–H 결합 + SPC/E 결합 · 각). ClayFF 수산기 O–H 와 grip 은 제외(FF_COMPATIBILITY §4)
  ① minimize(quartz 고정 유지) ② velocity mobile create T seed ③ NVT(mobile) relax_ps — 바인더 상부는 자유 표면이라 온도별 밀도가 스스로 맞춰짐
  ④ 인장: fix pull grip move linear 0 0 v  (v = pull_velocity · 1e-3 Å/fs), NVT 는 mobile 만, max_disp / v 만큼 run
  기록: compute fg grip reduce sum fz ; compute fq quartz reduce sum fz ;
        fix ave/time 50 10 500 → stress_disp.dat: step, time(ps), disp(Å), F_grip, F_quartz
        z 밀도: compute chunk/atom bin/1d z lower 0.5 → fix ave/chunk 로 인장 시작 · 끝 두 시점, 그룹별(quartz · water · binder) 질량 밀도
        dump 5 ps 간격(좌표만, 정렬), thermo 1000
  종료 후 write_data final.data
응력 변환(dtlab/analyze 에서 사용, 여기서는 상수만 정의): σ[MPa] = −F_grip[kcal/mol/Å] / A[Å²] × 6947.7  (1 kcal/mol/Å³ = 6947.7 MPa)
검증 규칙(FF_COMPATIBILITY V7): 진공 ≥ max_disp + 20 Å 인지 렌더 전에 검사(z 경계 f 밖으로 나가면 lost atoms). 정상 상태에서 F_grip ≈ −F_quartz (평균 차 < 10 %) — 힘 전달 경로 검사로 테스트에 넣는다.
1) tension.py: TensionSpec → 실행 폴더(in.tension, layered.data 링크, groups.json, run.sh, manifest.json). run.sh 는 `mpirun -np <ranks> <lmp> -sf omp -pk omp <threads> -in in.tension`, OMP_NUM_THREADS 명시.
2) 시간 간격 검증 모드: --dt-check 이면 같은 자식을 dt 1.0 fs 로도 만들어 σ_max 비교(차이 < 시드 산포) 계획을 남긴다.
3) 테스트: 템플릿 렌더 결과에 숫자 리터럴(온도 · 속도 · 스텝) 이 하드코딩되어 있지 않은지 정규식 검사, 축소판(원자 1,500, relax 5 ps, disp 5 Å) 실제 실행 후 stress_disp.dat 생성 · F_grip ≈ −F_quartz 검사.
완료 기준: 기준 부모 1개 × 293 K × seed 1 실행 완료, 응력–변위 곡선 PNG 생성.
참고: LA/src/orchestrator/tensile_extension.py(target_steps 계산), LA/src/metrics/tensile_metrics.py(W_sep 식), LA/docs/ops/LIT_SURVEY_TENSILE_SETUP_20260718.md(결정 고정 근거)
```

---

## S8 · 캠페인 계층 — 설계 → 부모 → 자식

```text
[S8] 공통 머리말 +
dtlab/campaign/design.py, dtlab/campaign/plan.py, specs/campaign_main.yaml 을 만들어라.
1) 설계 공간(specs/design_space.yaml):
   바인더 4분자 질량분율: 각 하한 · 상한(예: SAT 20–50, ARO 20–50, RES 10–30, ASP 5–20 wt%, 합 100) — 값은 명세에 두고 코드에 하드코딩 금지
   첨가제: none | ADD_AMN | ADD_FAC | ADD_PHN, 함량 {2, 4} wt% (none 이면 0)
   물층: {0, 1, 2}, 온도: {253, 273, 293} K, 기판: {quartz}(S9 에서 portlandite 추가)
2) 조성 표본: 제약 단체 위 Sobol(scrambled, seed 고정) 12점 — 제약 밖 점은 버리고 다음 점 사용. 각 점의 합이 100 인지 검사.
   조합: 조성마다 3개 = none 1 + 첨가제 설정 6개(3종 × 함량 2) 중 2개 → 12 × 3 = 36 조합. 첨가제 설정 6개가 각각 4번씩 나오도록 라틴 방진식으로 배정(seed 고정) — 배정 규칙을 명세에 기록.
   comp_id = 조성 + 첨가제 정규화 JSON 해시(기계학습 그룹 키).
3) 계층 계획(plan.py): 
   벌크(S3): 조합 36개 (각 1회, bulk_props 포함)
   부모(S6): 36 × water 3 = 108
   자식(S7): 108 × T 3 × seed 1 = 324  + 반복: 대표 조합 4개 × water 3 × T 3 × 추가 seed 2 = 72
   결과: plan.csv (level, id, parent_id, spec 해시, 예상 코어·시간)
4) 계산량 추정: 4주차 벤치마크(bench.json: 원자 수별 ns/day)를 읽어 자식별 예상 시간과 총 코어·시간, 병렬 작업 수별 소요 일수를 출력. bench.json 이 없으면 추정 불가로 표시(가정값을 쓰지 않음).
5) 실행 연계: `dtlab campaign plan specs/campaign_main.yaml` → plan.csv, `dtlab campaign materialize` → 벌크 · 부모 · 자식 폴더 생성(멱등), `dtlab campaign submit --jobs N --cores k` → 5주차 CPU 실행기(dtlab/gen/runner) 큐에 의존성 순서(벌크 → 부모 → 자식)대로 등록.
6) 수강생 할당: `dtlab campaign slice --student <id> --n 12` → 학습용 속도(0.5 Å/ps)로 바꾼 부분 계획(기준 캠페인과 섞이지 않게 campaign 태그 분리).
7) 테스트: 설계 제약 검사, 계층 개수(36/108/324/72), ID 결정성(같은 명세 → 같은 ID), slice 가 기준 태그와 분리되는지.
완료 기준: plan.csv 와 계산량 표, materialize --dry-run 이 전체 폴더 목록을 출력.
```

---

## S9 · 시멘트 기판(portlandite) 변형

```text
[S9] 공통 머리말 +
dtlab/build/portlandite.py 를 만들고 S6 의 substrate 선택지에 추가하라.
1) Ca(OH)₂ (P-3m1) CIF 를 COD 에서 받아(ID 기록) (001) 방향으로 직교 초격자, x · y 를 석영 기판과 가능한 한 가깝게(차이는 S3 lateral_xy 를 기판별로 다시 맞춤 — 벌크를 기판별로 따로 평형화).
2) 타입: cah(Ca, q +1.05) · oh · ho (ClayFF, 원 논문 대조). (001) 표면은 수산기 층으로 끝나며 전하 합 0 검사.
3) 결정 전체 고정은 석영과 같다.
4) 확장 캠페인 명세 specs/campaign_portlandite.yaml: 12 조합 × water 3 × 293 K = 36 자식.
완료 기준: portlandite 부모 1개 × water 1 × 293 K 인장 실행 완료, 석영과 같은 조건의 σ_max 비교 그림.
```

---

## S10 · 구조 품질 게이트

```text
[S10] 공통 머리말 +
dtlab/build/qc.py 와 `dtlab build qc <폴더>` 를 만들어라. S3 ~ S7 산출물을 학습 데이터에 넣기 전에 통과해야 하는 검사 모음.
검사 항목(각 항목: 통과/실패/경고, 측정값, 기준, 근거)
  벌크: wt% 오차, 밀도 평탄성, 고리 관통(ring threading) 검사(방향족 고리 중심을 다른 결합이 관통하는지 — 고리 평면과 결합 선분 교차), CED > 0
  슬래브: 전하 합, 실라놀 밀도, 결정 원자 이동 없음(최종 − 초기 변위 0)
  물층: 분자 수, O–O 최소 거리
  3층: 순전하, 층 간 거리, x·y 일치, 타입 표 충돌 없음
  인장: F_grip ≈ −F_quartz, 결정 z 앵커 불변(LA 교훈 31), 곡선 완주(최종 응력 < 최대의 5 % 또는 max_disp 도달), 에너지 발산 없음, 시간 간격 검증 결과
결과: qc.json + 요약 표. 실패한 자식은 학습에서 제외하는 플래그를 실행 대장에 기록(6 · 12주차에서 사용).
테스트: 일부러 망가뜨린 구조(전하 불일치, 겹침, 결정 이동) 3종이 각각 실패로 잡히는지.
완료 기준: 기준 캠페인 샘플 10개에 qc 를 돌려 결과 표 출력.
참고: LA/docs/HANDOFF_bulk_ced_guard.md, LA/docs/ops/LESSONS_LEARNED_20260901.md
```
