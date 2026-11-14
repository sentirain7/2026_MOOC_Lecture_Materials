/* deck.js — 공용 슬라이드 컨트롤러 (참조 덱 ReaxFF Cement Review 의 컨트롤러를 분리·확장)
 * 덱 파일은 <section class="slide"> 나열만 담는다. 이 파일이 스테이지(#vp/#stage)·툴바·진행 막대·노트 패널을 만든다.
 * 기능: 1920×1080 스케일 · ← → Home End · 반복/1회/자동 · 재생/정지 · R 재시작 · N 발표자 노트(data-notes) · P 발표자 창(별도 창 · 녹화 화면에 노트 안 찍힘) · 인쇄용 CSS는 deck.css
 * 동적 요소: <div class="emb" data-emb="id" data-dur="8"> + EMB["id"] = function(root, RAF, lang) 또는 {ko:fn, en:fn}
 * v2 단계 애니: data-steps="N" (+ data-labels="①|②|…") 이면 단계 버튼 줄(.stepbar)을 만들고 root.dataset.step('' = 전체 재생, '1'…'N' = 그 단계)을 EMB 함수가 읽는다. 키 [ ] 로 이동.
 * v2 프롬프트: .prompt 요소에 「복사」 버튼을 붙인다.
 * 언어: 기본 ko. .en 요소가 하나도 없으면 EN/KO 토글을 숨긴다(1차 덱은 한국어 단일, 가이드 §6.2).
 */
var EMB = window.EMB || {}, NEW = window.NEW || {}, DUR = window.DUR || {};
window.EMB = EMB; window.NEW = NEW; window.DUR = DUR;
var VT = 0; function CLK() { return VT; }

window.__L = function (ko, en) { return (document.documentElement.lang === 'en' && en) ? en : ko; };  /* 애니 글자 · 언어별 */
(function () {  /* 덱 스크립트가 글자를 만들기 전에 언어를 정하고, 안 쓰는 언어 쪽 조각은 지운다(같은 id 가 두 번 있지 않게 · 언어를 바꾸면 다시 읽음) */
  var has = !!document.querySelector('.slide .en'), en = false; window.__HAS_EN = has;
  try { en = has && localStorage.getItem('deck-lang') === 'en'; } catch (e) { }
  if (en) document.documentElement.lang = 'en';
  if (has) document.querySelectorAll(en ? '.ko[data-i]' : '.en[data-i]').forEach(function (x) { x.remove(); });
})();
(function () {
  function $(sel, el) { return (el || document).querySelector(sel); }
  function el(tag, attrs, html) { var e = document.createElement(tag); for (var k in attrs) e.setAttribute(k, attrs[k]); if (html != null) e.innerHTML = html; return e; }

  function build() {
    var slides = [].slice.call(document.querySelectorAll('section.slide'));
    if (!slides.length) return null;
    var vp = el('div', { id: 'vp' }), stage = el('div', { id: 'stage' });
    slides.forEach(function (s, i) {
      s.setAttribute('aria-label', String(i + 1));
      stage.appendChild(s);
      var pn = $('.pn', s);
      if (pn && !pn.textContent.trim()) pn.textContent = (i + 1 < 10 ? '0' : '') + (i + 1);
    });
    vp.appendChild(stage);
    document.body.appendChild(vp);
    document.body.appendChild(el('div', { id: 'prog' }));
    document.body.appendChild(el('div', { id: 'aprog' }));
    var hasEn = window.__HAS_EN !== undefined ? window.__HAS_EN : !!document.querySelector('.slide .en');
    var bar = el('nav', { id: 'bar', 'aria-label': '슬라이드 조작' },
      '<button id="prev" type="button" aria-label="이전 슬라이드" title="이전 (←)">←</button>' +
      '<span id="cnt">1 / ' + slides.length + '</span>' +
      '<button id="next" type="button" aria-label="다음 슬라이드" title="다음 (→)">→</button>' +
      '<span id="ttl"></span>' +
      '<div class="segm" role="group" aria-label="애니메이션 모드"><button type="button" data-m="loop" aria-pressed="true" title="끝나면 반복 (O)">↻ <span class="ko">반복</span><span class="en">Loop</span></button><button type="button" data-m="once" aria-pressed="false" title="1회 재생 후 정지 (O)">1× <span class="ko">1회</span><span class="en">Once</span></button></div>' +
      '<button id="play" type="button" aria-label="애니메이션 일시정지" title="재생/정지 (Space)">❚❚</button>' +
      '<button id="replay" type="button" aria-label="다시 재생" title="다시 재생 (R)">↺</button>' +
      '<button id="auto" type="button" aria-pressed="false" title="자동 넘김 (A)">▶▶ <span class="ko">자동</span><span class="en">Auto</span></button>' +
      '<button id="notesbtn" type="button" aria-pressed="false" title="발표자 노트 (N)"><span class="ko">노트</span><span class="en">Notes</span></button>' +
      (hasEn ? '<div class="seg" role="group" aria-label="언어"><button type="button" data-l="ko" aria-pressed="true">한국어</button><button type="button" data-l="en" aria-pressed="false">EN</button></div>' : ''));
    document.body.appendChild(bar);
    if (!document.querySelector('section.slide[data-notes]')) bar.querySelector('#notesbtn').style.display = 'none';   /* 원고를 뺀 학생용 덱 */
    document.body.appendChild(el('aside', { id: 'notes', 'aria-live': 'polite' }, '<h4>발표자 노트</h4><div id="notesbody"></div>'));
    return { slides: slides, stage: stage, vp: vp, hasEn: hasEn };
  }


  /* v3: 선아이콘 주입 — <span data-ico="target"> 에 common/icons.js 의 ICO(name) 결과를 넣는다 */
  function icons() { if (!window.ICO) return; document.querySelectorAll('[data-ico]').forEach(function (e) { if (!e.firstElementChild) e.innerHTML = window.ICO(e.dataset.ico); }); }
  /* v3: 큰 숫자(.n · .tot · .nn[data-count]) 를 1.3초 동안 세어 올린다 (참조 덱 countUp) */
  function countUp(el) {
    if (el.__busy) return; var nodes = [], w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null), t;
    while ((t = w.nextNode())) if (/\d/.test(t.nodeValue) && !/[⁰¹²³⁴⁵⁶⁷⁸⁹×^]/.test(t.nodeValue) && !(t.parentNode.closest && t.parentNode.closest('sup,small,.nosum'))) nodes.push({ n: t, o: t.nodeValue });
    if (!nodes.length) return; el.__busy = 1; var t0 = performance.now(), D = 1300;
    function fmt(tok, f) { var dec = (tok.split('.')[1] || '').length, v = parseFloat(tok.replace(/,/g, '')) * f, str = v.toFixed(dec); if (tok.indexOf(',') >= 0) { var p = str.split('.'); p[0] = p[0].replace(/\B(?=(\d{3})+(?!\d))/g, ','); str = p.join('.'); } return str; }
    function step(now) { var k = Math.max(0, Math.min(1, (now - t0) / D)), f = 1 - Math.pow(1 - k, 3); nodes.forEach(function (x) { x.n.nodeValue = k < 1 ? x.o.replace(/\d[\d,]*(\.\d+)?/g, function (tok) { return fmt(tok, f); }) : x.o; }); if (k < 1) requestAnimationFrame(step); else el.__busy = 0; }
    requestAnimationFrame(step);
  }
  /* v3: 단계 목록 동기화 — EMB 가 PXSYNC(root, k) 를 부르면 가장 가까운 .px 의 .pxl li 중 k 번째(0부터)가 켜진다 · k<0 이면 해제 */
  window.PXSYNC = function (root, k) { var px = root.closest('.px') || root.closest('section'); if (!px) return; if (px.__k === k) return; px.__k = k; var lis = px.querySelectorAll('.pxl li'); for (var i = 0; i < lis.length; i++) lis[i].classList.toggle('on', i === k); px.classList.toggle('sync', k >= 0); };
  window.COUNTUP = countUp;

  function init() {
    icons(); var B = build(); if (!B) return;
    var S = B.slides, stage = B.stage, vp = B.vp, cur = 0, lang = 'ko';
    var mode = 'loop', playing = true, auto = false, curD = 2, hold = 0, last = null, notesOn = false;
    try {
      if (B.hasEn) { var sv = localStorage.getItem('deck-lang'); if (sv === 'ko' || sv === 'en') lang = sv; }
      var sm = localStorage.getItem('deck-mode'); if (sm === 'loop' || sm === 'once') mode = sm;
      notesOn = localStorage.getItem('deck-notes') === '1';
    } catch (e) { }
    Object.keys(NEW).forEach(function (k) { if (!EMB[k]) EMB[k] = { en: function (r, R) { NEW[k](r, R, 'en'); }, ko: function (r, R) { NEW[k](r, R, 'ko'); } }; });

    function fit() { var w = vp.clientWidth, h = vp.clientHeight, s = Math.min(w / 1920, h / 1080); stage.style.transform = 'translate(-50%,-50%) scale(' + s + ')'; }
    function blocked() { return !playing || VT >= curD * 1000; }
    function stopAll() { document.querySelectorAll('.emb').forEach(function (e) { e._tok = (e._tok || 0) + 1; e._pending = null; e.innerHTML = ''; }); }
    function runEmb(e, R) {
      var f = EMB[e.dataset.emb]; if (!f) { console.warn('[deck] EMB 없음:', e.dataset.emb); return; }
      if (typeof f === 'function') return f(e, R, lang);
      var g = f[lang] || f.ko || f.en; if (g) g(e, R);
    }
    function start(e) {
      e._tok = (e._tok || 0) + 1; e._pending = null; var my = e._tok;
      var R = function (fn) { requestAnimationFrame(function () { if (e._tok !== my) return; if (blocked()) { e._pending = fn; return; } try { fn(CLK()); } catch (err) { console.error(err); } }); };
      e._R = R; try { runEmb(e, R); } catch (err) { console.error(err); }
    }
    function flush() { S[cur].querySelectorAll('.emb').forEach(function (e) { if (e._pending && e._R) { var f = e._pending; e._pending = null; e._R(f); } }); }
    function restart() { VT = 0; hold = 0; var s = S[cur]; s.classList.remove('active'); void s.offsetWidth; s.classList.add('active'); stopAll(); s.querySelectorAll('.emb').forEach(start); }
    function dur(e) { return parseFloat(e.dataset.dur) || DUR[e.dataset.emb] || 8; }
    function showNotes() { var s = S[cur]; $('#notesbody').textContent = s.dataset.notes || '(이 슬라이드에는 노트가 없다)'; $('#notes').classList.toggle('on', notesOn); $('#notesbtn').setAttribute('aria-pressed', notesOn ? 'true' : 'false');  presUpdate(); }
    // 발표자 창(P): 노트를 별도 창에 크게 · 화면 녹화에 노트가 찍히지 않게 · 창에서 ← → 로 넘김
    var PW = null, T0 = Date.now();
    function ttl(s) { if (!s) return ''; var h = s.querySelector('h1, h2, .h'), t = s.querySelector('.hubt'), e = s.querySelector('.eb'); var x = h ? h.textContent : t ? (e ? e.textContent + ' · ' : '') + t.textContent : e ? e.textContent : ''; return x.replace(/\s+/g, ' ').trim(); }
    function presUpdate() {
      if (!PW || PW.closed) return; var d = PW.document, s = S[cur], nx = S[cur + 1];
      d.getElementById('pn').textContent = (cur + 1) + ' / ' + S.length;
      d.getElementById('pt').textContent = ttl(s);
      d.getElementById('pb').textContent = s.dataset.notes || '(노트 없음)';
      d.getElementById('px').textContent = nx ? '다음 ▸ ' + (cur + 2) + '장 · ' + ttl(nx) : '마지막 장';
      d.getElementById('pb').scrollTop = 0;
    }
    function openPresenter() {
      if (PW && !PW.closed) { PW.focus(); return; }
      PW = window.open('', 'deck-presenter', 'width=980,height=760'); if (!PW) return;
      PW.document.open(); PW.document.write('<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><title>발표자 노트 · ' + document.title + '</title><style>' +
        'body{margin:0;background:#1A1716;color:#F4EFE8;font-family:"IBM Plex Sans KR","Noto Sans KR",sans-serif;display:flex;flex-direction:column;height:100vh}' +
        'header{display:flex;gap:16px;align-items:baseline;padding:14px 22px;border-bottom:1px solid #4A423E}#pn{font:700 22px monospace;color:#F08C3A}#pt{font-weight:700;font-size:20px}#clk{margin-left:auto;font:600 18px monospace;color:#B8AFA6}' +
        '#pb{flex:1;overflow:auto;padding:18px 26px;white-space:pre-line;font-size:var(--fs,22px);line-height:1.75}#px{padding:10px 22px;border-top:1px solid #4A423E;color:#B8AFA6;font-size:16px}' +
        'footer{padding:6px 22px 10px;color:#7d746c;font-size:13px}</style></head><body><header><span id="pn"></span><span id="pt"></span><span id="clk">00:00</span></header>' +
        '<div id="pb"></div><div id="px"></div><footer>← → 넘김 · + − 글자 크기 · 0 시계 초기화 · 【 】 = 진행 지시(읽지 않음)</footer></body></html>');
      PW.document.close(); var fs = 22;
      PW.document.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') { e.preventDefault(); show(cur + 1); }
        else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); show(cur - 1); }
        else if (e.key === ']') stepMove(1); else if (e.key === '[') stepMove(-1);
        else if (e.key === '+' || e.key === '=') { fs = Math.min(40, fs + 2); PW.document.body.style.setProperty('--fs', fs + 'px'); }
        else if (e.key === '-') { fs = Math.max(14, fs - 2); PW.document.body.style.setProperty('--fs', fs + 'px'); }
        else if (e.key === '0') T0 = Date.now();
      });
      T0 = Date.now(); var tk = setInterval(function () { if (!PW || PW.closed) { clearInterval(tk); return; } var t = Math.floor((Date.now() - T0) / 1000); PW.document.getElementById('clk').textContent = String(Math.floor(t / 60)).padStart(2, '0') + ':' + String(t % 60).padStart(2, '0'); }, 1000);
      presUpdate();
    }

    function stepBar(s) {
      s.querySelectorAll('.emb[data-steps]').forEach(function (e) {
        var N = parseInt(e.dataset.steps, 10) || 0; if (!N) return;
        var bar = e._bar; if (!bar) { bar = el('div', { 'class': 'stepbar', role: 'group', 'aria-label': '애니메이션 단계' }); (s.querySelector('.stepslot') || s).appendChild(bar); e._bar = bar; }
        bar.innerHTML = '';
        var all = el('button', { type: 'button', 'data-step': '' }, __L('▶ 전체', '▶ All')); bar.appendChild(all);
        for (var k = 1; k <= N; k++) bar.appendChild(el('button', { type: 'button', 'data-step': String(k) }, (((lang === 'en' && e.dataset.labelsEn) ? e.dataset.labelsEn : e.dataset.labels) ? (((lang === 'en' && e.dataset.labelsEn) ? e.dataset.labelsEn : e.dataset.labels).split('|')[k - 1] || k) : String(k))));
        bar.appendChild(el('span', { 'class': 'lab' }, ((lang === 'en' && e.dataset.steplabEn) ? e.dataset.steplabEn : e.dataset.steplab) || ''));
        bar.appendChild(el('span', { 'class': 'kbd' }, __L('[ ] 단계 · R 다시', '[ ] steps · R replay')));
        function sync() { bar.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.step === (e.dataset.step || '') ? 'true' : 'false'); }); }
        bar.querySelectorAll('button').forEach(function (b) { b.onclick = function () { e.dataset.step = b.dataset.step; sync(); VT = 0; hold = 0; start(e); if (!playing) { playing = true; syncUI(); } }; });
        sync();
      });
      s.querySelectorAll('.prompt').forEach(function (pr) {
        if (pr.querySelector('button.copy')) return;
        var b = el('button', { type: 'button', 'class': 'copy' }, '복사'); pr.appendChild(b);
        b.onclick = function () { var cl = pr.cloneNode(true); cl.querySelectorAll(lang === 'en' ? '.ko,button.copy' : '.en,button.copy').forEach(function (x) { x.remove(); }); var txt = cl.textContent.trim(); function ok() { b.textContent = lang === 'en' ? 'Copied' : '복사됨'; b.classList.add('done'); setTimeout(function () { b.textContent = lang === 'en' ? 'Copy' : '복사'; b.classList.remove('done'); }, 1500); }
          if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(ok, ok); else { var ta = document.createElement('textarea'); ta.value = txt; document.body.appendChild(ta); ta.select(); try { document.execCommand('copy'); } catch (err) { } document.body.removeChild(ta); ok(); } };
      });
    }
    function stepMove(d) {
      var e = S[cur].querySelector('.emb[data-steps]'); if (!e) return; var N = parseInt(e.dataset.steps, 10) || 0;
      var k = e.dataset.step ? parseInt(e.dataset.step, 10) : 0; k = Math.max(0, Math.min(N, k + d)); e.dataset.step = k ? String(k) : '';
      if (e._bar) e._bar.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.step === (e.dataset.step || '') ? 'true' : 'false'); });
      VT = 0; hold = 0; start(e); if (!playing) { playing = true; syncUI(); }
    }
    function show(i, push) {
      i = Math.max(0, Math.min(S.length - 1, i)); stopAll(); S[cur].classList.remove('active'); cur = i; var s = S[cur]; VT = 0; hold = 0;
      var ds = [].map.call(s.querySelectorAll('.emb'), dur); curD = ds.length ? Math.max.apply(0, ds) : 2.5;
      s.classList.add('active'); s.querySelectorAll('.emb').forEach(start); stepBar(s);
      $('#cnt').textContent = (cur + 1) + ' / ' + S.length;
      var h = s.querySelector('h2,h1'); $('#ttl').textContent = h ? ((lang === 'ko' ? h.querySelector('.ko') : h.querySelector('.en')) || h).textContent : '';
      $('#prog').style.width = ((cur + 1) / S.length * 100) + '%';
      showNotes();
      if (s.classList.contains('v3')) setTimeout(function () { if (S[cur] !== s) return; s.querySelectorAll('.n,.tot,[data-count]').forEach(countUp); }, 300);
      if (push !== false) { try { history.replaceState(null, '', '#slide-' + (cur + 1)); } catch (e) { location.hash = 'slide-' + (cur + 1); } }
    }
    function tick(ts) {
      if (last !== null && playing) {
        var dt = Math.min(100, ts - last);
        if (VT < curD * 1000) { VT = Math.min(curD * 1000, VT + dt); }
        else {
          hold += dt; var hasE = S[cur].querySelector('.emb'); var wait = hasE ? 2500 : 8000;
          if (auto && hold >= (hasE ? 3500 : 8000) && cur < S.length - 1) { show(cur + 1); }
          else if (!auto && mode === 'loop' && hasE && hold >= wait) { restart(); }
        }
      }
      last = ts; $('#aprog').style.width = (Math.min(1, VT / (curD * 1000)) * 100) + '%'; requestAnimationFrame(tick);
    }
    function syncUI() {
      document.querySelectorAll('.segm button').forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.m === mode ? 'true' : 'false'); });
      var pb = $('#play'); pb.textContent = playing ? '❚❚' : '▶'; pb.setAttribute('aria-label', playing ? '애니메이션 일시정지' : '애니메이션 재생'); pb.setAttribute('aria-pressed', playing ? 'false' : 'true');
      $('#auto').setAttribute('aria-pressed', auto ? 'true' : 'false'); document.body.classList.toggle('paused', !playing);
    }
    function setMode(m) { mode = m; try { localStorage.setItem('deck-mode', m); } catch (e) { } if (m === 'loop' && VT >= curD * 1000) hold = 0; syncUI(); }
    function togglePlay() { playing = !playing; syncUI(); if (playing) flush(); }
    function setLang(l) {
      if (!B.hasEn) return; lang = l; document.documentElement.lang = l; try { localStorage.setItem('deck-lang', l); } catch (e) { }
      location.reload();  /* 미리 만들어 둔 애니 글자까지 바꾸려고 다시 읽는다(쪽 번호 #slide-N 유지) */
    }
    function toggleNotes() { notesOn = !notesOn; try { localStorage.setItem('deck-notes', notesOn ? '1' : '0'); } catch (e) { } showNotes(); }
    function fromHash() { var m = /^#slide-(\d+)$/.exec(location.hash); return m ? parseInt(m[1], 10) - 1 : 0; }

    $('#prev').onclick = function () { show(cur - 1); }; $('#next').onclick = function () { show(cur + 1); };
    document.querySelectorAll('.seg button').forEach(function (b) { b.onclick = function () { setLang(b.dataset.l); }; });
    document.querySelectorAll('.segm button').forEach(function (b) { b.onclick = function () { setMode(b.dataset.m); }; });
    $('#play').onclick = togglePlay; $('#replay').onclick = function () { restart(); if (!playing) { playing = true; syncUI(); } };
    $('#auto').onclick = function () { auto = !auto; hold = 0; syncUI(); }; $('#notesbtn').onclick = toggleNotes;
    document.addEventListener('keydown', function (e) {
      var t = e.target.tagName; if (t === 'INPUT' || t === 'TEXTAREA' || t === 'SELECT') return;           // 시뮬레이터 입력 중에는 단축키 무시
      if (t === 'BUTTON' && (e.key === ' ' || e.key === 'Enter')) return;
      if (e.key === 'ArrowRight' || e.key === 'PageDown') { e.preventDefault(); show(cur + 1); }
      else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); show(cur - 1); }
      else if (e.key === ' ' || e.key === 'k' || e.key === 'K') { e.preventDefault(); togglePlay(); }
      else if (e.key === 'r' || e.key === 'R') { restart(); } else if (e.key === 'o' || e.key === 'O') { setMode(mode === 'loop' ? 'once' : 'loop'); }
      else if (e.key === 'a' || e.key === 'A') { auto = !auto; hold = 0; syncUI(); } else if (e.key === 'n' || e.key === 'N') { toggleNotes(); } else if (e.key === 'p' || e.key === 'P') { openPresenter(); }
      else if (e.key === 'Home') show(0); else if (e.key === 'End') show(S.length - 1);
      else if (e.key === ']') stepMove(1); else if (e.key === '[') stepMove(-1);
      else if ((e.key === 'l' || e.key === 'L') && B.hasEn) setLang(lang === 'en' ? 'ko' : 'en');
    });
    var tx = null; vp.addEventListener('touchstart', function (e) { tx = e.touches[0].clientX; }, { passive: true });
    vp.addEventListener('touchend', function (e) { if (tx === null) return; var dx = e.changedTouches[0].clientX - tx; if (Math.abs(dx) > 50) show(cur + (dx < 0 ? 1 : -1)); tx = null; });
    window.addEventListener('hashchange', function () { var i = fromHash(); if (i !== cur) show(i, false); });
    window.addEventListener('resize', fit);
    document.documentElement.lang = lang;
    document.querySelectorAll('.seg button').forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.l === lang ? 'true' : 'false'); });
    fit(); cur = 0; S[0].classList.add('active'); show(fromHash(), false); syncUI(); requestAnimationFrame(tick);
    window.DECK = { show: show, restart: restart, count: S.length, current: function () { return cur; }, step: function (k) { var e = S[cur].querySelector('.emb[data-steps]'); if (!e) return; e.dataset.step = k ? String(k) : ''; stepBar(S[cur]); VT = 0; hold = 0; start(e); } };
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
