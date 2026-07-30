import { EVENT_ROUTES } from './event-routes.generated.js';

const CANONICAL_HOST = 'epoch-arc.com';
const HOME_PATHS = new Set([
  '/',
  '/index.html',
  '/zh-hans',
  '/zh-hans/',
  '/zh-hans/index.html'
]);
const PATH_ALIASES = new Map([
  ['/index.html', '/'],
  ['/methods.html', '/methods'],
  ['/methods/', '/methods'],
  ['/arcs.html', '/arcs'],
  ['/arcs/', '/arcs'],
  ['/directions.html', '/directions'],
  ['/directions/', '/directions'],
  ['/zh-hans', '/zh-hans/'],
  ['/zh-hans/index.html', '/zh-hans/']
]);

function routeFor(value) {
  if (!value) return null;
  return Object.prototype.hasOwnProperty.call(EVENT_ROUTES, value)
    ? EVENT_ROUTES[value]
    : null;
}

function canonicalEventPath(url) {
  const requestedEvent = url.searchParams.get('event')?.trim();
  if (requestedEvent && HOME_PATHS.has(url.pathname)) {
    const slug = routeFor(requestedEvent);
    if (!slug) return url.pathname.startsWith('/zh-hans') ? '/zh-hans/' : '/';
    const prefix = url.pathname.startsWith('/zh-hans') ? '/zh-hans' : '';
    return `${prefix}/events/${slug}/`;
  }

  const match = url.pathname.match(
    /^\/(?:(zh-hans)\/)?events\/([^/]+)(?:\/index\.html|\/)?$/
  );
  if (!match) return null;

  let eventKey = match[2];
  try {
    eventKey = decodeURIComponent(eventKey);
  } catch {
    return null;
  }
  const slug = routeFor(eventKey);
  if (!slug) return null;
  const prefix = match[1] ? '/zh-hans' : '';
  return `${prefix}/events/${slug}/`;
}

export function onRequest(context) {
  const url = new URL(context.request.url);
  let shouldRedirect = false;
  const isProductionHost =
    url.hostname === CANONICAL_HOST || url.hostname === 'www.epoch-arc.com';

  if (isProductionHost && url.protocol !== 'https:') {
    url.protocol = 'https:';
    url.port = '';
    shouldRedirect = true;
  }

  if (url.hostname === 'www.epoch-arc.com') {
    url.hostname = CANONICAL_HOST;
    shouldRedirect = true;
  }

  const eventPath = canonicalEventPath(url);
  if (eventPath && eventPath !== url.pathname) {
    url.pathname = eventPath;
    url.search = '';
    shouldRedirect = true;
  } else if (url.searchParams.has('event') && HOME_PATHS.has(url.pathname)) {
    url.search = '';
    shouldRedirect = true;
  }

  const canonicalPath = PATH_ALIASES.get(url.pathname);
  if (canonicalPath && canonicalPath !== url.pathname) {
    url.pathname = canonicalPath;
    shouldRedirect = true;
  }

  if (shouldRedirect) {
    return Response.redirect(url.toString(), 301);
  }

  return context.next();
}
