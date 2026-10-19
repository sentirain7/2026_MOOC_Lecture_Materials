import math, re, sys, glob
F = glob.glob('08주차*.dc.html')[0]
SEC = "background:#0c1222;color:#f1f5f9;font-family:'Pretendard Variable',Pretendard,'Noto Sans KR',sans-serif;padding:40px 80px 28px;display:flex;flex-direction:column;gap:16px;"
MONO = "font-family:'JetBrains Mono',monospace;"
SB = '<span style="text-decoration:overline;">S</span>'  # 시멘트 표기 S̄ = SO3

# ---------- (1/2) 4상별 수화도 · 로그 시간 ----------
W, H = 1000, 640
X0, X1, Y0, Y1 = 110, 970, 110, 560          # 그림 영역 (viewBox)
LMIN, LMAX = -1.0, math.log10(8760)           # 0.1 h ~ 1 y
X = lambda th: X0 + (math.log10(th) - LMIN) / (LMAX - LMIN) * (X1 - X0)
Y = lambda p: Y1 - p / 100 * (Y1 - Y0)
curves = {  # 교과서 경향 개략값 (수화도 %) — 판독용 아님
    'C₃A':  ('#facc15', [(0.1,8),(0.25,15),(1,18),(3,22),(12,40),(24,50),(72,62),(168,70),(672,80),(2160,86),(8760,90)]),
    'C₃S':  ('#60a5fa', [(0.1,1),(0.25,2),(1,3),(3,6),(12,20),(24,30),(72,42),(168,55),(672,70),(2160,82),(8760,88)]),
    'C₄AF': ('#a78bfa', [(0.1,2),(0.25,4),(1,6),(3,9),(12,18),(24,25),(72,35),(168,45),(672,57),(2160,68),(8760,76)]),
    'C₂S':  ('#4ade80', [(0.1,0),(0.25,0),(1,0.5),(3,1),(12,2),(24,4),(72,8),(168,13),(672,28),(2160,50),(8760,68)]),
}
def smooth(pts):
    # 로그 시간에서 단조 3차 보간 (Fritsch–Carlson)
    xs = [math.log10(t) for t, _ in pts]; ys = [p for _, p in pts]
    n = len(xs); d = [(ys[i+1]-ys[i])/(xs[i+1]-xs[i]) for i in range(n-1)]
    m = [d[0]] + [(0 if d[i-1]*d[i] <= 0 else (d[i-1]+d[i])/2) for i in range(1, n-1)] + [d[-1]]
    out = []
    for i in range(n-1):
        h = xs[i+1]-xs[i]
        for k in range(12):
            s = k/12; h00=2*s**3-3*s**2+1; h10=s**3-2*s**2+s; h01=-2*s**3+3*s**2; h11=s**3-s**2
            y = h00*ys[i]+h10*h*m[i]+h01*ys[i+1]+h11*h*m[i+1]
            out.append((10**(xs[i]+s*h), y))
    out.append(pts[-1])
    return ' '.join(f'{X(t):.1f},{Y(p):.1f}' for t, p in out)
stages = [('I', '초기', 0.1, 0.25, '#1e293b'), ('II', '유도기', 0.25, 3, '#111827'), ('III', '가속기', 3, 12, '#1e293b'),
          ('IV', '감속기', 12, 48, '#111827'), ('V', '확산 지배', 48, 8760, '#1e293b')]
g = []
for i, (r, name, a, b, col) in enumerate(stages):
    g.append(f'<rect x="{X(a):.1f}" y="{Y0}" width="{X(b)-X(a):.1f}" height="{Y1-Y0}" fill="{col}" opacity="0.9"/>')
    cx = (X(a)+X(b))/2
    g.append(f'<text x="{cx:.1f}" y="{Y0-44}" text-anchor="middle" font-size="22" font-weight="700" fill="#e2e8f0" font-family="JetBrains Mono, monospace">{r}</text>')
    if name and X(b)-X(a) > 60:
        g.append(f'<text x="{cx:.1f}" y="{Y0-16}" text-anchor="middle" font-size="20" fill="#94a3b8">{name}</text>')
# 격자 · 축
for p in (0, 25, 50, 75, 100):
    g.append(f'<line x1="{X0}" y1="{Y(p):.1f}" x2="{X1}" y2="{Y(p):.1f}" stroke="#334155" stroke-width="1" stroke-dasharray="{"" if p in (0,) else "4 6"}"/>')
    g.append(f'<text x="{X0-14}" y="{Y(p)+7:.1f}" text-anchor="end" font-size="20" fill="#94a3b8" font-family="JetBrains Mono, monospace">{p}</text>')
ticks = [(0.1,'6분'),(1,'1시간'),(24,'1일'),(168,'7일'),(672,'28일'),(8760,'1년')]
for t, lab in ticks:
    g.append(f'<line x1="{X(t):.1f}" y1="{Y1}" x2="{X(t):.1f}" y2="{Y1+8}" stroke="#94a3b8" stroke-width="1.5"/>')
    g.append(f'<text x="{X(t):.1f}" y="{Y1+34}" text-anchor="middle" font-size="20" fill="#94a3b8">{lab}</text>')
g.append(f'<line x1="{X0}" y1="{Y1}" x2="{X1}" y2="{Y1}" stroke="#94a3b8" stroke-width="1.5"/><line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y1}" stroke="#94a3b8" stroke-width="1.5"/>')
g.append(f'<text x="{(X0+X1)/2:.0f}" y="{Y1+70}" text-anchor="middle" font-size="22" fill="#cbd5e1">수화 경과 시간 (로그 눈금)</text>')
g.append(f'<text transform="translate(34 {(Y0+Y1)/2:.0f}) rotate(-90)" text-anchor="middle" font-size="22" fill="#cbd5e1">수화도 (%) · 개략</text>')
for name, (col, pts) in curves.items():
    g.append(f'<polyline points="{smooth(pts)}" fill="none" stroke="{col}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
# 범례: 그림 왼쪽 위 빈 영역 (초기 시간대 곡선이 낮음)
lx, ly = X0+24, Y0+26
g.append(f'<rect x="{lx-14}" y="{ly-24}" width="330" height="178" rx="10" fill="#0c1222" stroke="#334155"/>')
order = ['C₃A', 'C₃S', 'C₄AF', 'C₂S']
rank = {'C₃A': '가장 빠름', 'C₃S': '빠름', 'C₄AF': '중간', 'C₂S': '느림'}
for i, name in enumerate(order):
    col = curves[name][0]; yy = ly + i*40
    g.append(f'<line x1="{lx}" y1="{yy}" x2="{lx+44}" y2="{yy}" stroke="{col}" stroke-width="4" stroke-linecap="round"/>')
    g.append(f'<text x="{lx+58}" y="{yy+8}" font-size="22" fill="{col}" font-family="JetBrains Mono, monospace">{name}</text>')
    g.append(f'<text x="{lx+156}" y="{yy+8}" font-size="20" fill="#94a3b8">{rank[name]}</text>')
svgA = f'<svg viewBox="0 0 {W} {H}" style="width:100%;height:auto;display:block;" role="img" aria-label="클링커 4상별 수화도 시간 경과 개략도">' + ''.join(g) + '</svg>'

def card(col, head, eq, lines):
    li = ''.join(f'<div style="font-size:24px;color:#94a3b8;line-height:1.4;">· {x}</div>' for x in lines)
    return (f'<div style="background:#111827;border:1px solid #1f2937;border-left:3px solid {col};border-radius:12px;padding:14px 22px;display:flex;flex-direction:column;gap:6px;word-break:keep-all;">'
            f'<div style="{MONO}font-size:24px;color:{col};letter-spacing:0.04em;">{head}</div>'
            f'<div style="font-size:24px;color:#e2e8f0;line-height:1.4;">{eq}</div>{li}</div>')
cardsA = ''.join([
    card('#facc15', 'C₃A · 알루미네이트(aluminate)', f'C₃A + 3C{SB}H₂ + 26H → C₆A{SB}₃H₃₂', ['수화 속도 최고 · 발열 최대', '석고(gypsum) 없으면 급결(flash set)']),
    card('#60a5fa', 'C₃S · 알라이트(alite)', '2C₃S + 6H → C₃S₂H₃ + 3CH', ['수화 빠름 · 발열 큼', '28일까지 초기 강도 대부분 담당']),
    card('#a78bfa', 'C₄AF · 페라이트(ferrite)', 'C₄AF + 2CH + 10H → C₃AH₆ + C₃FH₆', ['수화 속도 중간', '강도 기여 작음 · 시멘트 색 결정']),
    card('#4ade80', 'C₂S · 벨라이트(belite)', '2C₂S + 4H → C₃S₂H₃ + CH', ['수화 느림 · 발열 작음', '28일 이후 장기 강도 증가 담당']),
])
eyebrow = lambda n: f'<div style="{MONO}font-size:26px;letter-spacing:0.14em;color:#599eff;">8-1 · HYDRATION KINETICS · {n} / 2</div>'
h2 = lambda t: f'<h2 style="font-size:52px;font-weight:700;letter-spacing:-0.02em;line-height:1.1;margin:0;">{t}</h2>'
cap = lambda t: f'<div style="font-size:24px;color:#64748b;">{t}</div>'
REF = '개략도 · 교과서 경향 재현(Taylor, Cement Chemistry 2판 1997 · Mindess · Young · Darwin, Concrete 2판 2003) · 수치 판독용 아님'
notesA = ('8-1 교과서 개략도. 포틀랜드 시멘트 페이스트에서 클링커 4상의 수화도(degree of hydration)가 시간에 따라 증가하는 경향을 로그 시간축에 그렸다. '
          '곡선은 Taylor(1997) · Mindess · Young · Darwin(2003) · Scrivener · Juilland · Monteiro(2015, Cement and Concrete Research 78)가 공통으로 제시하는 순서(초기 C3A > C3S > C4AF > C2S, 장기에는 C2S 증가)를 재현한 개략값이며 측정값이 아니다. '
          '배경 띠 I~V는 다음 장의 수화 5단계 구간이다(초기 0~15분 · 유도기 15분~3시간 · 가속기 3~12시간 · 감속기 12~48시간 · 확산 지배 이후). '
          '반응식은 앞 장 라이브 계산기(#10 예정 위치)와 같은 Mindess 교재 표기이며 H = H2O, CH = Ca(OH)2, S 윗줄 = SO3이다. 실제 C-S-H 조성은 Ca/Si 약 1.7로 C3S2H3보다 물 함량이 가변이다.')
secA = (f'<section data-label="클링커 수화 경과 (1/2)" data-screen-label="00" data-speaker-notes="{notesA}" style="{SEC}">\n  {eyebrow(1)}\n  {h2("클링커 4상별 수화도 · 시간 경과")}\n'
        f'  <div style="display:grid;grid-template-columns:1.18fr 1fr;gap:22px;align-items:start;">\n'
        f'    <div style="background:#111827;border:1px solid #2d3748;border-radius:12px;padding:12px 16px;">{svgA}</div>\n'
        f'    <div style="display:flex;flex-direction:column;gap:12px;">{cardsA}</div>\n  </div>\n  {cap(REF)}\n</section>')

# ---------- (2/2) 수화 5단계 · 발열 속도 ----------
W2, H2 = 1760, 450
P0, P1, Q0, Q1 = 110, 1720, 70, 360
TMAX, QMAX = 48.0, 4.6
tx = lambda t: P0 + t / TMAX * (P1 - P0)
qy = lambda q: Q1 - min(q, QMAX) / QMAX * (Q1 - Q0)
def q(t):
    spike = 9.0 * math.exp(-t / 0.08)                                   # 초기 용해 · 습윤 발열 (수 분)
    main = 3.3 * math.exp(-((t - 10.0) / (3.6 if t < 10 else 4.6)) ** 2)  # C3S 주 피크
    shoulder = 1.15 * math.exp(-((t - 17.5) / 2.6) ** 2)                  # 황산염 고갈 · AFt→AFm
    base = 0.22 + 0.25 * math.exp(-t / 40)
    dorm = 1 - 0.55 * math.exp(-((t - 1.2) / 1.1) ** 2)                   # 유도기 최소
    return spike + (main + shoulder) + base * dorm * 0.8
pts = [0.001] + [i * 0.02 for i in range(1, 50)] + [1 + i * 0.1 for i in range(0, 471)]
poly = ' '.join(f'{tx(t):.1f},{qy(q(t)):.1f}' for t in pts)
st2 = [('I', 0, 0.25), ('II', 0.25, 3), ('III', 3, 12), ('IV', 12, 30), ('V', 30, 48)]
g2 = []
for i, (r, a, b) in enumerate(st2):
    g2.append(f'<rect x="{tx(a):.1f}" y="{Q0}" width="{tx(b)-tx(a):.1f}" height="{Q1-Q0}" fill="{"#1e293b" if i % 2 == 0 else "#111827"}"/>')
for tt in (0, 6, 12, 18, 24, 30, 36, 42, 48):
    g2.append(f'<line x1="{tx(tt):.1f}" y1="{Q1}" x2="{tx(tt):.1f}" y2="{Q1+8}" stroke="#94a3b8" stroke-width="1.5"/><text x="{tx(tt):.1f}" y="{Q1+32}" text-anchor="middle" font-size="20" fill="#94a3b8" font-family="JetBrains Mono, monospace">{tt}</text>')
g2.append(f'<line x1="{P0}" y1="{Q1}" x2="{P1}" y2="{Q1}" stroke="#94a3b8" stroke-width="1.5"/><line x1="{P0}" y1="{Q0}" x2="{P0}" y2="{Q1}" stroke="#94a3b8" stroke-width="1.5"/>')
g2.append(f'<text x="{(P0+P1)/2:.0f}" y="{Q1+68}" text-anchor="middle" font-size="22" fill="#cbd5e1">물 접촉 후 경과 시간 (시간)</text>')
g2.append(f'<text transform="translate(40 {(Q0+Q1)/2:.0f}) rotate(-90)" text-anchor="middle" font-size="22" fill="#cbd5e1">발열 속도 · 개략</text>')
g2.append(f'<polyline points="{poly}" fill="none" stroke="#fb923c" stroke-width="4" stroke-linejoin="round"/>')
# 주석: 곡선 위 빈 공간에 두고 짧은 지시선 (글자와 선 간격 유지)
def ann(t, qv, label, dx, dy, anchor='start'):
    x, y = tx(t), qy(qv)
    lx, ly = x + dx, y + dy
    g2.append(f'<line x1="{x:.1f}" y1="{y-6:.1f}" x2="{lx:.1f}" y2="{ly+12:.1f}" stroke="#cbd5e1" stroke-width="1.5"/>')
    g2.append(f'<text x="{lx + (8 if anchor=="start" else -8):.1f}" y="{ly:.1f}" text-anchor="{anchor}" font-size="22" fill="#e2e8f0">{label}</text>')
ann(0.03, q(0.03), '초기 피크 · 수 분 내 용해 · AFt 생성', 39, 36)
ann(1.3, q(1.3), '유도기 · 발열 최소', -4, -208)
ann(10.0, q(10.0), '주 피크 · C₃S 수화 → C-S-H · CH', 60, -8)
ann(17.5, q(17.5), '황산염 고갈 피크 · AFt → AFm', 90, -80)
for i, (r, a, b) in enumerate(st2):
    # 단계 번호는 그림 영역 위 (곡선과 분리)
    g2.append(f'<text x="{(tx(a)+tx(b))/2 if r != "I" else tx(b)+4:.1f}" y="{Q0-16}" text-anchor="{"middle" if r != "I" else "start"}" font-size="22" font-weight="700" fill="#94a3b8" font-family="JetBrains Mono, monospace">{r}</text>')
svgB = f'<svg viewBox="0 0 {W2} {H2}" style="width:100%;height:auto;display:block;" role="img" aria-label="시멘트 수화 발열 속도 곡선과 5단계 개략도">' + ''.join(g2) + '</svg>'
def scard(r, name, en, when, phen, chem, col):
    return (f'<div style="background:#111827;border:1px solid #1f2937;border-top:3px solid {col};border-radius:12px;padding:12px 18px;display:flex;flex-direction:column;gap:6px;word-break:keep-all;">'
            f'<div style="{MONO}font-size:24px;color:{col};">{r} · {name}</div>'
            f'<div style="{MONO}font-size:24px;color:#64748b;">{en}</div>'
            f'<div style="font-size:24px;color:#cbd5e1;">{when}</div>'
            f'<div style="font-size:24px;color:#94a3b8;line-height:1.35;"><span style="color:#e2e8f0;">현상</span> {phen}</div>'
            f'<div style="font-size:24px;color:#94a3b8;line-height:1.35;"><span style="color:#e2e8f0;">화학</span> {chem}</div></div>')
cardsB = ''.join([
    scard('I', '초기 반응', 'pre-induction', '0 ~ 15분', '물 접촉 즉시 급격한 발열 · 이온 용해', 'C₃A + 석고 → 에트린자이트(AFt) 생성 시작 · C₃S 표면 Ca²⁺ · OH⁻ 용출', '#fb923c'),
    scard('II', '유도기', 'induction · dormant', '15분 ~ 2–4시간', '발열 최소 · 유동성 유지 → 운반 · 타설 가능', 'Ca²⁺ · OH⁻ 농도 증가 → CH 과포화 · 용해 속도 저하', '#94a3b8'),
    scard('III', '가속기', 'acceleration', '3 ~ 12시간', '주 발열 피크 · 초결 → 종결(setting)', 'C₃S 본격 수화 · <span style="white-space:nowrap;">C-S-H</span> 핵생성(nucleation) · 성장 · CH 석출', '#60a5fa'),
    scard('IV', '감속기', 'deceleration', '12시간 ~ 수일', '발열 감소 · 강도 발현 본격화', '생성물 층 증가 → 확산 지배 전환 · 석고 고갈 → AFt → 모노설페이트(AFm)', '#a78bfa'),
    scard('V', '확산 지배', 'diffusion-controlled', '수일 이후', '느린 발열 · 장기 강도 증가 · 공극 충전', 'C₂S 수화 기여 증가 · <span style="white-space:nowrap;">C-S-H</span> 치밀화 · C₄AF 느린 수화', '#4ade80'),
])
notesB = ('[분할] 앞 장에서 이어짐. 등온 열량계(isothermal calorimetry)로 측정하는 발열 속도(heat flow) 곡선의 교과서 개략도와 수화 5단계. '
          '구간 시각은 교과서가 제시하는 대표 범위이며 시멘트 조성 · 분말도 · 물시멘트비 · 온도에 따라 달라진다. 곡선 모양(초기 피크 → 유도기 최소 → C3S 주 피크 → 황산염 고갈 어깨 피크)은 Taylor(1997) · Mindess · Young · Darwin(2003) · Scrivener 외(2015)의 공통 서술을 재현한 개략값이며 측정값이 아니다. '
          '유도기의 원인은 표면 보호층설과 용해 속도 저하설이 있으며 현재는 후자(과포화 근처에서 용해 속도 급감)가 유력하다(Scrivener 외 2015). 초결 · 종결은 대략 유도기 끝 ~ 가속기 구간에서 나타난다. '
          'MD 관점에서 연결: 8-2 ReaxFF 수화 계산은 I~II 단계(수 ns, 표면 용해 · 초기 반응)만 직접 다루며, III 이후 단계는 시간 규모상 MD로 직접 재현 불가.')
secB = (f'<section data-label="클링커 수화 경과 (2/2)" data-screen-label="00" data-speaker-notes="{notesB}" style="{SEC}">\n  {eyebrow(2)}\n  {h2("수화 5단계 · 발열 속도 곡선과 단계별 현상 · 화학")}\n'
        f'  <div style="background:#111827;border:1px solid #2d3748;border-radius:12px;padding:10px 16px;">{svgB}</div>\n'
        f'  <div style="display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:14px;">{cardsB}</div>\n  {cap(REF)}\n</section>')

t = open(F, encoding='utf-8').read()
secs = list(re.finditer(r'<section\b.*?</section>', t, re.S))
if 'data-label="클링커 수화 경과 (1/2)"' in t:
    # 재실행: 기존 두 장 교체
    t = re.sub(r'<section data-label="클링커 수화 경과 \(1/2\)".*?</section>\s*<section data-label="클링커 수화 경과 \(2/2\)".*?</section>', lambda m: secA + '\n\n' + secB, t, count=1, flags=re.S)
else:
    m = next(x for x in secs if 'data-label="클링커 4상"' in x.group(0))
    t = t[:m.end()] + '\n\n' + secA + '\n\n' + secB + t[m.end():]
open(F, 'w', encoding='utf-8').write(t)
print('ok', len(t))
