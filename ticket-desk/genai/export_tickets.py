"""Export the tickets of one status, with each customer's email, to a CSV file."""
import csv
import logging
import os
import sys

import mysql.connector

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def main():
    """Write every ticket of the status given on the command line to tickets.csv."""
    status = sys.argv[1]
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="desk_app",
        password=os.environ.get("DESK_DB_PASSWORD", "deskapp"),
        database="ticket_desk",
        ssl_disabled=True,
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT t.ticket_id, t.title, t.status, c.email FROM tickets t "
        "JOIN customers c ON c.customer_id = t.customer_id "
        f"WHERE t.status = '{status}'"
    )
    rows = cursor.fetchall()
    cursor.close()
    with open("tickets.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["ticket_id", "title", "status", "email"])
        writer.writeheader()
        for row in rows:
            log.info("writing %s", row)
            writer.writerow(row)
    conn.close()


if __name__ == "__main__":
    main()
