"""MD 워크플로우 (mdwf) — 강좌용 간이 분자동역학 파이프라인.
분자(RDKit) → 힘장(AmberTools GAFF2 · AM1-BCC) → 셀(Packmol) → 실행(LAMMPS) → 물성(밀도 · CED) → 결과 표.
연구 플랫폼의 같은 일을 교육용으로 줄인 것 · 모든 중간 결과가 파일로 남는다.
"""
__version__ = "1.0"
