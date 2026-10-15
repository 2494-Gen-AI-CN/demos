"""Support-ticket desk: tickets, SLA deadlines and a board."""
import logging
from datetime import timedelta
from chart import hours_chart, status_chart
from desk import NOW, Ticket, redact, ticket_refs
from frame import hours_by_priority, load_frame, status_table
from report import status_counts
from stats import summary
from storage import append_line, export_board, load_desk, read_lines, save_desk

log = logging.getLogger(__name__)
DATA = "tickets.json"


def main():
    """Load or seed the desk, print the board and save the tickets."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    desk = load_desk(DATA)
    if len(desk) == 0:
        t1 = Ticket(1, "Login page returns 500", "high", NOW - timedelta(hours=30))
        t2 = Ticket(2, "Invoice PDF is blank", "normal", NOW - timedelta(hours=50))
        t3 = Ticket(3, "Typo on pricing page", "normal", NOW - timedelta(hours=20))
        t4 = Ticket(4, "Checkout button frozen", "high", NOW - timedelta(hours=6))
        t5 = Ticket(5, "Export is missing rows", "normal", NOW - timedelta(hours=26))
        t6 = Ticket(6, "Add dark mode", "low", NOW - timedelta(hours=2))
        for t in [t1, t2, t3, t4, t5, t6]:
            desk.add(t)
        t1.close(t1.opened_at + timedelta(hours=3))
        t2.close(t2.opened_at + timedelta(hours=30))
        t3.close(t3.opened_at + timedelta(hours=10))
        t4.assign("Priya")
        t5.assign("Marco")

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
    df = load_frame(DATA)
    print(df[["ticket_id", "priority", "status"]])
    print(status_table(df))
    print(hours_by_priority(df))
    status_chart(df, "status.png")
    hours_chart(df, "hours.png")


if __name__ == "__main__":
    main()
