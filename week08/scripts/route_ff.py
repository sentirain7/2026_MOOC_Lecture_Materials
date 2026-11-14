#!/usr/bin/env python3
"""week08 — FF-neutral 토폴로지 → 힘장별 타입 · 파라미터 라우팅.

FF-neutral 토폴로지(원본 05주차 #22~#24): 원소 · 좌표 · 결합(차수) · 분자 ID · 역할(mineral / water / organic) 만 담고
힘장 타입 · 전하 · ε · σ 는 담지 않는다. 같은 구조에서 힘장별 data 를 각각 만들 수 있다(구조 해시 동일 · 힘장 해시만 상이).

라우팅 규칙(COMID ff_stack.py clayff_gaff2_v1 · 원본 05#27):
  organic → GAFF2(타입 규칙 아래) + AM1-BCC 전하(아티팩트에서 · 없으면 「확인 필요」)
  mineral → ClayFF(Si st · O ob · 전하 +2.1 / −1.05 · week04/data/clayff_lj.csv)
  water   → SPC/E (ClayFF 스택의 짝 물 모델 · TIP3P 는 순수 유기 스택)
  COMPASS(9-6) → 타입 이름만 만들고 blocked (12-6 ↔ 9-6 변환 불가 · 이종쌍 정의 불가)
  ReaxFF → 원소만 · 고정 타입 · 전하 없음(QEq 매 스텝) → 고전 힘장과 한 셀 혼용 불가

GAFF2 타입 규칙(이 강좌의 최소 집합 · 톨루엔 · 메틸페놀 범위): 방향족 C(차수 1.5 결합 2개) ca · sp³ C c3 · 방향족 C 에 붙은 H ha · sp³ C 의 H hc · 히드록시 O oh · O 의 H ho
COMPASS 대응(원본 05#24): ca→c3a · c3→c4 · oh→o2h · ho→h1o · ha→h1 · hc→h1

실행: python3 scripts/route_ff.py data/topology_toluene.json [data/topology_quartz.json data/topology_water.json] → out/routed_<name>.json
"""
import csv, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
GAFF2 = {r["ff_type"]: r for r in csv.DictReader(open(HERE.parent / "week04" / "data" / "gaff2_atom_types.csv"))}
CLAYFF = {r["element"]: r for r in csv.DictReader(open(HERE.parent / "week04" / "data" / "clayff_lj.csv"))}
SPCE = {"O": ("OW", -0.8476, 0.1553, 3.166), "H": ("HW", 0.4238, 0.0, 0.0)}
COMPASS_OF = {"ca": "c3a", "c3": "c4", "oh": "o2h", "ho": "h1o", "ha": "h1", "hc": "h1"}
MASS = {"Si": 28.0855, "O": 15.999, "H": 1.008, "C": 12.011}


def gaff2_type(i, top):
    """i = 0-based index · 결합 목록은 1-based id"""
    me = top["atoms"][i]["id"]; el = top["atoms"][i]["el"]
    nb = [((b if a == me else a), o) for a, b, o in top["bonds"] if me in (a, b)]
    atom = {x["id"]: x for x in top["atoms"]}; idx = {x["id"]: k for k, x in enumerate(top["atoms"])}
    if el == "C":
        return "ca" if sum(1 for _, o in nb if o == 1.5) >= 2 else "c3"
    if el == "O":
        return "oh" if any(atom[j]["el"] == "H" for j, _ in nb) else "os"
    if el == "H":
        j = nb[0][0]; pel = atom[j]["el"]
        if pel == "O": return "ho"
        return "ha" if gaff2_type(idx[j], top) == "ca" else "hc"
    return "?"


def route(top, artifact=None):
    role = top["role"]; atoms = top["atoms"]; rows = []
    art_q = {a["index"]: a["charge"] for a in artifact["atoms"]} if artifact else {}
    for i, a in enumerate(atoms):
        r = {"id": a["id"], "el": a["el"]}
        if role == "organic":
            t = gaff2_type(i, top); g = GAFF2.get(t)
            r["gaff2"] = {"type": t, "eps": float(g["epsilon_kcal_mol"]) if g else None, "sig": float(g["sigma_A"]) if g else None, "q": art_q.get(a["id"], "확인 필요 (AM1-BCC 아티팩트 없음)")}
            r["compass"] = {"type": COMPASS_OF.get(t, "?"), "status": "blocked", "why": "9-6 함수형 · 6제곱 조합 규칙 → 12-6 ClayFF 와 이종쌍 정의 불가"}
            r["reaxff"] = {"type": a["el"], "q": "QEq (매 스텝)", "status": "research_only", "why": "고정 타입 · 전하 없음 → 고전 힘장과 한 셀 혼용 불가 · 영역 분할만"}
        elif role == "mineral":
            c = CLAYFF[a["el"]]; r["clayff"] = {"type": "st" if a["el"] == "Si" else "ob", "eps": float(c["epsilon_kcal_mol"]), "sig": float(c["sigma_A"]), "q": float(c["charge_SiO2_e"])}
            r["compass"] = {"type": "si4z/o2z (PCFF-IFF)", "status": "blocked", "why": "pcff_iff_v1 미구현 · 9-6"}
        elif role == "water":
            t, q, e, s = SPCE[a["el"]]; r["spce"] = {"type": t, "q": q, "eps": e, "sig": s, "note": "ClayFF 스택의 짝 물 모델 · 순수 유기 스택은 TIP3P"}
        rows.append(r)
    return rows


def main():
    files = sys.argv[1:] or [str(HERE / "data" / "topology_toluene.json")]
    for f in files:
        top = json.load(open(f)); art = None
        if top.get("artifact"): art = json.load(open(HERE.parent / top["artifact"]))
        rows = route(top, art)
        out = {"source_topology": Path(f).name, "role": top["role"], "structure_hash": top.get("structure_hash", ""), "n_atoms": len(rows), "n_bonds": len(top["bonds"]),
               "stack": "clayff_gaff2_v1", "routes": rows,
               "type_counts": {}}
        for r in rows:
            for ff in ("gaff2", "clayff", "spce"):
                if ff in r: out["type_counts"].setdefault(ff, {}); out["type_counts"][ff][r[ff]["type"]] = out["type_counts"][ff].get(r[ff]["type"], 0) + 1
        if art:
            mism = [(r["id"], r["gaff2"]["type"], a["ff_type"]) for r, a in zip(rows, art["atoms"]) if r["gaff2"]["type"] != a["ff_type"]]
            out["artifact_check"] = {"artifact": top["artifact"], "type_mismatch": mism, "all_match": not mism}
        p = OUT / f"routed_{Path(f).stem.replace('topology_', '')}.json"; p.write_text(json.dumps(out, ensure_ascii=False, indent=1))
        print(p.name, out["type_counts"], out.get("artifact_check", {}).get("all_match"))


if __name__ == "__main__":
    main()
