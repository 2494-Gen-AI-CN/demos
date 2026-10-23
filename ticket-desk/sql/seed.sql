USE ticket_desk;

INSERT INTO priorities VALUES ('high', 4), ('normal', 24), ('low', 72);

INSERT INTO customers (customer_id, name, email, country, monthly_fee)
VALUES
    (1, 'Dana Whitfield', 'dana@example.com', 'CA', 49.00),
    (2, 'Ravi Patel', 'ravi@example.com', 'CA', 199.00),
    (3, 'Mei Chen', 'mei@example.com', 'US', 0.00),
    (4, 'Omar Haddad', 'omar@example.com', 'GB', 49.00);

INSERT INTO agents (agent_id, name, email)
VALUES
    (1, 'Priya', 'priya@desk.example'),
    (2, 'Marco', 'marco@desk.example'),
    (3, 'Sam', 'sam@desk.example'),
    (4, 'Lee', 'lee@desk.example');

INSERT INTO tickets (ticket_id, title, priority, status, customer_id, agent_id, opened_at, closed_at)
VALUES
    (1, 'Login page returns 500', 'high', 'closed', 1, NULL, '2026-10-18 08:00:00', '2026-10-18 11:00:00'),
    (2, 'Invoice PDF is blank', 'normal', 'closed', 2, NULL, '2026-10-17 12:00:00', '2026-10-18 18:00:00'),
    (3, 'Typo on pricing page', 'normal', 'closed', 1, NULL, '2026-10-18 18:00:00', '2026-10-19 04:00:00'),
    (4, 'Checkout button frozen', 'high', 'assigned', 3, 1, '2026-10-19 08:00:00', NULL),
    (5, 'Export is missing rows', 'normal', 'assigned', 2, 2, '2026-10-18 12:00:00', NULL),
    (6, 'Add dark mode', 'low', 'open', 3, NULL, '2026-10-19 12:00:00', NULL);

INSERT INTO tags (name) VALUES ('login'), ('billing'), ('ui');

INSERT INTO ticket_tags VALUES (1, 1), (2, 2), (4, 2), (4, 3), (6, 3);
