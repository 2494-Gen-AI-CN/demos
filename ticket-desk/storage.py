"""Files for the desk: plain text, and the tickets saved as JSON."""
import json
import logging
from datetime import datetime
from pathlib import Path

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
