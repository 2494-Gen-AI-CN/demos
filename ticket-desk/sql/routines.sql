-- Active: 1793208302891@@127.0.0.1@3306@ticket_desk

-- Trigger - Functions/code that the server auto-runs when a specific event (INSERT, UPDATE, DELETE, etc)
-- occurs on a specific table. 

DELIMITER //
CREATE TRIGGER tickets_status_change
AFTER UPDATE ON tickets
FOR EACH ROW
BEGIN
    IF OLD.status <> NEW.status OR NOT (OLD.agent_id <=> NEW.agent_id) THEN
        INSERT INTO ticket_events (ticket_id, kind, note)
        VALUES (NEW.ticket_id, NEW.status, CONCAT('was ', OLD.status, ', agent ', COALESCE(NEW.agent_id, 'none')));
    END IF;
END //
DELIMITER ;

UPDATE tickets
SET status = 'closed', closed_at = CURRENT_TIMESTAMP
WHERE ticket_id = 5;

SELECT * FROM ticket_events;

SHOW TRIGGERS\G

-- Views

-- OR REPLACE swaps the definition of a view that already exists
CREATE OR REPLACE VIEW open_board AS
SELECT t.ticket_id, CONCAT('TD-', t.ticket_id) AS ref, t.title, t.priority, t.status,
    c.name AS customer,
    a.name AS agent,
    DATE_ADD(t.opened_at, INTERVAL p.sla_hours HOUR) AS deadline
FROM tickets AS t
JOIN customers AS c ON c.customer_id = t.customer_id -- our first join, joining tickets and customers on customer_id
JOIN priorities AS p ON p.priority = t.priority
LEFT JOIN agents AS a ON a.agent_id = t.agent_id
WHERE t.status <> 'closed' -- the board only shows tickets still being worked
ORDER BY t.ticket_id;

SELECT * FROM open_board;

-- how many open tickets each agent holds (agents with none still show up, thanks to the LEFT JOIN)
CREATE VIEW agent_load AS
SELECT a.name AS agent, COUNT(t.ticket_id) AS open_tickets
FROM agents AS a
LEFT JOIN tickets AS t ON t.agent_id = a.agent_id AND t.status <> 'closed'
GROUP BY a.agent_id, a.name
ORDER BY a.agent_id;

SELECT * FROM agent_load;


-- Stored procedure - just a block of named SQL. Similar to a trigger except we can ask for it
-- to be run using CALL. 
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

-- every ticket one customer has opened, looked up by their email
CREATE PROCEDURE tickets_for_customer(IN p_email VARCHAR(255))
BEGIN
    SELECT t.ticket_id, t.title, t.status
    FROM tickets AS t
    JOIN customers AS c ON c.customer_id = t.customer_id
    WHERE c.email = p_email
    ORDER BY t.ticket_id;
END //
DELIMITER ;

CALL log_event(1, 'test', 'Trying out my new stored procedure');

SELECT * FROM ticket_events;

CALL close_ticket (4, CURRENT_TIMESTAMP);

SELECT * FROM tickets;

SELECT * FROM ticket_events;

CALL tickets_for_customer('pancake@revature.com');

-- User Defined Functions
-- The same way we have a bunch of built in Scalar and Aggregate functions that we can call during a query
-- we can define our own. 

CREATE FUNCTION hours_open(p_opened DATETIME, p_closed DATETIME)
RETURNS DECIMAL(8,2) -- specifying return type
DETERMINISTIC -- for a given set of inputs I will get the same outputs
RETURN ROUND(TIMESTAMPDIFF(MINUTE, p_opened, p_closed) / 60, 2); -- getting that return

SELECT ticket_id, hours_open(opened_at, closed_at) AS hours FROM tickets;

-- Index 
-- If we find ourselves commonly doing a lookup against a particular clumn's value - we can create an index
-- Similar to the index of a book. Under the hood InnoDB (the database engine) stores everything in a B-tree 

EXPLAIN SELECT * FROM tickets WHERE status = 'open';

CREATE INDEX idx_tickets_status ON tickets (status);

EXPLAIN SELECT * FROM tickets WHERE status = 'open';