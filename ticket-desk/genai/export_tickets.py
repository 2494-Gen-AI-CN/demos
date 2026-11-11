"""Export the tickets of one status, with each customer's email, to a CSV file."""
import csv
import logging
import sys

from db import connect

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def main():
    """Write every ticket of the status given on the command line to tickets.csv."""
    if len(sys.argv) < 2:
        raise SystemExit("Usage: export_tickets.py <status>")

    status = sys.argv[1].strip()
    if not status:
        raise SystemExit("Status cannot be empty.")

    conn = connect()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT t.ticket_id, t.title, t.status, c.email "
            "FROM tickets t "
            "JOIN customers c ON c.customer_id = t.customer_id "
            "WHERE t.status = %s",
            (status,),
        )
        rows = cursor.fetchall()
        cursor.close()

        with open("tickets.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["ticket_id", "title", "status", "email"])
            writer.writeheader()
            for row in rows:
                log.info("writing ticket %s (%s)", row["ticket_id"], row["title"])
                writer.writerow(row)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
