# week11 · 아스팔트: 혼합물 · PG · SARA 모델 · 첨가제 · 노화 MD (모듈 M3 · 물성 · 소재)

| 항목 | 내용 |
|---|---|
| 덱 | `slides/W11_아스팔트.html` (v3 · 4차시 · 11-1 혼합물과 바인더 특성 · 11-2 SARA 모델과 13분자 · 11-3 첨가제 라이브러리 · 11-4 노화와 점탄성 지표) |
| 학습목표 | ① 바인더의 성능 3(소성변형 · 저온 균열 · 수분 손상 · 노화)과 PG 등급(PG 64-22)을 모델의 표적으로 쓴다 ② SARA 4분획(용해도 기준)과 Li & Greenfield 12분자 + 고황 1 의 역할을 말하고, 측정 SARA wt% → 13분자 개수를 스크립트로 역산한다 ③ 첨가제 23종을 SMILES · RDKit 기술자(MW · logP · TPSA · 방향족 분율)로 표현한다 ④ 노화 = 조성 치환(U → S → L 변이 분자) 의 구조 변화를 숫자로 읽고, 점탄성 · 점착 지표의 MD ↔ 실험 대응 한계(시간 창)를 안다 |
| 선수 지식 | W01 두 재료 · W04 GAFF2 타입 · W06 Packmol · 개수 역산 · W08 라우팅 |
| 소요 시간 | 강의 50분 + 실습 20분 |
| 새 용어 (5) | SARA 분획 · 콜로이드 모형 · PG 등급 · 분자 기술자(descriptor) · 조성 치환 노화 → `../GLOSSARY.md` |

## 실행 환경 · Claude Code (기본)
1. 터미널 → `conda activate mdai` → `cd 2026_MOOC_Lecture_Materials/week11` → `claude`. RDKit · Packmol 은 mdai(`../environment.yml`)에 포함 · 설치 · 조작은 `../docs/claude_code_quickstart.md`.
2. 지시 예: 「scripts/sara_library.py 와 scripts/aging_substitute.py 를 실행하고 out/sara_library.csv 를 expected_output/ 과 비교해」 → 승인 창에서 명령 확인 → 승인.
3. 결과는 `out/` 에 그대로 남는다 · 대화는 `claude -c` 로 이어서.
- 노트북(`notebooks/*.ipynb`)은 같은 스크립트를 부르는 묶음이다. 실행: 「@notebooks/01_sara_library.ipynb 를 실행하고 결과를 요약해」 → Claude Code 가 `python ../run_nb.py notebooks/01_sara_library.ipynb` 를 승인 후 실행(주차 폴더 기준 경로 · 출력은 노트북에 저장).
- (선택) Colab: 노트북 첫 셀의 `google.colab` 분기가 저장소 받기 · RDKit 설치를 한다.

## Claude Code 지시 (덱 「만들어 보기」 장)
`prompts.md`: P11-1 내 바인더의 성능 표적 표 · P11-2 측정 SARA → 13분자 개수표 검토 · P11-3 내 첨가제 SMILES → 기술자 · 힘장 · 함량 표. 지시를 붙여 넣고 [ ] 안만 바꾼다 · 파일은 Claude Code 가 경로로 직접 읽는다. 결과 = `out/P11-n_result.md`. 사용법 = `../docs/prompt_setup.md`(W01 12장).

## 실습 순서
1. **01** `notebooks/01_sara_library.ipynb`: 13분자 라이브러리(SMILES → 분자량 · 원소 · 기술자 · 2D 그림) → 노화 변이 표 (5분)
2. **02** `notebooks/02_composition_and_additives.ipynb`: SARA wt% → 개수 역산 → Packmol 작은 셀 → 첨가제 23종 기술자 표 (10분 · Packmol 1분)
3. **확인** `out/sara_library.csv` 13행 · `out/composition_report_mix.json` 의 `wt_error_pct` 절대값 ≤ 1 · `packmol.success` · `out/additive_library.csv` 23행
4. **제출** `composition_report_mix.json` · `additive_library.csv` · P11-1 ~ P11-3 결과
5. **바꿔 보기** `python3 scripts/composition_to_counts.py --sara 15,45,15,25 --tag asp25 --no-pack` (아스팔텐 15 → 25 wt%) · `--sara 11,32,40,17` (Li & Greenfield AAA-1 의 질량 분율)

Claude Code 없이 직접 실행: `conda activate mdai` 뒤 `python3 scripts/sara_library.py` → `aging_substitute.py` → `composition_to_counts.py` → `additive_library.py` 순서 (RDKit · Packmol = mdai 포함).

## 스크립트
| 파일 | 역할 |
|---|---|
| `scripts/sara_library.py` | `data/sara_molecules.csv`(12분자 U/S/L 32행) + 고황 분자 mol → 분자량 · 원소 · H/C · 방향족 C 분율 · logP · TPSA · 2D SVG |
| `scripts/aging_substitute.py` | 같은 골격 U → S → L 의 O 수 · 분자량 · TPSA 변화 표 (노화 = 조성 치환의 근거) |
| `scripts/additive_library.py` | 연구 플랫폼 첨가제 mol 23종 → SMILES · 기술자 · 군(고분자 · 계면 · 왁스 · 나노) · 힘장 표시 |
| `scripts/composition_to_counts.py` | SARA wt% → 13분자 개수(분획 내 배분 = AAA-1 비율 · 탐욕 ±1 조정) → 원소비 · 상자 길이 → RDKit 3D → Packmol 상자 → 분자간 최소 거리 |

## 숫자의 출처
- 12분자 SMILES · 노화 변이(S = RTFOT 단기 · L = PAV 장기): 연구 플랫폼 `paper_exports/molecule_id_map_20260716.csv` · `data/molecules/asphalt_binder.yaml`: 원전 Li & Greenfield (2014) Table 1
- 고황 13번째 분자 HighS13: 연구 플랫폼 선행 연구 S6422 세트(`paper7_s6422_moles/S6422-AS-HighS13.mol`)
- AAA-1 · AAK-1 · AAM-1 개수표(X1 72 · 60 · 90 분자) · 분획 분율: 같은 yaml(Li & Greenfield 2014 Table 1 · 2026-10-12 보정)
- 첨가제 23종 · 분자량 · 분류: 연구 플랫폼 `data/molecules/additives.yaml` + mol 파일(NanoClay 는 CTAB 형식 오류로 분자량만)
- 바인더 성능 3 · PG 64-22 · RTFO/PAV · G*/sinδ · S · m-value · SARA wt% 범위(S 5~15 · A 30~45 · R 25~35 · As 5~20) · 측정 예(S 11 A 38 R 31 As 20) · 3.6 Å 적층: 원본 07주차 덱 #6~#11 · #19 · #20
- 이 저장소에서 계산한 값(RDKit 2026.09 · Packmol 20.x): 13분자 분자량 · 원소 · 기술자 · 15/45/25/15 wt% → 40분자 3,220원자 · L 53.4 Å(ρ0 0.2) · wt% 오차 ≤ 0.8 · Packmol 분자간 최소 거리 3.297 Å · AAA-1 X1 질량 분율 11.1/31.9/39.7/17.2(개수 분율 11/33/44/11 과 다름) · 노화 ΔMW(L) +14 ~ +98 · O 0 → 최대 7

## 기대 결과 (`expected_output/`)
| 파일 | 내용 |
|---|---|
| `sara_library.csv` · `.json` · `svg/` | 33행(13 비노화 + 20 노화 변이) · 2D 구조 13 |
| `aging_table.csv` | 10 골격의 U → S → L 변화 |
| `additive_library.csv` | 23종 기술자 |
| `composition_report_{mix,asp25,aaa1like}.json` · `mix.inp` · `mix_packmol.log` | 개수 · 오차 · 원소비 · 상자 · Packmol 결과 |
| `mol2d.json` | 덱 그림용 2D 좌표(원자 · 결합) |

## 체크리스트
- [ ] `sara_library.csv` 13 비노화 행 · HighS13 의 S = 3
- [ ] `composition_report_mix.json` 의 `wt_error_pct` 네 값 모두 |오차| ≤ 1 · `packmol.success: true`
- [ ] `additive_library.csv` 에 내 첨가제 1행 추가(P11-3) · ff 열이 비어 있지 않음
- [ ] 노화 표에서 포화분 2종에 변이가 없는 이유 설명
- [ ] P11-1 ~ P11-3 결과 파일 3개 · 퀴즈 5문항

## 13분자 혼합 셀과 W18 「아스팔트 평균 분자」 (2026-11-14 · 18주 과정)
- 이번 주의 13분자 혼합 셀(Li & Greenfield 12분자 + HighS13 · Packmol 상자)은 **조성 · 구조 학습용**이다. LAMMPS 로 계산하지 않는다 · 강좌의 LAMMPS 계산 사례는 단순화 분자 한 종류를 채운 상자(W06 톨루엔 상자 방식 · `../mdworkflow/`)만 쓴다. 12분자 혼합 셀 계산은 `../mdworkflow/README.md` 「확장(강의 밖 · 선택)」.
- W18 폐루프(`../loop/`)는 바인더를 **평균 분자(average molecule) 한 종류**로 나타낸다: 후보 168개 = 방향족 핵 7(벤젠 · 테트랄린 · 나프탈렌 · 페난트렌 · 벤조티오펜 · 디벤조티오펜 · 퀴놀린) × 알킬 사슬 1 · 2개 × 길이 1 ~ 12 · 대리모델 입력 = RDKit 기술자 5개(MW · fa · H/C · het · rot).
- 만드는 법: `../loop/scripts/library.py` · Claude Code 지시문 L-2(`../loop/prompts.md`). 덱 11장 아래 띠.

## 덱에서 뺀 내용
`docs/case_wet_bulk.md`: 원본 07주차 부록 사례연구(물 · 염수 열화 MD · 습윤 벌크 물 군집) · `docs/rheology_notes.md`: 점탄성 식 · 마스터커브 · 실측 대조(W16 에서 다룸)
