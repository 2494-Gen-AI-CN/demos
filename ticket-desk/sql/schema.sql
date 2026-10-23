CREATE DATABASE IF NOT EXISTS ticket_desk;
USE ticket_desk;

CREATE TABLE IF NOT EXISTS customers (
    customer_id INT,
    name VARCHAR(100),
    email VARCHAR(255),
    country CHAR(2),
    monthly_fee DECIMAL(8,2)
);

CREATE TABLE IF NOT EXISTS agents (
    agent_id INT,
    name VARCHAR(50),
    email VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS tickets (
    ticket_id INT,
    title VARCHAR(200),
    priority VARCHAR(10),
    status VARCHAR(10),
    customer_id INT,
    agent_id INT,
    opened_at DATETIME,
    closed_at DATETIME
);
