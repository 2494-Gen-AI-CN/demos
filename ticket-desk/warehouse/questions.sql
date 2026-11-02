-- How long does a ticket take to close, per priority?
-- A priority whose average passes its SLA is where the desk staffs first.
SELECT t.priority, t.sla_hours, AVG(f.hours_since_open) AS hours_to_close, SUM(f.event_count) AS closed,
  CASE WHEN AVG(f.hours_since_open) <= t.sla_hours THEN 'within SLA'
  ELSE 'over SLA' END AS sla_band
FROM desk_dw.fact_ticket_events AS f
JOIN desk_dw.dim_ticket AS t ON t.ticket_key = f.ticket_key
WHERE f.kind = 'closed'
GROUP BY t.priority, t.sla_hours
ORDER BY t.priority;

-- The same question through the snowflake.
-- Same answer, one join more: the outrigger saves a copied column and costs a join.
SELECT t.priority, p.sla_hours, AVG(f.hours_since_open) AS hours_to_close, SUM(f.event_count) AS closed
FROM desk_dw.fact_ticket_events AS f
JOIN desk_dw.dim_ticket AS t ON t.ticket_key = f.ticket_key
JOIN desk_dw.dim_priority AS p ON p.priority = t.priority
WHERE f.kind = 'closed'
GROUP BY t.priority, p.sla_hours
ORDER BY t.priority;

-- Which weekdays and agents see the most ticket events?
-- The busiest weekday per agent is where a second agent helps.
SELECT d.weekday, d.is_weekend, a.name AS agent, SUM(f.event_count) AS events
FROM desk_dw.fact_ticket_events AS f
JOIN desk_dw.dim_date AS d ON d.date_key = f.date_key
JOIN desk_dw.dim_agent AS a ON a.agent_key = f.agent_key
GROUP BY d.weekday, d.is_weekend, a.name
ORDER BY d.weekday, agent;

-- Whose tickets moved on one day?
-- One day's movers are the customers the desk calls back first.
SELECT c.name AS customer, SUM(f.event_count) AS events
FROM desk_dw.fact_ticket_events AS f
JOIN desk_dw.dim_customer AS c ON c.customer_key = f.customer_key
WHERE f.event_date = '2026-10-18'
GROUP BY c.name
ORDER BY events DESC, customer;
