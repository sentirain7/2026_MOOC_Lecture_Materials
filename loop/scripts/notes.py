"""⑥ 환류: 계산 결과를 Obsidian 볼트의 실행 노트로 남긴다 → 그래프에서 문헌 ↔ 후보 분자 ↔ 결과가 이어진다.
  vault/runs/<id>.md      후보 · 물성 · 표적과의 차 · 근거 문헌 [[citekey]] · 라운드 [[링크]]
  vault/rounds/round_k.md 라운드 요약(모델 · 획득함수 · 고른 이유 · 가장 가까운 계산)
"""
from common import LOOP


def run_note(r, rnd, t, tol, lit, why=""):
    d = LOOP / "vault" / "runs"; d.mkdir(parents=True, exist_ok=True)
    cites = sorted(set(lit["density"]["citekeys"] + lit["ced"]["citekeys"]))
    ok = str(r["ok"]) == "True"
    dr = abs(float(r["density_gcm3"]) - t["density"]) if ok else None; dc = abs(float(r["ced_MJm3"]) - t["ced"]) if ok else None
    hit = ok and dr <= tol["density"] and dc <= tol["ced"]
    txt = f"""---
id: {r['id']}
round: {rnd}
candidate: {r['cand']}
smiles: "{r['smiles']}"
density_gcm3: {r['density_gcm3']}
ced_MJm3: {r['ced_MJm3']}
tags: [mdrun, round{rnd}{', hit' if hit else ''}]
---
# {r['id']} · {r['cand']} · 라운드 {rnd}

| 항목 | 값 |
|---|---|
| 후보 분자 | {r['cand']} · `{r['smiles']}` |
| 밀도 | {r['density_gcm3']} ± {r['density_se']} g/cm³ (표적 {t['density']} · 차 {'' if dr is None else round(dr, 4)}) |
| CED | {r['ced_MJm3']} ± {r['ced_se']} MJ/m³ (표적 {t['ced']} · 차 {'' if dc is None else round(dc, 1)}) |
| 두 표적 안 | {'예' if hit else '아니오'} |
| 계산 | 분자 {r['n_mol']} · 원자 {r['n_atoms']} · {r['wall_s']} s · {r['mode']} |

- 근거 문헌: {' · '.join(f'[[{c}]]' for c in cites)}
- 라운드: [[round_{rnd}]]
- 고른 이유: {why}
"""
    (d / f"{r['id']}.md").write_text(txt, encoding="utf-8")
    return hit


def round_note(rnd, cfg, picks, best, summary):
    d = LOOP / "vault" / "rounds"; d.mkdir(parents=True, exist_ok=True)
    prev = f"[[round_{rnd - 1}]] → " if rnd > 0 else ""
    lines = [f"# 라운드 {rnd}", "", f"- 흐름: {prev}이번 → 다음", f"- 모델 {cfg['model']} · 획득함수 {cfg['acquisition']} · 배치 {len(picks)}",
             f"- 고른 계산: {' · '.join(f'[[{p}]]' for p in picks)}", f"- 지금까지 가장 가까운 계산: [[{best}]]", "", summary, ""]
    (d / f"round_{rnd}.md").write_text("\n".join(lines), encoding="utf-8")
