# MD 워크플로우 · Claude Code 지시문 M-1 ~ M-6

시작: 터미널 → `conda activate mdai` → `cd 2026_MOOC_Lecture_Materials/mdworkflow` → `claude` · [ ] 안만 바꾼다 · 명령은 승인 뒤 실행 · 결과는 `out/M-n_result.md`

## M-1 · 분자 3D (W04)
```
[톨루엔 · Cc1ccccc1] 의 3D 구조를 python mdwf.py mol 로 만들어라(목록에 없으면 --smiles 와 이름).
ws/mol/<이름>.json 을 읽어 원자 수 · 분자식 · 분자량 · 형식전하 · 입체 중심 수(SMILES 와 3D) · MMFF 수렴을 표로 적고,
수소를 붙이기 전후 원자 수가 왜 다른지 한 줄로 설명해라. → out/M-1_result.md
```

## M-2 · 힘장 만들기와 검사 (W04)
```
python mdwf.py ff [Toluene] 를 실행해라. 이어서 ws/ff/<이름>_gaff2.json 과 ws/ff/<이름>/ 의 로그를 읽고
① 원자별 표(번호 · 원소 · GAFF2 타입 · 전하 q · ε · σ) ② 전하 합과 형식전하 ③ parmchk2 가 빌린 값(ATTN) 개수와 그 의미
④ 결합 · 각 · 이면각 · 비정규 이면각 개수 ⑤ 톨루엔이면 @../week04/data/Toluene_gaff2.json 과 타입 · 전하 · 결합 매개변수 비교
를 적어라. 강좌 스크립트(mdwf/)는 고치지 마라. → out/M-2_result.md
```

## M-3 · 단분자 상자 (W06)
```
python mdwf.py build --id [tol100] --comp [Toluene=100] 으로 상자를 만들어라.
ws/cells/<id>/cell.json 을 읽어 분자 수 · 원자 수 · 초기 밀도 ρ0 · 상자 한 변 L · Packmol 시도 횟수 · 분자간 최소 거리 · 전하 합을 표로 적고,
L = (N·M / (ρ0·N_A))^(1/3) 로 손계산한 값과 비교해라. → out/M-3_result.md
```

## M-4 · 실행과 판독 (W07)
```
python mdwf.py run [tol100] --threads [4] --seed 4928460 을 실행해라(약 5분 · seed = 기준 결과와 같은 값). 끝나면 status.json 과 log.lammps 를 읽어
단계(A 섞기 · B 압축 · C 이완 · D 냉각 · E 평형 · P 생산)마다 끝 온도 · 압력 · 밀도를 표로 적고, 실패 규칙이 쓰였는지 · 벽시계 · 코어 수를 적어라.
오류가 나면 마지막 ERROR 줄과 R1 · R2 중 어느 규칙인지 설명하고 멈춰라. → out/M-4_result.md
```

## M-5 · 밀도 · CED (W09)
```
python mdwf.py analyze [tol100] 를 실행해라. props.json · ced_frames.csv 를 읽어
밀도 ± 표준오차 · 전반/후반 차 · CED ± · δ 를 적고, 실측(톨루엔 0.86238 g/cm³ · CED 332.5 MJ/m³ · NIST)과의 차이를 % 로 계산해라.
차이가 생기는 이유를 힘장 · 짧은 실행 · 크기 측면에서 두 줄로 써라. → out/M-5_result.md
```

## M-6 · 결과 표 (W09 · W13)
```
python mdwf.py store [tol100] --source [nist_toluene] 로 결과를 기록하고 ws/db/results.csv 를 표로 보여 줘라.
같은 id 를 다시 기록하면 왜 거부되는지, 실패한 계산을 지우지 않고 남기는 이유를 한 줄씩 써라. → out/M-6_result.md
```

## 한 번에(③ ~ ⑥)
```
python mdwf.py all --id [tol100] --comp [Toluene=100] --threads [4] 를 실행하고, 끝나면 M-5 와 같은 표를 만들어라.
```
