"""Support-ticket desk: tickets, SLA deadlines and a board."""
import logging
from datetime import timedelta
from desk import NOW, Desk, Ticket, redact, ticket_refs


def main():
    """Build the sample desk, print the board and the overdue count."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    t1 = Ticket(1, "Login page returns 500", "high", NOW - timedelta(hours=30))
    t2 = Ticket(2, "Invoice PDF is blank", "normal", NOW - timedelta(hours=50))
    t3 = Ticket(3, "Typo on pricing page", "normal", NOW - timedelta(hours=20))
    t4 = Ticket(4, "Checkout button frozen", "high", NOW - timedelta(hours=6))
    t5 = Ticket(5, "Export is missing rows", "normal", NOW - timedelta(hours=26))
    t6 = Ticket(6, "Add dark mode", "low", NOW - timedelta(hours=2))
    desk = Desk()
    for t in [t1, t2, t3, t4, t5, t6]:
        desk.add(t)
    t1.close(t1.opened_at + timedelta(hours=3))
    t2.close(t2.opened_at + timedelta(hours=30))
    t3.close(t3.opened_at + timedelta(hours=10))
    t4.assign("Priya")
    t5.assign("Marco")

    for t in desk:
        print(t.ticket_id, t.priority, t.status, t.days_open())
    late = desk.overdue()
    print(len(late))

    note = "Same problem as TD-2 and TD-5, reply to dana@example.com"
    print(ticket_refs(note))
    print(redact(note))


if __name__ == "__main__":
    main()
