# week05 Claude Code 지시: 덱 「만들어 보기」 장의 원문

사용 환경 · 순서 · 규칙: `../docs/prompt_setup.md` · `../docs/claude_code_quickstart.md` (W01 12장). 시작: 터미널 → `conda activate mdai` → `cd week05` → `claude`. 지시 1개 = 대화 1개(주제가 바뀌면 `/clear`). 대괄호 [ ] 안만 바꾼다. 파일은 붙여 넣지 않고 `@경로` 로 가리킨다. 명령 실행 · 파일 생성은 승인 창에서 읽고 승인한다. 결과 = Claude Code 가 `out/P5-n_result.md` 로 저장(저장소 `CLAUDE.md` 규칙). 수치의 「확인 필요」 표시는 지우지 않는다.

## P5-1 · 내 시계열용 평형 판정 · 블록 평균 스크립트 (덱 16장) → `out/P5-1_result.md`
Claude Code 가 노트북 `02_equilibration_stats.ipynb` 를 실행해 `out/block_stats.json` 을 만든다(`python ../run_nb.py notebooks/02_equilibration_stats.ipynb` · 10초). 직접 하려면 `python3 scripts/md_stats.py`. 노트북이 멈추면 이 명령으로 대신한다.
```text
@notebooks/02_equilibration_stats.ipynb 를 python ../run_nb.py 로 실행하고 out/block_stats.json 을 expected_output/ 과 비교해라. 그다음 [@data/T_series_week03.csv] (열 [step, T_K])에 같은 판정을 하는 numpy 스크립트를 out/ 에 새로 만들어 실행해라. ① 이동평균으로 추세가 사라지는 평형 시점 t_eq ② t_eq 이후 전반 · 후반 평균 차 2 SE 이내 검정 ③ 블록 크기 1 · 2 · 5 · 10 · 20 · 50 · 100 · 200 의 블록 평균 SE ④ 자기상관 첫 0 교차까지의 적분 τ_c · N_eff = n / 2τ_c → JSON. 함수 이름은 scripts/md_stats.py 의 equilibration() 과 같게 하고 scripts/ 는 고치지 마라. 두 결과의 차이를 표로 보고하고 「t_eq 이후 n 점 = 독립 표본 N_eff 개 · 보고값 = 평균 ± SE」 한 줄로 끝내라.
```
확인: W03 시계열이면 `expected_output/block_stats.json` 과 비교: t_eq 60 · 블록 SE(100) 2.30 K · τ_c 27.3 · N_eff 17.2. N_eff 가 n 보다 훨씬 작은가(1/55) · 새 스크립트가 t_eq 이전을 폐기하는가 · 블록 SE 가 평탄한 b 를 골랐는가 · 새 스크립트가 `out/` 에 있고 `scripts/md_stats.py` 는 그대로인가(`git status`).

## P5-2 · 내 로그의 실패 유형 판별 표 (덱 23장) → `out/P5-2_result.md`
Claude Code 가 노트북 `01_thermostats.ipynb` 를 실행해 `out/thermostat_sigma.csv` 를 만든다(`python ../run_nb.py notebooks/01_thermostats.ipynb` · 약 2분). 내 LAMMPS 로그가 없으면 대괄호의 로그 경로 부분을 지우고 요동 표만 받는다(W06 이후 로그로 다시).
```text
@notebooks/01_thermostats.ipynb 를 python ../run_nb.py 로 실행하고 out/thermostat_sigma.csv 의 조절기별 σ_T 를 expected_output/ 과 비교해라. 그다음 [@path/to/log.lammps] 의 thermo 출력(Step · Temp · PotEng · TotEng · Press)과 설정(Δt [1 fs] · 조절기 [fix nvt 100] · skin [2.0] · kspace [pppm 1e-4] · 시드 [12345])을 읽고 ① 깨진 시점 ② Temp · TotEng 이 오르는지 ③ NVE 로 재현하면 무엇을 확인해야 하는지 세 질문에 답해라. 실패 4유형(첫 스텝 발산 · 온도 급상승 · NVE 드리프트 · 시드 의존) 중 어느 것인지와 조치 명령을 표로 적되, 조치는 실행하지 말고 제안만 해라. 근거가 로그에 없으면 「확인 필요」로 표시해라.
```
확인: `thermostat_sigma.csv` 의 Langevin σ_T 가 기대 30.6 K 의 ±20 % 안(29.5) · Berendsen 8.8 ≪ 기대 · rescale 0. 판별 표에 세 질문(시점 · T · E · NVE 재현)이 모두 있는가 · 조치가 LAMMPS 명령(또는 설정값)으로 적혔는가 · 조치를 실행하지 않고 제안만 했는가. 전체 표는 `docs/ensemble_notes.md` §7.

## (선택) 채팅형 LLM 으로 쓸 때 · 이전 원문
Claude Code 를 쓸 수 없으면 아래 이전 원문을 채팅창에 붙여 넣고, 대괄호 자리에 파일 내용을 붙인다(`../docs/prompt_setup.md` §5). 노트북은 Colab(`../docs/colab_quickstart.md`) 또는 로컬 JupyterLab 에서 실행한다.

P5-1 이전 원문:
```text
아래는 MD 온도(또는 밀도) 시계열 CSV 의 앞 20줄과 열 이름이다. ① 이동평균으로 추세가 사라지는 평형 시점 t_eq 를 찾고 ② t_eq 이후를 전반 · 후반으로 나눠 평균 차가 2 SE 이내인지 검정하고 ③ 블록 크기 1 · 2 · 5 · 10 · 20 · 50 · 100 · 200 의 블록 평균 SE 와 ④ 자기상관 첫 0 교차까지의 적분 τ_c · N_eff = n / 2τ_c 를 JSON 으로 저장하는 numpy 스크립트를 써라. 함수 이름은 week05/scripts/md_stats.py 의 equilibration() 과 같게 하고, 결과 해석은 「t_eq 이후 n 점 = 독립 표본 N_eff 개 · 보고값 = 평균 ± SE」 한 줄로 끝내라.

열 이름: [step, T_K]
[여기에 CSV 앞 20줄을 붙여 넣는다]
```
P5-2 이전 원문:
```text
아래는 LAMMPS 로그의 thermo 출력 조각(Step · Temp · PotEng · TotEng · Press)과 설정(Δt [1 fs] · 조절기 [fix nvt 100] · skin [2.0] · kspace [pppm 1e-4] · 시드 [12345])이다. ① 깨진 시점 ② Temp · TotEng 이 오르는지 ③ NVE 로 재현하면 무엇을 확인해야 하는지 세 질문에 답하고, 실패 4유형(첫 스텝 발산 · 온도 급상승 · NVE 드리프트 · 시드 의존) 중 어느 것인지와 조치 명령을 표로 적어라. 근거가 로그에 없으면 「확인 필요」로 표시해라.

[여기에 thermo 출력 20~40줄을 붙여 넣는다]
```
