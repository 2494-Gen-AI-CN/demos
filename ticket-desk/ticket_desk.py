"""Support-ticket desk: tickets, SLA deadlines and a board."""
import logging
from chart import hours_chart, status_chart
from db import connect
from desk import NOW, Ticket, redact, ticket_refs
from frame import hours_by_priority, load_frame, status_table
from report import status_counts
from stats import summary
from storage import append_line, export_board, load_desk_db, open_board, read_lines, save_desk

log = logging.getLogger(__name__)
DATA = "tickets.json"


def main():
    """Load the desk from MySQL, print the board and save the tickets."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    conn = connect()
    desk = load_desk_db(conn)
    for row in open_board(conn):
        print(row["ref"], row["customer"], row["agent"], row["deadline"])

    try:
        extra = Ticket(7, "Refund charged twice", "urgent", NOW)
    except ValueError as err:
        log.error("rejected ticket: %s", err)
    else:
        desk.add(extra)
    finally:
        log.info("intake done")

    for t in desk:
        print(t.ticket_id, t.priority, t.status, t.days_open())
    late = desk.overdue()
    print(len(late))

    note = "Same problem as TD-2 and TD-5, reply to dana@example.com"
    print(ticket_refs(note))
    print(redact(note))

    export_board(desk, "board.txt")
    append_line("board.txt", "end of shift")
    print(read_lines("board.txt"))
    print(summary(desk))
    print(status_counts(desk))
    save_desk(desk, DATA)
    conn.close()
    df = load_frame(DATA)
    print(df[["ticket_id", "priority", "status"]])
    print(status_table(df))
    print(hours_by_priority(df))
    status_chart(df, "status.png")
    hours_chart(df, "hours.png")


if __name__ == "__main__":
    main()
