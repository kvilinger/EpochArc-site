import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';

import { EVENT_ROUTES } from '../functions/event-routes.generated.js';
import { onRequest } from '../functions/_middleware.js';

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
