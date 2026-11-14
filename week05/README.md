# week05 · 앙상블 · 평형화 · 오차 (모듈 M1 · MD 기초)

| 항목 | 내용 |
|---|---|
| 덱 | `slides/W05_앙상블평형화오차.html` (v3 · 24장 · 50.5분 · 3차시) · 식 · 표 보충 = `docs/ensemble_notes.md` |
| 학습목표 | ① NVE · NVT · NPT 의 고정량과 쓰임을 말하고 실무 순서(NPT → NVT)를 설명한다 ② 조절기 4종의 요동 · 왜곡 · 용도를 구분하고 T_damp · P_damp 를 고른다 ③ 평형 판정 절차와 정량 기준 4개를 적용한다 ④ 블록 평균과 자기상관으로 표준오차 · N_eff 를 구한다 ⑤ 실패 4유형을 로그에서 판별한다 |
| 선수 지식 | 온도 정의식 · 궤적의 시간 평균 (W03) · 주기경계 (W04) |
| 소요 시간 | 강의 50분 + 실습 20분 |
| 새 용어 (6) | 앙상블 · 조절기 · 평형화 · 표준오차 · 상관 시간 · 유효 표본 수(블록 평균 포함) → `../GLOSSARY.md` |
| Claude Code 지시 | `prompts.md`: P5-1 평형 판정 · 블록 평균 스크립트(덱 16장) · P5-2 로그 실패 유형 판별 표(덱 23장) → `out/P5-n_result.md` · 사용법 `../docs/prompt_setup.md` · `../docs/claude_code_quickstart.md` |

## 실습 순서
0. **시작** 터미널 → `conda activate mdai` → `cd week05` → `claude` · 노트북은 Claude Code 가 `python ../run_nb.py notebooks/<이름>.ipynb` 로 실행(승인 후 · week05 폴더 기준 경로) · 출력이 노트북에 저장되어 JupyterLab 으로 그림 확인
1. **01** `notebooks/01_thermostats.ipynb`: LJ 유체 64입자 · rescale · Berendsen · Langevin 각 2,000스텝 → σ_T 표 (약 2분)
2. **02** `notebooks/02_equilibration_stats.ipynb`: W03 온도 시계열 → t_eq · 블록 SE(b) · C(τ) · τ_c · N_eff (10초)
3. **확인** Langevin σ_T ≈ 30 K(기대 30.6) · Berendsen ≈ 9 K · 블록 SE 평탄값 ≈ 2.3 K · N_eff ≈ 17
4. **제출** `thermostat_sigma.csv` · `block_stats.json` · 그림 1장
5. **선택** `live/ensemble_2d.ipynb`(덱 5장) · `live/berendsen_tau.ipynb`(8장) · `live/block_average.ipynb`(15장)
6. **지시** P5-1(덱 16장) · P5-2(덱 23장) · `prompts.md` 의 지시를 Claude Code 에 붙여 넣기

노트북 없이 직접: `python3 scripts/md_stats.py` (week05 폴더에서 · numpy 만 필요) → `out/` 에 결과 파일. 노트북이 멈추면 이 명령으로 대신한다.

(선택) Colab 을 쓸 때: 노트북 첫 셀이 저장소를 clone 하고 `week05` 로 이동한다(`../docs/colab_quickstart.md`).

## 숫자의 출처
- 2D 라이브 설정(Δt 0.005 τ · r_c 2.5σ · Berendsen τ_T 0.5 τ · λ 식): 원본 03주차 덱 #25 라이브의 계산 코드 그대로
- fix nvt/npt 인수 · T_damp ≈ 100 Δt · P_damp ≈ 10 T_damp: 원본 03주차 #22 · 조절기 4종: #23 · 압력 식 · iso/aniso/tri: #24
- 평형 기준 4 · 물성별 평형화 길이 · 오판 3: 03#27 · 샘플링 3: 03#28 · C(τ) · N_eff: 03#29 · 실패 4유형: 03#30 · 실무 순서 · 비용: 01주차 #17
- 온도 시계열: `week03/expected_output/lj_energy.csv` (이 폴더 `data/T_series_week03.csv`)

## 기대 결과 (`expected_output/`)
| 파일 | 내용 |
|---|---|
| `thermostat_sigma.csv` | NVE 평균 ≈ 214 K / rescale σ 0 / Berendsen σ 8.8 K · 174스텝 도달 / Langevin σ 29.5 K (기대 30.6) |
| `block_stats.json` | t_eq 60 · 순진한 SE 0.30 K · 블록 SE 100 → 2.30 K · τ_c 27.3 스텝 · N_eff 17.2 |
| `autocorr.csv` | C(τ) 200 지연 · 첫 0 교차 49 스텝 |

## 체크리스트
- [ ] 노트북 01 의 Langevin σ_T 가 기대값의 ±20 % 안
- [ ] 노트북 02 의 블록 SE 가 b 50 이상에서 평탄 · N_eff < 30
- [ ] 라이브 2D 에서 NVE 의 E 가 수평이고 NVT 전환 후 E 가 변한다
- [ ] 퀴즈 5문항 (`quiz.md`)

## 못 끝냈다면
`expected_output/` 의 결과 파일로 W06 으로 간다. W06 은 mdai 환경의 LAMMPS(`lmp`) · Packmol 을 쓴다(`../environment.yml` 에 포함) · 터미널에서 `lmp -h` 로 미리 확인.

## 폴더
```
week05/
  README.md
  slides/W05_앙상블평형화오차.html
  notebooks/01_thermostats.ipynb   02_equilibration_stats.ipynb
  live/ensemble_2d.ipynb  berendsen_tau.ipynb  block_average.ipynb     덱 5 · 8 · 15장과 같은 계산
  scripts/md_stats.py              노트북 01 · 02 와 같은 계산
  data/T_series_week03.csv  README.md
  expected_output/thermostat_sigma.csv  block_stats.json  autocorr.csv
  out/                             실행 결과 (git 제외)
  prompts.md                       P5-1 · P5-2 지시 원문(Claude Code)
  docs/ensemble_notes.md           v1 덱의 식 · 표 · 절차(보존)
  quiz.md
```
