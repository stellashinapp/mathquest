// Quick sanity test: extract generators from index.html and run them many times.
// Verifies no undefined answers, no NaN, no negative answers where not expected.
import { readFileSync } from 'fs';

const html = readFileSync('e:/개발/math/www/index.html', 'utf8');
const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/);
if (!scriptMatch) throw new Error('script tag not found');
let code = scriptMatch[1];

// VISUAL/renderVisual은 노출시키되, DOM 의존 글로벌 코드는 그대로 둘 수 있게
// document/window를 stub으로 제공 — 함수 선언만 평가되므로 호출 시점이 아닌 한 안전
const stub = `
const document = {
  getElementById: () => null,
  createElement: () => ({ appendChild: () => {}, setAttribute: () => {}, style: {}, classList: { add: () => {}, remove: () => {}, contains: () => false }, addEventListener: () => {}, querySelector: () => null, querySelectorAll: () => [] }),
  createTextNode: () => ({}),
  addEventListener: () => {},
  body: { appendChild: () => {} },
  querySelector: () => null,
  querySelectorAll: () => [],
};
const window = { Capacitor: undefined, addEventListener: () => {} };
const localStorage = { getItem: () => null, setItem: () => {}, removeItem: () => {} };
const navigator = { userAgent: '' };
const requestAnimationFrame = () => 0;
const setTimeout = () => 0;
const clearTimeout = () => {};
const Audio = function () { return { play: () => {}, pause: () => {} }; };
`;
// 모듈 최상위에서 자동 실행되는 부트 코드는 테스트에서 비활성화
code = code.replace(/^initAds\(\);\s*$/m, '');
code = code.replace(/^showSplash\(\);\s*$/m, '');
code = code.replace(/^render\(screenHome\(\)\);\s*$/m, '');

code = stub + code;
code += '\nexport { GRADES, checkAnswer, parseAnswer, fracStr, VISUAL, renderVisual };';

// Write temp module
import { writeFileSync } from 'fs';
writeFileSync('e:/개발/math/_gen_only.mjs', code);

const { GRADES, checkAnswer, VISUAL, renderVisual } = await import('./_gen_only.mjs');

const RUNS = 50;
const STAGES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15];
let total = 0, issues = 0;
const issuesByUnit = {};
const examples = {};
const recordIssue = (unitId, msg) => {
  issues++;
  issuesByUnit[unitId] = (issuesByUnit[unitId] || 0) + 1;
  console.log(msg);
};

for (const [grade, info] of Object.entries(GRADES)) {
  for (const unit of info.units) {
    examples[unit.id] = [];
    for (const stage of STAGES) {
      for (let i = 0; i < RUNS; i++) {
        total++;
        try {
          const p = unit.generate(stage);
          if (!p || p.q == null || p.a == null) {
            recordIssue(unit.id, `MISSING FIELD grade=${grade} unit=${unit.id} stage=${stage} ${JSON.stringify(p)}`);
            continue;
          }
          // Verify parsing of expected answer works
          if (!checkAnswer(String(p.a), p.a)) {
            recordIssue(unit.id, `SELF-CHECK FAIL grade=${grade} unit=${unit.id} q="${p.q}" a=${p.a}`);
            continue;
          }
          // Check for NaN/Infinity in numeric answers
          if (typeof p.a === 'number' && (Number.isNaN(p.a) || !Number.isFinite(p.a))) {
            recordIssue(unit.id, `NaN/Infinity grade=${grade} unit=${unit.id} q=${p.q} a=${p.a}`);
            continue;
          }
          // 문제 텍스트에 미치환 변수 (${...}, undefined, NaN) 검사
          if (/\$\{|undefined|NaN/.test(p.q)) {
            recordIssue(unit.id, `BAD TEXT grade=${grade} unit=${unit.id} q="${p.q}"`);
            continue;
          }
          // 답이 NaN 문자열
          if (String(p.a).includes('NaN') || String(p.a).includes('undefined')) {
            recordIssue(unit.id, `BAD ANSWER grade=${grade} unit=${unit.id} q="${p.q}" a=${p.a}`);
            continue;
          }
          // 답이 0인 케이스 (몇몇 단원에선 부자연스러움 — 분수 0/d, 둘레 0 등)
          // g2-num3 같은 자릿수 질문은 0이 자연스러운 답이라 제외
          const zeroOk = ['g2-num3', 'g4-bignum'];
          if (typeof p.a === 'number' && p.a === 0 && !zeroOk.includes(unit.id)) {
            recordIssue(unit.id, `ZERO ANSWER grade=${grade} unit=${unit.id} q="${p.q}"`);
            continue;
          }
          // 답이 음수 (현재 모든 단원에 음수 답 없어야 함)
          if (typeof p.a === 'number' && p.a < 0) {
            recordIssue(unit.id, `NEGATIVE grade=${grade} unit=${unit.id} q="${p.q}" a=${p.a}`);
            continue;
          }
          // 답 자릿수 검사 (키패드 max 10자)
          if (String(p.a).replace(/[\-\.\/]/g, '').length > 10) {
            recordIssue(unit.id, `TOO LONG grade=${grade} unit=${unit.id} q="${p.q}" a=${p.a}`);
            continue;
          }
          // visual: 타입이 정의되어 있고, 호출 시 예외 없이 SVG 문자열 반환해야 함
          if (p.visual) {
            if (!VISUAL[p.visual.type]) {
              recordIssue(unit.id, `UNKNOWN VISUAL grade=${grade} unit=${unit.id} q="${p.q}" type=${p.visual.type}`);
              continue;
            }
            try {
              const svg = renderVisual(p.visual);
              if (!svg || !svg.includes('<svg')) {
                recordIssue(unit.id, `VISUAL EMPTY grade=${grade} unit=${unit.id} q="${p.q}" type=${p.visual.type}`);
                continue;
              }
              // SVG에 NaN/undefined가 있으면 SVG 그릴 때 오류
              if (/NaN|undefined/.test(svg)) {
                recordIssue(unit.id, `VISUAL BAD CONTENT grade=${grade} unit=${unit.id} q="${p.q}" type=${p.visual.type}`);
                continue;
              }
            } catch (e) {
              recordIssue(unit.id, `VISUAL THROW grade=${grade} unit=${unit.id} q="${p.q}" type=${p.visual.type}: ${e.message}`);
              continue;
            }
          }
          // MCQ: 정답이 보기 안에 있어야 함, 보기는 4개, 중복 없어야 함
          if (p.choices) {
            if (!Array.isArray(p.choices) || p.choices.length !== 4) {
              recordIssue(unit.id, `MCQ BAD CHOICES (len) grade=${grade} unit=${unit.id} q="${p.q}" choices=${JSON.stringify(p.choices)}`);
              continue;
            }
            const strs = p.choices.map(String);
            if (new Set(strs).size !== 4) {
              recordIssue(unit.id, `MCQ DUP CHOICES grade=${grade} unit=${unit.id} q="${p.q}" choices=${JSON.stringify(p.choices)}`);
              continue;
            }
            if (!strs.includes(String(p.a))) {
              recordIssue(unit.id, `MCQ NO CORRECT grade=${grade} unit=${unit.id} q="${p.q}" a=${p.a} choices=${JSON.stringify(p.choices)}`);
              continue;
            }
            // 보기에 음수/이상값 없는지
            if (p.choices.some(c => typeof c === 'number' && (Number.isNaN(c) || !Number.isFinite(c)))) {
              recordIssue(unit.id, `MCQ BAD VALUES grade=${grade} unit=${unit.id} q="${p.q}" choices=${JSON.stringify(p.choices)}`);
              continue;
            }
          }
          if (examples[unit.id].length < 3 && stage <= 5) {
            const tag = p.choices ? ' [MCQ]' : '';
            examples[unit.id].push(`[s${stage}]${tag} ${p.q}  → ${p.a}`);
          }
        } catch (e) {
          recordIssue(unit.id, `THROW grade=${grade} unit=${unit.id} stage=${stage}: ${e.message}`);
        }
      }
    }
  }
}

console.log(`\n=== ${total} problems generated, ${issues} issues ===\n`);
if (issues > 0) {
  console.log('Issues by unit:');
  for (const [uid, count] of Object.entries(issuesByUnit)) {
    console.log(`  ${uid}: ${count}`);
  }
  console.log('');
}
console.log('Sample problems per unit:');
for (const [uid, samples] of Object.entries(examples)) {
  console.log(`\n--- ${uid} ---`);
  samples.forEach(s => console.log('  ' + s));
}
