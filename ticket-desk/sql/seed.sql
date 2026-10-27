-- DML 
-- Data Manipulation Langauge - subset of commands for working with individual rows of data
-- We can Create, update, etc. 
-- We already saw INSERT - allowing us to create rows. Lets insert some more records across our 
-- DB tables, agents, customers, tickets

USE ticket_desk; 

INSERT INTO customers (customer_id, name, email, country, monthly_fee)
VALUES 
    (1, "Jonathan De La Cruz", "jonathan.delacruz@revature.com", "US", 49.00),
    (2, "Pancake", "pancake@revature.com", "US", 19.00),
    (3, "John Doe", "jdoe@gmail.com", "CN", 29.00),
    (4, "Jane Doe", "jane.doe@revature.com", "UK", 39.00);

INSERT INTO agents (agent_id, name, email)
VALUES 
    (1, "Astha Patel", "a.patel@gmail.com"),
    (2, "Michael Skinner", "m.skinner@yahoo.com"),
    (3, "David Luu", "d.luu@gmail.com");

INSERT INTO tickets (ticket_id, title, priority, status, customer_id, agent_id, opened_at, closed_at)
VALUES
    (1, 'Login page returns 500', 'high', 'closed', 1, NULL, '2026-10-18 08:00:00', '2026-10-18 11:00:00'),
    (2, 'Invoice PDF is blank', 'normal', 'closed', 2, NULL, '2026-10-17 12:00:00', '2026-10-18 18:00:00'),
    (3, 'Typo on pricing page', 'normal', 'closed', 1, NULL, '2026-10-18 18:00:00', '2026-10-19 04:00:00'),
    (4, 'Checkout button frozen', 'high', 'assigned', 3, 1, '2026-10-19 08:00:00', NULL),
    (5, 'Export is missing rows', 'normal', 'assigned', 2, 2, '2026-10-18 12:00:00', NULL),
    (6, 'Add dark mode', 'low', 'open', 3, NULL, '2026-10-19 12:00:00', NULL);

