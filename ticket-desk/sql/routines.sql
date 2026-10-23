USE ticket_desk;

DELIMITER //
CREATE TRIGGER tickets_status_change
AFTER UPDATE ON tickets
FOR EACH ROW
BEGIN
    IF OLD.status <> NEW.status OR NOT (OLD.agent_id <=> NEW.agent_id) THEN
        CALL log_event(NEW.ticket_id, NEW.status, CONCAT('was ', OLD.status, ', agent ', COALESCE(NEW.agent_id, 'none')));
    END IF;
END //
DELIMITER ;

CREATE VIEW open_board AS
SELECT t.ticket_id, CONCAT('TD-', t.ticket_id) AS ref, t.title, t.priority, t.status, c.name AS customer, a.name AS agent, DATE_ADD(t.opened_at, INTERVAL p.sla_hours HOUR) AS deadline
FROM tickets AS t
JOIN customers AS c ON c.customer_id = t.customer_id
JOIN priorities AS p ON p.priority = t.priority
LEFT JOIN agents AS a ON a.agent_id = t.agent_id
WHERE t.status <> 'closed'
ORDER BY t.ticket_id;

CREATE VIEW agent_load AS
SELECT a.name AS agent, COUNT(t.ticket_id) AS open_tickets
FROM agents AS a
LEFT JOIN tickets AS t ON t.agent_id = a.agent_id AND t.status <> 'closed'
GROUP BY a.agent_id, a.name
ORDER BY a.agent_id;

DELIMITER //
CREATE PROCEDURE log_event(IN p_ticket_id INT, IN p_kind VARCHAR(20), IN p_note VARCHAR(255))
BEGIN
    INSERT INTO ticket_events (ticket_id, kind, note)
    VALUES (p_ticket_id, p_kind, p_note);
END //

CREATE PROCEDURE close_ticket(IN p_ticket_id INT, IN p_closed_at DATETIME)
BEGIN
    UPDATE tickets
    SET status = 'closed', closed_at = p_closed_at
    WHERE ticket_id = p_ticket_id;
END //

CREATE PROCEDURE tickets_for_customer(IN p_email VARCHAR(255))
BEGIN
    SELECT t.ticket_id, t.title, t.status
    FROM tickets AS t
    JOIN customers AS c ON c.customer_id = t.customer_id
    WHERE c.email = p_email
    ORDER BY t.ticket_id;
END //
DELIMITER ;

CREATE FUNCTION hours_open(p_opened DATETIME, p_closed DATETIME)
RETURNS DECIMAL(8,2)
DETERMINISTIC
RETURN ROUND(TIMESTAMPDIFF(MINUTE, p_opened, p_closed) / 60, 2);

CREATE INDEX idx_tickets_status ON tickets (status);
