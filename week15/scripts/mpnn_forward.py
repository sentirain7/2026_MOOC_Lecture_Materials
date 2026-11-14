#!/usr/bin/env python3
"""메시지 패싱 2층 순전파(numpy · 학습 없음 · 고정 시드 가중치).  W15 · 15-1
  m_v = Σ_{u∈N(v)} W_m h_u   ·   h_v' = tanh(W_s h_v + m_v)   ·   판독 y = Σ_v w_r·h_v   (원본 10주차 #8 · sum 집계)
확인 3가지: ① 층마다 노드 상태 변화 ② 원자 번호를 섞어도 y 동일(순열 불변) ③ L층 = L결합 거리까지 정보 도달
  python3 scripts/mpnn_forward.py [--graph out/graph_toluene.json] [--hidden 4] [--layers 2]
출력: out/mpnn_forward.json"""
import argparse, json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)

def forward(X, A, Ws, Wm, wr):
    H = np.tanh(X @ Ws[0]); hist = [H.copy()]
    for l in range(len(Wm)):
        M = A @ (H @ Wm[l]); H = np.tanh(H @ Ws[l + 1] + M); hist.append(H.copy())
    return float((H @ wr).sum()), hist

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--graph', default=os.path.join(ROOT, 'out', 'graph_toluene.json'))
    ap.add_argument('--hidden', type=int, default=4); ap.add_argument('--layers', type=int, default=2); ap.add_argument('--seed', type=int, default=15)
    a = ap.parse_args(); g = json.load(open(a.graph, encoding='utf-8'))
    X = np.array([n['x'] for n in g['nodes']]); N = len(X); A = np.zeros((N, N))
    for e in g['edges']: A[e['u'], e['v']] = A[e['v'], e['u']] = 1
    rng = np.random.default_rng(a.seed); d = a.hidden
    Ws = [rng.normal(0, 0.5, (X.shape[1], d))] + [rng.normal(0, 0.5, (d, d)) for _ in range(a.layers)]
    Wm = [rng.normal(0, 0.5, (d, d)) for _ in range(a.layers)]; wr = rng.normal(0, 0.5, d)
    y, hist = forward(X, A, Ws, Wm, wr)
    perm = rng.permutation(N); P = np.eye(N)[perm]
    y2, _ = forward(P @ X, P @ A @ P.T, Ws, Wm, wr)
    # 수용 영역: 노드 0(메틸 C)에서 L층 뒤 정보가 닿는 원자 수 = 그래프 거리 ≤ L
    dist = np.full(N, np.inf); dist[0] = 0; frontier = [0]
    while frontier:
        nxt = []
        for v in frontier:
            for u in np.nonzero(A[v])[0]:
                if dist[u] == np.inf: dist[u] = dist[v] + 1; nxt.append(u)
        frontier = nxt
    reach = {L: int((dist <= L).sum()) for L in range(0, 5)}
    out = {'graph': g.get('name', a.graph), 'nodes': N, 'edges': len(g['edges']), 'hidden': d, 'layers': a.layers, 'seed': a.seed,
           'symbols': [n['symbol'] + ('ar' if n['aromatic'] else '') for n in g['nodes']], 'adjacency': A.astype(int).tolist(),
           'h': [np.round(h, 3).tolist() for h in hist], 'readout_y': round(y, 6), 'readout_y_permuted': round(y2, 6), 'perm_abs_diff': float(abs(y - y2)),
           'reach_from_node0': reach, 'graph_distance_from_node0': [int(x) for x in dist]}
    os.makedirs(os.path.join(ROOT, 'out'), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, 'out', 'mpnn_forward.json'), 'w'), ensure_ascii=False, indent=1)
    print(f'노드 {N} · 은닉 {d} · 층 {a.layers} · 판독 y = {y:.4f}')
    print(f'원자 번호를 섞은 입력 y = {y2:.4f} · 차이 {abs(y - y2):.1e} → 순열 불변')
    print('노드 0 에서 L층 뒤 도달 원자 수:', ' · '.join(f'L{L} {c}' for L, c in reach.items()))
    print('→ out/mpnn_forward.json')

if __name__ == '__main__': main()
