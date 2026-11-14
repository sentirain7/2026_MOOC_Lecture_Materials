# data/ — W13 학습 표

## `bulk_md_373.csv` (373행 · 11열)
COMID 플랫폼의 아스팔트 바인더 벌크 MD 실행 중 `study_type = bulk` · `status = completed` 인 것 전부(GAFF2 · NPT). 한 행 = MD 실행 1회.
강사가 `scripts/export_dataset.py` 로 플랫폼 DB 를 **읽기 전용**으로 열어 한 번 내보냈다. 실행 ID 는 순번(`run`)으로 바꿨고 경로 · 호스트 · 개인 정보는 없다. 수강생은 다시 내보낼 필요가 없다.

| 열 | 뜻 | 단위 · 값 |
|---|---|---|
| run | 실행 순번 | 1 ~ 373 |
| binder | 바인더 모델 | AAA1 367 · AAK1 3 · AAM1 3 |
| aging | 노화 상태 | 0 비노화 · 1 단기 · 2 장기 |
| additive_wt | 첨가제 함량 | wt % |
| h2o | 물 분자 수 | 0 · 100 · 200 · 300 |
| T_K | 온도 | 133 ~ 433 K · 18단계 |
| seed | 속도 초기화 난수 시드 | 22종 |
| cell | 조성 셀 이름 = 그룹 열 | 10종 |
| density | 밀도 | g/cm³ |
| ced | 응집에너지밀도 | MJ/m³ |
| bulk_modulus | 체적탄성률 | GPa |

## 셀 구성
| cell | 행 |
|---|---|
| AAA1-non_aging | 114 |
| AAA1-short_aging | 111 |
| AAA1-long_aging | 111 |
| AAA1-non_aging+w100 · +w200 · +w300 | 각 9 |
| AAK1-non_aging · AAM1-non_aging | 각 3 |
| AAA1-non_aging+SBS_L31_KR · +SBS_R3_S2B9_KR | 각 2 |

## 이 주차의 기본 부분집합 = AAA1 노화 3셀 (336행)
`scripts/common.py` 의 `load(cells="core")`. 셀 3 × 온도 18 × 반복 약 6(일부 조건 9 · 12) = 조건(셀@온도) 54개.
물 · 첨가제 · 다른 바인더 셀은 행 수가 2 ~ 9 로 적어 분할 비교가 잡음에 묻힌다. 전체를 쓰려면 `--cells all`.

같은 조건 반복 간 표준편차 중앙값(MD 반복 오차) — 모델 RMSE 의 바닥:

| 표적 | 값 |
|---|---|
| density | 0.0027 g/cm³ |
| ced | 3.80 MJ/m³ |
| bulk_modulus | 0.436 GPa |
