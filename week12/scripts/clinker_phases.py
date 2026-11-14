#!/usr/bin/env python3
"""클링커 4상 조성(질량 %) → 완전 수화 시 생성물 · 소요 질량 (클링커 100 g 기준).
  python3 scripts/clinker_phases.py [--c3s 55 --c2s 18 --c3a 10 --c4af 8] [--json out/hydration_products.json]
반응식(시멘트 화학 표기 · C = CaO · S = SiO2 · A = Al2O3 · F = Fe2O3 · S̄ = SO3 · H = H2O):
  2 C3S + 6 H → C3S2H3 + 3 CH            2 C2S + 4 H → C3S2H3 + CH
  C3A + 3 CS̄H2 + 26 H → C6AS̄3H32          C4AF + 2 CH + 10 H → C3AH6 + C3FH6
출처: Mindess · Young · Darwin, Concrete 2판 · Taylor, Cement Chemistry 2판 (원본 08주차 덱 12장).
가정: 석고 충분 · C3A 전량 에트린자이트 · C-S-H = C3S2H3 이상화(실제 Ca/Si ≈ 1.7 · 물 함량 가변) · 완전 수화 · 나머지 질량 불활성.
"""
import argparse, json
M = dict(C=56.077, S=60.084, A=101.961, F=159.688, SO3=80.063, H=18.015)      # g/mol · 산화물 표준 원자량
def mm(**k): return sum(M[a] * n for a, n in k.items())
MM = {'C3S': mm(C=3, S=1), 'C2S': mm(C=2, S=1), 'C3A': mm(C=3, A=1), 'C4AF': mm(C=4, A=1, F=1),
      'CSH2': mm(C=1, SO3=1, H=2), 'C3S2H3': mm(C=3, S=2, H=3), 'CH': mm(C=1, H=1), 'AFt': mm(C=6, A=1, SO3=3, H=32),
      'C3AH6': mm(C=3, A=1, H=6), 'C3FH6': mm(C=3, F=1, H=6), 'H': M['H']}
def hydrate(c3s=55, c2s=18, c3a=10, c4af=8, clinker_g=100.0):
    n = {k: clinker_g * p / 100 / MM[k] for k, p in (('C3S', c3s), ('C2S', c2s), ('C3A', c3a), ('C4AF', c4af))}
    csh = n['C3S'] / 2 + n['C2S'] / 2                          # mol C3S2H3
    ch_made = 1.5 * n['C3S'] + 0.5 * n['C2S']; ch_used = 2 * n['C4AF']
    aft = n['C3A']; gyp = 3 * n['C3A']; hyd = n['C4AF']          # mol
    water = 3 * n['C3S'] + 2 * n['C2S'] + 26 * n['C3A'] + 10 * n['C4AF']
    g = lambda mol, k: mol * MM[k]
    out = {'input_wt%': {'C3S': c3s, 'C2S': c2s, 'C3A': c3a, 'C4AF': c4af, 'inert': 100 - c3s - c2s - c3a - c4af},
           'products_g': {'C-S-H (C3S2H3)': g(csh, 'C3S2H3'), 'CH 순생성': g(ch_made - ch_used, 'CH'), '에트린자이트 (C6AS3H32)': g(aft, 'AFt'), 'C3AH6 + C3FH6': g(hyd, 'C3AH6') + g(hyd, 'C3FH6')},
           'consumed_g': {'석고 CSH2': g(gyp, 'CSH2'), '결합수 H2O': g(water, 'H')},
           'ratios': {'결합수/클링커': g(water, 'H') / clinker_g, 'CH 생성 mol': ch_made, 'CH 소비 mol (C4AF)': ch_used, 'CH 순 mol': ch_made - ch_used},
           'molar_mass': MM}
    return out
if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--c3s', type=float, default=55); ap.add_argument('--c2s', type=float, default=18)
    ap.add_argument('--c3a', type=float, default=10); ap.add_argument('--c4af', type=float, default=8); ap.add_argument('--json', default='')
    a = ap.parse_args(); r = hydrate(a.c3s, a.c2s, a.c3a, a.c4af)
    for k, v in r['products_g'].items(): print(f"{k:28s} {v:7.1f} g")
    for k, v in r['consumed_g'].items(): print(f"{k:28s} {v:7.1f} g")
    print(f"결합수/클링커 {r['ratios']['결합수/클링커']:.3f} · CH 순 {r['ratios']['CH 순 mol']:.3f} mol")
    if a.json: json.dump(r, open(a.json, 'w'), indent=1, ensure_ascii=False)
