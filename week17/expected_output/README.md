# week17 expected_output · 기준 결과 (2026-11-14 · mdai · MD 워크플로우 실제 실행)

조건: LAMMPS 22 Jul 2025 - Update 6 (CPU · OpenMP) · AmberTools 26 · 표준 프로토콜 130 ps(Δt 1 fs · 최소화 → A 10 · B 20 · C 20 · D 20 · E 20 · P 40 ps) · 4코어(tol100_t2 만 2코어) · seed 4928460 · 단분자 상자 약 1,500 원자. 만든 명령 = `../../mdworkflow/mdwf.py` (`all --comp 이름=개수 --threads 4` · seed 1 → LAMMPS seed 4928460). 덱 W17 의 모든 실행 수치의 출처.

| 파일 · 폴더 | 내용 | 덱 |
|---|---|---|
| `Toluene_gaff2.json` | 톨루엔 GAFF2 · AM1-BCC 힘장(강좌 JSON `mdwf-ff-1`) · 원자 15 · 타입 4 · 전하 합 −0.000001 · checks.pass true · ATTN 0 · 결합 15 · 각 24 · 이면각 30 · 비정규 6 · AM1-BCC 0.2 s · W04 `data/Toluene_gaff2.json` 과 타입 · 전하 · 결합 값 같음 | 2 · 9 · 10 · 11 · 13 |
| `Decane_gaff2.json` | n-데칸 힘장 · 원자 32 · 비정규 이면각 0 · AM1-BCC 4.5 s | 12 |
| `validation_results.csv` | 검증 5회의 결과 표(`store.py` 열 24개): tol100 · mnp72 · dec47 · tol100_t2 · tol100_t4b · 밀도 ± · CED ± · δ · 벽시계 | 18 · 23 · 25 |
| `tol100/` | 톨루엔 100분자 · 1,500 원자 · 4코어 · `cell.json`(ρ0 0.5 · L 31.278 Å · 게이트 1번째 시도 · 최소 거리 2.166 Å · Σq −0.0001) · `status.json`(시도 1 · exit 0 · 404.6 s · 프레임 21) · `props.json`(ρ 0.8703 ± 0.0024 · 전반/후반 차 0.72 % · CED 352.3 ± 2.2 · δ 18.77 · 프레임 17 · 분자 크기 6.1 Å) · `ced_frames.csv`(생산 프레임 17개의 E_bulk · Σ E_분자 · V · CED) | 15 · 17 · 19 · 21 · 22 · 25 |
| `tol100_t4b/` | tol100 과 같은 입력 · 4코어 다시 실행 · ρ 0.8724 ± 0.0036 · CED 357.1 ± 3.3 · 461.7 s | 18 · 23 |
| `tol100_t2/` | 같은 입력 · 2코어 · ρ 0.8801 ± 0.0013 · CED 362.6 ± 4.9 · 761.8 s | 18 · 23 · 26 |
| `dec47/` | n-데칸 47분자 · 1,504 원자 · ρ 0.734 ± 0.0014 · CED 303.0 ± 2.0 · 454.0 s · 분자 크기 13.3 Å | 15 · 18 · 23 |
| `mnp72/` | 1-메틸나프탈렌 72분자 · 1,512 원자 · ρ 1.0299 ± 0.0012 · CED 452.9 ± 3.1 · 445.6 s (NIST 밀도 없음 → 참고점) | 15 · 18 · 23 · 24 |
| `candidates/results.csv` | W18 후보 8개 시험(4코어 · 8개 동시 · 430.9 ~ 509.2 s) 결과 표 | 18 · 24 |
| `candidates/<이름>/` | 후보별 `cell.json` · `status.json` · `props.json` (궤적 · 로그는 용량 때문에 제외) | 15 · 24 |

후보 이름 = 핵-사슬 수 x 사슬 탄소 수: naph-1x4 · naph-2x6 (naphthalene) · phen-1x4 (phenanthrene) · dbt-1x2 · dbt-2x6 (dibenzothiophene) · bt-1x6 (benzothiophene) · quin-1x4 (quinoline) · tet-1x8 (tetralin). 분자당 원자 27 ~ 57 · AM1-BCC 8 ~ 57 s.

## 내 결과와 비교하는 법
- 「같은 결과」 = 판정 폭 안: 밀도 ±0.015 g/cm³ · CED ±15 MJ/m³ (반복 흔들림의 약 1.5배 · `../../mdworkflow/README.md`). OpenMP 합산 순서 때문에 같은 seed 라도 비트 단위로 같지 않다.
- 벽시계는 코어 수 · 동시 실행 수에 따라 다르다(검증 3개 동시 405 ~ 454 s · 단독 약 5분 = 455 스텝/s).
- 궤적(`prod.lammpstrj`) · 로그(`log.lammps`)는 용량 때문에 넣지 않았다 → `analyze` 를 다시 하려면 M-4 로 직접 실행한다.
