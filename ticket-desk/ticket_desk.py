"""Support-ticket desk: tickets, SLA deadlines and a board."""
import logging
import math
import re
from datetime import datetime, timedelta

SLA_HOURS = {"high": 4, "normal": 24, "low": 72}
NOW = datetime(2026, 10, 19, 14, 0)
TICKET_REF = re.compile(r"\bTD-(\d+)\b")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
log = logging.getLogger(__name__)


class Ticket:
    def __init__(self, ticket_id, title, priority, opened_at):
        self.ticket_id = ticket_id
        self.title = title
        self.priority = priority
        self.opened_at = opened_at
        self.status = "open"
        self.assignee = None
        self.closed_at = None

    def __repr__(self):
        return f"TD-{self.ticket_id} {self.title} [{self.priority}, {self.status}]"

    def deadline(self):
        return self.opened_at + timedelta(hours=SLA_HOURS[self.priority])

    def days_open(self, now=NOW):
        hours = (now - self.opened_at).total_seconds() / 3600
        return math.ceil(hours / 24)

    def assign(self, agent):
        self.assignee = agent
        self.status = "assigned"
        log.info("%s assigned to %s", self, agent)

    def close(self, at):
        self.status = "closed"
        self.closed_at = at
        log.info("%s closed", self)


class Desk:
    def __init__(self):
        self.tickets = []

    def add(self, ticket):
        self.tickets.append(ticket)
        log.info("added %s", ticket)

    def __len__(self):
        return len(self.tickets)

    def __iter__(self):
        return iter(self.tickets)

    def overdue(self, now=NOW):
        late = []
        for t in self.tickets:
            if t.status != "closed" and now > t.deadline():
                log.warning("%s is past its SLA", t)
                late.append(t)
        return late


def ticket_refs(text):
    refs = []
    for match in TICKET_REF.finditer(text):
        refs.append(int(match.group(1)))
    return refs


def redact(text):
    return EMAIL.sub("[email]", text)


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
