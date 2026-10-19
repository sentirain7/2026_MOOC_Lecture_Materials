#!/usr/bin/env node
/* 덱 → PDF (슬라이드 한 장 = 1920×1080 한 페이지). deck-stage 의 @media print 레이아웃을 쓴다.
 *   python3 -m http.server 8765 &   (프로젝트 루트)
 *   NODE_PATH=<puppeteer-core>/node_modules node tools/export_pdf.js <출력폴더> [주차 …] [--dir 발표용]
 *   --dir: 덱이 들어 있는 하위 폴더(프로젝트 루트 기준). 생략하면 루트의 원본 덱.
 */
const puppeteer = require('puppeteer-core'); const fs = require('fs'); const path = require('path');
const ROOT = path.resolve(__dirname, '..'); const BASE = process.env.DECK_BASE || 'http://localhost:8765/';
const argv = process.argv.slice(2);
const di = argv.indexOf('--dir');
const sub = di >= 0 ? argv.splice(di, 2)[1] : '';
const [out, ...weeks] = argv;
const decks = JSON.parse(fs.readFileSync(path.join(ROOT, 'tools/decks.json'), 'utf8')).decks
  .filter(d => !weeks.length || weeks.some(w => Number(w) === d.week));
(async () => {
  fs.mkdirSync(out, { recursive: true });
  const b = await puppeteer.launch({ executablePath: process.env.CHROME || '/usr/bin/google-chrome', headless: 'new', args: ['--no-sandbox'] });
  const p = await b.newPage(); await p.setViewport({ width: 1920, height: 1080 });
  for (const d of decks) {
    await p.goto(BASE + (sub ? encodeURIComponent(sub) + '/' : '') + encodeURIComponent(d.file), { waitUntil: 'networkidle0', timeout: 120000 });
    await p.waitForFunction(() => document.querySelectorAll('deck-stage > section').length > 0, { timeout: 60000 });
    await p.evaluate(() => document.fonts.ready); await new Promise(r => setTimeout(r, 1000));
    const n = await p.evaluate(() => document.querySelectorAll('deck-stage > section').length);
    const f = path.join(out, d.file.replace(/\.dc\.html$/, '.pdf'));
    await p.pdf({ path: f, width: '1920px', height: '1080px', printBackground: true, preferCSSPageSize: true });
    console.log(`${n}장 → ${path.basename(f)} (${(fs.statSync(f).size / 1e6).toFixed(1)} MB)`);
  }
  await b.close();
})().catch(e => { console.error(e); process.exit(2); });
