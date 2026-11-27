import { FORECAST_IDS } from '../event-routes.generated.js';

const COOKIE_NAME = 'ea_reader_id';
const ONE_YEAR_SECONDS = 60 * 60 * 24 * 365;
const UUID_PATTERN = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const VALID_FORECAST_IDS = new Set(Array.isArray(FORECAST_IDS) ? FORECAST_IDS : []);

function json(data, init = {}) {
  return new Response(JSON.stringify(data), {
    status: init.status || 200,
    headers: {
      'Cache-Control': 'no-store',
      'Content-Type': 'application/json; charset=utf-8',
      ...(init.headers || {})
    }
  });
}

function readCookie(cookieHeader, name) {
  if (!cookieHeader) return '';
  const match = cookieHeader.match(new RegExp(`(?:^|; )${name}=([^;]+)`));
  if (!match) return '';
  try {
    const value = decodeURIComponent(match[1]).trim();
    return UUID_PATTERN.test(value) ? value : '';
  } catch {
    return '';
  }
}

function buildCookie(readerId) {
  return `${COOKIE_NAME}=${encodeURIComponent(readerId)}; Path=/; HttpOnly; SameSite=Lax; Max-Age=${ONE_YEAR_SECONDS}; Secure`;
}

function resolveReaderId(request, { issueIfMissing }) {
  const existing = readCookie(request.headers.get('Cookie'), COOKIE_NAME);
  if (existing) {
    return { readerId: existing, setCookie: '' };
  }
  if (!issueIfMissing) {
    return { readerId: '', setCookie: '' };
  }
  const readerId = crypto.randomUUID();
  return {
    readerId,
    setCookie: buildCookie(readerId)
  };
}

async function readSelectedForecastId(db, readerId) {
  if (!readerId) return '';
  const result = await db
    .prepare('SELECT forecast_id FROM reader_pulse_votes WHERE reader_id = ? LIMIT 1')
    .bind(readerId)
    .first();
  return typeof result?.forecast_id === 'string' && VALID_FORECAST_IDS.has(result.forecast_id)
    ? result.forecast_id
    : '';
}

async function readSelectionCounts(db) {
  const result = await db
    .prepare(`
      SELECT forecast_id, COUNT(*) AS total
      FROM reader_pulse_votes
      GROUP BY forecast_id
    `)
    .all();

  return Object.fromEntries(
    (result?.results || [])
      .map((row) => [row.forecast_id, Number(row.total || 0)])
      .filter(([forecastId, total]) => VALID_FORECAST_IDS.has(forecastId) && total > 0)
  );
}

async function writeSelection(db, readerId, forecastId) {
  if (!readerId) return;
  if (!forecastId) {
    await db
      .prepare('DELETE FROM reader_pulse_votes WHERE reader_id = ?')
      .bind(readerId)
      .run();
    return;
  }

  await db
    .prepare(`
      INSERT INTO reader_pulse_votes (reader_id, forecast_id, updated_at)
      VALUES (?, ?, datetime('now'))
      ON CONFLICT(reader_id) DO UPDATE SET
        forecast_id = excluded.forecast_id,
        updated_at = datetime('now')
    `)
    .bind(readerId, forecastId)
    .run();
}

async function handleReaderPulse(context, { allowWrite }) {
  const db = context.env.READER_PULSE_DB;
  if (!db) {
    return json({ error: 'Missing READER_PULSE_DB binding.' }, { status: 500 });
  }

  let forecastId = '';
  if (allowWrite) {
    const body = await context.request.json().catch(() => ({}));
    forecastId = String(body?.forecastId || '').trim();
    if (forecastId && !VALID_FORECAST_IDS.has(forecastId)) {
      return json({ error: 'Unknown forecastId.' }, { status: 400 });
    }
  }

  const { readerId, setCookie } = resolveReaderId(context.request, {
    issueIfMissing: Boolean(allowWrite && forecastId)
  });

  if (allowWrite) {
    await writeSelection(db, readerId, forecastId);
  }

  const [selectedForecastId, counts] = await Promise.all([
    readSelectedForecastId(db, readerId),
    readSelectionCounts(db)
  ]);

  return json(
    {
      selectedForecastId,
      counts
    },
    {
      headers: setCookie ? { 'Set-Cookie': setCookie } : {}
    }
  );
}

export async function onRequestGet(context) {
  return handleReaderPulse(context, { allowWrite: false });
}

export async function onRequestPost(context) {
  return handleReaderPulse(context, { allowWrite: true });
}
