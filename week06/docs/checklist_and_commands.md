# week06 보충: v1 덱에서 옮긴 표 · 체크리스트 · 명령 한 줄씩

덱(v3 · 26장)에 넣지 않은 v1 덱(28장 · `decks/v1/W06_LAMMPS입력과구조생성.html`)의 내용을 전문으로 둔다. 출처는 원본 04주차 덱 장 번호.

## 1. 실행 전 검증 체크리스트 6 (원본 04#35)
1. 원자 수 = Σ(분자 수 × 분자당 원자) · data 헤더와 대조 (톨루엔 50 × 15 = 750)
2. 총 전하 |Σq| < 1e−4 e · 분자별도 0 (톨루엔 셀 −5e−5 → LAMMPS 가 `System is not charge neutral` 경고를 내지만 허용 범위)
3. 분자간 최소 원자 거리 > 1.8 Å (게이트 기준은 0.9 × tolerance = 2.7 Å · 톨루엔 셀 3.283 Å)
4. 발산 · 관통 → 시드 변경 재패킹 · ρ0 · tolerance 유지 · 상한 3회
5. 주기경계 겹침 방지 · Packmol `inside box` 는 경계 안쪽 2 Å
6. 무작위 배치이므로 반드시 최소화 · 어닐링 뒤 물성

## 2. 출력 4종 (원본 04#24)
| 파일 | 내용 | 쓰임 | 주의 |
|---|---|---|---|
| `log.*` | Step Temp Press Density 시계열 · 경고 | 평형 판정 · 밀도 평균 (W05) | 원본 binderA: step 0 밀도 0.8123 → 500000 에서 0.9968 g/cm³ |
| `*.lammpstrj` | id type x y z 궤적 | RDF · MSD · 점도의 원본 (W09) | 덤프 주기 = 표본 간격 · 촘촘하면 용량만 |
| `final.data` | 상자 · 좌표 · 전하 · 결합 (텍스트) | 다른 온도 · 계면 계산의 입력 | 속도 · 시간 없음 |
| `*.restart` | 좌표 + 속도 + fix 상태 (이진) | 중단 복구 · 같은 계산 계속 | 버전 바뀌면 못 읽을 수 있음 → 둘 다 보관 |
실행 결과(톨루엔 50 · 9,000스텝): log 13 KB · prod.lammpstrj 87 KB(1,000스텝마다) · final.data 171 KB · final.restart 209 KB.

## 3. 4단계 프로토콜 표 (원본 04#25 · #36)
| 단계 | 설정 | 목적 · 판정 | 권장 조건 |
|---|---|---|---|
| ① 최소화 | `minimize 1e-4 1e-6 5000 50000` | 겹침 제거 · 최대 힘이 유한값으로 수렴 | 겹침 심하면 soft 포텐셜로 먼저 |
| ② 어닐링 | NPT 600 → 298 K · 1 ns | 초기 배치 의존성 제거 | 분해 온도 아래(바인더 ≤ 600 K) · 냉각률 ≤ 0.5 K/ps |
| ③ 평형화 | NPT 298 K · 2 ns | 밀도 · 부피 추세 소멸 (W05 기준) | 밀도 변화 < 0.5 %/ns → 통과 |
| ④ 생산 | NPT · NVT 2 ~ 10 ns | 물성 샘플링 · 이 구간만 통계 | 밀도 · CED 2 ns · 점도 10 ns 이상 · 시드 3 |
조합: 평형 구조를 다른 온도로 → 어닐링 생략 · 점도 = NPT 평형 후 NVT 생산 · 계면 = aniso 한 단계 더 · Tg = 냉각률 여러 개. 벌크 셀 절차: 조성 → 개수(5만~10만 원자) → ρ0 0.2 상자 → 최소화 + 짧은 NVT → NPT.
톨루엔 실제 실행(mdai · 최소화 973스텝 E 993 → −276 kcal/mol · NPT 6 ps 밀도 0.200 → 0.309 · 1 ns ≈ 39 분/코어): 6 ps 는 압축 중이라 ③ 의 기준을 통과하지 못한다. 그래서 2 ns.

## 4. 힘장 → pair_style 표 (원본 04#18 · #19)
| 힘장 | pair_style | special_bonds | 비고 |
|---|---|---|---|
| GAFF2 · AMBER | `lj/cut/coul/long 12.0` | `amber` (lj 0 0 0.5 · coul 0 0 0.8333) | 이 강좌 기준 · `pair_modify mix arithmetic tail yes` |
| OPLS-AA | `lj/cut/coul/long 12.0` | `lj/coul 0 0 0.5` | mix geometric |
| COMPASS · PCFF | `lj/class2/coul/long 12.0` | `lj/coul 0 0 1` | Class II · 9-6 |
| ClayFF (계면) | `lj/cut/coul/long` + `hybrid/overlay` | 유기 쪽 규약 | W08 · W10 · `kspace_modify slab 3.0` |
pppm 1e−4 = 상대 힘 오차 · 벌크 표준. 컷오프 10 → 14 Å 는 실공간 비용 ↑ · 역공간 격자 성김 → 총 비용 최소점. 컷오프 · 정확도는 데이터셋 전체 고정.

## 5. 구간별 셀 변화 (원본 04#20 · #23 · squalane 100 + DOCHN 100)
M = 100 × 422.8 + 100 × 406.7 = 82,950 g/mol · ρ = M/(0.60221·L³): ④ 최소화 L 62 Å → 0.58 g/cm³(상자 불변) · ⑤ NPT 압축 L 55 → 0.83(폐기) · ⑥ 생산 L 54 → 0.87(이 구간만 평균). density.txt 200개 값 → 후반 평균 ≈ 0.89 · 블록 표준편차 = 오차. 확인 순서: T · P 설정값 주위 → 밀도 평탄 → 전 · 후반 차 0.5 % 이내.

## 6. data 파일 예: 메탄 CH₄ 1분자 (원본 04#28 · #29)
```
5 atoms / 2 atom types / 4 bonds / 1 bond types / 0.0 78.42 xlo xhi (y · z 같음)
Masses: 1 12.011 (c3) · 2 1.008 (hc)
Atoms # full: id mol type q x y z — 1 1 1 -0.108 0 0 0 · 2 1 2 0.027 0.63 0.63 0.63 …
Bonds: id type atom1 atom2 — 1 1 1 2 · 2 1 1 3 …
```
atom type · bond type 번호는 임의 · 의미는 그 번호에 붙는 계수가 결정 · C–H 와 C–C 는 다른 bond type. 원본 binderA.data 는 같은 형식이 98,304 atoms · 68 atom types · 105.82 Å.

## 7. 설치 규칙 4 (원본 04#7 · #8 · #9)
CPU 전용 · MPI 없음(laptop 프로필) · 설치 실패 1순위가 conda MPI 와 시스템 MPI 혼용 · 버전은 학기 중 올리지 않고 실험 ID 에 빌드 종류 기록 · Windows 는 WSL2 Ubuntu 안에서만(저장소는 WSL 홈) · 소스 빌드(cmake · PKG_MOLECULE · KSPACE · RIGID)는 선택 → `install_gpu.md`.
mdai 환경(2026-11-08 확인): LAMMPS 22 Jul 2025 Update 6 · 설치 패키지에 MOLECULE · KSPACE · RIGID · EXTRA-DUMP · REAXFF 포함.

강좌 환경 = 저장소 맨 위 `environment.yml` 의 mdai(`conda env create -f environment.yml` · 처음 1회 · `lammps` · `packmol` 포함). LAMMPS 는 이 환경의 `lmp` 를 터미널에서 실행한다(Claude Code 가 `lmp -in …` 을 승인 후 실행하고 log 를 읽는다). 확인 2줄: `lmp -h | grep -A3 "Installed packages"` · `lmp -in in.lj` → `Total wall time`.

이전 덱 5장의 버전 고정 설치 명령(보존 · 2026-11-14 Claude Code 전환 때 덱에서 옮김 · conda-forge 2026-09 확인):
```bash
conda create -n mdai -c conda-forge python=3.11 \
  "lammps=2025.07.22=cpu_py311*nompi*" \
  packmol=21.2.1 rdkit ambertools
conda activate mdai
```
판 이름의 `nompi` = MPI 없는 빌드. 이미 `environment.yml` 로 mdai 을 만들었다면 같은 이름으로 다시 만들지 않는다(필요하면 다른 이름 `-n mdai_pin`).

(선택) Colab 을 쓸 때: 노트북 01 · 02 의 첫 셀이 Colab 에서만 condacolab 을 깔고 위 고정 판 `lammps` · `packmol` 을 설치한다(약 3분 · 로컬에서는 설치하지 않음). 안내 `../../docs/colab_quickstart.md`.

## 8. 원본 04주차의 프롬프트 장 (04#11 · #12 · #26)
설치 요청 · 스크립트 요청 프롬프트는 이 강좌에서 P6-1 · P6-2(`../prompts.md`)로 대체했다. 설치 자체는 mdai 환경(덱 5장 · `environment.yml`)으로 끝나므로 설치 요청 프롬프트는 두지 않는다. `lmp` 를 찾지 못하면 Claude Code 에 원인 · 조치를 묻고 승인 후 실행한다.
