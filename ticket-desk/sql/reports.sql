USE ticket_desk;

-- board
SELECT t.ticket_id, CONCAT('TD-', t.ticket_id) AS ref, t.title, t.priority, t.status, c.name AS customer, a.name AS agent, DATE_ADD(t.opened_at, INTERVAL p.sla_hours HOUR) AS deadline
FROM tickets AS t
JOIN customers AS c ON c.customer_id = t.customer_id
JOIN priorities AS p ON p.priority = t.priority
LEFT JOIN agents AS a ON a.agent_id = t.agent_id
ORDER BY t.ticket_id;

-- agent load
SELECT a.name AS agent, COUNT(t.ticket_id) AS open_tickets
FROM agents AS a
LEFT JOIN tickets AS t ON t.agent_id = a.agent_id AND t.status <> 'closed'
GROUP BY a.agent_id, a.name
ORDER BY a.agent_id;

-- breached
SELECT t.ticket_id, t.title, t.priority, p.sla_hours, TIMESTAMPDIFF(HOUR, t.opened_at, t.closed_at) AS hours
FROM tickets AS t
JOIN priorities AS p ON p.priority = t.priority AND TIMESTAMPDIFF(HOUR, t.opened_at, t.closed_at) > p.sla_hours
ORDER BY t.ticket_id;

-- quiet customers
SELECT c.name AS customer, c.email
FROM customers AS c
LEFT JOIN tickets AS t ON t.customer_id = c.customer_id
WHERE t.ticket_id IS NULL;
