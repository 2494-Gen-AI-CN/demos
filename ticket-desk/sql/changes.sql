USE ticket_desk;
UPDATE customers SET monthly_fee = 199.00 WHERE customer_id = 1;
CALL close_ticket(5, '2026-10-19 16:00:00');
