"""① 분자: SMILES → 수소 추가 → 3D 좌표(ETKDG · seed 고정) → MMFF94 정리 → mol · pdb.

넣는 것: 분자 이름(data/molecules.csv) 또는 --smiles
나오는 것: ws/mol/<이름>.mol (antechamber 입력) · <이름>.pdb (Packmol 입력) · <이름>.json (원자 수 · 분자량 · 형식전하)
틀리기 쉬운 곳: 수소를 안 붙임 · 입체(@ / @@)가 바뀜 · 형식전하 ≠ 0 인데 전하 계산에 0 을 넣음
확인: 원자 수 = 무거운 원자 + 수소 · 입체 중심 수가 SMILES 와 같음 · MMFF 수렴(0)
"""
import argparse, json
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors, rdMolDescriptors
from .common import workspace, molecules, dump


def build(name, smiles, ws, seed=7):
    m = Chem.MolFromSmiles(smiles)
    if m is None:
        raise SystemExit(f"SMILES 를 읽지 못함: {name}")
    n_stereo_in = len(Chem.FindMolChiralCenters(m, includeUnassigned=True, useLegacyImplementation=False))
    mh = Chem.AddHs(m)
    p = AllChem.ETKDGv3(); p.randomSeed = seed
    if AllChem.EmbedMolecule(mh, p) != 0:
        p.useRandomCoords = True
        if AllChem.EmbedMolecule(mh, p) != 0:
            raise SystemExit(f"3D 좌표 생성 실패: {name}")
    conv = AllChem.MMFFOptimizeMolecule(mh, maxIters=5000)
    Chem.AssignStereochemistryFrom3D(mh)
    n_stereo_out = len(Chem.FindMolChiralCenters(mh, includeUnassigned=True, useLegacyImplementation=False))
    out = ws / "mol"
    Chem.MolToMolFile(mh, str(out / f"{name}.mol"))
    pdb = Chem.MolToPDBBlock(mh, flavor=4)   # CONECT 없이 원자 줄만(Packmol 용)
    (out / f"{name}.pdb").write_text("\n".join(l for l in pdb.splitlines() if l.startswith(("HETATM", "ATOM"))) + "\nEND\n")
    info = {"name": name, "smiles": smiles, "seed": seed, "n_atoms": mh.GetNumAtoms(), "n_heavy": m.GetNumAtoms(),
            "formula": rdMolDescriptors.CalcMolFormula(mh), "MW": round(Descriptors.MolWt(mh), 3),
            "formal_charge": Chem.GetFormalCharge(mh), "stereo_centers_smiles": n_stereo_in, "stereo_centers_3d": n_stereo_out,
            "mmff_converged": conv == 0}
    dump(info, out / f"{name}.json")
    return info


def main(argv=None):
    ap = argparse.ArgumentParser(description="분자 3D 만들기 (MD 워크플로우 ①)")
    ap.add_argument("names", nargs="*", help="data/molecules.csv 의 이름 · 비우면 전체")
    ap.add_argument("--smiles", help="목록에 없는 분자: --smiles 와 이름 하나")
    ap.add_argument("--seed", type=int, default=7); ap.add_argument("--ws")
    a = ap.parse_args(argv); ws = workspace(a.ws); lib = molecules()
    if a.smiles:
        todo = [(a.names[0] if a.names else "MyMol", a.smiles)]
    else:
        todo = [(n, lib[n]["smiles"]) for n in (a.names or lib)]
    for n, s in todo:
        i = build(n, s, ws, a.seed)
        print(f"{n:12s} 원자 {i['n_atoms']:4d} · {i['formula']:14s} · M {i['MW']:8.2f} · 전하 {i['formal_charge']} · 입체 {i['stereo_centers_smiles']}→{i['stereo_centers_3d']} · MMFF {'수렴' if i['mmff_converged'] else '미수렴'}")


if __name__ == "__main__":
    main()
