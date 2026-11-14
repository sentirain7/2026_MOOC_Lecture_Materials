# 폐루프 · 「아스팔트 평균 분자」 역설계 (W18 · 최종 프로젝트의 틀)

질문: 아스팔트 바인더를 **한 종류의 단순화 분자(평균 분자)** 로 나타낸다면, 어떤 구조여야 바인더의 **밀도와 CED** 를 동시에 맞추는가.

```
① 문헌     Zotero(서지 · 인용키) → lit/library.bib → Obsidian 논문 노트 vault/papers/ ──lit_extract──▶ 표적 2개
② 설계     후보 분자 표 library.csv (방향족 핵 7 × 사슬 1 · 2개 × 길이 1 ~ 12 = 168) · RDKit 기술자 5개
③ 계산     MD 워크플로우(../mdworkflow): 후보 1종 → 3D → GAFF2 · AM1-BCC → 단분자 상자(약 1,500 원자) → LAMMPS → 밀도 · CED
④ 대리모델  gp(길이 하나 RBF) · rf · xgb 중 선택(불확실성 σ) · 단일 제외 교차검증으로 비교
⑤ 능동학습  체비셰프 EI: 두 표적 중 더 먼 쪽 거리(표적 폭 단위)를 줄일 기대 개선 → 다음 후보 2개 (선택: EHVI · UCB)
⑥ 환류     결과 → vault/runs · vault/rounds 노트(근거 문헌 링크) → 정지 규칙 → 아니면 ③
```

## 실행 (conda activate mdai · 이 폴더에서)
```
python scripts/library.py          # 후보 표
python scripts/lit_extract.py      # 문헌 노트 → 표적
python scripts/loop_step.py        # 한 라운드(재생 모드) · --all = 정지까지 · --mode live = 내 컴퓨터에서 MD
python scripts/surrogate.py compare   # 모델 3종 비교
```
- 설정: `config/loop.yaml` (모드 · 표적 폭 · 모델 · 획득함수 · 배치 · 라운드 · seed)
- 결과: `ws/<이름>/` (library · lit_values · lit_targets · db/loop_results.csv · state.json · ff · cells · runs) · 노트 = `vault/runs` · `vault/rounds`
- Claude Code 지시문: `prompts.md` (L-1 ~ L-8)

## 두 모드와 「같은 결과」
| 모드 | 하는 일 | 같은 결과의 뜻 |
|---|---|---|
| 재생(replay · 기본) | ③ 에서 MD 를 돌리지 않고 기준 결과(`expected_output/`)를 넣는다 · 몇 초 | 라운드별 후보 이름 · 순서 · 표적 거리가 기준과 모두 같다 |
| 실행(live) | ③ 을 내 컴퓨터에서 실제로(후보 하나 약 5분 · 4코어) | 라운드 0 의 6개 후보는 같고, 밀도 · CED 차가 반복 오차 안 · 그 뒤 경로는 MD 값 차이로 갈라질 수 있다 |

## 표적 (2026-11-14 · 문헌 노트에서 자동 추출)
| 표적 | 값 | 근거 | 폭(tol) |
|---|---|---|---|
| 밀도 | 1.018 g/cm³ | 문헌 11편 · 무첨가 바인더 25 °C 실측 22개 중앙값(평균 1.0208) | ±0.02 |
| CED | 354.2 MJ/m³ | 바인더 전체 값 7개 중앙값: 실측 기반 Hansen δt 19.15(Redelius 2004 → Zhu et al. 2019) 1 · MD 문헌(COMPASS · PCFF · COMPASS II) 6 | ±20 |
- 바인더는 증발하지 않아 CED 를 직접 잴 수 없다 → 용해도 시험값과 MD 문헌값을 함께 쓴 이유
- 힘장 검증(../mdworkflow/README.md): GAFF2 는 CED 를 방향족 +6 % · 포화 +21 % 크게 낸다 → 결과 해석에 반영

## 범위와 한계
- 평균 분자 하나는 혼합물의 분포 · 분자 사이 상호작용 차이를 한 분자로 줄인 모델이다(점도 · 노화 · 상분리는 설명 못 함)
- 짧은 프로토콜(130 ps) · 작은 상자(약 1,500 원자) · 한 힘장(GAFF2) → 값은 비교용
