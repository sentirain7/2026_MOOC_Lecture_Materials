#!/usr/bin/env python3
"""C-S-H 층상 개념 모델(토버모라이트형) — Ca/Si 비에 따른 사슬 결손 · 층 구성 · 밀도 추정.
  python3 scripts/csh_layer_model.py [--ca-si 1.7] [--water 2] [--json out/csh_model.json]
모델(교육용 · 결정학 좌표가 아니라 구성 단위 수를 세는 모델):
  층 1개 = Ca–O 주 층(main layer) 7 Ca + 양쪽 실리케이트 사슬 2개(드라이어케텐 dreierkette · 3개 사면체 반복 = 쌍 사면체 2 + 가교 사면체 1)
  + 층간(interlayer) Ca + 층간 물. 토버모라이트 14 Å: 층간격 14 Å · Ca/Si 0.83(완전 사슬) → 가교 사면체 제거 → Ca/Si ↑ · 층간 Ca 추가 → 1.7(C-S-H 평균).
  밀도 추정은 원본 08주차 덱 · Pellenq 외 2009 범위(2.4~2.6 g/cm³) 안에서 층간 물 수에 비례해 보간 → 「확인 필요」 표시.
출처: 토버모라이트 층 구조(Hamid 1981 · Bonaccorsi 2005 · 원본 08주차 덱 25장) · C-S-H Ca/Si ≈ 1.7(Richardson 2008).
"""
import argparse, json
def model(ca_si=1.7, water=2.0, repeat=4):
    """repeat = 드라이어케텐 반복 단위 수(사슬 하나당). 반복 단위 1개 = 사면체 3(쌍 2 + 가교 1)."""
    pair = 2 * repeat * 2          # 쌍 사면체(사슬 2개)
    bridge_full = repeat * 2       # 가교 사면체(완전 사슬)
    ca_main = 7 * repeat // 2 + 1  # 주 층 Ca (대략 Ca:Si_pair = 7:8 → 반복당 3.5)
    # Ca/Si 목표를 맞추기 위해 가교 사면체를 제거하고 층간 Ca 를 더한다
    best = None
    for removed in range(0, bridge_full + 1):
        si = pair + (bridge_full - removed)
        for ca_inter in range(0, 4 * repeat + 1):
            ca = ca_main + ca_inter
            r = ca / si
            if best is None or abs(r - ca_si) < abs(best['Ca/Si'] - ca_si):
                best = {'Ca/Si': round(r, 3), 'Si_total': si, 'pair_tetra': pair, 'bridge_tetra': bridge_full - removed, 'bridge_removed': removed, 'Ca_main': ca_main, 'Ca_interlayer': ca_inter}
    chain_length = (3 * repeat) if best['bridge_removed'] == 0 else round((pair + best['bridge_tetra']) / (best['bridge_removed'] + 1), 1)   # 평균 사슬 길이(사면체 수)
    h2o = round(water * best['Si_total'] / 2, 1)
    # 층간격 · 밀도: 토버모라이트 14 Å(물 많음) 2.23 · 11 Å 2.46 · 9 Å 2.6 g/cm³ 범위(문헌 대표값) 를 물 함량으로 보간 — 개념값
    spacing = 9.3 + 2.35 * min(2.0, water)
    density = round(2.6 - 0.185 * min(2.0, water), 2)
    return {**best, 'repeat_units': repeat, 'mean_chain_length_tetra': chain_length, 'interlayer_H2O': h2o, 'H2O_per_Si': water,
            'layer_spacing_A(개념)': round(spacing, 1), 'density_est_g_cm3(확인 필요)': density,
            'note': '구성 단위 수 모델 · 결정 좌표 아님 · 밀도 · 간격은 문헌 범위 보간(확인 필요)'}
if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--ca-si', type=float, default=1.7); ap.add_argument('--water', type=float, default=2.0); ap.add_argument('--json', default='')
    a = ap.parse_args(); r = model(a.ca_si, a.water)
    for k, v in r.items(): print(f"{k:28s} {v}")
    if a.json: json.dump(r, open(a.json, 'w'), indent=1, ensure_ascii=False)
