const COOKIE_NAME = 'ea_reader_id';
const ONE_YEAR_SECONDS = 60 * 60 * 24 * 365;
const FORECAST_ID_PATTERN = /^[a-z0-9-]{1,80}$/;

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
  return match ? decodeURIComponent(match[1]) : '';
}

function buildCookie(readerId) {
  return `${COOKIE_NAME}=${encodeURIComponent(readerId)}; Path=/; HttpOnly; SameSite=Lax; Max-Age=${ONE_YEAR_SECONDS}; Secure`;
}

function normalizeForecastId(value) {
  const forecastId = String(value || '').trim();
  if (!forecastId) return '';
  return FORECAST_ID_PATTERN.test(forecastId) ? forecastId : '';
}

async function ensureReaderId(request) {
  const existing = readCookie(request.headers.get('Cookie'), COOKIE_NAME);
  if (existing) {
    return { readerId: existing, setCookie: '' };
  }
  const readerId = crypto.randomUUID();
  return {
    readerId,
    setCookie: buildCookie(readerId)
  };
}

async function readSelectedForecastId(db, readerId) {
  const result = await db
    .prepare('SELECT forecast_id FROM reader_pulse_votes WHERE reader_id = ? LIMIT 1')
    .bind(readerId)
    .first();
  return typeof result?.forecast_id === 'string' ? result.forecast_id : '';
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
      .filter(([forecastId, total]) => forecastId && total > 0)
  );
}

async function writeSelection(db, readerId, forecastId) {
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

  const { readerId, setCookie } = await ensureReaderId(context.request);

  if (allowWrite) {
    const body = await context.request.json().catch(() => ({}));
    const forecastId = normalizeForecastId(body?.forecastId);
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
