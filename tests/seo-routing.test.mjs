import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';

import { EVENT_ROUTES, FORECAST_IDS } from '../functions/event-routes.generated.js';
import { onRequest } from '../functions/_middleware.js';
import { onRequestGet as pulseGet, onRequestPost as pulsePost } from '../functions/api/reader-pulse.js';

function requestUrl(url) {
  return onRequest({
    request: new Request(url),
    next: () => new Response('next', { status: 200 })
  });
}

function assertRedirect(source, target) {
  const response = requestUrl(source);
  assert.equal(response.status, 301);
  assert.equal(response.headers.get('location'), target);
}

test('legacy event query redirects to the canonical event page', () => {
  assertRedirect(
    'https://epoch-arc.com/?event=spacex-xai-cursor-2026',
    'https://epoch-arc.com/events/spacex-xai-cursor-2026/'
  );
  assertRedirect(
    'https://epoch-arc.com/index.html?event=mcp-protocol-2024',
    'https://epoch-arc.com/events/model-context-protocol/'
  );
});

test('local Pages development keeps the local origin while canonicalizing paths', () => {
  assertRedirect(
    'http://localhost:4180/?event=o1-2024',
    'http://localhost:4180/events/o1/'
  );
});

test('www and legacy event paths collapse into one redirect', () => {
  assertRedirect(
    'https://www.epoch-arc.com/events/anthropic-asl3-2025/',
    'https://epoch-arc.com/events/anthropic-asl3/'
  );
  assertRedirect(
    'https://www.epoch-arc.com/?event=resnet-2015',
    'https://epoch-arc.com/events/resnet/'
  );
});

test('localized legacy routes preserve the Chinese URL namespace', () => {
  assertRedirect(
    'https://www.epoch-arc.com/zh-hans/index.html?event=o1-2024',
    'https://epoch-arc.com/zh-hans/events/o1/'
  );
  assertRedirect(
    'https://epoch-arc.com/zh-hans/events/anthropic-asl3-2025/index.html',
    'https://epoch-arc.com/zh-hans/events/anthropic-asl3/'
  );
});

test('unknown event queries are removed instead of serving duplicate homepages', () => {
  assertRedirect(
    'https://epoch-arc.com/?event=not-a-published-event',
    'https://epoch-arc.com/'
  );
});

test('static page aliases redirect to their canonical paths', () => {
  assertRedirect(
    'https://www.epoch-arc.com/methods.html',
    'https://epoch-arc.com/methods'
  );
  assertRedirect(
    'https://epoch-arc.com/arcs.html',
    'https://epoch-arc.com/arcs'
  );
});

test('canonical event URLs pass through unchanged', () => {
  const response = requestUrl('https://epoch-arc.com/events/o1/');
  assert.equal(response.status, 200);
  assert.equal(response.headers.get('location'), null);
});

test('generated event aliases and sitemap stay aligned with published events', () => {
  const events = JSON.parse(
    readFileSync(new URL('../data/events.json', import.meta.url), 'utf8')
  );
  const sitemap = readFileSync(new URL('../sitemap.xml', import.meta.url), 'utf8');

  assert.doesNotMatch(sitemap, /www\.epoch-arc\.com|\?event=|\/index\.html/);
  for (const event of events) {
    assert.equal(EVENT_ROUTES[event.id], event.slug);
    assert.equal(EVENT_ROUTES[event.slug], event.slug);
    assertRedirect(
      `https://epoch-arc.com/?event=${event.id}`,
      `https://epoch-arc.com/events/${event.slug}/`
    );
    assertRedirect(
      `https://www.epoch-arc.com/events/${event.id}/index.html`,
      `https://epoch-arc.com/events/${event.slug}/`
    );
    assert.match(sitemap, new RegExp(
      `<loc>https://epoch-arc\\.com/events/${event.slug}/</loc>`
    ));
    assert.match(sitemap, new RegExp(
      `<loc>https://epoch-arc\\.com/zh-hans/events/${event.slug}/</loc>`
    ));
  }
});

test('events_summary.json preserves consensusLevel, impactCount, and impactDimensions for homepage filters', () => {
  const summary = JSON.parse(
    readFileSync(new URL('../data/events_summary.json', import.meta.url), 'utf8')
  );
  assert.ok(summary.length >= 251);
  for (const item of summary) {
    assert.ok(['broad', 'debated', 'emerging'].includes(item.consensusLevel), `${item.id} missing consensusLevel`);
    assert.ok(Number.isInteger(item.impactCount) && item.impactCount >= 0, `${item.id} missing impactCount`);
    assert.ok(Array.isArray(item.impactDimensions), `${item.id} missing impactDimensions`);
  }
});

test('reader-pulse GET does not set unsolicited cookies and POST rejects unknown forecastId', async () => {
  const rows = new Map();
  const mockDb = {
    prepare(sql) {
      return {
        bind(...args) {
          return {
            async first() {
              const id = rows.get(args[0]);
              return id ? { forecast_id: id } : null;
            },
            async run() {
              if (sql.includes('DELETE')) rows.delete(args[0]);
              else rows.set(args[0], args[1]);
              return {};
            }
          };
        },
        async all() {
          const counts = {};
          for (const v of rows.values()) counts[v] = (counts[v] || 0) + 1;
          return { results: Object.entries(counts).map(([forecast_id, total]) => ({ forecast_id, total })) };
        }
      };
    }
  };

  // Passive GET without cookie must NOT emit Set-Cookie
  const getRes = await pulseGet({ request: new Request('https://epoch-arc.com/api/reader-pulse'), env: { READER_PULSE_DB: mockDb } });
  assert.equal(getRes.status, 200);
  assert.equal(getRes.headers.get('set-cookie'), null);

  // POST with unknown forecastId must return 400
  const badPost = await pulsePost({
    request: new Request('https://epoch-arc.com/api/reader-pulse', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ forecastId: 'fake-stuffed-id' })
    }),
    env: { READER_PULSE_DB: mockDb }
  });
  assert.equal(badPost.status, 400);

  // POST with valid forecastId issues UUID cookie and records vote
  const validId = FORECAST_IDS[0];
  const okPost = await pulsePost({
    request: new Request('https://epoch-arc.com/api/reader-pulse', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ forecastId: validId })
    }),
    env: { READER_PULSE_DB: mockDb }
  });
  assert.equal(okPost.status, 200);
  assert.match(okPost.headers.get('set-cookie') || '', /^ea_reader_id=[0-9a-f-]{36};/i);
  const body = await okPost.json();
  assert.equal(body.selectedForecastId, validId);
  assert.equal(body.counts[validId], 1);
});
