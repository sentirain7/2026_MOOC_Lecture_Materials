#!/usr/bin/env python3
"""2단계: 강의계획서 기준 번호 정렬 (1회성 변환, 재실행해도 결과가 같도록 작성).

  python3 tools/renumber_step2.py --dry-run   # 바뀌는 조각만 출력
  python3 tools/renumber_step2.py             # 적용
  python3 tools/renumber_step2.py --only "파일명"   # 덱 하나만 (병렬 작업 시 필수)

하는 일
  1. 모든 덱: data-screen-label 을 순번(01, 02 …)으로
  2. 모든 덱: 표지 WEEK 줄, 본강의의 구성 행·구분 슬라이드 시간을 강의계획서 값으로
  3. 예전 강의 순서로 만든 7개 덱: 차시 코드와 본문·노트의 "N주차" 언급을 예전→현재로 변환
  4. 덱별 수작업 치환: 지난 주차 라벨, 다음 주차 예고, 주차 범위 표기 등
내용은 삭제하지 않는다 (STYLE_GUIDE §2.3).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRY = "--dry-run" in sys.argv

syllabus = {w["week"]: w for w in json.loads((ROOT / "tools/syllabus.json").read_text(encoding="utf-8"))["weeks"]}
decks = {d["file"]: d for d in json.loads((ROOT / "tools/decks.json").read_text(encoding="utf-8"))["decks"]}

# 예전 강의 순서의 주차 → 현재 위치 (본문 속 "N주차" 언급 변환용)
OLD_WEEK = {7: "6주차 보충 A", 8: "12주차", 9: "10주차", 10: "10주차 보충 A", 11: "10주차 보충 B", 12: "13주차", 13: "13주차 보충 A"}

# 예전 순서로 만든 덱: 파일 → (예전 주차, 차시 코드 변환, 예전→현재 주차 예외)
SHIFTED = {
    "06주차_보충A_계면 부착 물성.dc.html": (7, lambda k: f"6-S{k}", {}),
    "10주차_강의_기계학습 (2) - 그래프 신경망과 능동학습.dc.html": (9, lambda k: f"10-{k}", {8: "9주차"}),
    "10주차_보충A_대리모델 평가와 불확실성.dc.html": (10, lambda k: f"10-S{k}", {}),
    "10주차_보충B_능동학습과 탐색 전략.dc.html": (11, lambda k: f"10-S{k + 4}", {}),
    "12주차_강의_자율 탐색 파이프라인 (1) - 구조와 데이터 큐레이션.dc.html": (8, lambda k: f"12-{k}", {}),
    "13주차_강의_자율 탐색 파이프라인 (2) - 다목적 최적화·LLM 에이전트·검증.dc.html": (12, lambda k: f"13-{k}", {}),
    "13주차_보충A_플랫폼 통합과 최종 프로젝트.dc.html": (13, lambda k: f"13-S{k}", {}),
}

# 덱별 수작업 치환 (일반 변환 뒤에 적용). (찾을 문자열, 바꿀 문자열)
MANUAL = {
    "01주차_강의_강의 개요 - 멀티스케일 모델링·디지털 트윈과 역설계 패러다임.dc.html": [
        ("다음 주차 — 분자동역학 기초이론: 힘장과 적분 알고리즘", "다음 주차 — 분자동역학 기초이론 (1): 원리와 수치적분"),
    ],
    "03주차_강의_분자동역학 기초이론 (2) - 힘장·전하 모델과 앙상블.dc.html": [
        ("다음 주차 — LAMMPS 시뮬레이션 설정: 입력 스크립트와 재현성 규약", "다음 주차 — LAMMPS 기초와 시스템 구축: 입력 스크립트 · 초기 및 다층구조"),
        ("정리 후 4주차 예고: LAMMPS 실행과 재현성.", "정리 후 4주차 예고: LAMMPS 기초와 시스템 구축."),
    ],
    "04주차_강의_LAMMPS 활용 (1) - 환경 구축·입력 스크립트·초기 및 다층구조.dc.html": [
        ("다음 주차 — 벌크 물성 계산: 밀도 · CED · 용해도 파라미터", "다음 주차 — 자동화 워크플로우와 다중 힘장 스택"),
        ("정리 후 5주차 예고: 벌크 물성 계산.", "정리 후 5주차 예고: 자동화 워크플로우와 다중 힘장 스택."),
    ],
    "06주차_강의_물성 계산·후처리 - 역학·부착·점도·CED.dc.html": [
        ("RECAP · WEEK 04", "RECAP · WEEK 05"),
        (">4주차 산출물<", ">4–5주차 산출물<"),
        ("4주차 평형 궤적이 이번 주차 입력.", "4–5주차에 만든 평형 궤적이 이번 주차 입력."),
        ("8주차 학습 데이터의 첫 라벨", "9주차 학습 데이터의 첫 라벨"),
    ],
    "06주차_보충A_계면 부착 물성.dc.html": [
        ("6주차 보충 A. MD 블록의 마지막. 계면은 공용성과 직결.", "6주차 보충 A. 6주차 물성 계산을 계면으로 확장한다. 계면은 공용성과 직결."),
        (">5~6주차<", ">6주차<"),
        ("6주차 보충 A 정리 · MD 블록 마무리", "6주차 보충 A 정리 · 계면 부착 물성"),
        ("다음 주차 — 데이터 파이프라인과 특징 공학: MD 결과를 학습 데이터로", "다음 주차 — 아스팔트 소재와 바인더 MD"),
        ("MD 블록 마무리. 다음은 데이터 파이프라인.", "계면 부착 보충 마무리. 다음은 7주차 아스팔트 소재와 바인더 MD."),
    ],
    "10주차_보충A_대리모델 평가와 불확실성.dc.html": [
        ("RECAP · WEEK 09", "RECAP · WEEK 10"),
    ],
    "10주차_보충B_능동학습과 탐색 전략.dc.html": [
        ("RECAP · WEEK 10", "RECAP · WEEK 10 · 보충 A"),
        ("10주차 보충 B. 통합 블록 시작. 계산 예산을 어디에 쓸 것인가.", "10주차 보충 B. 계산 예산을 어디에 쓸 것인가."),
        ("다음 주차 — 다목적 최적화와 역설계: 파레토 전선과 EHVI", "다음 주차 — AI 기반 문헌조사와 자동 스크래핑"),
        ("정리 후 13주차 예고: 다목적 최적화.", "정리 후 11주차 예고: 문헌조사와 자동 스크래핑. 다목적 최적화는 13주차."),
    ],
    "10주차_강의_기계학습 (2) - 그래프 신경망과 능동학습.dc.html": [
        ("RECAP · WEEK 08", "RECAP · WEEK 09"),
    ],
    "12주차_강의_자율 탐색 파이프라인 (1) - 구조와 데이터 큐레이션.dc.html": [
        ("12주차. ML 블록의 시작. 데이터가 없으면 학습도 없다.", "12주차. 자율 탐색 블록의 시작. 데이터가 없으면 학습도 없다."),
        ("RECAP · WEEK 02–07", "RECAP · WEEK 02–08"),
        ("5~7주차 결과를", "6~8주차 결과를"),
        ("다음 주차 — 그래프 신경망 기초: 분자 그래프와 메시지 패싱", "다음 주차 — 자율 탐색 파이프라인 (2): 다목적 최적화와 역설계"),
        ("정리 후 10주차 예고: GNN.", "정리 후 13주차 예고: 다목적 최적화와 역설계."),
    ],
    "13주차_강의_자율 탐색 파이프라인 (2) - 다목적 최적화·LLM 에이전트·검증.dc.html": [
        ("RECAP · WEEK 11", "RECAP · WEEK 10–12"),
    ],
    "13주차_보충A_플랫폼 통합과 최종 프로젝트.dc.html": [
        ("RECAP · WEEK 01–12", "RECAP · WEEK 01–13"),
        # 통합 구조 도식: 모듈 → 담당 주차
        (">3주차</text>", ">3–4주차</text>"),
        (">4주차</text>", ">4–5주차</text>"),
        (">5–7주차</text>", ">6–8주차</text>"),
        (">8주차</text>", ">12주차</text>"),
        (">11–12주차</text>", ">10·13주차</text>"),
    ],
}

changes = []  # (file, before, after)


def sub(pattern, repl, text, file, flags=0):
    def f(m):
        new = repl(m) if callable(repl) else m.expand(repl)
        if new != m.group(0):
            changes.append((file, m.group(0), new))
        return new
    return re.sub(pattern, f, text, flags=flags)


def process(file, meta):
    path = ROOT / file
    t = path.read_text(encoding="utf-8")
    orig = t
    week, supp = meta["week"], meta.get("supplement")
    syl = syllabus[week]

    # 3. 예전 순서 덱: 차시 코드 · 주차 언급
    # 재실행 안전: 표지가 아직 예전 주차(WEEK 예전 · 차시)일 때만 변환
    if file in SHIFTED and re.search(rf"WEEK {SHIFTED[file][0]:02d} · 차시", t):
        old, code, override = SHIFTED[file]
        wmap = {**OLD_WEEK, **override}
        t = sub(rf'data-label="\[{old}-(\d+)\] 섹션"', lambda m: f'data-label="[{code(int(m.group(1)))}] 섹션"', t, file)
        t = sub(rf">{old}-(\d+)(<| · )", lambda m: f">{code(int(m.group(1)))}{m.group(2)}", t, file)
        # "N주차" (범위 표기 N~M주차 · N–M주차 의 뒤쪽 숫자는 건드리지 않음)
        t = sub(r"(?<![\d~–])(\d+)주차(?! 보충)", lambda m: wmap.get(int(m.group(1)), m.group(0)), t, file)

    # 4. 수작업 치환
    for a, b in MANUAL.get(file, []):
        if b in t:  # 이미 적용됨
            continue
        if a in t:
            changes.append((file, a, b))
            t = t.replace(a, b)
        else:
            print(f"  ! 치환 대상 없음: {file[:30]} 「{a[:50]}」")

    # 2. 표지 WEEK 줄
    codes = [s["code"] for s in syl["sessions"]]
    if supp:
        div_codes = re.findall(rf'data-label="\[({week}-S\d+)\] 섹션"', t)
        m = re.search(r"WEEK \d+ · [^<]*?(\d+)분", t)
        mins = m.group(1) if m else "45"
        line = f"WEEK {week:02d} · 보충 {supp} · 차시 {div_codes[0]} ~ {div_codes[-1]} · {mins}분"
    else:
        line = f"WEEK {week:02d} · 차시 {codes[0]} ~ {codes[-1]} · {syl['minutes']}분"
    t = sub(r"WEEK \d+ · (?:보충 [AB] · )?차시 [^<]*", lambda m: line, t, file)
    t = sub(r'(data-label="표지"[^>]*data-speaker-notes="[^"]*?)총 \d+분', lambda m: f"{m.group(1)}총 {syl['minutes']}분" if not supp else m.group(0), t, file)

    # 2. 본강의 시간: 구성 행 · 구분 슬라이드
    if not supp:
        mins = {s["code"]: s["minutes"] for s in syl["sessions"]}
        t = sub(r'(>(\d+-\d+)</div>\s*<div[^>]*>(?:(?!</div>).)*</div>\s*<div[^>]*>)(\d+)분(</div>)',
                lambda m: f"{m.group(1)}{mins.get(m.group(2), m.group(3))}분{m.group(4)}", t, file, re.S)

        def fix_divider(m):
            sec = m.group(0)
            c = m.group(1)
            if c not in mins:
                return sec
            return re.sub(r'(<p style="[^"]*">)(\d+)분', rf"\g<1>{mins[c]}분", sec, count=1)
        t = sub(r'<section data-label="\[(\d+-\d+)\] 섹션".*?</section>', fix_divider, t, file, re.S)

    # 1. data-screen-label 순번
    n = [0]

    def renum(m):
        n[0] += 1
        return f'{m.group(1)}data-screen-label="{n[0]:02d}"'
    t = sub(r'(<section\b[^>]*?)data-screen-label="[^"]*"', renum, t, file)

    if t != orig and not DRY:
        path.write_text(t, encoding="utf-8")
    return t != orig


def main():
    only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
    if only and only not in decks:
        sys.exit(f"decks.json 에 없는 파일: {only}")
    touched = [f for f, meta in decks.items() if (not only or f == only) and process(f, meta)]
    by_file = {}
    for f, a, b in changes:
        by_file.setdefault(f, []).append((a, b))
    for f, lst in by_file.items():
        sl = sum(1 for a, _ in lst if "data-screen-label" in a)
        print(f"── {f}  ({len(lst)}건, 이 중 screen-label {sl}건)")
        for a, b in lst:
            if "data-screen-label" in a:
                continue
            short = lambda s: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "‹›", s))[:90]
            print(f"   {short(a)}\n → {short(b)}")
    print(f"\n{'[dry-run] ' if DRY else ''}변경 덱 {len(touched)}개")


if __name__ == "__main__":
    main()
