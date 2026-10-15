"""Resolution hours and SLA breaches as NumPy arrays."""
import numpy as np
from desk import SLA_HOURS


def resolution_hours(desk):
    """Return the hours each closed ticket took, as an array."""
    hours = []
    for t in desk:
        if t.status == "closed":
            hours.append((t.closed_at - t.opened_at).total_seconds() / 3600)
    return np.array(hours)


def sla_limits(desk):
    """Return the SLA hours of each closed ticket's own priority."""
    limits = []
    for t in desk:
        if t.status == "closed":
            limits.append(SLA_HOURS[t.priority])
    return np.array(limits)


def breached(desk):
    """Return True for each closed ticket that took longer than its SLA."""
    return resolution_hours(desk) > sla_limits(desk)


def summary(desk):
    """Return the mean, median and longest hours and the breach count."""
    hours = resolution_hours(desk)
    return {
        "mean": float(hours.mean()),
        "median": float(np.median(hours)),
        "max": float(hours.max()),
        "breached": int(breached(desk).sum()),
    }
