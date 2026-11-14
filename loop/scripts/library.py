"""② 설계 후보: 「아스팔트 평균 분자」 후보 = 방향족 핵 × 알킬 사슬 수 × 사슬 길이 → SMILES · RDKit 기술자 표.

핵(아스팔트 방향족 · 레진 성분의 단순 모티프): 벤젠 · 테트랄린 · 나프탈렌 · 페난트렌 · 벤조티오펜 · 디벤조티오펜 · 퀴놀린
사슬: 1개 또는 2개(같은 길이) · 탄소 1 ~ 12
기술자(대리모델 입력 · W14 계열): 분자량 MW · 방향족 탄소 비율 fa · H/C · 헤테로 원자 비율 het · 회전 결합 비율 rot
  python scripts/library.py            → ws/<name>/library.csv
"""
import argparse, csv
from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors
from common import load_cfg, ws

CORES = {   # {R1} · {R2} = 사슬 자리 (두 번째 자리는 사슬 2개일 때만)
    "benzene":        ("c1ccc({R1})cc1",                "{R1}c1ccc({R2})cc1"),
    "tetralin":       ("{R1}c1ccc2CCCCc2c1",            "{R1}c1ccc2C({R2})CCCc2c1"),
    "naphthalene":    ("{R1}c1ccc2ccccc2c1",            "{R1}c1ccc2cc({R2})ccc2c1"),
    "phenanthrene":   ("{R1}c1ccc2c(c1)ccc1ccccc12",    "{R1}c1ccc2c(c1)ccc1cc({R2})ccc12"),
    "benzothiophene": ("{R1}c1ccc2sccc2c1",             "{R1}c1ccc2sc({R2})cc2c1"),
    "dibenzothiophene": ("{R1}c1ccc2sc3ccccc3c2c1",     "{R1}c1ccc2sc3ccc({R2})cc3c2c1"),
    "quinoline":      ("{R1}c1ccc2ncccc2c1",            "{R1}c1ccc2nc({R2})ccc2c1"),
}
FEAT = ["MW", "fa", "HC", "het", "rot"]


def enumerate_lib(nmax=12):
    rows = []
    for core, (mono, di) in CORES.items():
        for nch in (1, 2):
            for L in range(1, nmax + 1):
                R = "C" * L
                smi = (mono if nch == 1 else di).format(R1=R, R2=R)
                m = Chem.MolFromSmiles(smi)
                if m is None: raise SystemExit(f"SMILES 오류 {core} {nch} {L}: {smi}")
                mh = Chem.AddHs(m)
                C = sum(a.GetSymbol() == "C" for a in m.GetAtoms()); H = sum(a.GetSymbol() == "H" for a in mh.GetAtoms())
                arom = sum(a.GetSymbol() == "C" and a.GetIsAromatic() for a in m.GetAtoms())
                het = sum(a.GetSymbol() in ("S", "N", "O") for a in m.GetAtoms())
                rows.append({"cand": f"{core}-{nch}x{L}", "core": core, "n_chain": nch, "chain_len": L, "smiles": Chem.MolToSmiles(m),
                             "n_atoms": mh.GetNumAtoms(), "MW": round(Descriptors.MolWt(m), 3), "fa": round(arom / C, 4), "HC": round(H / C, 4),
                             "het": round(het / m.GetNumAtoms(), 4), "rot": round(rdMolDescriptors.CalcNumRotatableBonds(m) / m.GetNumAtoms(), 4)})
    return rows


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--config"); a = ap.parse_args(); cfg = load_cfg(a.config); w = ws(cfg)
    rows = enumerate_lib()
    with open(w / "library.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, list(rows[0])); wr.writeheader(); wr.writerows(rows)
    print(f"후보 {len(rows)}개 → {w / 'library.csv'} · 원자 수 {min(r['n_atoms'] for r in rows)}~{max(r['n_atoms'] for r in rows)} · 분자량 {min(r['MW'] for r in rows):.0f}~{max(r['MW'] for r in rows):.0f}")


if __name__ == "__main__":
    main()
