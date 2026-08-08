// Check what backend returns with crop/disease context
const res = await fetch('http://localhost:3100/api/qa/stream', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ query: 'এই রোগের প্রতিকার কি?', crop: 'Wheat', disease: 'Leaf Rust' }),
});

console.log('Status:', res.status);
const reader = res.body.getReader();
const decoder = new TextDecoder();
let buf = '';

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  buf += decoder.decode(value, { stream: true });
  const lines = buf.split('\n');
  buf = lines.pop() || '';
  for (const line of lines) {
    const t = line.trim();
    if (!t) continue;
    if (t.startsWith('final:')) {
      const jsonStr = t.slice(6).trim();
      const parsed = JSON.parse(jsonStr);
      console.log('\n=== ANSWER ===');
      console.log(parsed.answer);
      console.log('\n=== SOURCES ===');
      parsed.sources.forEach(s => console.log(`  ${s.id} score=${s.score}`));
    }
  }
}
