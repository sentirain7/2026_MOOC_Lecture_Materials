# 설치 지시문 (Claude Code 에 붙여 넣기) · I-1 ~ I-6

이 강좌에서 사람이 직접 설치하는 것은 **Claude Code 하나**다(W01 실습 · `claude_code_quickstart.md` §2).
나머지 소프트웨어는 아래 지시문을 Claude Code 에 붙여 넣어 설치하고 확인한다. 지시문마다 Claude Code 가 명령을 보여 주고 **승인한 뒤에만** 실행한다.

- 시작 위치: 터미널 → 저장소 맨 위 폴더(`environment.yml` 이 있는 곳) → `claude`
- 결과 기록: 각 지시가 `out/I-n_result.md` 에 표로 남긴다(다음 주차에서 다시 볼 수 있게)
- 검증 범위: **Ubuntu 22.04 / 24.04 (WSL2 포함)에서 실제 설치로 확인**(2026-11-14). macOS · Windows 명령은 공식 안내를 옮긴 것이며 **미검증**이다.
- 지켜야 할 것: 다른 conda 환경 · 시스템 파일을 건드리지 않는다 · `sudo` 가 필요하면 먼저 묻는다 · 모든 권한을 건너뛰는 옵션은 쓰지 않는다

| 번호 | 무엇 | 언제(처음 쓰는 주차) | 시간 |
|---|---|---|---|
| I-1 | conda(Miniforge) | W01 | 3분 |
| I-2 | 강좌 환경 mdai (Python · RDKit · scikit-learn · XGBoost · LAMMPS · Packmol · AmberTools) | W01 | 6~20분 |
| I-3 | Zotero + Better BibTeX | W02 | 5분 + 사람이 누를 것 2곳 |
| I-4 | Obsidian + 강좌 볼트 | W02 | 3분 + 사람이 누를 것 1곳 |
| I-5 | 전체 점검(작은 MD 한 번 · 폐루프 재생 1라운드) | W01 끝 · W06 · W18 | 3분 |
| I-6 | 설치 오류 진단 | 언제든 | · |

---

## I-1 · conda (Miniforge)

```
이 컴퓨터에 conda 가 있는지 확인해라(conda --version · which conda · 운영체제와 CPU 종류 uname -sm).
있으면 버전만 표로 적고 끝내라.
없으면 Miniforge 를 내 홈 폴더 ~/miniforge3 에 설치하는 명령을 운영체제에 맞게 보여 주고, 내 승인 뒤 실행해라.
- sudo 는 쓰지 마라 · 다른 Python · conda 설치는 건드리지 마라
- 설치 뒤 ~/miniforge3/bin/conda init bash(맥은 zsh)로 터미널 설정을 하고, 새 터미널에서 conda --version 이 나오는지 확인하는 방법을 알려 줘라
결과를 out/I-1_result.md 에 표(항목 · 값 · 확인)로 적어라.
```
- Ubuntu · WSL2(검증): `curl -fsSLo Miniforge3.sh https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh && bash Miniforge3.sh -b -p ~/miniforge3`
- macOS(미검증): 같은 주소의 `Miniforge3-MacOSX-arm64.sh`(Apple 칩) 또는 `-x86_64.sh`
- Windows: WSL2 Ubuntu 안에서 위 Ubuntu 명령(LAMMPS · AmberTools 때문)

## I-2 · 강좌 환경 mdai

```
@environment.yml 로 conda 환경 mdai 를 만들어라(conda env create -f environment.yml). 시간이 6~20분 걸린다.
- mdai 가 이미 있으면 지우지 말고 먼저 나에게 알려라
- 다른 conda 환경은 건드리지 마라
만든 뒤 conda run -n mdai 로 다음을 확인해 out/I-2_result.md 에 표(프로그램 · 버전 · 확인)로 적어라:
python · numpy · rdkit · scikit-learn · xgboost · shap · parmed · lmp(lmp -h 의 첫 줄과 Installed packages 에 KSPACE · MOLECULE · OPENMP 가 있는지) · packmol · antechamber · parmchk2 · tleap
실패한 항목은 원인과 조치를 적고, 조치는 내 승인 뒤에만 해라.
```
- 같은 판(버전까지 동일)을 원할 때(Ubuntu · linux-64): `conda create -n mdai --file environment.lock.txt` — 강좌 기준 결과를 만든 그대로
- 확인된 판(2026-11-14 · Ubuntu): python 3.12.16 · LAMMPS 22 Jul 2025 Update 6(CPU · OpenMP) · AmberTools 26(packmol 포함) · RDKit 2026.09.2 · scikit-learn 1.9.1 · XGBoost 3.4.2 · SHAP 0.52.0 · parmed 4.3.1
- 주의: Packmol 은 AmberTools 안에 들어 있다 · 따로 설치하면 충돌한다

## I-3 · Zotero + Better BibTeX

```
문헌 관리 프로그램 Zotero 를 설치하려 한다. 운영체제를 확인하고 설치 명령을 보여 준 뒤 내 승인 뒤 실행해라.
- Ubuntu · WSL2: 공식 Linux 판(tar.xz)을 ~/Applications/Zotero 에 풀고 ./set_launcher_icon 으로 바로가기 · sudo 없이
- 이미 설치돼 있으면 버전만 확인해라
이어서 Better BibTeX 플러그인 최신 .xpi 를 ~/Downloads 에 받아 두어라(GitHub retorquere/zotero-better-bibtex 의 최신 릴리스).
그다음 내가 Zotero 화면에서 직접 할 일 두 가지를 순서대로 알려 줘라:
 ① 도구 → 플러그인 → 톱니 → 파일에서 플러그인 설치 → 받아 둔 .xpi
 ② 「내 라이브러리」 오른쪽 클릭 → 컬렉션 내보내기 → Better BibTeX · 「Keep updated」 체크 → 저장 위치 = 이 저장소의 loop/lit/library.bib
결과를 out/I-3_result.md 에 적어라.
```
- Ubuntu(검증 · 내려받기 · 압축 풀기): `https://www.zotero.org/download/client/dl?channel=release&platform=linux-x86_64` → `tar -xJf`(이름은 .tar.bz2 로 받아도 실제 형식은 xz)
- macOS(미검증): `brew install --cask zotero` · Windows(미검증): `winget install Zotero.Zotero`
- Better BibTeX 9.0.77(2026-11-14 최신 확인) · Zotero 7 이상용
- 강좌 저장소에는 사례 서지 `loop/lit/library.bib` 가 미리 들어 있다(같은 형식 · Crossref 메타데이터로 만듦) → Zotero 없이도 폐루프는 돈다

## I-4 · Obsidian + 강좌 볼트

```
노트 프로그램 Obsidian 을 설치하려 한다. 운영체제를 확인하고 설치 명령을 보여 준 뒤 내 승인 뒤 실행해라.
- Ubuntu · WSL2: GitHub obsidianmd/obsidian-releases 최신 AppImage 를 ~/Applications 에 받아 실행 권한을 주어라(sudo 없이) · 실행에 FUSE 가 없다는 오류가 나면 --appimage-extract 로 푸는 방법을 제시해라
- 이미 설치돼 있으면 버전만 확인해라
그다음 내가 Obsidian 화면에서 할 일을 알려 줘라:
 ① 「폴더를 보관함으로 열기」 → 이 저장소의 loop/vault
 ② 설정 → 핵심 플러그인 → 템플릿 켜기 → 템플릿 폴더 = templates
 ③ 왼쪽 막대 「그래프 보기」로 papers · runs · rounds 노트가 이어진 모습 확인
결과를 out/I-4_result.md 에 적어라.
```
- Ubuntu(검증 · 내려받기): Obsidian 1.15.1 AppImage · .deb 도 있음(.deb 은 sudo 필요 → 묻고 진행)
- macOS(미검증): `brew install --cask obsidian` · Windows(미검증): `winget install Obsidian.Obsidian` · WSL 이면 볼트 경로 = `\\wsl$\Ubuntu\home\<나>\2026_MOOC_Lecture_Materials\loop\vault`

## I-5 · 전체 점검

```
mdai 환경으로 강좌 전체 점검을 해라. 명령마다 승인을 받아라.
① python mdworkflow/mdwf.py mol Toluene --ws out/check  → ② ff Toluene → ③ build --id t50 --comp Toluene=50 --rho0 0.2 --tol 3.0 → ④ run t50 --protocol quick --threads 4 → ⑤ analyze t50
⑥ cd loop 에서 python scripts/library.py · python scripts/lit_extract.py · python scripts/loop_step.py (재생 모드 1라운드)
단계마다 걸린 시간 · 결과(원자 수 · 전하 합 · 밀도 · CED · 라운드 0 의 후보 6개)를 out/I-5_result.md 표로 적고, 실패하면 멈추고 원인을 설명해라.
```
- 기대: ② 톨루엔 GAFF2 타입 4 · 전하 합 0 · ④ 4코어 약 1분 · ⑥ 표적 밀도 1.018 · CED 354.2 · 라운드 0 후보 6개(`loop/expected_output/` 와 같음)

## I-6 · 설치 오류 진단

```
방금 [설치 · 실행] 에서 난 오류의 원인을 설명해라. 강좌 스크립트는 고치지 말고 환경 · 경로 · 입력 쪽 조치만 제안해라.
조치마다 무엇을 바꾸는지 한 줄로 쓰고, 내 승인 뒤에만 실행해라. 다른 conda 환경과 시스템 파일은 건드리지 마라.
```
- 자주 나는 것: `conda: command not found`(새 터미널을 안 엶 → I-1 의 conda init) · `lmp: not found`(conda activate mdai 안 함) · Packmol 충돌(따로 설치함 → mdai 를 지우지 말고 새 이름으로 다시 만들기)
