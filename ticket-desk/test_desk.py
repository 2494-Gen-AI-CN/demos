from datetime import datetime, timedelta

import pytest

from desk import NOW, Desk, Ticket, redact, ticket_refs
from storage import load_desk, save_desk


def test_high_priority_deadline_is_four_hours():
    opened = datetime(2026, 10, 19, 8, 0)
    ticket = Ticket(1, "Login page returns 500", "high", opened)
    assert ticket.deadline() == opened + timedelta(hours=4)


def test_unknown_priority_raises():
    with pytest.raises(ValueError, match="urgent"):
        Ticket(1, "Login page returns 500", "urgent", NOW)


def test_overdue_skips_closed_tickets():
    desk = Desk()
    opened = NOW - timedelta(hours=100)
    done = Ticket(1, "Invoice PDF is blank", "high", opened)
    late = Ticket(2, "Checkout button frozen", "high", opened)
    desk.add(done)
    desk.add(late)
    done.close(opened + timedelta(hours=2))
    assert desk.overdue() == [late]


def test_redact_hides_email():
    assert redact("write to ana@example.com now") == "write to [email] now"


def test_ticket_refs_reads_numbers():
    assert ticket_refs("Same problem as TD-2 and TD-5") == [2, 5]


@pytest.fixture
def sample_desk():
    desk = Desk()
    opened = datetime(2026, 10, 19, 8, 0)
    fast = Ticket(1, "Login page returns 500", "high", opened)
    slow = Ticket(2, "Invoice PDF is blank", "normal", opened)
    busy = Ticket(3, "Checkout button frozen", "high", opened)
    fresh = Ticket(4, "Add dark mode", "low", opened)
    for ticket in [fast, slow, busy, fresh]:
        desk.add(ticket)
    fast.close(opened + timedelta(hours=3))
    slow.close(opened + timedelta(hours=30))
    busy.assign("Priya")
    return desk


def test_save_then_load_keeps_every_ticket(tmp_path, sample_desk):
    path = tmp_path / "tickets.json"
    save_desk(sample_desk, path)
    loaded = load_desk(path)
    assert len(loaded) == len(sample_desk)
    assert repr(loaded.tickets) == repr(sample_desk.tickets)
    assert loaded.tickets[1].closed_at == sample_desk.tickets[1].closed_at


def test_missing_file_gives_empty_desk(tmp_path):
    assert len(load_desk(tmp_path / "nothing.json")) == 0


def test_corrupt_file_raises_value_error(tmp_path):
    path = tmp_path / "tickets.json"
    path.write_text("[{", encoding="utf-8")
    with pytest.raises(ValueError, match="not valid JSON"):
        load_desk(path)


@pytest.mark.parametrize("priority, hours", [("high", 4), ("normal", 24), ("low", 72)])
def test_sla_hours(priority, hours):
    ticket = Ticket(1, "Any title", priority, NOW)
    assert ticket.deadline() - NOW == timedelta(hours=hours)
