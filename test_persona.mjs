// 학습자 페르소나 시뮬레이션 — 단원별로 다양한 stage의 문제를 생성해 보고
// 학습자 관점에서 검토할 수 있도록 정리해 출력
import './test_generators.mjs'; // _gen_only.mjs 갱신
const { GRADES, VISUAL, renderVisual } = await import('./_gen_only.mjs');

console.log('=== 학습자 페르소나 시뮬레이션: 모든 단원 샘플 ===\n');

for (const [grade, info] of Object.entries(GRADES)) {
  console.log(`\n${'='.repeat(60)}`);
  console.log(`${grade}학년 — ${info.desc}`);
  console.log('='.repeat(60));

  for (const unit of info.units) {
    console.log(`\n  [${unit.id}] ${unit.name} ${unit.icon || ''}`);
    const stages = [1, 5, 10];
    for (const stage of stages) {
      try {
        const p = unit.generate(stage);
        const tag = p.choices ? '[MCQ]' : (p.visual ? '[VISUAL]' : '');
        const visualInfo = p.visual ? ` 🖼️ ${p.visual.type}${p.visual.highlight ? '/' + p.visual.highlight : ''}` : '';
        const choicesInfo = p.choices ? ` 보기: [${p.choices.join(', ')}]` : '';
        console.log(`    s${stage} ${tag} ${p.q}`);
        console.log(`         정답: ${p.a}${visualInfo}${choicesInfo}`);
      } catch (e) {
        console.log(`    s${stage} THROW: ${e.message}`);
      }
    }
  }
}
