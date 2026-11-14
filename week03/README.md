# week03 · 원자 세계와 운동방정식 (모듈 M1 · MD 기초)

| 항목 | 내용 |
|---|---|
| 덱 | `slides/W03_원자세계와운동방정식.html` (v3 · 27장 · 55분 · 4차시) |
| 학습목표 | ① 거시 물성(강성 · 점도 · Tg · 부착 · 강도)을 원자 간 상호작용으로 설명한다 ② MD 의 정의 m d²r/dt² = F 와 4단계 순환(퍼텐셜 → 힘 → 적분 → 기록)을 말한다 ③ 퍼텐셜 에너지 5항(결합 3 + 비결합 2)의 역할을 구분한다 ④ velocity-Verlet 한 스텝을 코드로 쓴다 ⑤ Δt 를 가장 빠른 진동 주기의 1/10 규칙으로 고르고 발산을 에너지 오차로 판정한다 |
| 선수 지식 | 응력–변형률 곡선 · 미분 = 기울기 · Python 5요소 (W02) |
| 소요 시간 | 강의 50분 + 실습 20분 |
| 새 용어 (6) | 원자 · 분자 · 화학 결합 · 퍼텐셜 에너지 · 궤적 · 시간 간격 → `../GLOSSARY.md` |

## Claude Code 지시문 (덱 「만들어 보기」 장)
`prompts.md` · P3-1 거시 물성 → 미시 원인 표(덱 7장) · P3-2 SMILES → 결합 · 각 · 이면각 · 쌍 수(덱 19장) · P3-3 lj_verlet.py 실행 → 질량을 수소로(덱 26장). 사용 환경 = 이 폴더에서 연 Claude Code (`../docs/claude_code_quickstart.md` · `../docs/prompt_setup.md`). 결과 → `out/P3-n_result.md` (Claude Code 가 저장).

## 실습 순서
**시작**: 터미널 → `conda activate mdai` → `cd week03` → `claude`. 노트북은 「`@notebooks/01_lj_pair_verlet.ipynb` 를 실행하고 결과를 요약해」 처럼 지시한다 → 승인 → Claude Code 가 주차 폴더에서 `python ../run_nb.py notebooks/<이름>.ipynb` 로 실행하고 `out/` 결과를 `expected_output/` 과 비교해 보고한다. 그림을 직접 보려면 `jupyter lab` 으로 연다.

1. **01** `notebooks/01_lj_pair_verlet.ipynb` · 탄소 원자쌍 한 스텝(U −0.102 · F −0.0606 · a −2.11e−6 · r 4.00 → 4.01 Å) 재현 → velocity-Verlet 함수 → C–C 결합 Δt 스윕 (10분)
2. **02** `notebooks/02_lj_fluid_nve.ipynb` · numpy LJ 유체 64입자 · 주기 상자 · NVE 1,000스텝 → `out/lj_energy.csv` (10분 · 계산 1~3분)
3. **확인** `out/lj_energy.csv` 의 전체 에너지 드리프트 < 0.1 % (Δt 1 fs)
4. **제출** `lj_energy.csv` · 에너지 그림 1장
5. **선택** `live/verlet_dt.ipynb` · 덱 23장 조작형과 같은 계산 (Δt · 초기 신장 · 총 시간)

스크립트로 한 번에: `python3 scripts/lj_verlet.py` (week03 폴더 · mdai) → `out/` 에 5개 파일 (노트북 01 · 02 와 같은 계산 · P3-3 이 이 명령을 실행).

(선택) Colab 에서 열 때: 노트북 첫 셀의 `google.colab` 분기가 저장소를 받아 week03 으로 이동한다. 이 강좌의 기본 경로는 위의 Claude Code.

## 숫자의 출처
- LJ 탄소: ε 0.109 kcal/mol · σ 3.40 Å · m 12.011 g/mol · 원본 02주차 덱 #8
- C–C 결합: K 478.4 kcal/mol·Å² · r₀ 1.387 Å · 원본 02주차 덱 #16 노트 값 (연구 플랫폼 GAFF2 결과 `Toluene.json` 의 ca–ca 는 354.25 · 1.3986 · 원본 노트 값은 GAFF 1세대)
- 단위 환산 1 (kcal/mol/Å)/(g/mol) = 4.184 × 10⁻⁴ Å/fs² · k_B 0.0019872 kcal/mol/K

## 기대 결과 (`expected_output/`)
| 파일 | 내용 |
|---|---|
| `lj_pair_step.json` | 한 스텝: v½ 0.00999894 · r 4.00999894 · a −2.169e−6 · v 0.00999786 |
| `dt_sweep.json` | 주기 24.3 fs · 안정 한계 7.75 fs · 최대 에너지 오차 0.5 fs 0.4 % · 1 fs 1.7 % · 2 fs 6.7 % · 4 fs 27 % · 8 fs 발산 |
| `lj_fluid_summary.json` | N 64 · L 17.47 Å · 드리프트 −1e−5 · T 평균 213.9 K |
| `lj_energy.csv` | 1,001행 시계열 |

## 체크리스트
- [ ] 노트북 01 셀 1 출력이 `U −0.1024 · F −0.0606 · a −2.111e−06` 과 같다
- [ ] Δt 8 fs 행이 `발산` 이다
- [ ] `out/lj_energy.csv` 드리프트 < 0.1 %
- [ ] 퀴즈 5문항 (`quiz.md`)

## 못 끝냈다면
`expected_output/lj_energy.csv` 를 받고 W04 로 간다. W04 는 이 파일을 읽지 않고 같은 LJ 유체를 다시 만든다.

## 폴더
```
week03/
  README.md
  slides/W03_원자세계와운동방정식.html
  notebooks/01_lj_pair_verlet.ipynb   02_lj_fluid_nve.ipynb
  live/verlet_dt.ipynb                덱 23장 조작형과 같은 계산
  docs/motion_notes.md                덱에서 옮긴 식 · 기호표 · Verlet 7단계 표 (규칙 16)
  scripts/lj_verlet.py                노트북 01 · 02 와 같은 계산 (한 파일)
  data/README.md                      이번 주 입력 데이터 없음 (모든 수치는 스크립트 상수)
  expected_output/                    lj_pair_step.json · dt_sweep.json · lj_fluid_summary.json · lj_energy.csv
  out/                                실행 결과 (git 제외)
  quiz.md
```
