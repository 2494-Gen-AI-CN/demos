CREATE USER IF NOT EXISTS 'desk_app'@'%' IDENTIFIED BY 'deskapp';
GRANT SELECT, INSERT, UPDATE, DELETE ON ticket_desk.* TO 'desk_app'@'%';
-- lets the app CALL the procedures and use the function
GRANT EXECUTE ON ticket_desk.* TO 'desk_app'@'%';
