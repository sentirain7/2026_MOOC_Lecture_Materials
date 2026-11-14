#!/usr/bin/env python3
"""out/*.json → 덱이 읽는 W15 데이터(JS 한 줄). 덱 수치는 전부 이 파일을 거친다.
  python3 scripts/export_deck_data.py [--inject ../../decks/W15_신경망그래프불확실성.html]"""
import argparse, csv, json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); O = lambda f: os.path.join(ROOT, 'out', f)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--inject'); a = ap.parse_args()
    mp = json.load(open(O('mpnn_forward.json'))); gp = json.load(open(O('gp_demo.json'))); cal = json.load(open(O('calibration.json'))); ac = json.load(open(O('acquisition.json')))
    gs = list(csv.DictReader(open(O('graph_summary.csv'), encoding='utf-8')))
    D = {'mp': {k: mp[k] for k in ['nodes', 'edges', 'hidden', 'layers', 'symbols', 'adjacency', 'h', 'readout_y', 'readout_y_permuted', 'perm_abs_diff', 'reach_from_node0', 'graph_distance_from_node0']},
         'graphs': [{k: (int(v) if v.isdigit() else v) for k, v in r.items()} for r in gs],
         'gp': {'grid': gp['grid'], 'f': gp['f_true'], 'kernel': gp['kernel_fixed'], 'stages': gp['stages'], 'ad': gp['ad_2d'], 'fn': gp['assumed_function']},
         'cal': cal,
         'acq': {'true_max_x': ac['true_max_x'], 'true_max_f': ac['true_max_f'], 'start': ac['start'], 'k2': ac['runs']['ucb_k2'], 'ei': ac['runs']['ei'],
                 'summary': {k: {kk: r[kk] for kk in ['kind', 'kappa', 'best_x', 'true_best_f', 'x_final']} | {'x_next': [s['x_next'] for s in r['rounds']], 'dup': sum(s['duplicate'] for s in r['rounds'])} for k, r in ac['runs'].items()}}}
    js = 'var W15 = ' + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + ';'
    open(O('w15_deck_data.js'), 'w', encoding='utf-8').write(js)
    print(f'W15 데이터 {len(js) / 1024:.1f} KB → out/w15_deck_data.js')
    if a.inject:
        h = open(a.inject, encoding='utf-8').read()
        h2, n = re.subn(r'/\*W15DATA\*/.*?/\*/W15DATA\*/', lambda m: '/*W15DATA*/' + js + '/*/W15DATA*/', h, flags=re.S)
        assert n == 1, '덱에 /*W15DATA*/ … /*/W15DATA*/ 자리가 없다'
        open(a.inject, 'w', encoding='utf-8').write(h2); print('주입 →', a.inject)

if __name__ == '__main__': main()
