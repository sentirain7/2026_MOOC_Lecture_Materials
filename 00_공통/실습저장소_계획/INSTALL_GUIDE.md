# DT-Lab 설치 안내 — Linux · macOS · Windows(WSL2)

DT-Lab 실습에 필요한 모든 도구(LAMMPS · Packmol · AmberTools · RDKit · 파이썬 라이브러리)를 **전용 가상환경 `dtlab` 하나에** 설치하는 방법이다. 노트북에서도 돌아가도록 **CPU 전용 · 안정판 고정 버전**을 쓴다.

- 버전 확인일: 2026-09-22 (anaconda.org · PyPI · GitHub 태그 직접 조회)
- 관련 문서
  - `FF_COMPATIBILITY.md`: 힘장 · 원소 · LAMMPS 호환성
  - `PROMPTS_STRUCTURE.md`: S0 설치 자동화 프롬프트

---

## 0. 한눈에 보는 실행 순서

| 순서 | 할 일 | 명령 (저장소 폴더에서) | 걸리는 시간 |
|---|---|---|---|
| ① | 운영체제 준비 (Windows는 WSL2 설치) | §2 · §3 · §4 참고 | 10~30분 |
| ② | 저장소 받기 | `git clone <저장소 주소> && cd mooc-inverse-design` | 1분 |
| ③ | 가상환경 만들기 | `bash install/create_env.sh` | 5~10분 |
| ④ | 도구 설치 (기본 + MD 도구) | `bash install/install.sh G0 G1` | 10~20분 |
| ⑤ | 설치 점검 | `bin/dtlab check-env --group G1` | 1분 |
| ⑥ | Packmol · LAMMPS 동작 검사 | `bin/dtlab selftest md` | 3~5분 |
| ⑦ | 앱 실행 | `bin/dtlab-app` → 브라우저에서 `http://localhost:8501` | — |
| ⑧ | (필요할 때) ML · 문헌 도구 추가 | `bash install/install.sh G3` 등 | 5~15분 |

- **`conda activate dtlab`을 따로 입력하지 않아도 된다.** `bin/dtlab`과 `bin/dtlab-app`이 가상환경을 자동으로 켠다.
- 직접 명령을 입력할 때만 먼저 `source env/activate.sh`를 실행한다.
- ⑥에서 하나라도 실패하면 다음 단계로 넘어가지 않는다. §7 문제 해결표를 먼저 본다.

---

## 1. 지원 환경과 고정 버전

### 1.1 운영체제별 지원

| 운영체제 | 방식 | 비고 |
|---|---|---|
| Linux (Ubuntu 22.04 · 24.04, x86-64) | conda-forge 네이티브 | 기준 환경 |
| macOS Apple Silicon (M1~M4) | conda-forge 네이티브 (osx-arm64) | Rosetta(x86) 환경과 섞지 않는다 |
| macOS Intel | conda-forge 네이티브 (osx-64) | |
| **Windows 10 · 11** | **WSL2 + Ubuntu 24.04 안에서만** | Windows 네이티브는 지원하지 않는다 (아래 이유) |

**Windows 네이티브를 지원하지 않는 이유 (2026-09-22 확인)**
- conda-forge의 `lammps`, `packmol`, `ambertools`, `openmpi`에는 **win-64 빌드가 없다.**
- 따라서 Windows에서는 WSL2(리눅스 가상 커널) 안에 Ubuntu를 설치하고, 그 안에서 Linux 절차를 그대로 따른다.
- Git Bash · MSYS2 · Cygwin · PowerShell에서 직접 설치하는 방법은 쓰지 않는다.

### 1.2 고정 버전 (안정판)

| 도구 | 버전 | 설치 경로 | 선택 이유 |
|---|---|---|---|
| Python | 3.11 | conda-forge | 과학 패키지 호환 범위가 가장 넓다 |
| LAMMPS | **2025.07.22** (stable 22Jul2025) | conda-forge, **CPU 빌드** | 최신 안정판(stable)이다. 필요한 패키지가 모두 포함돼 있다 (§5.1) |
| LAMMPS 소스 빌드 (선택) | 태그 `stable_22Jul2025_update6` | GitHub | conda 판과 같은 안정판 계열의 최신 패치 |
| Packmol | **21.2.1** (conda-forge) / 21.2.3 (소스) | conda-forge 기본, 소스 컴파일은 선택 | §6 참고 |
| AmberTools | 26.0 | conda-forge | antechamber · parmchk2 · sqm · tleap (GAFF2 · AM1-BCC) |
| RDKit | 2026.03 계열 | conda-forge | |
| OpenMM | 8.6 계열 | conda-forge | 힘장 변환 검증용 (에너지 대조) |
| ParmEd | 4.3.1 | conda-forge | Amber 파라미터 읽기 |
| MDAnalysis | 2.10 계열 | conda-forge | 궤적 분석 |

- 설치가 끝나면 `env/versions.lock`에 실제 설치 버전과 빌드 문자열을 기록한다.
- `env/environment.lock.yml`로 같은 환경을 다시 만들 수 있다.
- **버전은 학기 중에 올리지 않는다.** 캠페인 도중에 설정을 바꾸지 않는다는 원칙과 같다.

### 1.3 컴퓨터 사양 프로필

| 프로필 | 대상 | LAMMPS 빌드 | 병렬 방식 | 셀 크기 | 인장 속도 |
|---|---|---|---|---|---|
| **laptop** (기본) | 노트북 · 4~8코어 · 메모리 8 GB 이상 | `cpu_*_nompi` | OpenMP 스레드만 (`-sf omp -pk omp 4`) | 미니 셀(약 1,500원자) | 학습용 0.5 Å/ps |
| **workstation** | 16코어 이상 · 메모리 32 GB 이상 | `cpu_*_mpi_openmpi` | MPI 랭크 × OpenMP | 표준 셀(약 5,000원자) | 기준 0.1 Å/ps |

- **laptop 프로필은 MPI를 쓰지 않는다.** macOS와 WSL2에서 MPI 설정 문제가 가장 흔한 설치 실패 원인이기 때문이다. OpenMP만으로도 수강생 할당분(12~20개)은 계산할 수 있다.
- 프로필 선택: `bash install/create_env.sh --profile laptop` (기본값) 또는 `--profile workstation`
- **CUDA 빌드는 설치하지 않는다.** conda-forge에는 `cuda129_*` 빌드도 있다. 빌드 문자열에 `cpu`를 고정하지 않으면 GPU가 있는 컴퓨터에서 CUDA 판이 설치될 수 있다.

```bash
# install/install.sh 안에서 실제로 쓰는 고정 방식
mamba install -n dtlab -c conda-forge "lammps=2025.07.22=cpu_py311*nompi*"        # laptop
mamba install -n dtlab -c conda-forge "lammps=2025.07.22=cpu_py311*mpi_openmpi*"  # workstation
```

---

## 2. Linux (Ubuntu) 준비

1. 기본 도구: `sudo apt update && sudo apt install -y git curl build-essential`
2. **시스템에 이미 설치된 Packmol · MPI와 섞이지 않게 한다.**
   - 예: `/usr/bin/packmol`(배포판 패키지), 사용자가 직접 설치한 `~/openmpi`
   - 이런 도구가 `PATH`에 먼저 잡히면 가상환경 밖의 다른 버전이 실행된다.
   - `bin/dtlab check-env`가 "환경 밖 도구"를 경고한다. 경고가 나오면 `which packmol mpirun lmp`로 경로를 확인한다. 모두 `…/envs/dtlab/bin/`이어야 한다.
   - `env/activate.sh`는 가상환경의 `bin`을 `PATH` 맨 앞에 둔다. `~/.bashrc`에서 `PATH`를 뒤에 덧붙이는 설정이 있으면 이 순서가 깨질 수 있다.
3. 이후 §0의 ②부터 진행한다.

---

## 3. macOS 준비

1. Xcode 명령행 도구: `xcode-select --install`
2. **conda 설치:** Miniforge 설치 파일을 받아 설치한다. `install/create_env.sh`는 conda가 없으면 micromamba를 사용자 폴더에 설치하겠다고 묻는다.
3. **Apple Silicon 주의 사항**
   - 터미널이 Rosetta(x86)로 실행되고 있지 않은지 확인한다: `uname -m` → `arm64`
   - x86 conda와 arm64 conda를 섞어 설치하지 않는다.
   - `bin/dtlab check-env`는 파이썬 · LAMMPS의 아키텍처가 서로 다르면 경고한다.
4. **OpenMP:** conda-forge LAMMPS는 `llvm-openmp`를 함께 설치한다. Homebrew의 `libomp`와 섞지 않는다. 두 가지가 동시에 불러와지면 "OMP: Error #15" 오류가 난다.
5. **절전:** 오래 걸리는 계산 중 덮개를 닫거나 잠자기에 들어가면 계산이 멈춘다. `caffeinate -i bin/dtlab run …`으로 실행한다.
6. **소스 컴파일한 실행 파일(선택 경로):** Gatekeeper가 막을 수 있다. 직접 빌드한 파일은 `xattr -d com.apple.quarantine <파일>`로 격리 속성을 해제한다. 인터넷에서 받은 실행 파일은 이렇게 쓰지 않는다.
7. **PyPI Packmol wheel은 macOS 15 이상 전용**이다(`macosx_15_0`). 그보다 오래된 macOS에서는 conda-forge 판을 쓴다.

---

## 4. Windows — WSL2에서 진행 (터미널 주의 사항)

### 4.1 WSL2 설치
1. **관리자 PowerShell**에서 `wsl --install -d Ubuntu-24.04`를 실행한 뒤 재부팅한다.
2. 시작 메뉴에서 **Ubuntu 24.04**를 열어 사용자 이름과 암호를 만든다. 이 암호는 `sudo`에 쓰인다.
3. 버전 확인
   - PowerShell: `wsl -l -v` → VERSION이 **2**여야 한다.
   - 1이면 `wsl --set-version Ubuntu-24.04 2`를 실행한다.
4. 이후 **모든 명령은 Ubuntu 터미널 안에서** 실행한다. §2 Linux 절차와 같다.

### 4.2 반드시 지킬 것
| 주의 사항 | 이유 · 방법 |
|---|---|
| **저장소를 WSL 홈(`~/`)에 둔다. `/mnt/c/...`에 두지 않는다** | `/mnt/c`(Windows 드라이브)를 거치면 파일 입출력이 수 배~수십 배 느려진다. 실행 권한 · 심볼릭 링크 문제도 생긴다. `cd ~ && git clone …` |
| **Windows 쪽 도구로 저장소 파일을 고치지 않는다** | 메모장 등으로 `.sh` 파일을 저장하면 줄끝이 CRLF로 바뀐다. 그러면 `bash: $'\r': command not found` 오류가 난다. 편집은 **VS Code + WSL 확장**(Remote-WSL)으로 한다 |
| **Git 줄끝 설정** | WSL 안에서 `git config --global core.autocrlf input`을 실행한다. 저장소 `.gitattributes`에 `*.sh text eol=lf`, `*.in text eol=lf`, `*.inp text eol=lf`를 둔다 |
| **PowerShell · CMD · Git Bash에서 `bin/dtlab`을 실행하지 않는다** | 실행 파일과 가상환경이 모두 WSL 안에 있다. Windows 터미널 앱에서는 **Ubuntu 탭**을 연다 |
| **경로에 한글 · 공백을 피한다** | LAMMPS · Packmol 입력 파일은 공백이 든 경로를 제대로 읽지 못할 수 있다. 저장소는 `~/mooc-inverse-design` 같은 영문 경로에 둔다 |
| **메모리 · 코어 한도** | WSL2는 기본으로 호스트 메모리의 절반까지만 쓴다. 필요하면 `C:\Users\<이름>\.wslconfig`에 `[wsl2]`, `memory=8GB`, `processors=6`을 적고, PowerShell에서 `wsl --shutdown` 뒤 다시 연다 |
| **절전 · 업데이트 재부팅** | Windows가 잠자기에 들어가거나 업데이트로 재부팅되면 WSL 안의 계산도 멈춘다. 긴 계산은 `tmux` 안에서 실행하고, 전원 설정에서 잠자기를 끈다 |
| **백신 실시간 검사** | `\\wsl$` 경로가 검사 대상이면 빌드 · 계산이 느려질 수 있다. 기관 정책이 허용할 때만 예외 폴더를 등록한다 |
| **앱 접속** | `bin/dtlab-app` 실행 뒤 Windows 브라우저에서 `http://localhost:8501`에 접속한다(WSL2가 포트를 자동으로 전달) |
| **Windows 파일 가져오기** | Windows 탐색기 주소창에 `\\wsl$\Ubuntu-24.04\home\<이름>`을 입력하면 WSL 파일을 볼 수 있다. 결과 그림을 복사하는 용도로만 쓰고, 입력 파일은 WSL 안에서 만든다 |
| **시계 어긋남** | 잠자기에서 깨어난 뒤 WSL 시계가 어긋나면 manifest 시각과 API 인증이 틀어질 수 있다. `sudo hwclock -s` |

---

## 5. 설치 단계 상세 (모든 운영체제 공통, WSL2 포함)

```bash
cd ~/mooc-inverse-design
bash install/create_env.sh --profile laptop     # ③ 가상환경 dtlab 생성 (이미 있으면 건너뜀)
bash install/install.sh G0 G1                   # ④ 기본 + MD 도구 (lammps · packmol · ambertools · rdkit · openmm · parmed · ase · mdanalysis)
bin/dtlab check-env --group G1                  # ⑤ 설치 점검 표
bin/dtlab selftest md                           # ⑥ Packmol · LAMMPS · AmberTools 동작 검사 (§5.2)
```

### 5.1 LAMMPS 패키지 확인
conda-forge LAMMPS CPU 빌드에는 DT-Lab에 필요한 패키지가 모두 포함되어 있다(빌드 스크립트 확인, 2026-09-22). 필요한 패키지는 MOLECULE · KSPACE · RIGID · EXTRA-MOLECULE · EXTRA-FIX · EXTRA-DUMP · MISC · MANYBODY · OPENMP · REAXFF · ML-SNAP이다.

`check-env`는 `lmp -h`의 Installed packages 목록과 요구 목록을 대조한다. 빠진 패키지가 있으면 실패로 판정한다.

- **소스 빌드는 선택이다(4-1 강의 실습용).** `bash install/build_lammps.sh --tag stable_22Jul2025_update6`
- 컴파일러 · CMake · FFTW도 conda-forge에서 같은 가상환경에 설치한다. 시스템 컴파일러에 의존하지 않는다.
- 빌드 결과는 `lmp_dtlab`이라는 이름으로 설치되어 conda 판 `lmp`와 구분된다. 사용할 실행 파일은 `DTLAB_LMP` 환경변수로 고른다.

### 5.2 `bin/dtlab selftest md`가 하는 검사
1. **Packmol**: 물 1,000개 상자 충전 → 종료 코드 0, 출력에 `Success!`, 원자 수 3,000 (§6.3)
2. **Packmol 실패 판정**: 일부러 불가능한 충전(작은 상자에 물 2,000개)을 실행 → 종료 코드 **173** · `_FORCED` 파일 생성을 **실패로 판정하는지** 확인
3. **LAMMPS**: LJ 예제 1,000스텝(1코어) · SPC/E 물 216개 NVT 1 ps(PPPM · SHAKE 포함) → 오류 없이 종료
4. **AmberTools**: 메탄올 1개에 antechamber AM1-BCC → 전하 합 0
5. 결과 표와 소요 시간을 `env/selftest.json`에 저장한다. 강의자에게 제출하면 수강생 환경 차이를 비교할 수 있다.

---

## 6. Packmol — 설치와 검증

Packmol은 **Fortran으로 작성된 프로그램이라 실행 전에 컴파일되어 있어야 한다.** DT-Lab은 다음 순서로 설치한다.

### 6.1 기본: conda-forge 미리 컴파일된 판 (권장)
- `bash install/install.sh G1`이 `packmol=21.2.1`을 가상환경에 설치한다(Linux · macOS · WSL2).
- 컴파일러가 필요 없어 가장 안정적이다.

### 6.2 선택: 소스 컴파일 (21.2.3, conda 판을 쓸 수 없을 때 · 4-4 실습용)
`bash install/build_packmol.sh --tag v21.2.3`이 아래 절차를 수행한다. 이 컴퓨터(Ubuntu 24.04, gfortran 13.3)에서 **CMake 경로로 컴파일과 예제 실행을 확인했다(2026-09-22).**

```bash
source env/activate.sh
mamba install -n dtlab -c conda-forge fortran-compiler cmake make     # 컴파일러도 가상환경 안에
git clone https://github.com/m3g/packmol.git build/packmol-src
cd build/packmol-src && git checkout v21.2.3
cmake -S . -B objdir -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_Fortran_COMPILER="$FC" -DCMAKE_INSTALL_PREFIX="$CONDA_PREFIX"
cmake --build objdir -j 4 && cmake --install objdir                  # → $CONDA_PREFIX/bin/packmol
```

주의 사항
- **`make`(Makefile) 경로는 쓰지 않는다.**
  - 저장소의 Makefile은 컴파일러를 `/usr/bin/gfortran`으로 고정하고 있다.
  - 최적화 옵션 `-march=native`도 들어 있어, 만든 실행 파일이 **빌드한 컴퓨터의 CPU에서만** 돌 수 있다.
  - 다른 컴퓨터로 복사하면 "Illegal instruction"으로 죽는다.
  - CMake 경로(Release)를 쓴다.
- **컴파일러는 가상환경 안의 것을 쓴다.** conda-forge `fortran-compiler`를 쓰고, `$FC`에 경로가 들어간다. 시스템 gfortran 버전 차이로 생기는 문제를 피하기 위해서다.
- macOS에서도 같은 명령을 쓴다. Homebrew gfortran과 섞지 않는다.
- 설치 뒤 `which packmol`이 `…/envs/dtlab/bin/packmol`인지 확인한다. conda 판이 이미 있으면 소스 빌드 판이 덮어쓴다. 어느 쪽인지 `env/versions.lock`에 기록한다.

### 6.3 Packmol 성공 · 실패 판정 규칙 (실제 동작 확인값)

| 상황 | 종료 코드 | 출력 파일 | 로그 |
|---|---|---|---|
| 충전 성공 | **0** | `output.pdb` | `Success!`, `Maximum violation of target distance: 0.000000` |
| 충전 실패(공간 부족 · 반복 한도 초과) | **173** | **`output.pdb`가 그래도 만들어짐** + `output.pdb_FORCED` | 거리 위반값 > 0 (예: 3.99) |
| 입력 · 구조 파일을 찾지 못함 | **172** | 없음 | `ERROR: Could not open file.` |

- **출력 파일이 있다고 성공이 아니다.** 실패해도 마지막 시도 구조가 같은 이름으로 저장된다.
- DT-Lab은 다음 네 가지를 **모두** 확인해야 성공으로 판정한다(`dtlab/build/packmol.py`).
  1. 종료 코드 0
  2. 로그에 `Success!`
  3. 최대 거리 위반 < 0.01 Å
  4. 원자 수 = 기대값
- 실패하면 `seed`를 바꿔 최대 2회 다시 시도한다. 그래도 실패하면 초기 밀도를 낮추거나 상자를 키우라고 안내한다.
- **입력 파일 규칙**
  - `seed`를 항상 명시한다(`seed -1`은 매번 다른 결과).
  - 구조 파일 경로는 입력 파일 기준 상대 경로다. DT-Lab은 실행 폴더로 이동한 뒤 실행하고 절대 경로를 쓴다.
  - 경로에 공백을 쓰지 않는다.
- 21.x 판은 주기 경계 키워드 `pbc`를 지원한다(예제로 확인). DT-Lab 벌크 충전은 `pbc`를 쓰고, 슬래브 위 물층은 `inside box` + 가장자리 여유 1 Å로 쓴다.

---

## 7. 문제 해결

| 증상 | 원인 | 조치 |
|---|---|---|
| `bash: $'\r': command not found` | Windows에서 저장해 줄끝이 CRLF가 됨 | `sed -i 's/\r$//' <파일>` 뒤 §4.2 줄끝 설정 |
| `packmol` 버전이 20.x로 나옴 | 시스템 `/usr/bin/packmol`이 먼저 잡힘 | `source env/activate.sh` 또는 `bin/dtlab` 사용, `which packmol` 확인 |
| `mpirun`이 `~/openmpi` 등 다른 MPI를 부름 | 가상환경 밖 MPI | workstation 프로필은 conda `openmpi`를 쓴다. laptop 프로필은 MPI 없이 실행 |
| LAMMPS `Unrecognized pair style` · `fix shake` 없음 | 필요한 패키지가 빠진 빌드 | `check-env` 패키지 표 확인, conda CPU 판으로 재설치 |
| GPU 컴퓨터에서 CUDA 판 LAMMPS가 설치됨 | 빌드 문자열을 고정하지 않음 | `lammps=2025.07.22=cpu_py311*` 형식으로 재설치 |
| `OMP: Error #15` (macOS) | libomp가 두 번 불러와짐 | Homebrew libomp 경로를 `DYLD_LIBRARY_PATH`에서 제거 |
| `Illegal instruction` (Packmol · LAMMPS) | `-march=native`로 다른 CPU에서 빌드한 파일 | conda 판을 쓰거나 이 컴퓨터에서 CMake Release로 다시 빌드 |
| antechamber가 sqm 수렴 실패 | 초기 구조 불량 · 전하 지정 오류 | RDKit 배좌를 다시 생성, `-nc 0` 확인 |
| WSL에서 매우 느림 | 저장소가 `/mnt/c` 아래 | 저장소를 `~/`로 옮김 |
| 계산이 밤사이 멈춤 | 절전 · 업데이트 재부팅 | `tmux` 안에서 실행, 절전 해제(macOS는 `caffeinate`) |

---

## 8. 가상환경 관리 명령

| 목적 | 명령 |
|---|---|
| 환경 켜기(직접 명령 입력할 때) | `source env/activate.sh` |
| 환경 끄기 | `conda deactivate` |
| 설치 상태 표 | `bin/dtlab check-env` |
| 잠금 파일 내보내기 | `bash install/export_env.sh` → `env/environment.lock.yml` |
| 잠금 파일로 같은 환경 만들기 | `bash install/create_env.sh --from-lock` |
| 환경 삭제 후 처음부터 | `bash install/remove_env.sh` → ③부터 |
| 노트북 커널 등록 | `bin/dtlab kernel install` → 커널 이름 "DT-Lab (dtlab)" |
