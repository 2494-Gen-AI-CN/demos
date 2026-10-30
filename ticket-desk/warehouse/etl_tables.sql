-- the cleaned events, with the same columns as the staged ones
CREATE TABLE IF NOT EXISTS desk_raw.ticket_events_clean LIKE desk_raw.ticket_events;

-- the rejected events, the same columns plus the reason
CREATE TABLE IF NOT EXISTS desk_dw.load_rejects AS
SELECT *, '' AS reason
FROM desk_raw.ticket_events
LIMIT 0;

-- one row per run of the job
CREATE TABLE IF NOT EXISTS desk_dw.load_log (
  run_at TIMESTAMP,
  rows_read INT64,
  rows_loaded INT64,
  rows_rejected INT64
);
