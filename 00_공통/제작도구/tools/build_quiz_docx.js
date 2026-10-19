#!/usr/bin/env node
/* 평가문항 JSON → Word 문서 1개(13주 전체) + CSV(LMS 입력용).
 *   NODE_PATH=<docx 설치 위치>/node_modules node tools/build_quiz_docx.js
 * 입력: 평가문항/json/qNN.json (tools/check_quiz_json.py 형식)
 * 출력: 평가문항/평가문항_전체_정답해설.docx · 평가문항/평가문항_전체.csv
 */
const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle, PageBreak, Footer, PageNumber,
} = require('docx');

const ROOT = path.resolve(__dirname, '..');
const DIR = path.join(ROOT, '평가문항');
const FONT = 'Malgun Gothic';
const C = { ink: '1F2937', muted: '64748B', blue: '1A56F5', green: '047857', line: 'CBD5E1', band: 'EEF2FF', key: 'ECFDF5' };
const NUM = ['①', '②', '③', '④'];
const run = (text, o = {}) => new TextRun({ text, font: FONT, size: o.size || 21, bold: o.bold, italics: o.italics, color: o.color || C.ink });
const B = { style: BorderStyle.SINGLE, size: 4, color: C.line };
const borders = { top: B, bottom: B, left: B, right: B };
const W = 9638;                                   // 세로 A4 본문 폭 (여백 1134)

const weeks = Array.from({ length: 13 }, (_, i) => i + 1)
  .map(w => path.join(DIR, 'json', `q${String(w).padStart(2, '0')}.json`))
  .filter(p => fs.existsSync(p)).map(p => JSON.parse(fs.readFileSync(p, 'utf8')));

const answerText = i => i.type === '객관식' ? `${NUM[i.answer - 1]} ${i.options[i.answer - 1]}`
  : i.type === 'OX' ? i.answer : i.answer + (i.accept && i.accept.length ? `  (인정: ${i.accept.filter(a => a !== i.answer).join(', ')})` : '');

function itemTable(q, i) {
  const cell = (children, o = {}) => new TableCell({
    width: { size: W, type: WidthType.DXA }, borders, margins: { top: 90, bottom: 90, left: 140, right: 140 },
    shading: o.fill ? { type: ShadingType.CLEAR, fill: o.fill, color: 'auto' } : undefined, children,
  });
  const head = [run(`${q.week}-${i.no}`, { bold: true, color: C.blue }), run(`   ${i.type} · 난이도 ${i.difficulty} · 차시 ${i.session}`, { size: 18, color: C.muted })];
  const body = [new Paragraph({ spacing: { after: 100, line: 320 }, children: [run(i.question, { bold: true })] })];
  if (i.type === '객관식') i.options.forEach((o, k) => body.push(new Paragraph({ indent: { left: 240 }, spacing: { after: 40 }, children: [run(`${NUM[k]} ${o}`)] })));
  if (i.type === 'OX') body.push(new Paragraph({ indent: { left: 240 }, children: [run('( O / X )', { color: C.muted })] }));
  if (i.type === '단답형') body.push(new Paragraph({ indent: { left: 240 }, children: [run('답: ____________________', { color: C.muted })] }));
  const key = [
    new Paragraph({ spacing: { after: 60 }, children: [run('정답  ', { bold: true, color: C.green }), run(answerText(i), { bold: true })] }),
    new Paragraph({ spacing: { after: 60, line: 300 }, children: [run('해설  ', { bold: true, color: C.green }), run(i.explanation, { size: 20 })] }),
    new Paragraph({ children: [run(`근거  ${q.week}주차 발표용 덱 #${String(i.source.slide).padStart(2, '0')} 「${i.source.label}」`, { size: 18, color: C.muted })] }),
  ];
  return new Table({
    width: { size: W, type: WidthType.DXA }, columnWidths: [W],
    rows: [new TableRow({ cantSplit: true, children: [cell([new Paragraph({ children: head })], { fill: C.band })] }),
      new TableRow({ cantSplit: true, children: [cell(body)] }),
      new TableRow({ cantSplit: true, children: [cell(key, { fill: C.key })] })],
  });
}

function summaryTable() {
  const widths = [900, 4538, 1100, 1100, 1000, 1000];
  const mk = (cells, head) => new TableRow({
    tableHeader: head, children: cells.map((t, k) => new TableCell({
      width: { size: widths[k], type: WidthType.DXA }, borders, margins: { top: 50, bottom: 50, left: 90, right: 90 },
      shading: head ? { type: ShadingType.CLEAR, fill: C.band, color: 'auto' } : undefined,
      children: [new Paragraph({ children: [run(String(t), { size: 18, bold: head })] })],
    })),
  });
  const rows = [mk(['주차', '주차명', '객관식', 'OX', '단답형', '합계'], true)];
  let tot = 0;
  for (const q of weeks) {
    const c = t => q.items.filter(i => i.type === t).length;
    tot += q.items.length;
    rows.push(mk([q.week, q.title.split(' — ')[0], c('객관식'), c('OX'), c('단답형'), q.items.length]));
  }
  rows.push(mk(['합계', '', '', '', '', tot]));
  return new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: widths, rows });
}

const kids = [
  new Paragraph({ heading: HeadingLevel.TITLE, spacing: { after: 160 }, children: [run('평가문항 (정답 · 해설 포함)', { size: 36, bold: true })] }),
  new Paragraph({ spacing: { after: 240 }, children: [run('건설소재 역설계 도구 개발을 위한 AI와 분자동역학 활용 · 윤태영 (Taeyoung Yun) · 요구사항 PLR-004 (주차당 5문항 이상)', { size: 19, color: C.muted })] }),
  summaryTable(),
  new Paragraph({ spacing: { before: 200, after: 60 }, children: [run('구성 기준', { bold: true, size: 20 })] }),
];
for (const t of ['주차당 6문항: 4지선다 3 · OX 2 · 단답형 1, 난이도 하 · 중 · 상 혼합',
  '모든 문항은 해당 주차 발표용 덱과 강의 스크립트 내용에서만 출제 · 근거 슬라이드 번호 표기',
  '부록 · 보충 덱 내용과 검토 중인 수치(tools/review_todo.md)는 출제에서 제외',
  '단답형 「인정」 = 채점 시 함께 정답으로 인정하는 표기 (영문 · 동의어)']) {
  kids.push(new Paragraph({ bullet: { level: 0 }, children: [run(t, { size: 19, color: C.muted })] }));
}
for (const q of weeks) {
  kids.push(new Paragraph({ children: [new PageBreak()] }));
  kids.push(new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { after: 200 }, children: [run(`${q.week}주차 · ${q.title}`, { size: 28, bold: true })] }));
  for (const i of q.items) { kids.push(itemTable(q, i)); kids.push(new Paragraph({ spacing: { after: 160 }, children: [] })); }
}
const doc = new Document({
  creator: '윤태영 (Taeyoung Yun)', title: '평가문항',
  styles: { default: { document: { run: { font: FONT, size: 21 } } } },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 16, color: C.muted })] })] }) },
    children: kids,
  }],
});

// CSV (UTF-8 BOM, 엑셀 호환)
const esc = v => `"${String(v ?? '').replace(/"/g, '""')}"`;
const csv = [['주차', '번호', '유형', '난이도', '차시', '문제', '선택지1', '선택지2', '선택지3', '선택지4', '정답', '인정답안', '해설', '근거슬라이드']];
for (const q of weeks) for (const i of q.items) {
  const o = i.options || [];
  csv.push([q.week, i.no, i.type, i.difficulty, i.session, i.question, o[0], o[1], o[2], o[3], i.answer, (i.accept || []).join(' | '), i.explanation, `#${i.source.slide} ${i.source.label}`]);
}
fs.writeFileSync(path.join(DIR, '평가문항_전체.csv'), '﻿' + csv.map(r => r.map(esc).join(',')).join('\r\n'));
Packer.toBuffer(doc).then(b => { fs.writeFileSync(path.join(DIR, '평가문항_전체_정답해설.docx'), b); console.log(`${weeks.length}주 · ${csv.length - 1}문항`); });
