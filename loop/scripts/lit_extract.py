"""① 문헌 → 값 표: Obsidian 볼트의 논문 노트(vault/papers/*.md) → lit_values.csv · 표적 lit_targets.json

노트 형식 = vault/templates/논문노트.md (W02 템플릿 + loop_role)
  머리(YAML): citekey · doi · year · loop_role (target = 표적 · validation = 검증 대조 · none)
  「## 보고 물성」 표: | 물성 | 값 | 단위 | 조건 | 근거 |
읽는 규칙: 물성 이름 밀도 → density(g/cm³) · CED → ced(MJ/m³) · 용해도 매개변수 δ(MPa^0.5) → ced = δ²
          조건에 25 °C 또는 298 K 가 있는 행만 표적 계산에 쓴다 · 값이 비었거나 「미기재」면 건너뛴다 · 근거 칸에 「표적 아님」이면 기록만
표적 = loop_role 이 target 인 행들의 중앙값(튀는 값에 덜 흔들림 · 평균도 함께 기록) · 근거 citekey 목록을 함께 남긴다(실행 노트가 링크)
  python scripts/lit_extract.py [--config config/loop.yaml]
"""
import argparse, csv, re
from pathlib import Path
from common import LOOP, load_cfg, ws, dump

PROP = [(re.compile(r"^밀도|density", re.I), "density", 1.0, "g/cm3"), (re.compile(r"^CED|응집", re.I), "ced", 1.0, "MJ/m3"),
        (re.compile(r"δ|용해도|solubility", re.I), "ced", "square", "MJ/m3")]


def parse(path):
    t = path.read_text(encoding="utf-8"); meta = {}
    m = re.match(r"---\n(.*?)\n---", t, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line: k, v = line.split(":", 1); meta[k.strip()] = v.strip().strip('"')
    sec = re.search(r"## 보고 물성\n(.*?)(\n## |\Z)", t, re.S); rows = []
    if sec:
        for line in sec.group(1).splitlines():
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            if len(c) >= 5 and c[0] not in ("물성", "") and not set(c[0]) <= set("-: "): rows.append(c[:5])
    return meta, rows


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--config"); a = ap.parse_args(); cfg = load_cfg(a.config); w = ws(cfg)
    out, tg = [], {"density": [], "ced": []}
    for p in sorted((LOOP / "vault" / "papers").glob("*.md")):
        meta, rows = parse(p)
        for name, val, unit, cond, ev in rows:
            try: v = float(val.replace(",", ""))
            except ValueError: continue
            for rx, key, conv, u in PROP:
                if rx.search(name):
                    v2 = v * v if conv == "square" else v
                    room = bool(re.search(r"25\s*°?C|298", cond))
                    out.append({"citekey": meta.get("citekey", p.stem), "doi": meta.get("doi", ""), "role": meta.get("loop_role", "none"),
                                "property": key, "value": round(v2, 4), "unit": u, "raw": f"{name} {val} {unit}", "condition": cond, "evidence": ev, "room_T": room})
                    use = meta.get("loop_role") == "target" and room and "표적 아님" not in ev
                    out[-1]["used_for_target"] = use
                    if use: tg[key].append((v2, meta.get("citekey", p.stem)))
                    break
    with open(w / "lit_values.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, list(out[0]) if out else ["citekey"]); wr.writeheader(); wr.writerows(out)
    res = {}
    for k, v in tg.items():
        if not v: raise SystemExit(f"표적 {k} 값이 노트에 없음 · loop_role: target 노트의 「보고 물성」 표를 확인")
        import statistics
        res[k] = {"value": round(statistics.median([x for x, _ in v]), 4), "mean": round(sum(x for x, _ in v) / len(v), 4), "n": len(v), "citekeys": sorted({c for _, c in v}), "values": [round(x, 4) for x, _ in v]}
    dump(res, w / "lit_targets.json")
    print(f"노트 → 값 {len(out)}행 · {w / 'lit_values.csv'}")
    for k, r in res.items(): print(f"  표적 {k}: {r['value']} (n {r['n']} · {', '.join(r['citekeys'])})")


if __name__ == "__main__":
    main()
