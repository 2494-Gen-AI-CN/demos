"""Sort a ticket's age into the bands the desk reports on."""


def ticket_age_band(hours):
    """Return the SLA band for the ticket age in hours."""
    if hours < 4:
        return "under 4"
    if 4 <= hours <= 24:
        return "4 to 24"
    if hours > 24:
        return "over 24"