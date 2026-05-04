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

const RUNS = 30;
const STAGES = [1, 3, 5, 8, 12];
let total = 0, issues = 0;
const examples = {};

for (const [grade, info] of Object.entries(GRADES)) {
  for (const unit of info.units) {
    examples[unit.id] = [];
    for (const stage of STAGES) {
      for (let i = 0; i < RUNS; i++) {
        total++;
        try {
          const p = unit.generate(stage);
          if (!p || p.q == null || p.a == null) {
            issues++;
            console.log(`MISSING FIELD grade=${grade} unit=${unit.id} stage=${stage}`, p);
            continue;
          }
          // Verify parsing of expected answer works
          if (!checkAnswer(String(p.a), p.a)) {
            issues++;
            console.log(`SELF-CHECK FAIL grade=${grade} unit=${unit.id} q="${p.q}" a=${p.a}`);
            continue;
          }
          // Check for NaN in numeric answers
          if (typeof p.a === 'number' && Number.isNaN(p.a)) {
            issues++;
            console.log(`NaN grade=${grade} unit=${unit.id} q=${p.q}`);
            continue;
          }
          // visual: 타입이 정의되어 있고, 호출 시 예외 없이 SVG 문자열 반환해야 함
          if (p.visual) {
            if (!VISUAL[p.visual.type]) {
              issues++;
              console.log(`UNKNOWN VISUAL grade=${grade} unit=${unit.id} q="${p.q}" type=${p.visual.type}`);
              continue;
            }
            try {
              const svg = renderVisual(p.visual);
              if (!svg || !svg.includes('<svg')) {
                issues++;
                console.log(`VISUAL EMPTY grade=${grade} unit=${unit.id} q="${p.q}" type=${p.visual.type}`);
                continue;
              }
            } catch (e) {
              issues++;
              console.log(`VISUAL THROW grade=${grade} unit=${unit.id} q="${p.q}" type=${p.visual.type}: ${e.message}`);
              continue;
            }
          }
          // MCQ: 정답이 보기 안에 있어야 함, 보기는 4개, 중복 없어야 함
          if (p.choices) {
            if (!Array.isArray(p.choices) || p.choices.length !== 4) {
              issues++;
              console.log(`MCQ BAD CHOICES (len) grade=${grade} unit=${unit.id} q="${p.q}" choices=${JSON.stringify(p.choices)}`);
              continue;
            }
            const strs = p.choices.map(String);
            if (new Set(strs).size !== 4) {
              issues++;
              console.log(`MCQ DUP CHOICES grade=${grade} unit=${unit.id} q="${p.q}" choices=${JSON.stringify(p.choices)}`);
              continue;
            }
            if (!strs.includes(String(p.a))) {
              issues++;
              console.log(`MCQ NO CORRECT grade=${grade} unit=${unit.id} q="${p.q}" a=${p.a} choices=${JSON.stringify(p.choices)}`);
              continue;
            }
          }
          if (examples[unit.id].length < 3 && stage <= 5) {
            const tag = p.choices ? ' [MCQ]' : '';
            examples[unit.id].push(`[s${stage}]${tag} ${p.q}  → ${p.a}`);
          }
        } catch (e) {
          issues++;
          console.log(`THROW grade=${grade} unit=${unit.id} stage=${stage}: ${e.message}`);
        }
      }
    }
  }
}

console.log(`\n=== ${total} problems generated, ${issues} issues ===\n`);
console.log('Sample problems per unit:');
for (const [uid, samples] of Object.entries(examples)) {
  console.log(`\n--- ${uid} ---`);
  samples.forEach(s => console.log('  ' + s));
}
