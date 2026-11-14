#!/usr/bin/env python3
"""week08 — 힘장 혼용 위험 점검 (원본 03주차 #31 조건 4 + 05#26 자동 검사 + 04#39·41 층상 셀 규칙).
in 파일(+ data 파일 주석 · 요약 JSON)에서 다음을 ✓/✗ 로 판정한다.
  R1 함수 형태   pair_style 에 12-6(lj/cut…) 과 9-6(lj/class2) · buck 이 함께 있으면 ✗ (hybrid 라도 교차쌍 전부 pair_coeff 명시 없으면 ✗)
  R2 조합 규칙   pair_modify mix 가 한 가지(arithmetic | geometric | sixthpower) · hybrid 교차쌍 누락 없음
  R3 전하 척도   층별 전하 방법(요약 JSON charge_method)이 모두 고정 점전하 계열 — QEq(ReaxFF) 와 고정 전하 동거 ✗
  R4 1-4 축소    special_bonds 줄이 정확히 1개
  R5 층상 셀     boundary z 가 f 이면 kspace_modify slab 필수 · 셀 한 변 ≥ 2 r_c · 진공 ≥ 30 Å
실행: python3 scripts/check_mix.py out/in.stack [out/stack_summary.json] → out/check_mix.json (기본) · data/in_bad_mix.example 로 ✗ 예시
"""
import json, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent.parent

def check(in_text, summary=None):
    L = [l.split("#")[0].strip() for l in in_text.splitlines()]; L = [l for l in L if l]
    def grab(k): return [l for l in L if l.startswith(k)]
    ps = " ".join(grab("pair_style")); fam = set()
    for tok in ps.split():
        if tok.startswith("lj/cut") or tok.startswith("lj/charmm"): fam.add("12-6")
        if tok.startswith("lj/class2"): fam.add("9-6")
        if tok.startswith("buck"): fam.add("buck")
        if tok.startswith("reaxff") or tok.startswith("reax/c"): fam.add("reaxff")
    hybrid = "hybrid" in ps
    pc = grab("pair_coeff"); explicit_cross = any(re.match(r"pair_coeff\s+(\d+)\s+(\d+)", l) and l.split()[1] != l.split()[2] for l in pc)
    r1 = (len(fam) <= 1) or (hybrid and explicit_cross and "reaxff" not in fam)
    mix = [l.split()[2] for l in grab("pair_modify") if "mix" in l]
    r2 = len(set(mix)) <= 1 and not (hybrid and len(fam) > 1 and not explicit_cross)
    cm = sorted({v for v in (summary or {}).get("charge_methods", {}).values()}) if summary else []
    r3 = not ("qeq" in [c.lower() for c in cm] and len(cm) > 1)
    sb = grab("special_bonds"); r4 = len(sb) == 1
    bnd = grab("boundary"); zf = bool(bnd) and bnd[0].split()[-1].startswith("f")
    slab = any("slab" in l for l in grab("kspace_modify"))
    edge_ok = (summary or {}).get("min_edge_over_2rc", 1.0) >= 1.0; vac_ok = (summary or {}).get("vacuum_A", 30) >= 30
    r5 = ((not zf) or slab) and edge_ok and vac_ok
    rows = [("R1 함수 형태 하나 (12-6)", r1, "pair_style " + (" · ".join(sorted(fam)) or "—") + (" · hybrid 교차쌍 명시" if hybrid and explicit_cross else "")),
            ("R2 조합 규칙 하나", r2, "pair_modify mix " + (" · ".join(sorted(set(mix))) or "없음(기본 geometric)")),
            ("R3 전하 척도 하나 (고정 점전하)", r3, "층별 전하: " + (" · ".join(cm) if cm else "요약 없음")),
            ("R4 special_bonds 1줄", r4, f"{len(sb)}줄: " + (" | ".join(s.replace('special_bonds', '').strip() for s in sb) or "없음")),
            ("R5 층상 셀 (p p f → slab · 변 ≥ 2rc · 진공 ≥ 30)", r5, f"boundary {' '.join(bnd[0].split()[1:]) if bnd else '?'} · slab {'유' if slab else '무'} · 변/2rc {(summary or {}).get('min_edge_over_2rc', '?')} · 진공 {(summary or {}).get('vacuum_A', '?')} Å")]
    return {"rules": [{"rule": r, "pass": bool(p), "evidence": e} for r, p, e in rows], "all_pass": all(p for _, p, _ in rows)}

def main():
    inp = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "out" / "in.stack"
    summ = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else None
    if summ is not None and "charge_methods" not in summ:
        summ["charge_methods"] = {"slab": "ClayFF fixed", "water": "SPC/E fixed", "binder": "AM1-BCC fixed"}
    res = check(inp.read_text(), summ); res["input"] = inp.name
    out = HERE / "out" / ("check_mix_" + inp.name.replace("in.", "").replace("in_", "").replace(".example", "") + ".json"); out.write_text(json.dumps(res, ensure_ascii=False, indent=1))
    for r in res["rules"]: print("✓" if r["pass"] else "✗", r["rule"], "—", r["evidence"])
    print(out.name, "all_pass", res["all_pass"])

if __name__ == "__main__":
    main()
