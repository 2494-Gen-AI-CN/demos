-- Lets explore DDL some more before we seed our database. 
-- DDL stands for Data Definition Language - the subset of commands for defining
-- database structures and constraints 
-- CREATE, ALTER, DROP, TRUNCATE, MODIFY, RENAME 
-- Some SQL dialects/vendor implementations have more commands than others - they
-- add them for quality of life reasons. 

USE ticket_desk; -- added to the top so MySQL knows what database to target these commands against

DROP TABLE scratch_notes;

-- CREATE - lets us create a database structure (Table, Database, Store procedure (later in the week), etc
CREATE TABLE scratch_notes (
    note_id INT,
    body VARCHAR(255)
);

-- ALTER - lets us change something about a table that already exists. Things like add or drop columns,
-- add new rules/constraints, etc. 
ALTER TABLE scratch_notes ADD COLUMN author VARCHAR(50);

-- Inside of MySQL we get access to MODIFY - MODIFY is used within an ALTER to change a table's definition
-- but keep it's name
ALTER TABLE scratch_notes MODIFY body VARCHAR(500);

-- RENAME - Another DDL keyword that MySQL has access to, lets us rename a column in place without touching
-- it's definition
ALTER TABLE scratch_notes RENAME COLUMN author TO written_by;

-- DROP - I can use DROP to get rid of database structure. Columns, tables, even entire databases.
-- I want to be REALLY REALLY careful when I call this because outside of external tools like snapshots
-- there is no UNDO in SQL. 
ALTER TABLE scratch_notes DROP COLUMN written_by;

-- Our first DML command - INSERT. We'll use it to add two scratch_note rows
INSERT INTO scratch_notes (note_id, body) 
VALUES 
    (1, "This is my first note"),
    (2, "This is my second note");

-- At this point - our table has some values

-- Lets do a very basic SELECT to see what's in our table.
SELECT * FROM scratch_notes;

-- TRUNCATE - empties all records from the table BUT preserves it's structure
-- columns, names, definitions (value type), constraints, etc
TRUNCATE TABLE scratch_notes;

SELECT * FROM scratch_notes; -- we should get nothing back here, but the table exists so no error

SHOW TABLES; -- this will just print out all the tables in my database.

DROP TABLE scratch_notes; -- there is no going back 

SHOW TABLES; -- just for demo we call this again to see that the scratch_notes table is gone

