"""Files for the desk: plain text, and the tickets saved as JSON."""
import json
import logging
from datetime import datetime
from pathlib import Path

import mysql.connector

from desk import Desk, Ticket

log = logging.getLogger(__name__)


def read_lines(path):
    """Return the lines of a text file as a list, without line endings."""
    with open(path, encoding="utf-8") as f:
        return f.read().splitlines()


def export_board(desk, path):
    """Write one tab-separated line per ticket, replacing the file."""
    with open(path, "w", encoding="utf-8") as f:
        for t in desk:
            fields = [str(t.ticket_id), t.title, t.priority, t.status]
            f.write("\t".join(fields) + "\n")


def append_line(path, text):
    """Add one line of text to the end of the file."""
    with open(path, "a", encoding="utf-8") as f:
        f.write(text + "\n")


def delete_file(path):
    """Delete the file and return True, or return False if it is missing."""
    try:
        Path(path).unlink()
    except FileNotFoundError:
        return False
    return True


def to_record(ticket):
    """Return the ticket as a dict of plain values JSON can hold."""
    closed = None
    if ticket.closed_at is not None:
        closed = ticket.closed_at.isoformat()
    return {
        "ticket_id": ticket.ticket_id,
        "title": ticket.title,
        "priority": ticket.priority,
        "status": ticket.status,
        "assignee": ticket.assignee,
        "opened_at": ticket.opened_at.isoformat(),
        "closed_at": closed,
    }


def from_record(record):
    """Rebuild a ticket from a dict made by to_record."""
    opened = datetime.fromisoformat(record["opened_at"])
    ticket = Ticket(record["ticket_id"], record["title"], record["priority"], opened)
    ticket.status = record["status"]
    ticket.assignee = record["assignee"]
    if record["closed_at"] is not None:
        ticket.closed_at = datetime.fromisoformat(record["closed_at"])
    return ticket


def save_desk(desk, path):
    """Write every ticket in the desk to a JSON file."""
    records = []
    for ticket in desk:
        records.append(to_record(ticket))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)


def load_desk(path):
    """Return the desk saved in the file, or an empty desk if there is none."""
    try:
        with open(path, encoding="utf-8") as f:
            records = json.load(f)
    except FileNotFoundError:
        return Desk()
    except json.JSONDecodeError as err:
        log.error("cannot read %s: %s", path, err)
        raise ValueError(f"{path} is not valid JSON") from err
    desk = Desk()
    for record in records:
        desk.add(from_record(record))
    return desk


def load_desk_db(conn):
    """Return a desk holding every ticket in the database, in id order."""
    cursor = conn.cursor()
    cursor.execute(
        """SELECT t.ticket_id, t.title, t.priority, t.status, a.name, t.opened_at, t.closed_at
        FROM tickets AS t
        LEFT JOIN agents AS a ON a.agent_id = t.agent_id
        ORDER BY t.ticket_id"""
    )
    desk = Desk()
    for ticket_id, title, priority, status, agent_name, opened_at, closed_at in cursor.fetchall():
        ticket = Ticket(ticket_id, title, priority, opened_at)
        ticket.status = status
        ticket.assignee = agent_name
        ticket.closed_at = closed_at
        desk.add(ticket)
    cursor.close()
    conn.commit()
    return desk


def insert_ticket(conn, ticket, customer_id):
    """Insert a new ticket for a customer and commit it."""
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO tickets (ticket_id, title, priority, customer_id, opened_at)
        VALUES (%s, %s, %s, %s, %s)""",
        (ticket.ticket_id, ticket.title, ticket.priority, customer_id, ticket.opened_at),
    )
    conn.commit()


def close_ticket_db(conn, ticket_id, at):
    """Close a ticket in the database at the given moment and commit."""
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE tickets
        SET status = 'closed', closed_at = %s
        WHERE ticket_id = %s""",
        (at, ticket_id),
    )
    conn.commit()


def delete_ticket_db(conn, ticket_id):
    """Delete a ticket, commit, and return how many rows went."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tickets WHERE ticket_id = %s", (ticket_id,))
    conn.commit()
    return cursor.rowcount


def assign_ticket(conn, ticket_id, agent_id):
    """Give a ticket to an agent in one transaction, rolling back on any error."""
    cursor = conn.cursor()
    try:
        conn.start_transaction()
        cursor.execute(
            """UPDATE tickets
            SET agent_id = %s, status = 'assigned'
            WHERE ticket_id = %s AND status <> 'closed'""",
            (agent_id, ticket_id),
        )
        if cursor.rowcount == 0:
            raise ValueError(f"ticket {ticket_id} was not assigned")
        cursor.execute(
            """INSERT INTO ticket_events (ticket_id, kind, note)
            VALUES (%s, 'assigned', %s)""",
            (ticket_id, f"agent {agent_id}"),
        )
        event_id = cursor.lastrowid
        conn.commit()
    except (mysql.connector.Error, ValueError):
        conn.rollback()
        log.error("assignment of ticket %s rolled back", ticket_id)
        raise
    finally:
        cursor.close()
    return event_id
