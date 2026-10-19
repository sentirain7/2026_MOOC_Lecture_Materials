#!/usr/bin/env node
/* 겹침 · 그림 속 글자 크기 점검 (STYLE_GUIDE §8).
 *
 * 슬라이드를 한 장씩 보이게 한 뒤 브라우저 hit-test(elementsFromPoint)로 검사한다.
 *   - line-overlap : 글자 영역 위에 SVG 선·도형·다른 그림이 칠해져 있음
 *                    (글자를 완전히 감싸는 상자·원은 배경으로 보고 제외)
 *   - text-overlap : 글자 상자끼리 겹침 (작은 쪽 면적의 15% 이상)
 *   - big-svg-text : SVG 안 글자의 실제 크기가 MAX_SVG_PX(설계 px)를 넘음
 *   - small-svg-text : SVG 안 글자의 실제 크기가 MIN_SVG_PX 미만 (참고)
 *
 *   python3 -m http.server 8765 &
 *   NODE_PATH=<puppeteer-core>/node_modules node tools/check_layout.js [주차 …] [--json 파일]
 */
const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..');
const BASE = process.env.DECK_BASE || 'http://localhost:8765/';
const MAX_SVG_PX = Number(process.env.MAX_SVG_PX || 32);
const MIN_SVG_PX = Number(process.env.MIN_SVG_PX || 16);

const args = process.argv.slice(2);
const ji = args.indexOf('--json');
const jsonOut = ji >= 0 ? args.splice(ji, 2)[1] : null;
const decks = JSON.parse(fs.readFileSync(path.join(ROOT, 'tools/decks.json'), 'utf8')).decks
  .filter(d => !args.length || args.some(a => a === d.file || Number(a) === d.week));

(async () => {
  const b = await puppeteer.launch({ executablePath: process.env.CHROME || '/usr/bin/google-chrome', headless: 'new', args: ['--no-sandbox'] });
  const p = await b.newPage();
  await p.setViewport({ width: 1920, height: 1080 });
  const report = [];
  let total = 0;
  for (const d of decks) {
    await p.goto(BASE + encodeURIComponent(d.file), { waitUntil: 'networkidle0', timeout: 120000 });
    await p.waitForFunction(() => document.querySelectorAll('deck-stage > section').length > 0, { timeout: 60000 });
    await p.evaluate(() => document.fonts.ready);
    await new Promise(r => setTimeout(r, 600));
    // 덱 런타임이 슬라이드에 pointer-events:none 을 걸어 hit-test 가 안 되므로 검사 중에만 푼다
    await p.addStyleTag({ content: 'deck-stage > section, deck-stage > section * { pointer-events: auto !important; } deck-stage > section svg * { pointer-events: visiblePainted !important; }' });
    const n = await p.evaluate(() => document.querySelectorAll('deck-stage > section').length);
    const deckIssues = [];
    for (let i = 0; i < n; i++) {
      const res = await p.evaluate((i, MAX, MIN) => {
        const secs = [...document.querySelectorAll('deck-stage > section')];
        secs.forEach((s, j) => {
          s.style.setProperty('visibility', j === i ? 'visible' : 'hidden', 'important');
          s.style.setProperty('opacity', j === i ? '1' : '0', 'important');
        });
        const s = secs[i];
        const sr = s.getBoundingClientRect();
        const k = sr.width / 1920;
        const out = [];
        const SHAPES = new Set(['line', 'path', 'polyline', 'polygon', 'rect', 'circle', 'ellipse', 'img', 'image', 'canvas']);
        // 글자 상자 수집: HTML 텍스트 노드의 줄 상자 + SVG <text>
        const boxes = [];
        const walker = document.createTreeWalker(s, NodeFilter.SHOW_TEXT);
        let node;
        while ((node = walker.nextNode())) {
          const txt = node.textContent.trim();
          if (!txt) continue;
          const el = node.parentElement;
          if (!el || el.closest('svg')) continue;
          const cs = getComputedStyle(el);
          if (cs.visibility === 'hidden' || cs.display === 'none' || parseFloat(cs.opacity) === 0) continue;
          const rg = document.createRange();
          rg.selectNodeContents(node);
          for (const r of rg.getClientRects()) if (r.width > 2 && r.height > 2) boxes.push({ r, el, txt, svg: false });
        }
        s.querySelectorAll('svg text').forEach(el => {
          const txt = el.textContent.trim();
          if (!txt) return;
          const r = el.getBoundingClientRect();
          if (r.width > 1 && r.height > 1) boxes.push({ r, el, txt, svg: true });
          // 실제 글자 크기 (설계 px)
          const fs0 = parseFloat(getComputedStyle(el).fontSize);
          const ctm = el.getScreenCTM();
          if (ctm && fs0) {
            const px = fs0 * Math.hypot(ctm.a, ctm.b) / k;
            if (px > MAX) out.push({ kind: 'big-svg-text', px: Math.round(px), txt: txt.slice(0, 30) });
            else if (px < MIN) out.push({ kind: 'small-svg-text', px: Math.round(px), txt: txt.slice(0, 30) });
          }
        });
        // 글자 위 선·도형 (hit-test)
        const contains = (a, r) => a.left <= r.left + 1 && a.right >= r.right - 1 && a.top <= r.top + 1 && a.bottom >= r.bottom - 1;
        for (const bx of boxes) {
          const r = bx.r;
          const hits = new Map();
          // 글자 본체(줄 간격 여백 제외)를 가로 11점 × 세로 3점으로 훑는다
          for (const fx of [0.02, 0.12, 0.22, 0.32, 0.42, 0.5, 0.58, 0.68, 0.78, 0.88, 0.98]) for (const fy of [0.3, 0.5, 0.7]) {
            const x = r.left + r.width * fx, y = r.top + r.height * fy;
            for (const e of document.elementsFromPoint(x, y)) {
              if (e === bx.el || bx.el.contains(e) || e.contains(bx.el)) continue;
              const tag = e.tagName.toLowerCase();
              if (!SHAPES.has(tag)) continue;
              if (!s.contains(e)) continue;
              const er = e.getBoundingClientRect();
              if (contains(er, r)) {
                // 글자를 감싸는 배경 상자: 불투명하게 칠해져 있으면 그 아래 요소는 가려져 보이지 않으므로 더 보지 않는다
                const bs = getComputedStyle(e);
                if (bs.fill !== 'none' && parseFloat(bs.fillOpacity || '1') >= 0.95 && parseFloat(bs.opacity || '1') >= 0.95) break;
                continue;
              }
              const cs = getComputedStyle(e);
              if (cs.visibility === 'hidden' || parseFloat(cs.opacity) === 0) continue;
              // 테두리 없이 칠만 된 사각형은 배경 띠로 본다 (막대가 글자를 덮는 경우는 픽셀 검사가 잡음)
              if (tag === 'rect' && (cs.stroke === 'none' || cs.strokeWidth === '0px')) continue;
              // 칠해지지 않은 도형(fill none, stroke none) 제외
              if ((cs.fill === 'none' || cs.fillOpacity === '0') && (cs.stroke === 'none' || cs.strokeWidth === '0px') && !['img', 'image', 'canvas'].includes(tag)) continue;
              hits.set(e, (hits.get(e) || 0) + 1);
            }
          }
          for (const [e, c] of hits) if (c >= (['line', 'path', 'polyline'].includes(e.tagName.toLowerCase()) ? 1 : 2)) {
            out.push({ kind: 'line-overlap', txt: bx.txt.slice(0, 30), with: e.tagName.toLowerCase(), pts: c });
            break;
          }
        }
        // 글자끼리 겹침
        for (let a = 0; a < boxes.length; a++) for (let c = a + 1; c < boxes.length; c++) {
          const A = boxes[a], B = boxes[c];
          if (A.el === B.el || A.el.contains(B.el) || B.el.contains(A.el)) continue;
          // 글자 본체만 비교: 줄 상자 위아래 20%는 줄 간격 여백으로 본다
          const body = r => ({ left: r.left, right: r.right, top: r.top + r.height * 0.2, bottom: r.bottom - r.height * 0.2 });
          const a1 = body(A.r), b1 = body(B.r);
          const w = Math.min(a1.right, b1.right) - Math.max(a1.left, b1.left);
          const h = Math.min(a1.bottom, b1.bottom) - Math.max(a1.top, b1.top);
          if (w <= 0 || h <= 0) continue;
          const small = Math.min(A.r.width * A.r.height, B.r.width * B.r.height) * 0.6;
          if (w * h / small >= 0.10) out.push({ kind: 'text-overlap', txt: `${A.txt.slice(0, 18)} ⟂ ${B.txt.slice(0, 18)}` });
        }
        return { label: s.getAttribute('data-label'), out };
      }, i, MAX_SVG_PX, MIN_SVG_PX);
      // 같은 문구 중복 제거
      const seen = new Set();
      const iss = res.out.filter(o => { const key = o.kind + o.txt; if (seen.has(key)) return false; seen.add(key); return true; });
      if (iss.length) deckIssues.push({ slide: i + 1, label: res.label, issues: iss });
    }
    const cnt = k => deckIssues.reduce((s, x) => s + x.issues.filter(o => o.kind === k).length, 0);
    const bad = cnt('line-overlap') + cnt('text-overlap') + cnt('big-svg-text');
    total += bad;
    console.log(`${d.file.replace('.dc.html', '').slice(0, 40).padEnd(40)} ${String(n).padStart(3)}장  선겹침 ${cnt('line-overlap')}  글자겹침 ${cnt('text-overlap')}  큰글자 ${cnt('big-svg-text')}  (작은글자 ${cnt('small-svg-text')})`);
    if (args.length) for (const x of deckIssues) {
      const main = x.issues.filter(o => o.kind !== 'small-svg-text');
      if (main.length) console.log(`    #${String(x.slide).padStart(2, '0')} ${x.label}: ` + main.map(o => `${o.kind}${o.px ? '(' + o.px + 'px)' : ''}「${o.txt}」`).join(' · '));
    }
    report.push({ file: d.file, week: d.week, supplement: d.supplement, slides: n, issues: deckIssues });
  }
  if (jsonOut) fs.writeFileSync(jsonOut, JSON.stringify(report, null, 1));
  await b.close();
  process.exit(total ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
