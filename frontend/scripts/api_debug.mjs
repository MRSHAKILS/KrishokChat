// Debug: test the stream parsing directly
const res = await fetch('http://localhost:3100/api/qa/stream', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ query: 'আলুর দেরি ব্লাইট রোগের প্রতিকার কি?' }),
});

console.log('Status:', res.status);
const reader = res.body.getReader();
const decoder = new TextDecoder();
let buf = '';
let finalAnswer = null;

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
      console.log('\n=== FINAL LINE (first 1000 chars) ===');
      console.log(t.substring(0, 1000));
      const jsonStr = t.slice(6).trim();
      try {
        const parsed = JSON.parse(jsonStr);
        console.log('\n=== PARSED FINAL ===');
        console.log('category:', parsed.category);
        console.log('confidence:', parsed.confidence);
        console.log('answer length:', parsed.answer?.length);
        console.log('answer (first 300):', parsed.answer?.substring(0, 300));
        console.log('sources count:', parsed.sources?.length);
      } catch (e) {
        console.log('JSON parse error:', e.message);
      }
    }
  }
}
console.log('\nDone');
