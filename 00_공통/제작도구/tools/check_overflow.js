#!/usr/bin/env node
/* 강의 덱 넘침 점검 (STYLE_GUIDE §8).
 *
 * 각 덱을 headless Chrome으로 띄워, 모든 <section>(1920×1080)에 대해
 *   - 슬라이드 밖으로 나간 내용 (세로·가로, 설계 px 단위)
 *   - overflow:hidden 인 상자 안에서 잘린 내용
 * 을 보고한다. 필요하면 슬라이드별 PNG도 저장한다.
 *
 *   python3 -m http.server 8765 &             # 프로젝트 루트에서
 *   NODE_PATH=<puppeteer-core 설치 위치>/node_modules node tools/check_overflow.js [주차 …] [--shots DIR]
 *
 * 종료 코드: 넘침이 하나라도 있으면 1.
 */
const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const BASE = process.env.DECK_BASE || 'http://localhost:8765/';
const CHROME = process.env.CHROME || '/usr/bin/google-chrome';
const TOL = 2; // px

const args = process.argv.slice(2);
const shotIdx = args.indexOf('--shots');
const shotDir = shotIdx >= 0 ? args.splice(shotIdx, 2)[1] : null;
const decks = JSON.parse(fs.readFileSync(path.join(ROOT, 'tools/decks.json'), 'utf8')).decks
  .filter(d => !args.length || args.some(a => a === d.file || Number(a) === d.week));

(async () => {
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080 });
  let bad = 0;
  const report = [];
  for (const d of decks) {
    await page.goto(BASE + encodeURIComponent(d.file), { waitUntil: 'networkidle0', timeout: 120000 });
    await page.waitForFunction(() => document.querySelectorAll('deck-stage > section').length > 0, { timeout: 60000 });
    await page.evaluate(() => document.fonts.ready);
    await new Promise(r => setTimeout(r, 800));
    const res = await page.evaluate((TOL) => {
      const out = [], density = [];
      const secs = [...document.querySelectorAll('deck-stage > section')];
      secs.forEach((s, i) => {
        const sr = s.getBoundingClientRect();
        const k = sr.width / 1920 || 1; // 화면 배율 → 설계 px
        const issues = [];
        let maxB = -Infinity, maxR = -Infinity;
        s.querySelectorAll('*').forEach(el => {
          if (el.closest('svg') && el.tagName.toLowerCase() !== 'svg') return;
          const r = el.getBoundingClientRect();
          if (!r.width && !r.height) return;
          maxB = Math.max(maxB, (r.bottom - sr.bottom) / k);
          maxR = Math.max(maxR, (r.right - sr.right) / k);
          const cs = getComputedStyle(el);
          if ((cs.overflow === 'hidden' || cs.overflowY === 'hidden') && el.scrollHeight - el.clientHeight > TOL && el !== s) {
            issues.push(`상자 안 잘림 ${el.scrollHeight - el.clientHeight}px 「${(el.textContent || '').trim().slice(0, 24)}」`);
          }
        });
        // 슬라이드 padding 안쪽 경계 기준으로도 본다 (여백 침범)
        const pb = parseFloat(getComputedStyle(s).paddingBottom) || 0;
        const over = Math.round(maxB), overR = Math.round(maxR);
        if (over > TOL) issues.unshift(`세로 넘침 ${over}px`);
        else if (over > -pb + TOL) issues.unshift(`하단 여백 침범 ${Math.round(over + pb)}px`);
        if (overR > TOL) issues.unshift(`가로 넘침 ${overR}px`);
        if (issues.length) out.push({ slide: i + 1, label: s.getAttribute('data-label'), issues });
        // 가독성 지표: 채움 비율(내용 하단 / 사용 가능 높이), 글자 수
        const pt = parseFloat(getComputedStyle(s).paddingTop) || 0;
        const fill = (1080 - pb + Math.min(maxB, 0) - pt) / (1080 - pb - pt);
        density.push({ slide: i + 1, label: s.getAttribute('data-label'), fill: Math.round(fill * 100), chars: (s.textContent || '').replace(/\s+/g, '').length });
      });
      return { n: secs.length, out, density };
    }, TOL);
    const hard = res.out.filter(o => o.issues.some(x => !x.startsWith('하단 여백')));
    bad += hard.length;
    report.push({ file: d.file, week: d.week, supplement: d.supplement, slides: res.n, problems: res.out, density: res.density });
    console.log(`${d.file.replace('.dc.html', '').slice(0, 44).padEnd(44)} ${String(res.n).padStart(3)}장  넘침 ${hard.length}  여백침범 ${res.out.length - hard.length}`);
    for (const o of res.out) console.log(`    #${String(o.slide).padStart(2, '0')} ${o.label}: ${o.issues.join(' · ')}`);
    if (shotDir) {
      const dir = path.join(shotDir, `w${String(d.week).padStart(2, '0')}${d.supplement || ''}`);
      fs.mkdirSync(dir, { recursive: true });
      for (let i = 0; i < res.n; i++) {
        await page.evaluate(i => {
          document.querySelectorAll('deck-stage > section').forEach((s, j) => {
            s.style.setProperty('visibility', j === i ? 'visible' : 'hidden', 'important');
            s.style.setProperty('opacity', j === i ? '1' : '0', 'important');
          });
        }, i);
        const el = (await page.$$('deck-stage > section'))[i];
        await el.screenshot({ path: path.join(dir, `${String(i + 1).padStart(2, '0')}.png`) });
      }
    }
  }
  if (process.env.REPORT) fs.writeFileSync(process.env.REPORT, JSON.stringify(report, null, 1));
  await browser.close();
  process.exit(bad ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
