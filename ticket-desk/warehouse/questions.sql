-- hours to close per priority (star)
SELECT t.priority, t.sla_hours, AVG(f.hours_since_open) AS hours_to_close, SUM(f.event_count) AS closed
FROM desk_dw.fact_ticket_events AS f
JOIN desk_dw.dim_ticket AS t ON t.ticket_key = f.ticket_key
WHERE f.kind = 'closed'
GROUP BY t.priority, t.sla_hours
ORDER BY t.priority;

-- the same through the snowflake
SELECT t.priority, p.sla_hours, AVG(f.hours_since_open) AS hours_to_close, SUM(f.event_count) AS closed
FROM desk_dw.fact_ticket_events AS f
JOIN desk_dw.dim_ticket AS t ON t.ticket_key = f.ticket_key
JOIN desk_dw.dim_priority AS p ON p.priority = t.priority
WHERE f.kind = 'closed'
GROUP BY t.priority, p.sla_hours
ORDER BY t.priority;

-- events per weekday and agent
SELECT d.weekday, d.is_weekend, a.name AS agent, SUM(f.event_count) AS events
FROM desk_dw.fact_ticket_events AS f
JOIN desk_dw.dim_date AS d ON d.date_key = f.date_key
JOIN desk_dw.dim_agent AS a ON a.agent_key = f.agent_key
GROUP BY d.weekday, d.is_weekend, a.name
ORDER BY d.weekday, agent;

-- one day only
SELECT c.name AS customer, SUM(f.event_count) AS events
FROM desk_dw.fact_ticket_events AS f
JOIN desk_dw.dim_customer AS c ON c.customer_key = f.customer_key
WHERE f.event_date = '2026-10-18'
GROUP BY c.name
ORDER BY events DESC, customer;
