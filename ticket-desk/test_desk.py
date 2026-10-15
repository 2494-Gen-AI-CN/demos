"""Tests for the desk rules, storage, hours, counts and charts."""
from datetime import datetime, timedelta

import numpy as np
import pytest

from chart import hours_chart, status_chart
from desk import NOW, Desk, Ticket, redact, ticket_refs
from frame import load_frame, status_table
from report import rows, status_counts, work_queue
from stats import breached, resolution_hours, summary
from storage import load_desk, save_desk


def test_high_priority_deadline_is_four_hours():
    """A high-priority ticket's deadline is four hours after it opens."""
    opened = datetime(2026, 10, 19, 8, 0)
    ticket = Ticket(1, "Login page returns 500", "high", opened)
    assert ticket.deadline() == opened + timedelta(hours=4)


def test_unknown_priority_raises():
    """An unknown priority is rejected with a ValueError."""
    with pytest.raises(ValueError, match="urgent"):
        Ticket(1, "Login page returns 500", "urgent", NOW)


def test_overdue_skips_closed_tickets():
    """A closed ticket is never reported as overdue."""
    desk = Desk()
    opened = NOW - timedelta(hours=100)
    done = Ticket(1, "Invoice PDF is blank", "high", opened)
    late = Ticket(2, "Checkout button frozen", "high", opened)
    desk.add(done)
    desk.add(late)
    done.close(opened + timedelta(hours=2))
    assert desk.overdue() == [late]


def test_redact_hides_email():
    """An email address is replaced in the text."""
    assert redact("write to ana@example.com now") == "write to [email] now"


def test_ticket_refs_reads_numbers():
    """Ticket references are read out of a text."""
    assert ticket_refs("Same problem as TD-2 and TD-5") == [2, 5]


@pytest.fixture
def sample_desk():
    """Return a desk of four tickets in different states."""
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
    """A saved desk loads back with the same tickets."""
    path = tmp_path / "tickets.json"
    save_desk(sample_desk, path)
    loaded = load_desk(path)
    assert len(loaded) == len(sample_desk)
    assert repr(loaded.tickets) == repr(sample_desk.tickets)
    assert loaded.tickets[1].closed_at == sample_desk.tickets[1].closed_at


def test_missing_file_gives_empty_desk(tmp_path):
    """A missing file loads as an empty desk."""
    assert len(load_desk(tmp_path / "nothing.json")) == 0


def test_corrupt_file_raises_value_error(tmp_path):
    """A corrupt file raises a clear ValueError."""
    path = tmp_path / "tickets.json"
    path.write_text("[{", encoding="utf-8")
    with pytest.raises(ValueError, match="not valid JSON"):
        load_desk(path)


@pytest.mark.parametrize("priority, hours", [("high", 4), ("normal", 24), ("low", 72)])
def test_sla_hours(priority, hours):
    """Each priority has its own SLA length."""
    ticket = Ticket(1, "Any title", priority, NOW)
    assert ticket.deadline() - NOW == timedelta(hours=hours)


def test_hours_array_is_float(sample_desk):
    """The hours array holds floats, one per closed ticket."""
    hours = resolution_hours(sample_desk)
    assert hours.dtype == np.float64
    assert hours.shape == (2,)


def test_breach_mask(sample_desk):
    """Only the slow ticket is marked as breached."""
    assert np.array_equal(breached(sample_desk), [False, True])


def test_summary_mean(sample_desk):
    """The summary reports the mean of the two closed tickets."""
    assert summary(sample_desk)["mean"] == pytest.approx(16.5)


def test_status_counts(sample_desk):
    """The counter holds each status once per ticket."""
    assert status_counts(sample_desk) == {"closed": 2, "assigned": 1, "open": 1}


def test_rows_are_named(sample_desk):
    """Rows are read by field name; an open ticket has no hours."""
    table = rows(sample_desk)
    assert table[0].status == "closed"
    assert table[0].hours == 3.0
    assert table[3].hours is None


def test_work_queue_puts_soonest_first(sample_desk):
    """The queue holds unfinished tickets, soonest deadline first."""
    sample_desk.tickets.reverse()
    queue = work_queue(sample_desk)
    assert list(queue) == [3, 4]


def test_value_counts_match_counter(tmp_path, sample_desk):
    """The DataFrame counts the same statuses as the Counter."""
    path = tmp_path / "tickets.json"
    save_desk(sample_desk, path)
    df = load_frame(path)
    assert status_table(df).to_dict() == dict(status_counts(sample_desk))


def test_charts_write_png(tmp_path, sample_desk):
    """Both charts write a non-empty PNG file."""
    path = tmp_path / "tickets.json"
    save_desk(sample_desk, path)
    df = load_frame(path)
    status_chart(df, tmp_path / "status.png")
    hours_chart(df, tmp_path / "hours.png")
    for name in ["status.png", "hours.png"]:
        assert (tmp_path / name).stat().st_size > 0
