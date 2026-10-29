-- Active: 1793208302891@@127.0.0.1@3306@ticket_desk
DROP DATABASE IF EXISTS ticket_desk;
CREATE DATABASE ticket_desk;
USE ticket_desk;

-- Priorities table - the SLA Hours and their associated priorities. 
CREATE TABLE priorities (
    priority VARCHAR(10) PRIMARY KEY, -- Tells the database that priority has to be unique and non-null
    sla_hours INT NOT NULL CHECK (sla_hours > 0)  -- CHECK lets us validate data on the way in. A failed check never inserts.
);

-- 3NF: customers 
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY, -- now I don't have to supply the PK on INSERTS
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE, -- enforces unique emails for a customer. 
    country CHAR(2) NOT NULL DEFAULT 'CA',
    monthly_fee DECIMAL(8,2) NOT NULL DEFAULT 0 CHECK (monthly_fee >= 0)
);

CREATE TABLE agents (
    agent_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE
);

-- So far - setting Primary Keys and some basic constraints. Now the tickets table - our first Foreign Key constraints
CREATE TABLE tickets (
    ticket_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    priority VARCHAR(10) NOT NULL, -- points to a record in our priorities table (FK)
    status VARCHAR(10) NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'assigned', 'closed')), -- can only be one of these 3 values
    customer_id INT NOT NULL, -- points to a record in customers table
    agent_id INT, -- CAN be null, when a ticket is created but not yet assigned. Points to agents table
    opened_at DATETIME NOT NULL,
    closed_at DATETIME CHECK (closed_at IS NULL OR closed_at >= opened_at), -- can't have a ticket closed before it was ever opened
    -- Lets add our Foreign Key constraints
    FOREIGN KEY (priority) REFERENCES priorities (priority),
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
    FOREIGN KEY (agent_id) REFERENCES agents (agent_id) ON DELETE SET NULL
);

-- Lets add ticket tagging - this is going to require a linking table to tickets
CREATE TABLE tags (
    tag_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30) NOT NULL UNIQUE
);

-- Our linking table - and we can see what a Composite Primary Key looks like in SQL
CREATE TABLE ticket_tags (
    ticket_id INT,
    tag_id INT,
    PRIMARY KEY (ticket_id, tag_id),
    FOREIGN KEY (ticket_id) REFERENCES tickets (ticket_id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags (tag_id) ON DELETE CASCADE
);

CREATE TABLE ticket_events (
    event_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    ticket_id INT NOT NULL,
    kind VARCHAR(20) NOT NULL,
    note VARCHAR(255),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, -- asking the DB for the current TIME
    FOREIGN KEY (ticket_id) REFERENCES tickets (ticket_id) ON DELETE CASCADE
);
