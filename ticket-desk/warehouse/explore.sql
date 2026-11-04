-- Tickets per status
SELECT status, COUNT(*) as tickets
FROM desk_raw.tickets
GROUP BY status
ORDER BY tickets DESC;

-- open tickets with their customer
SELECT t.ticket_id, t.title, t.status, c.name AS customer
FROM desk_raw.tickets AS t
JOIN desk_raw.customers AS c ON c.customer_id = t.customer_id
WHERE t.status <> 'closed'
ORDER BY t.ticket_id;

-- hours since the previous event
WITH timed AS (
  SELECT ticket_id, event_id, kind, created_at,
    LAG(created_at) OVER (PARTITION BY ticket_id ORDER BY created_at, event_id) AS previous_at
  FROM desk_raw.ticket_events
)
SELECT ticket_id, event_id, kind, DATETIME_DIFF(created_at, previous_at, HOUR) AS hours_since_previous
FROM timed
ORDER BY ticket_id, created_at, event_id;

-- tickets opened per day
WITH RECURSIVE days AS (
  SELECT DATE '2026-10-16' AS day
  UNION ALL
  SELECT DATE_ADD(day, INTERVAL 1 DAY)
  FROM days
  WHERE day < '2026-10-20'
)
SELECT d.day, COUNT(t.ticket_id) AS opened
FROM days AS d
LEFT JOIN desk_raw.tickets AS t ON DATE(t.opened_at) = d.day
GROUP BY d.day
ORDER BY d.day;

-- board, denormalised
SELECT t.ticket_id, t.title, t.status, p.sla_hours, c.name AS customer, a.name AS agent,
  ARRAY_AGG(STRUCT(e.kind, e.created_at) ORDER BY e.created_at, e.event_id) AS history
FROM desk_raw.tickets AS t
JOIN desk_raw.customers AS c ON c.customer_id = t.customer_id
JOIN desk_raw.priorities AS p ON p.priority = t.priority
LEFT JOIN desk_raw.agents AS a ON a.agent_id = t.agent_id
JOIN desk_raw.ticket_events AS e ON e.ticket_id = t.ticket_id
GROUP BY t.ticket_id, t.title, t.status, p.sla_hours, c.name, a.name
ORDER BY t.ticket_id;