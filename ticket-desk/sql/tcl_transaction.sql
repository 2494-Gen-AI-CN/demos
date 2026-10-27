-- TCL - Transaction Control Langauge

-- If we want to send money from one account at a bank to another
-- that sounds simple in english 
-- "I want to send $50 CAD to Paul"
-- In practice that is a series of discreet steps
USE ticket_desk;

-- TCL - We are wrapping individual statements inside a transaction
START TRANSACTION; -- denotes the beginning of a transaction
DELETE * FROM TICKETS;
ROLLBACK; -- Rollback - typically used inside of a conditional check or an exception try-catch
-- it rolls everything back since the START TRANSACTION

-- Real transactions are typically more complex
START TRANSACTION;

UPDATE tickets SET priority = 'normal' WHERE ticket_id = 6;
SAVEPOINT before_title; -- a named marker inside a transaction

UPDATE tickets SET title = 'Dark mode' WHERE ticket_id = 6;
ROLLBACK TO SAVEPOINT before_title;
COMMIT; -- commit saves everything in the transaction up to this point and ends it

-- ACID Properties
-- Transactions in SQL follow 4 core pillars - ACID

-- Atomicity - Transactions are all or nothing. If a single statement in the transactions fails, 
-- the entire transaction is rolled back to its original state (or a named SAVEPOINT)

-- Consistency - There should never be invalid data as a result of a transaction. The database must 
-- transition from one valid state to another, following all schemas, constraints, triggers

-- Isolation - Concurrent transactions execute independently from one another - without interfering 
-- with or reading uncommitted data from one another. 

-- Durability - Once a transaction is committed, it's changes are permanently written to the disk. 

