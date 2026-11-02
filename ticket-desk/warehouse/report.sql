-- How long does a ticket take to close, per priority, against its SLA?
-- A priority whose bar passes its SLA mark is where the desk is late.
SELECT t.priority, t.sla_hours, ROUND(AVG(DATETIME_DIFF(t.closed_at, t.opened_at, MINUTE)) / 60, 2) AS hours_to_close
FROM desk_dw.fact_ticket_events AS f
JOIN desk_dw.dim_ticket AS t ON t.ticket_key = f.ticket_key
WHERE f.kind = 'closed'
GROUP BY t.priority, t.sla_hours
ORDER BY t.sla_hours;
