import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import test from 'node:test';
import { impactCount, impactDimensions, impactIndexLabel, impactEmptyMessage } from '../src/js/impact-display.js';
import { escapeSourceText, safeSourceUrl, SOURCE_TYPE_LABELS } from '../src/js/source-safety.js';

test('empty impacts never display as measured 0/10', () => {
  assert.equal(impactIndexLabel({ impacts: [], impactIndex: 0 }), 'No impacts recorded');
  assert.equal(impactIndexLabel({ impacts: [], impactIndex: 0 }, true), '尚无已记录影响');
  assert.match(impactEmptyMessage(), /does not establish zero/);
  assert.match(impactEmptyMessage(true), /不表示实测影响为零/);
});

test('trimmed summaries carry explicit impactCount; missing data is not evidence of zero', () => {
  assert.equal(impactCount({ impactCount: 0 }), 0);
  assert.equal(impactIndexLabel({ impactIndex: 0, impactCount: 0 }), 'No impacts recorded');
  assert.equal(impactIndexLabel({ impactIndex: 0 }), 'Impact data pending');
  assert.equal(impactIndexLabel({ impacts: [{}], impactIndex: 2 }), '2/10');
  assert.equal(impactIndexLabel({ impacts: [{ severity: 0 }], impactIndex: 0 }), '0/10');
  assert.equal(impactCount({ impactCount: false }), null);
});

test('summary dimensions remain filterable without full impacts and missing data is safe', () => {
  assert.deepEqual(impactDimensions({}), []);
  assert.deepEqual(impactDimensions({ impactDimensions: ['risk_creation', 'risk_creation'] }), ['risk_creation']);
  assert.deepEqual(impactDimensions({ impacts: [{ dimension: 'risk_creation' }, { dimension: 'risk_creation' }], impactDimensions: [] }), ['risk_creation']);
});

test('untrusted source citations cannot use script URLs or inject HTML', () => {
  assert.equal(safeSourceUrl('javascript:alert(1)'), null);
  assert.equal(safeSourceUrl('https://example.com/\nfoo'), null);
  assert.equal(safeSourceUrl('https://example.com/a?x=1'), 'https://example.com/a?x=1');
  assert.equal(escapeSourceText('<img onerror="alert(1)">'), '&lt;img onerror=&quot;alert(1)&quot;&gt;');
});

test('Python static and JS dynamic labels/messages agree for both languages', () => {
  const cases = [{ impacts: [], impactIndex: 0 }, { impacts: [{}], impactIndex: 2 }];
  const script = `import json,sys;sys.path.insert(0,'scripts');from impact_display import impact_index_label,EMPTY;from html_safety import SOURCE_TYPE_LABELS;cases=json.loads(sys.argv[1]);print(json.dumps({'labels':[[impact_index_label(e,l) for l in ['en','zhHans']] for e in cases],'messages':[EMPTY['en'],EMPTY['zhHans']],'sourceTypes':SOURCE_TYPE_LABELS}))`;
  const result = JSON.parse(execFileSync('python3', ['-B', '-c', script, JSON.stringify(cases)], { cwd: new URL('..', import.meta.url), encoding: 'utf8' }));
  assert.deepEqual(result.labels, cases.map(e => [impactIndexLabel(e), impactIndexLabel(e, true)]));
  assert.deepEqual(result.messages, [impactEmptyMessage(), impactEmptyMessage(true)]);
  assert.deepEqual(result.sourceTypes, SOURCE_TYPE_LABELS);
});

test('main.js category tooltip matches canonical 6 categories and avoids legacy 8-category labels', async () => {
  const { readFileSync } = await import('node:fs');
  const mainJs = readFileSync(new URL('../src/js/main.js', import.meta.url), 'utf8');
  for (const label of ['Capability Breakthrough', 'Products &amp; Tools', 'Commerce &amp; Industry', 'Governance &amp; Regulation', 'Safety &amp; Ethics', 'Society &amp; Culture']) {
    assert.match(mainJs, new RegExp(label));
  }
  assert.doesNotMatch(mainJs, /· <strong>Model<\/strong>|· <strong>Open Source<\/strong>/);
});
