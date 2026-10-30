"""Extract the desk's MySQL tables into files for the warehouse."""
import csv
import json
from pathlib import Path

from db import connect

EXPORTS = Path("exports")
TABLES = ("priorities", "customers", "agents", "tickets")


def read_table(conn, table):
    """Return every row of one desk table as a list of dicts."""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    cursor.close()
    conn.commit()
    return rows


def read_events(conn, after):
    """Return the desk's events with an event_id above after, oldest first."""
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ticket_events WHERE event_id > %s ORDER BY event_id", (after,))
    rows = cursor.fetchall()
    cursor.close()
    conn.commit()
    return rows


def write_csv(rows, path):
    """Write rows to a CSV file, with a header row of column names."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_jsonl(rows, path):
    """Write rows to a JSON-lines file, one JSON object per line."""
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, default=str) + "\n")


def main():
    """Export the four tables to CSV files and the event history to JSON lines."""
    EXPORTS.mkdir(exist_ok=True)
    conn = connect()
    for table in TABLES:
        rows = read_table(conn, table)
        write_csv(rows, EXPORTS / f"{table}.csv")
        print(table, len(rows))
    events = read_table(conn, "ticket_events")
    write_jsonl(events, EXPORTS / "ticket_events.jsonl")
    print("ticket_events", len(events))
    conn.close()


if __name__ == "__main__":
    main()
