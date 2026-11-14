#!/usr/bin/env python3
"""week08 — FF-neutral 토폴로지 JSON 만들기 (원소 · 좌표 · 결합 차수 · 분자 ID · 역할 — 타입 · 전하 · ε · σ 없음).
  톨루엔: week06/data/Toluene.mol (결합 차수 포함) · 석영: α-quartz 보정 단위셀 1개(결합 = Si–O 2.0 Å 이내) · 물: SPC/E 1분자
실행: python3 scripts/make_topology.py → data/topology_{toluene,quartz,water}.json
"""
import hashlib, json, math, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "scripts")); from stack_cell import QUARTZ, SPCE  # noqa

def shash(atoms, bonds):
    s = json.dumps([[a["el"], a["xyz"]] for a in atoms] + sorted(bonds)); return hashlib.sha1(s.encode()).hexdigest()[:12]

def main():
    D = HERE / "data"; D.mkdir(exist_ok=True)
    L = (HERE.parent / "week06" / "data" / "Toluene.mol").read_text().splitlines(); na, nb = int(L[3][:3]), int(L[3][3:6])
    atoms = [{"id": i + 1, "el": l[31:34].strip(), "xyz": [round(float(l[:10]), 3), round(float(l[10:20]), 3), round(float(l[20:30]), 3)], "mol": 1} for i, l in enumerate(L[4:4 + na])]
    bonds = []
    for l in L[4 + na:4 + na + nb]:
        a, b, o = int(l[:3]), int(l[3:6]), int(l[6:9]); bonds.append([a, b, 1.5 if o == 4 else float(o)])
    # mol 파일의 방향족 결합이 1/2 교대로 적혀 있으면 고리(6원 · 모두 C · 각 C 가 고리 안 결합 2개)를 1.5 로 통일
    ring = {i["id"] for i in atoms if i["el"] == "C" and sum(1 for a, b, o in bonds if i["id"] in (a, b) and {atoms[a-1]["el"], atoms[b-1]["el"]} == {"C"}) >= 2}
    ring = {i for i in ring if sum(1 for a, b, o in bonds if (a in ring and b in ring) and i in (a, b)) == 2}
    for bd in bonds:
        if bd[0] in ring and bd[1] in ring: bd[2] = 1.5
    top = {"role": "organic", "name": "toluene", "atoms": atoms, "bonds": bonds, "artifact": "week06/data/Toluene_gaff2.json", "note": "타입 · 전하 · ε · σ 없음 — 힘장은 route_ff.py 가 붙인다"}
    top["structure_hash"] = shash(atoms, bonds); (D / "topology_toluene.json").write_text(json.dumps(top, ensure_ascii=False, indent=1))
    # 석영 단위셀 (직교 좌표 · 육방 → 데카르트)
    a, c = QUARTZ["a"], QUARTZ["c"]; qa = []
    for i, (el, fx, fy, fz) in enumerate(QUARTZ["atoms"], 1):
        x = a * (fx - 0.5 * fy); y = a * math.sqrt(3) / 2 * fy; z = c * fz; qa.append({"id": i, "el": el, "xyz": [round(x, 3), round(y, 3), round(z, 3)], "mol": 1})
    qb = []
    for i in qa:
        for j in qa:
            if i["el"] == "Si" and j["el"] == "O":
                d = math.dist(i["xyz"], j["xyz"])
                if d < 2.0: qb.append([i["id"], j["id"], 1.0])
    qt = {"role": "mineral", "name": "alpha-quartz unit cell (Levien 1980 · COMID corrected)", "cell": {"a": a, "c": c, "gamma": 120}, "atoms": qa, "bonds": qb, "note": "셀 안 Si–O 결합만 (주기 이미지 결합 제외) · ClayFF 는 비결합 모델이라 결합은 그림용"}
    qt["structure_hash"] = shash(qa, qb); (D / "topology_quartz.json").write_text(json.dumps(qt, ensure_ascii=False, indent=1))
    th = math.radians(SPCE["theta"]); r = SPCE["rOH"]
    wa = [{"id": 1, "el": "O", "xyz": [0, 0, 0], "mol": 1}, {"id": 2, "el": "H", "xyz": [r, 0, 0], "mol": 1}, {"id": 3, "el": "H", "xyz": [round(r * math.cos(th), 3), round(r * math.sin(th), 3), 0], "mol": 1}]
    wt = {"role": "water", "name": "water (SPC/E geometry)", "atoms": wa, "bonds": [[1, 2, 1.0], [1, 3, 1.0]]}; wt["structure_hash"] = shash(wa, wt["bonds"])
    (D / "topology_water.json").write_text(json.dumps(wt, ensure_ascii=False, indent=1))
    print("toluene", len(atoms), len(bonds), "ring", sorted(ring), "| quartz", len(qa), len(qb), "| water 3")

if __name__ == "__main__":
    main()
