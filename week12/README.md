# week12 · 시멘트: 클링커 · 수화 · ReaxFF · C-S-H (모듈 M3 · 소재 2)

| 항목 | 내용 |
|---|---|
| 덱 | `slides/W12_시멘트.html` (v3 · 4차시 · 12-1 시멘트 콘크리트와 클링커 모델 · 12-2 ReaxFF 수화 · 12-3 C-S-H 구조 · 물성 · 12-4 ML 힘장 대체) |
| 학습목표 | ① 클링커 4상(C₃S · C₂S · C₃A · C₄AF)의 역할과 완전 수화 시 생성물 질량을 계산기로 구한다 ② ReaxFF 가 고전 힘장과 다른 두 가지(결합 차수 연속 · QEq 전하)를 식과 실행 결과로 말한다 ③ ReaxFF 의 비용 · 시간 규모 한계와 온도 가속(사례연구 1)을 설명한다 ④ C-S-H 층상 모델에서 Ca/Si · 층간 물이 설계 변수임을 안다 ⑤ ML 퍼텐셜이 ReaxFF 를 대체하는 흐름과 조건(적용 영역)을 안다 |
| 선수 지식 | W04 힘장 혼용 조건 · W06 LAMMPS in/data · W08 라우팅(ClayFF) · W01 두 재료 |
| 소요 시간 | 강의 50분 + 실습 25분 |
| 새 용어 (6) | 클링커 · 수화 · 결합 차수 · 전하 평형(QEq) · C-S-H · 토버모라이트 → `../GLOSSARY.md` |

## 실행 환경 · Claude Code (기본)
1. 터미널 → `conda activate mdai` → `cd 2026_MOOC_Lecture_Materials/week12` → `claude`. LAMMPS(REAXFF 패키지 · 실행 파일 `lmp`) · Packmol 은 mdai(`../environment.yml`)에 포함 · 설치 · 조작은 `../docs/claude_code_quickstart.md`.
2. 지시 예: 「@notebooks/01_reaxff_portlandite.ipynb 를 실행하고 결과를 요약해」 → Claude Code 가 `python ../run_nb.py notebooks/01_reaxff_portlandite.ipynb` 를 승인 후 실행 → `out/reaxff_summary.json` 을 `expected_output/` 과 비교.
3. 결과는 `out/` 에 그대로 남는다 · 그림을 직접 보려면 `jupyter lab` · 대화는 `claude -c` 로 이어서.
- (선택) Colab: 노트북 01 첫 셀의 설치 주석(condacolab · LAMMPS · Packmol)을 푼다.

## Claude Code 지시 (덱 「만들어 보기」 장)
`prompts.md`: P12-1 내 조성의 수화 생성물 표(8장) · P12-2 ReaxFF 실행 결과 읽기(13장) · P12-3 C-S-H 층 모델 Ca/Si 바꾸기(20장). 지시를 붙여 넣고 [ ] 안만 바꾼다 · 스크립트 실행과 결과 파일 읽기는 Claude Code 가 한다. 결과 = `out/P12-n_result.md`. 사용법 = `../docs/prompt_setup.md`.

## 실습 순서
1. **01** `notebooks/01_reaxff_portlandite.ipynb`: 포틀란다이트 Ca(OH)₂ 슬래브(160원자) + 물 71분자 → ReaxFF 2,000스텝(Δt 0.25 fs · 0.5 ps) → `out/reaxff_summary.json` (결합 차수 · 전하 · thermo) · 1코어 약 40초
2. **02** `notebooks/02_hydration_and_csh.ipynb`: 수화 화학량론 계산기(조성 A · B · 내 조성) · C-S-H 층 모델(Ca/Si 0.83 · 1.0 · 1.5 · 1.7)
3. **확인** `reaxff_summary.json` 의 `frames` 마지막 행(Ca–O_w 결합 수 · 물 O 의 H 개수 분포) · `charges` 처음 · 끝 · `hydration_products.json` 의 결합수/클링커 0.371(조성 A)
4. **제출** `reaxff_summary.json` · `hydration_products.json` · `csh_model.json` · P12-1~3 결과
5. **바꿔 보기** `--steps 8000`(2 ps · 약 3분) · `--nwater 40` · `clinker_phases.py --c3a 15` · `csh_layer_model.py --water 1`

LAMMPS 가 없으면: `expected_output/` 의 같은 이름 파일로 W13 진행(W13 은 이 파일을 읽지 않는다).

## 스크립트
| 파일 | 역할 |
|---|---|
| `scripts/clinker_phases.py` | 4상 wt% → 완전 수화 생성물 · 석고 · 결합수(g) · Mindess · Taylor 표준 반응식 4개 |
| `scripts/reaxff_input.py` | 포틀란다이트 직교 초격자 슬래브(4 × 2 × 2 · P-3m1 a 3.5853 · c 4.895) + Packmol 물 층 → data · in(ReaxFF · QEq) · 실행 · `bonds.reaxff` · `dump.q` 파싱 |
| `scripts/csh_layer_model.py` | 토버모라이트형 층 구성 단위 수 모델 · Ca/Si 목표 → 가교 사면체 제거 수 · 층간 Ca · 평균 사슬 길이 · 층간 물 |
| `data/ffield.reax.cement` | 연구실 보관 ReaxFF(머리글 Si/O/H Fogarty 2010 + Ca · Fe · Cl · Na 확장 · **확장분 출처 미표기 → 확인 필요** · `docs/reaxff_lineage.md` §2) |
| `data/control.reax` | ReaxFF 제어 파일(연구실 페라이트 계 템플릿) |

## 숫자의 출처
- 클링커 4상 wt% 55 · 20 · 10 · 8(W01 14장 · 보통포틀랜드 대표값) · 수화 반응식 4개 · 몰질량 · 예시 조성 A(55 · 18 · 10 · 8) · B(30 · 45 · 4 · 12): 원본 08주차 덱 12장(Mindess · Young · Darwin 2판 · Taylor 2판)
- 결합 차수 파라미터(O–H · Ca–O · Si–O) · 판정 거리 2.8 · 2.2 Å: 원본 08주차 15장 노트 = `data/ffield.reax.cement` 결합 · off-diagonal 항
- ReaxFF 9식: 참조 덱 Part I 14~22장 → `docs/reaxff_equations.md`
- 사례연구 1(Shimelis · Yang · Haider · Yun · Bae, CBM 537 (2026) 147150): 가속 300 → 600 → 1000 K 10 ps · 1300 K 300 ps · ~10⁶배 · Ea 45 kJ/mol(역산) · 결합 생성 C₃S 4.20 · C₃A 2.40 bonds/ps · 알라이트/벨라이트 1.75 · 용출 Ca 1.40 ± 0.08 · 0.60 ± 0.05 · Al 1.30 ± 0.11 ions/ps: 원본 08주차 18~23장
- 사례연구 2(Bae · Kil · Yun · Yang, CBM 489 (2025) 142297) γ_por 1.12e−3 · γ_tob 6.8e−5 · E 입력값: 원본 26~36장 → `docs/case_csh_precipitation.md`
- MLIP 수치(힘 RMSE 2662 → 218 meV/Å · 2000배 · 302 구조 · 115,000 원자) · 비용 10~10³배 · 문헌 분포 93 · 13 · 5편: 원본 38~42장 → `docs/reaxff_lineage.md`
- 덱에 싣지 않은 원본 7장(강도 · 내구성) · 19장(계면 모델 준비 절차 ③④): `docs/original_preserved.md`
- 실행 결과(이 저장소에서 측정 · mdai LAMMPS 22 Jul 2025 · 1코어): `expected_output/reaxff_summary.json`
