// 에뮬레이터 WebView에 연결해서 모든 단원 자동 테스트
import { WebSocket } from 'ws';

const targetsRes = await fetch('http://localhost:9222/json/list');
const targets = await targetsRes.json();
const target = targets.find(t => t.type === 'page');
if (!target) throw new Error('No page found');
console.log('Target:', target.title, target.url);

const ws = new WebSocket(target.webSocketDebuggerUrl);
let msgId = 0;
const pending = new Map();

ws.on('message', (data) => {
  const msg = JSON.parse(data.toString());
  if (msg.id && pending.has(msg.id)) {
    const { resolve } = pending.get(msg.id);
    pending.delete(msg.id);
    resolve(msg.result);
  }
});

await new Promise(r => ws.on('open', r));

function send(method, params = {}) {
  const id = ++msgId;
  return new Promise((resolve, reject) => {
    pending.set(id, { resolve, reject });
    ws.send(JSON.stringify({ id, method, params }));
  });
}

async function evalJs(code) {
  const res = await send('Runtime.evaluate', {
    expression: code,
    awaitPromise: true,
    returnByValue: true,
  });
  if (res.exceptionDetails) {
    throw new Error('JS error: ' + JSON.stringify(res.exceptionDetails));
  }
  return res.result.value;
}

// 모든 단원 × 3회 자동 테스트
const testCode = `
(async () => {
  const report = {
    totalGrades: 0,
    totalUnits: 0,
    totalProblems: 0,
    totalCorrect: 0,
    failures: [],
    samples: [],
  };
  for (const [g, info] of Object.entries(GRADES)) {
    report.totalGrades++;
    for (const unit of info.units) {
      report.totalUnits++;
      // 각 단원 3회 검증 (랜덤 stage 1~10)
      for (let trial = 0; trial < 3; trial++) {
        const stage = 1 + Math.floor(Math.random() * 10);
        const p = unit.generate(stage);
        if (!p || p.q == null || p.a == null) {
          report.failures.push({ grade: g, unit: unit.id, stage, reason: 'invalid problem', p });
          continue;
        }
        report.totalProblems++;
        // 자기 자신을 정답으로 체크
        const ok = checkAnswer(String(p.a), p.a);
        if (ok) {
          report.totalCorrect++;
        } else {
          report.failures.push({ grade: g, unit: unit.id, stage, q: p.q, a: p.a, reason: 'self-check failed' });
        }
        // 풀이 생성도 확인
        try {
          const exp = getExplanation(p);
          if (!exp || exp.length < 10) {
            report.failures.push({ grade: g, unit: unit.id, stage, q: p.q, reason: 'short explanation', exp });
          }
        } catch (e) {
          report.failures.push({ grade: g, unit: unit.id, stage, q: p.q, reason: 'explanation throw: ' + e.message });
        }
        // 처음 2개씩 샘플 저장 (각 단원별로)
        if (trial === 0 && report.samples.length < 60) {
          report.samples.push({ unit: unit.id, q: p.q, a: p.a, stage });
        }
      }
    }
  }
  return report;
})();
`;

console.log('Running automated test of all units (3× each)...');
const start = Date.now();
const result = await evalJs(testCode);
const elapsed = ((Date.now() - start) / 1000).toFixed(1);

console.log(`\n=== 결과 (${elapsed}s) ===`);
console.log(`학년: ${result.totalGrades}`);
console.log(`단원: ${result.totalUnits}`);
console.log(`문제: ${result.totalProblems}`);
console.log(`정답률: ${(result.totalCorrect / result.totalProblems * 100).toFixed(1)}%`);
console.log(`실패: ${result.failures.length}`);

if (result.failures.length > 0) {
  console.log('\n--- 실패 사례 ---');
  result.failures.slice(0, 20).forEach(f => {
    console.log(`  [${f.grade}/${f.unit} stage ${f.stage}] ${f.reason}: ${f.q || ''}`);
  });
}

console.log('\n--- 단원별 샘플 ---');
result.samples.forEach(s => console.log(`  ${s.unit} (s${s.stage}): ${s.q} → ${s.a}`));

ws.close();
process.exit(0);
