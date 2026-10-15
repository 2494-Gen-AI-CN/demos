"""Report on the desk's tickets with the collections module."""
from collections import Counter, OrderedDict, defaultdict, namedtuple

TicketRow = namedtuple("TicketRow", ["ticket_id", "priority", "status", "hours"])


def status_counts(desk):
    """Return how many tickets are in each status."""
    statuses = []
    for t in desk:
        statuses.append(t.status)
    return Counter(statuses)


def rows(desk):
    """Return one TicketRow per ticket; hours is None while it is open."""
    table = []
    for t in desk:
        hours = None
        if t.closed_at is not None:
            hours = (t.closed_at - t.opened_at).total_seconds() / 3600
        table.append(TicketRow(t.ticket_id, t.priority, t.status, hours))
    return table


def work_queue(desk):
    """Return the unfinished tickets by id, soonest deadline first."""
    waiting = []
    for t in desk:
        if t.status != "closed":
            waiting.append(t)
    queue = OrderedDict()
    for t in sorted(waiting, key=lambda t: t.deadline()):
        queue[t.ticket_id] = t
    return queue


def by_agent(desk):
    """Return the ticket ids each agent holds."""
    groups = defaultdict(list)
    for t in desk:
        if t.assignee is not None:
            groups[t.assignee].append(t.ticket_id)
    return groups
