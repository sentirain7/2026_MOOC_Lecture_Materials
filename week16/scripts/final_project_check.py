#!/usr/bin/env python3
"""W16 · 최종 프로젝트 제출 폴더 점검 — 평가 5항목(원본 13주차 보충A #23 배점)마다 필요한 파일 · 필드를 확인해 체크리스트를 만든다.
점수는 「요건 충족 여부」만 본다(내용의 질은 발표에서 평가).

  python3 scripts/final_project_check.py out/example_project --out out/checklist.json
제출 폴더 = problem.json · protocol.json · pareto.json · recommendations.csv · validation.json · run_manifest.json · limits.md · slides/(≤ 10장)
"""
import argparse, csv, json, os, re

ap = argparse.ArgumentParser(); ap.add_argument("proj"); ap.add_argument("--out", default="out/checklist.json"); a = ap.parse_args()
P = lambda *x: os.path.join(a.proj, *x)
def J(n):
    try: return json.load(open(P(n), encoding="utf-8"))
    except Exception: return None
items = []
def add(group, pts, name, ok, why): items.append(dict(group=group, points=pts, item=name, ok=bool(ok), evidence=why))

pr = J("problem.json") or {}
tg = pr.get("targets", [])
add("문제 정의", 8, "표적 물성 2개 이상 · 방향 지정", len(tg) >= 2 and all(t.get("direction") in ("max", "min", "range") for t in tg), f"targets {len(tg)}")
add("문제 정의", 6, "제약 명시", len(pr.get("constraints", [])) >= 1, f"constraints {len(pr.get('constraints', []))}")
add("문제 정의", 6, "성공 기준 수치", bool(pr.get("success")), str(pr.get("success", ""))[:60])
pc = J("protocol.json") or {}
add("계산 · 검증 설계", 10, "프로토콜(힘장 · 앙상블 · 길이)", all(k in pc for k in ("forcefield", "ensemble", "length")), ",".join(pc.keys())[:60])
add("계산 · 검증 설계", 10, "오차 보고 방식(평균 ± SE · n)", "error_report" in pc, str(pc.get("error_report", ""))[:60])
va = J("validation.json") or {}
add("계산 · 검증 설계", 10, "분할 전략 · 실측 대조", "split" in pc and ("density" in va or "tg" in va), f"split={pc.get('split','-')} · validation keys {list(va)[:3]}")
pa = J("pareto.json") or {}
add("탐색 결과", 8, "파레토 전선 · HV", "front" in pa and "hv" in pa, f"front {len(pa.get('front', []))} · HV {pa.get('hv')}")
add("탐색 결과", 7, "회차별 HV 곡선", len(pa.get("trajectory", [])) >= 3, f"trajectory {len(pa.get('trajectory', []))}")
rc = list(csv.DictReader(open(P("recommendations.csv"), encoding="utf-8"))) if os.path.exists(P("recommendations.csv")) else []
add("탐색 결과", 10, "추천 조성 ≥ 3 · 예측 ± 불확실성", len(rc) >= 3 and all(r.get("sd_K") and r.get("sd_CED") for r in rc), f"rows {len(rc)}")
mf = J("run_manifest.json") or {}
add("재현성", 10, "매니페스트 4묶음(코드 · 데이터 · 모델 · 실행)", all(k in mf for k in ("code", "data", "model", "run")), ",".join(mf.keys()))
add("재현성", 5, "데이터 해시 · 난수 시드", bool(re.search(r"[0-9a-f]{8}", json.dumps(mf.get("data", {})))) and "seed" in json.dumps(mf.get("model", {})), "sha256 · seed")
lm = open(P("limits.md"), encoding="utf-8").read() if os.path.exists(P("limits.md")) else ""
add("한계 논의", 5, "한계 3개 이상(모델 · 힘장 · 데이터)", lm.count("\n- ") >= 3, f"bullets {lm.count(chr(10) + '- ')}")
add("한계 논의", 5, "실패한 시도와 원인", "실패" in lm, "「실패」 절" if "실패" in lm else "없음")
sl = [f for f in os.listdir(P("slides"))] if os.path.isdir(P("slides")) else []
add("발표 형식", 0, "슬라이드 1~10장(10분 + 질의 5분)", 1 <= len(sl) <= 10, f"slides {len(sl)}")
score = sum(i["points"] for i in items if i["ok"]); total = sum(i["points"] for i in items)
res = dict(project=a.proj, score=score, total=total, items=items, rubric={"문제 정의": 20, "계산 · 검증 설계": 30, "탐색 결과": 25, "재현성": 15, "한계 논의": 10})
json.dump(res, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for i in items: print(("✓" if i["ok"] else "✗"), f"[{i['group']} {i['points']}] {i['item']} — {i['evidence']}")
print(f"요건 충족 {score} / {total}")
