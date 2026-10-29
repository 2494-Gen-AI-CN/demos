-- Active: 1793208302891@@127.0.0.1@3306@ticket_desk

-- SELECT with WHERE - we've already seen this. But I think with at most one criteria/condition

-- Give me the ticket_id, title, priority and status of every OPEN high priority ticket
SELECT ticket_id, title, priority, status
FROM tickets
WHERE priority = 'high' AND status <> 'closed'; -- priority high, status NOT EQUAL TO 'closed'

SELECT ticket_id, title, status
FROM tickets
WHERE status IN ('open', 'assigned'); -- saves us chaining with OR when checking same column 

-- We can can check for values between a start and end value, if the column's type is
-- comparable in that way. So datetimes, numbers of all kinds, currency, etc
SELECT *
FROM tickets
WHERE opened_at BETWEEN '2026-10-18 00:00:00' AND '2026-10-18 23:59:59';

-- We can do string searching on CHAR() and VARCHAR() columns
-- It looks similar to but does not follow REGEX rules
SELECT ticket_id, title FROM tickets WHERE title LIKE '%page%';


-- If I want to find unassigned tickets - intuitively I would search for missing agent_id's
-- but in SQL Null is never equal to anything. 
SELECT ticket_id, title FROM tickets WHERE agent_id = NULL; -- bad, doesn't work how we expect it to

SELECT ticket_id, title FROM tickets WHERE agent_id IS NULL; -- IS and IS NOT for NULL or not NULL checks

-- Finally, we can tweak things about our result set
SELECT ticket_id, title, opened_at
FROM tickets
ORDER BY opened_at DESC
LIMIT 3;

-- Column aliasing  and Scalar Functions
SELECT LOWER(name) FROM agents;

-- Calling Concat - for string concat and ALSO using an alias.
SELECT CONCAT('TD-', ticket_id) as ref, title
FROM tickets;

SELECT ticket_id, ROUND(TIMESTAMPDIFF(MINUTE, opened_at, closed_at) / 60, 1) AS hours
FROM tickets
ORDER BY hours DESC;

-- Aggregate functions
SELECT COUNT(*) AS tickets
FROM tickets;

-- GROUP BY and HAVING
-- How many tickets belong to each status? 
SELECT status, COUNT(*) AS tickets
FROM tickets
GROUP BY status;

SELECT priority, ROUND(AVG(TIMESTAMPDIFF(MINUTE, opened_at, closed_at) / 60), 1) AS avg_hours
FROM tickets
GROUP BY priority
HAVING AVG(TIMESTAMPDIFF(MINUTE, opened_at, closed_at) / 60) > 5;


-- Subqueries
-- nesting queries inside of other queries. The SQL database engine runs the inner query, then
-- runs the outer query against the result set of the inner query
SELECT ticket_id, title
FROM tickets
WHERE customer_id = (SELECT customer_id FROM customers WHERE email = 'jonathan.delacruz@revature.com');

-- If the inner query returns more than one value, use IN instead of =
SELECT ticket_id, title FROM tickets
WHERE customer_id IN (SELECT customer_id FROM customers WHERE country = 'US')

-- A subquery only returns info from one table in its result set - even if it looks into another
-- table to do some filtration based on a comparison
-- If we need values from two tables in the same result set (from the same query) - we need a join
SELECT t.ticket_id, t.title, c.name AS customer
FROM tickets AS t -- this table becomes my LEFT table
INNER JOIN customers as c -- this table becomes my RIGHT table
ON c.customer_id = t.customer_id;


-- This is an example of a theta join - one of the ON clauses uses anything thats not strict 
-- equality comparison
SELECT t.ticket_id, t.title, p.sla_hours, TIMESTAMPDIFF(HOUR, t.opened_at, t.closed_at) AS hours
FROM tickets AS t
JOIN priorities AS p
ON p.priority = t.priority
AND TIMESTAMPDIFF(HOUR, t.opened_at, t.closed_at) > p.sla_hours;

-- Left and Right joins
-- LEFT JOIN keeps every row of the left table (left table is the FROM table)
-- RIGHT JOIN is the inverse, keeps every row of the RIGHT table (the JOIN table)
-- Left and right are arbitrary, its literally what order you list the tables in
SELECT a.name, t.ticket_id
FROM agents AS a
LEFT JOIN tickets as t ON t.agent_id = a.agent_id;

-- Complex/multi-joins
SELECT t.ticket_id, t.title, t.priority, t.status, c.name, a.name, DATE_ADD(t.opened_at, INTERVAL p.sla_hours HOUR) AS deadline
FROM tickets AS t
JOIN customers AS c ON c.customer_id = t.customer_id -- our first join, joining tickets and customers on customer_id
JOIN priorities AS p ON p.priority = t.priority
LEFT JOIN agents AS a ON a.agent_id = t.agent_id
ORDER BY t.ticket_id;

-- MySQL does not have a FULL OUTER JOIN - if we want to get back that sort of result
-- we need to use a LEFT JOIN, UNION, RIGHT JOIN
-- UNION combines the result sets of two or more SELECT statements
-- into a single distinct result set. It automatically removes duplicate rows.
SELECT a.name, t.ticket_id
FROM agents AS a
LEFT JOIN tickets AS t ON t.agent_id = a.agent_id
UNION
SELECT a.name, t.ticket_id
FROM agents AS a
RIGHT JOIN tickets AS t ON t.agent_id = a.agent_id;

SELECT a.name AS agent, p.priority
FROM agents AS a
CROSS JOIN priorities AS p
ORDER BY a.agent_id, p.sla_hours;