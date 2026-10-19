#!/usr/bin/env node
/* 강의 스크립트 JSON + 슬라이드 캡처 → 주차별 Word 문서.
 *   NODE_PATH=<docx 설치 위치>/node_modules node tools/build_scripts_docx.js <캡처폴더> [주차 …]
 * 입력: 스크립트/json/wNN.json (tools/check_script_json.py 형식), <캡처폴더>/wNN/NN.jpg (1920×1080)
 * 출력: 스크립트/NN주차_강의스크립트_<주차명>.docx
 */
const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, ImageRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle, PageBreak, Footer, PageNumber, TableOfContents, PageOrientation,
} = require('docx');

const ROOT = path.resolve(__dirname, '..');
const [shots, ...weeksArg] = process.argv.slice(2);
const syl = Object.fromEntries(JSON.parse(fs.readFileSync(path.join(ROOT, 'tools/syllabus.json'), 'utf8')).weeks.map(w => [w.week, w]));
const weeks = weeksArg.length ? weeksArg.map(Number) : Array.from({ length: 13 }, (_, i) => i + 1);

const FONT = 'Malgun Gothic';
const C = { ink: '1F2937', muted: '64748B', blue: '1A56F5', violet: '6D28D9', green: '047857', line: 'CBD5E1', band: 'EEF2FF', concrete: 'ECFDF5' };
const mmss = s => `${Math.floor(s / 60)}:${String(Math.round(s % 60)).padStart(2, '0')}`;
const dur = s => (s >= 60 ? `${Math.floor(s / 60)}분 ` : '') + (s % 60 ? `${s % 60}초` : '').trim();
const run = (text, o = {}) => new TextRun({ text, font: FONT, size: o.size || 21, bold: o.bold, italics: o.italics, color: o.color || C.ink });
const cellBorders = { top: { style: BorderStyle.SINGLE, size: 4, color: C.line }, bottom: { style: BorderStyle.SINGLE, size: 4, color: C.line }, left: { style: BorderStyle.SINGLE, size: 4, color: C.line }, right: { style: BorderStyle.SINGLE, size: 4, color: C.line } };

function sessionTable(J, S) {
  const widths = [1600, 8570, 2000, 2400];
  const head = ['차시', '차시명 (강의계획서)', '시간', '슬라이드'];
  const mk = (cells, isHead) => new TableRow({
    tableHeader: isHead,
    children: cells.map((t, i) => new TableCell({
      width: { size: widths[i], type: WidthType.DXA }, borders: cellBorders,
      shading: isHead ? { type: ShadingType.CLEAR, fill: C.band, color: 'auto' } : undefined,
      margins: { top: 60, bottom: 60, left: 100, right: 100 },
      children: [new Paragraph({ children: [run(String(t), { bold: isHead, size: 19 })] })],
    })),
  });
  const rows = [mk(head, true)];
  const groups = [['도입', '도입 (표지 · 목표 · 구성)']].concat(syl[J.week].sessions.map(s => [s.code, s.name])).concat([['마무리', '실습 안내 · 정리']]);
  for (const [code, name] of groups) {
    const ss = S.filter(s => s.session === code);
    if (!ss.length) continue;
    const sec = ss.reduce((a, s) => a + s.seconds, 0);
    rows.push(mk([code, name, dur(sec), `#${ss[0].n}–#${ss[ss.length - 1].n}`]));
  }
  const tot = S.filter(s => s.session !== '부록').reduce((a, s) => a + s.seconds, 0);
  rows.push(mk(['합계', '', dur(tot), `${S.length}장`]));
  return new Table({ width: { size: 14570, type: WidthType.DXA }, columnWidths: widths, rows });
}

function build(w) {
  const J = JSON.parse(fs.readFileSync(path.join(ROOT, `스크립트/json/w${String(w).padStart(2, '0')}.json`), 'utf8'));
  const S = J.slides;
  const title = syl[w].title;
  const kids = [];
  kids.push(new Paragraph({ spacing: { after: 120 }, children: [run(`${String(w).padStart(2, '0')}주차 강의 스크립트`, { size: 22, color: C.blue, bold: true })] }));
  kids.push(new Paragraph({ heading: HeadingLevel.TITLE, spacing: { after: 200 }, children: [run(title, { size: 36, bold: true })] }));
  kids.push(new Paragraph({ spacing: { after: 120 }, children: [run('건설소재 역설계 도구 개발을 위한 AI와 분자동역학 활용 · 윤태영 (Taeyoung Yun) · 강의 50분', { size: 19, color: C.muted })] }));
  kids.push(new Paragraph({ spacing: { after: 240 }, children: [run(`학습목표: ${syl[w].goal}`, { size: 20 })] }));
  kids.push(sessionTable(J, S));
  kids.push(new Paragraph({ spacing: { before: 200, after: 80 }, children: [run('읽는 법', { bold: true, size: 20 })] }));
  for (const t of ['2단 표: 왼쪽 = 화면(슬라이드 · 순번 · 차시 · 배정 시간 · 누적 시각) · 오른쪽 = 설명([진행] 지시 → 말할 내용)',
    '【콘크리트 예시】 문단 = 시멘트 · 콘크리트 사례로 개념을 설명하는 부분 (녹색 배경)',
    '부록 슬라이드는 50분 발표 시간에 포함하지 않음 · 질문이 나올 때 참고용']) {
    kids.push(new Paragraph({ bullet: { level: 0 }, children: [run(t, { size: 19, color: C.muted })] }));
  }
  // 스크립트 본문: 2단 표 (왼쪽 = 화면 · 오른쪽 = 설명) — 영상 · 강의 스크립트의 일반 형식
  kids.push(new Paragraph({ children: [new PageBreak()] }));
  const W_L = 6100, W_R = 8470;           // 가로 A4 본문 폭 14570 DXA
  const hdrCell = (t, w) => new TableCell({
    width: { size: w, type: WidthType.DXA }, borders: cellBorders,
    shading: { type: ShadingType.CLEAR, fill: C.band, color: 'auto' }, margins: { top: 80, bottom: 80, left: 120, right: 120 },
    children: [new Paragraph({ children: [run(t, { bold: true, size: 20 })] })],
  });
  const rows = [new TableRow({ tableHeader: true, cantSplit: true, children: [hdrCell('화면', W_L), hdrCell('설명', W_R)] })];
  let acc = 0;
  for (const s of S) {
    const appx = s.session === '부록';
    const img = path.join(shots, `w${String(w).padStart(2, '0')}`, `${String(s.n).padStart(2, '0')}.jpg`);
    const meta = appx ? '부록 · 발표 시간 외' : `${s.session} · ${dur(s.seconds)}`;
    const clock = appx ? '' : `${mmss(acc)} → ${mmss(acc + s.seconds)}`;
    if (!appx) acc += s.seconds;
    const left = [
      new Paragraph({ spacing: { after: 80 }, children: [new ImageRun({ type: 'jpg', data: fs.readFileSync(img), transformation: { width: 384, height: 216 } })] }),
      new Paragraph({ spacing: { after: 40 }, children: [run(`#${String(s.n).padStart(2, '0')}  ${s.label}`, { bold: true, size: 20 })] }),
      new Paragraph({ spacing: { after: 20 }, children: [run(meta, { size: 18, color: appx ? C.violet : C.blue })] }),
    ];
    if (clock) left.push(new Paragraph({ children: [run(clock, { size: 18, color: C.muted })] }));
    const right = [];
    if (s.cue) right.push(new Paragraph({ spacing: { after: 100 }, children: [run('[진행] ', { bold: true, size: 19, color: C.blue }), run(s.cue, { size: 19, italics: true, color: C.muted })] }));
    for (const para of s.script) {
      const ex = para.startsWith('【콘크리트 예시】');
      right.push(new Paragraph({
        spacing: { after: 120, line: 320 },
        shading: ex ? { type: ShadingType.CLEAR, fill: C.concrete, color: 'auto' } : undefined,
        children: ex ? [run('【콘크리트 예시】', { bold: true, color: C.green }), run(para.slice('【콘크리트 예시】'.length))] : [run(para)],
      }));
    }
    rows.push(new TableRow({
      children: [
        new TableCell({ width: { size: W_L, type: WidthType.DXA }, borders: cellBorders, margins: { top: 100, bottom: 100, left: 120, right: 120 }, children: left,
          shading: appx ? { type: ShadingType.CLEAR, fill: 'F5F3FF', color: 'auto' } : undefined }),
        new TableCell({ width: { size: W_R, type: WidthType.DXA }, borders: cellBorders, margins: { top: 100, bottom: 100, left: 160, right: 160 }, children: right }),
      ],
    }));
  }
  kids.push(new Table({ width: { size: W_L + W_R, type: WidthType.DXA }, columnWidths: [W_L, W_R], rows }));
  const doc = new Document({
    creator: '윤태영 (Taeyoung Yun)', title: `${w}주차 강의 스크립트`,
    styles: { default: { document: { run: { font: FONT, size: 21 } } } },
    sections: [{
      properties: { page: { size: { width: 11906, height: 16838, orientation: PageOrientation.LANDSCAPE }, margin: { top: 1000, bottom: 1000, left: 1134, right: 1134 } } },
      footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [run(`${w}주차 · `, { size: 16, color: C.muted }), new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 16, color: C.muted })] })] }) },
      children: kids,
    }],
  });
  const safe = title.split(' — ')[0].replace(/[\\/:*?"<>|]/g, '');
  const out = path.join(ROOT, '스크립트', `${String(w).padStart(2, '0')}주차_강의스크립트_${safe}.docx`);
  return Packer.toBuffer(doc).then(buf => { fs.writeFileSync(out, buf); console.log(path.basename(out), `${(buf.length / 1e6).toFixed(1)} MB`); });
}

(async () => { for (const w of weeks) await build(w); })().catch(e => { console.error(e); process.exit(1); });
