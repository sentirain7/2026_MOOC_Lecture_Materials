# week09 · 물성 산출: 밀도 · T_g · CED · 용해도 · 점도 · 후처리 자동화 (모듈 M3 · 물성 · 소재)

| 항목 | 내용 |
|---|---|
| 덱 | `slides/W09_물성산출.html` (v3 · 27장 · 54.5분 · 4차시 · 9-1 후처리 개요 · 밀도 · T_g / 9-2 CED · 용해도 / 9-3 점도 · 확산 / 9-4 후처리 자동화 · 오차) |
| 학습목표 | ① 궤적 하나에서 나오는 물성 5 갈래(부피 통계 · 에너지 차 · 자기상관 · 계면 · 공통 규칙)를 말하고 밀도를 평균 ± 블록 SE 로 보고한다 ② CED 를 Method A(직접) · B(간접 차감) 두 경로로 구해 비교하고 δ = √CED 로 상용성을 판정한다 ③ Green–Kubo 러닝 적분의 평탄 구간이 왜 필요한지 곡선으로 설명한다 ④ 후처리 체인(폴더 하나 → 표 한 줄)을 돌리고 flags 열의 뜻을 안다 |
| 선수 지식 | W05 블록 평균 · t_eq · W06 in/data · W08 셀 |
| 소요 시간 | 강의 50분 + 실습 25분(체인 실행 ≈ 5분 · 1코어) |
| 새 용어 (5) | 후처리 · 응집에너지밀도(CED) · 용해도 파라미터(δ) · Green–Kubo 적분 · 유리전이 꺾임(T_g) → `../GLOSSARY.md` |

## Claude Code 지시문 (덱 「만들어 보기」 장)
`prompts.md`: P9-1 density.json → 보고 문장(8장) · P9-2 ced.json → 두 경로 점검 표(14장) · P9-3 results.csv 열 ↔ 내 파일 대응표(26장). 결과 = `out/P9-n_result.md`. 사용 환경 = `../docs/prompt_setup.md`.

## 실행 환경 · Claude Code (기본)
터미널 → `conda activate mdai` → `cd 2026_MOOC_Lecture_Materials/week09` → `claude` (설치 · 조작 = `../docs/claude_code_quickstart.md` · 강좌 규칙 = `../CLAUDE.md` 자동 적용). 덱 지시 상자(= `prompts.md`)를 붙여 넣고 [ ] 안만 바꾼다 → 명령 실행 · 파일 복사는 승인 창에서 확인 → `out/` 결과와 `expected_output/` 비교 보고를 읽는다. 결과 파일은 `out/` 에 그대로 남는다(`git commit` 으로 보관).

## 실습 순서
1. **체인** P9-3 지시(덱 26장) 또는 「`scripts/postprocess_all.py --exp-id toluene50_w09 --lmp lmp` 를 실행하고 결과를 요약해」 → `out/results.csv` · `summary.json` · JSON 4 (LAMMPS 필요 · ≈ 5분). LAMMPS 가 없으면 `expected_output/` 의 로그를 `out/prod` 로 복사해 `--skip-md` 로 후처리만. 같은 체인을 노트북으로: `python ../run_nb.py notebooks/01_postprocess.ipynb` (week09 폴더에서 · 출력이 노트북에 저장 · JupyterLab 으로 열어 확인).
2. **확인** `density.json` 의 half_diff_pct · `ced.json` 의 diff_pct · `viscosity_gk.json` 의 plateau_reached · `tg.json` 의 n_T · 이번 주 실행은 모두 「수렴 전」(flags = short-run;rho-not-converged)
3. **제출** `out/results.csv` · P9-1 ~ P9-3 결과
4. **바꿔 보기** `data/in.prod` 의 `run` 두 줄을 2 ns · 10 ns 로(덱 20장) · `scripts/viscosity_gk.py --tmax 500` (덱 18장 슬라이더와 같은 계산)

Claude Code 없이 터미널에서 직접: `python3 scripts/postprocess_all.py --lmp lmp` (week09 폴더 · mdai · numpy · LAMMPS 22 Jul 2025 또는 유사). Colab 은 선택 경로(노트북 첫 셀 주석).

## 스크립트 (체인 순서)
| 파일 | 역할 | 산출 |
|---|---|---|
| `scripts/run_md.py prod` | W06 final.data → NPT 298 K 30 ps → NVT 20 ps · 응력 xy · xz · yz 5 fs 기록 (`data/in.prod`) | `out/prod/log.prod` · `stress.txt` · `nvt_final.data` |
| `scripts/density_from_log.py` | thermo 블록 → 밀도 시계열 · 누적 평균 · 앞 30 % 폐기 · 블록 10 SE · 전반 · 후반 차 | `density.json` · `density_series.csv` |
| `scripts/ced_method_ab.py` | Method A(벌크 좌표 고정 · 분자 50 run 0) · Method B(기상 분자 1 NVT 20 ps 평균 · 차감) · δ | `ced.json` · `ced_trace.csv` |
| `scripts/viscosity_gk.py` | 응력 자기상관(FFT) → 러닝 적분 η(t) · 성분별 · 평탄 판정 | `viscosity_gk.json` · `gk_curve.csv` |
| `scripts/run_md.py tg` + `scripts/tg_fit.py` | 온도 4점(100 · 175 · 250 · 325 K) × 8 ps NPT → V–T 두 직선 격자 적합 → 교점 | `out/tg/*` · `tg.json` · `vt_points.csv` |
| `scripts/postprocess_all.py` | 위 체인 → `results.csv` 1행(열 = W16 스키마) · `summary.json`(벽시계 · 입력 · 출력) | `results.csv` · `summary.json` |

## MD 워크플로우 연결 (`../mdworkflow` · ⑤ analyze · ⑥ store · 지시문 M-5 · M-6)
`docs/mdworkflow_link.md`: ⑤ analyze = 이번 주 Method A 와 같은 CED 정의(생산 프레임마다 분자를 120 Å 격자로 떼어 LAMMPS rerun 1회) · 밀도 블록 표준오차 · ⑥ store = 계산 1건 = `results.csv` 한 줄(같은 id 거부 · 실패도 `ok=False`) · 힘장 검증 표(톨루엔 · n-데칸 MD vs NIST) · 같은 seed 반복 흔들림(W05 연결). 덱 11 · 22장 아래 줄 · 23장 출처 줄이 이 문서를 가리킨다. 참고 사례(연구 플랫폼 결과)는 CED 를 B 로, MD 워크플로우는 A 로 고정한다.

## 숫자의 출처
- 물성 5 갈래 · 밀도 식 · 수렴 이유 · P(V) · α · T_g 절차 · 냉각률 · CED 정의 · 두 분자 예시(−12.4 kcal/mol · 1.2 nm³ → 71.8 MJ/m³ · δ 8.5) · Method A/B · 숫자 예(−43,490 · −17,820 · 482,000 Å³ → 370 MJ/m³ · δ 19.2) · |Δδ| 판정 3 · Green–Kubo 식 · 설정 · MSD 3구간 · 규칙 5 · 오차 2종 · 시드 표 · 예산 표: 원본 06주차 덱 #6~#28 (전문 = `docs/postprocess_notes.md`)
- 단위 상수: kcal/mol/Å³ → MJ/m³ 6.9477 · GK 7.436e−10 (연구 플랫폼 `src/metrics/viscosity.py`) · CED = E_intra 차감(연구 플랫폼 `src/metrics/ced.py`) · T_g 격자 적합(연구 플랫폼 `src/metrics/tg.py`)
- 이번 주 실행값(덱 2 · 5 · 7 · 8 · 11 · 12 · 14 · 17 · 18 · 20 · 22장 · `expected_output/*.json`): 이 저장소에서 2026-11-08 mdai LAMMPS 22 Jul 2025 · 1코어로 실제 실행 · 수십 ps 라 **수렴 전 · 형태만**(flags 열 기록). 톨루엔 참고 실험값(δ ≈ 18.2 MPa^0.5 · η ≈ 0.56 mPa·s · 298 K)은 「확인 필요」.
