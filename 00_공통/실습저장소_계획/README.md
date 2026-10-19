# 깃허브 실습 자료 — 문서 안내

「건설소재 역설계 도구 개발을 위한 AI와 분자동역학 활용」 실습 저장소(DT-Lab)를 만들고 운영하기 위한 문서 모음이다. 모든 문서는 한국어로 되어 있다.

## 문서 목록과 읽는 순서

| 순서 | 문서 | 내용 | 누가 · 언제 |
|---|---|---|---|
| 1 | `INTEGRATED_APP_PLAN.md` | DT-Lab 전체 계획: 3층 직접인장 데이터셋, 주차별 모듈, 이정표, 계산량 | 강의자 · 준비 단계에서 먼저 |
| 2 | `INSTALL_GUIDE.md` | 설치 안내: Linux · macOS · Windows(WSL2), 고정 버전, 사양 프로필, **Packmol 설치 · 판정**, Windows 터미널 주의, 문제 해결 | 강의자 · 수강생 모두, 설치 전에 |
| 3 | `FF_COMPATIBILITY.md` | 힘장 · 원소 · LAMMPS 호환성: 권장 조합(GAFF2 · SPC/E · ClayFF), 대안 비교, 타입 접두어, 검증 사다리 V1~V9 | 강의자 · 구조 생성 전에 |
| 4 | `PROMPTS_STRUCTURE.md` | 구조 생성 프롬프트 S0 ~ S10 (설치 · Packmol · 자체 검사 · 분자 · 물 · 광물 · 벌크 · 물층 · 3층 · 인장 · 캠페인) | 저장소를 만드는 사람 · P00 ~ P08과 함께 |
| 5 | `PROMPTS_APP.md` | 앱 구성 프롬프트 P00 ~ P13 (주차마다 모듈 · CLI · 앱 페이지 · 테스트) | 저장소를 만드는 사람 · 주차 순서대로 |
| 참고 | `GITHUB_PLAN.md` | 강의계획서 GitHub 항목과 주차별 저장 내용 원안(첫 버전) | 강의계획서 대조용. 충돌 시 1번 문서가 우선 |

## 저장소를 만드는 실행 순서 (강의자 · 조교)

1. **설치 환경 결정**: `INSTALL_GUIDE.md` §1에서 운영체제와 프로필(laptop · workstation)을 고른다. Windows면 §4의 WSL2 준비를 먼저 끝낸다.
2. **저장소 뼈대 · 가상환경**: Claude Code에서 새 폴더를 연다. 다음 순서로 실행한다.
   - `PROMPTS_APP.md`의 공통 머리말 + **P00**
   - `PROMPTS_STRUCTURE.md`의 공통 머리말 + **S0 → S0-P → S0-V**
   - 끝나면 `bin/dtlab check-env`와 `bin/dtlab selftest md`가 통과해야 한다.
3. **주차 순서대로 진행**: P01 → P02 → … → P13. 각 P 프롬프트가 지정한 S 프롬프트를 함께 실행한다. 표는 `PROMPTS_APP.md` 첫 부분에 있다.
   - 구조 생성의 실행 순서는 S1 → S2 → S4 → S3 → S5 → S6 → S7 → S8이다. S3는 S4 슬래브 치수를 쓴다.
   - 각 단계의 **완료 기준**을 통과한 뒤 다음으로 넘어간다.
4. **힘장 검증**: S7까지 끝나면 `bin/dtlab selftest ff --level V1..V7`을 실행한다. 실패한 단계가 있으면 `FF_COMPATIBILITY.md` §5 함정 목록부터 확인한다.
5. **기준 캠페인 계산**(개강 전, 늦어도 7주차 전): `bin/dtlab campaign plan` → `materialize` → `submit`. 계산량은 `INTEGRATED_APP_PLAN.md` §3, 4주차 벤치마크로 갱신한다.
6. **세 플랫폼 확인**: Linux · macOS · WSL2에서 `selftest md` · `selftest ff`(V9)를 실행하고 결과를 `data/reference/selftest/`에 둔다.

## 수강생 실행 순서 (요약)

1. `INSTALL_GUIDE.md` §0의 ①~⑦을 따라 설치한다. Windows는 WSL2 Ubuntu 터미널에서 진행하고, 저장소는 `~/` 아래에 둔다.
2. 주차마다 `weekNN/README.md`의 「실행 순서」를 따른다.
3. 주차가 끝나면 `bin/dtlab test NN`, `bin/dtlab check-env --week NN`을 실행하고, 앱(`bin/dtlab-app`)에 새 페이지가 열리는지 확인한다.

## 확인 · 결정이 필요한 사항
- **힘장 수치 확정:** 전하 · LJ · 실라놀 밀도 등은 「검증 대상 기대값」이다. 원 논문과 대조하는 테스트로 확정한다.
- **덱 · 스크립트 수정 여부:** 4-1 GPU/KOKKOS → CPU, 8-4 ML 힘장 → SNAP, 실습 안내 슬라이드(2 · 4 · 6 · 7 · 9 · 10 · 12 · 13주차)를 이 계획에 맞출지 정해야 한다.
- **데이터 공개 범위:** 기준 캠페인 결과를 저장소에 공개할 범위를 정해야 한다.
