import { test } from 'node:test';
import assert from 'node:assert/strict';
import worker from '../workers/cv-download-tracker/src/index.js';

for (const language of ['fr', 'en']) {
  test(`counts a ${language} GET request, not a completed download`, async () => {
    const events = [];
    const response = await worker.fetch(new Request(`https://cv.example/${language}`), {
      CV_DOWNLOADS: { writeDataPoint: (event) => events.push(event) },
    });
    assert.equal(response.status, 302);
    assert.equal(response.headers.get('Cache-Control'), 'no-store');
    assert.ok(response.headers.get('Location').endsWith(`cv-${language}.pdf`));
    assert.deepEqual(events, [{ blobs: [language, 'cv_request'], doubles: [1], indexes: ['cv-download'] }]);
  });
}
for (const options of [{ method: 'HEAD' }, { headers: { Purpose: 'prefetch' } }, { headers: { 'Sec-Purpose': 'prefetch;prerender' } }]) {
  test(`does not count ${JSON.stringify(options)}`, async () => {
    let count = 0;
    const response = await worker.fetch(new Request('https://cv.example/fr', options), {
      CV_DOWNLOADS: { writeDataPoint: () => count++ },
    });
    assert.equal(response.status, 302);
    assert.equal(count, 0);
  });
}
test('measurement failure does not block the CV', async () => {
  const response = await worker.fetch(new Request('https://cv.example/en'), {});
  assert.equal(response.status, 302);
});
test('rejects unsupported languages and methods without measurement', async () => {
  assert.equal((await worker.fetch(new Request('https://cv.example/de'), {})).status, 404);
  const response = await worker.fetch(new Request('https://cv.example/fr', { method: 'POST' }), {});
  assert.equal(response.status, 405);
  assert.equal(response.headers.get('Allow'), 'GET, HEAD');
});
