#!/usr/bin/env node
/* 픽셀 기반 겹침 점검 — 글자를 투명하게 만든 화면에서, 각 글자 본체 자리에 배경이 아닌 픽셀(선·화살촉·그림)이 있는지 본다.
 * 브라우저 hit-test 가 못 잡는 SVG marker(화살촉)·이미지 위 글자까지 잡는다.
 *   NODE_PATH=<puppeteer-core>/node_modules node tools/check_overlap_px.js <작업폴더> [주차 …]
 *   python3 tools/check_overlap_px.py <작업폴더>        # 분석 · 보고
 */
const puppeteer = require('puppeteer-core'); const fs = require('fs'); const path = require('path');
const ROOT = path.resolve(__dirname, '..'); const BASE = process.env.DECK_BASE || 'http://localhost:8765/';
const [work, ...weeks] = process.argv.slice(2);
const decks = JSON.parse(fs.readFileSync(path.join(ROOT, 'tools/decks.json'), 'utf8')).decks
  .filter(d => !weeks.length || weeks.some(w => Number(w) === d.week || w === d.file));
(async () => {
  const b = await puppeteer.launch({ executablePath: process.env.CHROME || '/usr/bin/google-chrome', headless: 'new', args: ['--no-sandbox'] });
  const p = await b.newPage(); await p.setViewport({ width: 1920, height: 1080 });
  for (const d of decks) {
    const dir = path.join(work, `w${String(d.week).padStart(2, '0')}${d.supplement || ''}`); fs.mkdirSync(dir, { recursive: true });
    await p.goto(BASE + encodeURIComponent(d.file), { waitUntil: 'networkidle0', timeout: 120000 });
    await p.waitForFunction(() => document.querySelectorAll('deck-stage > section').length > 0, { timeout: 60000 });
    await p.evaluate(() => document.fonts.ready); await new Promise(r => setTimeout(r, 600));
    // 슬라이드를 1:1(1920×1080)로 보도록 noscale
    await p.evaluate(() => document.querySelector('deck-stage').setAttribute('noscale', ''));
    await new Promise(r => setTimeout(r, 300));
    const n = await p.evaluate(() => document.querySelectorAll('deck-stage > section').length);
    const meta = [];
    for (let i = 0; i < n; i++) {
      const info = await p.evaluate(i => {
        const secs = [...document.querySelectorAll('deck-stage > section')];
        secs.forEach((s, j) => { s.style.setProperty('visibility', j === i ? 'visible' : 'hidden', 'important'); s.style.setProperty('opacity', j === i ? '1' : '0', 'important'); });
        const s = secs[i]; const sr = s.getBoundingClientRect(); const k = sr.width / 1920;
        const boxes = [];
        const walker = document.createTreeWalker(s, NodeFilter.SHOW_TEXT); let node;
        while ((node = walker.nextNode())) {
          const txt = node.textContent.trim(); if (!txt) continue;
          const el = node.parentElement; if (!el) continue;
          const inSvg = !!el.closest('svg');
          let rects;
          if (inSvg) rects = [el.getBoundingClientRect()];
          else { const rg = document.createRange(); rg.selectNodeContents(node); rects = [...rg.getClientRects()]; }
          const fsz = parseFloat(getComputedStyle(el).fontSize) || 16;
          for (const r of rects) if (r.width > 2 && r.height > 2)
            boxes.push({ txt: txt.slice(0, 40), svg: inSvg, x: (r.left - sr.left) / k, y: (r.top - sr.top) / k, w: r.width / k, h: r.height / k, fs: fsz });
        }
        return { label: s.getAttribute('data-label'), boxes };
      }, i);
      await p.addStyleTag({ content: `#__t{}` });
      await p.evaluate(() => { let st = document.getElementById('__hide'); if (!st) { st = document.createElement('style'); st.id = '__hide'; document.head.appendChild(st); }
        st.textContent = 'deck-stage > section, deck-stage > section * { color: transparent !important; -webkit-text-fill-color: transparent !important; text-shadow:none !important; } deck-stage > section svg text, deck-stage > section svg tspan { fill: transparent !important; stroke: transparent !important; }'; });
      const el = (await p.$$('deck-stage > section'))[i];
      await el.screenshot({ path: path.join(dir, `${String(i + 1).padStart(2, '0')}_notext.png`) });
      await p.evaluate(() => { document.getElementById('__hide').textContent = ''; });
      meta.push({ slide: i + 1, ...info });
    }
    fs.writeFileSync(path.join(dir, 'boxes.json'), JSON.stringify({ file: d.file, slides: meta }));
    console.log(`${d.file.slice(0, 40)}  ${n}장 촬영`);
  }
  await b.close();
})().catch(e => { console.error(e); process.exit(2); });
