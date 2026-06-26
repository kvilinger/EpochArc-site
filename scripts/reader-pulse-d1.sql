CREATE TABLE IF NOT EXISTS reader_pulse_votes (
  reader_id TEXT PRIMARY KEY,
  forecast_id TEXT NOT NULL,
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_reader_pulse_votes_forecast_id
ON reader_pulse_votes (forecast_id);
