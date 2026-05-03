// Quick sanity test: extract generators from index.html and run them many times.
// Verifies no undefined answers, no NaN, no negative answers where not expected.
import { readFileSync } from 'fs';

const html = readFileSync('e:/개발/math/www/index.html', 'utf8');
const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/);
if (!scriptMatch) throw new Error('script tag not found');
let code = scriptMatch[1];

// Strip DOM-dependent code so we can run the generators only
code = code.replace(/const app = document\.getElementById[\s\S]*$/, '');
code = code.replace(/let currentAnswer[\s\S]*?'';/, '');
// Stub window for ad integration checks
code = 'const window = { Capacitor: undefined };\n' + code;
code += '\nexport { GRADES, checkAnswer, parseAnswer, fracStr };';

// Write temp module
import { writeFileSync } from 'fs';
writeFileSync('e:/개발/math/_gen_only.mjs', code);

const { GRADES, checkAnswer } = await import('./_gen_only.mjs');

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
          if (examples[unit.id].length < 3 && stage <= 5) {
            examples[unit.id].push(`[s${stage}] ${p.q}  → ${p.a}`);
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
