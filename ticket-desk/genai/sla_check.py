"""Settle the SLA questions in code: calendar hours, then business hours."""
from datetime import datetime, timedelta

TICKETS = [(1, "high", "2026-10-18 08:00", "2026-10-18 11:00"),
           (2, "normal", "2026-10-17 12:00", "2026-10-18 18:00"),
           (3, "normal", "2026-10-18 18:00", "2026-10-19 04:00"),
           (5, "normal", "2026-10-18 12:00", "2026-10-19 16:00")]
CALENDAR_SLA = {"high": 4, "normal": 24}
BUSINESS_SLA = {"high": 2, "normal": 6}


def calendar_hours(opened, closed):
    """Return the hours between two times, every hour counted."""
    return (datetime.fromisoformat(closed) - datetime.fromisoformat(opened)).total_seconds() / 3600


def business_hours(opened, closed):
    """Return the whole hours between two times that fall Monday to Friday, 09:00 to 17:00."""
    t, end, hours = datetime.fromisoformat(opened), datetime.fromisoformat(closed), 0
    while t < end:
        if t.weekday() < 5 and 9 <= t.hour < 17:
            hours += 1
        t += timedelta(hours=1)
    return hours


if __name__ == "__main__":
    print("ticket  opened on  calendar h  over  business h  over")
    for ticket, priority, opened, closed in TICKETS:
        cal, bus = calendar_hours(opened, closed), business_hours(opened, closed)
        day = datetime.fromisoformat(opened).strftime("%A")
        print(f"{ticket:>6}  {day:<9}  {cal:>10.0f}  {max(0, cal - CALENDAR_SLA[priority]):>4.0f}"
              f"  {bus:>10}  {max(0, bus - BUSINESS_SLA[priority]):>4}")
