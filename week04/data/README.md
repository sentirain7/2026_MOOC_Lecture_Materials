# week04/data
| 파일 | 내용 | 출처 |
|---|---|---|
| `gaff2_atom_types.csv` | GAFF2 원자 타입 32종의 ε (kcal/mol) · σ (Å) · 라이브러리 내 원자 수 · 분자 수 | COMID `data/forcefield_artifacts/organic_gaff2/*.json` 73분자에서 추출 (antechamber · AmberTools GAFF2) |
| `clayff_lj.csv` | ClayFF Si · O · Al · Na 의 σ · ε · SiO₂/Al₂O₃/NaCl 전하 | COMID `data/forcefields/mineral_lj_catalog.yaml` · `mineral_charge_catalog.yaml` (Cygan, Liang & Kalinichev 2004) |
| `Toluene_gaff2.json` | 톨루엔 GAFF2 + AM1-BCC 아티팩트 원본 (원자 15 · 결합 · 각 · 이면각 상수) | COMID `Toluene.json` 사본 |

ε · σ 는 LAMMPS `pair_coeff` 의 σ 규약(r_min 아님). 1-4 축소 · 조합 규칙 · kspace 설정은 `../README.md` 「숫자의 출처」.
