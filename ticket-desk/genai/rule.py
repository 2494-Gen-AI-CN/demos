"""The desk's hand-written triage rule, printed in the shape the grader reads."""

TITLES = ["Login page returns 500", "Invoice PDF is blank", "Typo on pricing page",
          "Checkout button frozen", "Export is missing rows", "Add dark mode"]


def triage(title):
    """Return a priority for a ticket title, from conditions a person wrote."""
    t = title.lower()
    if "500" in t or "frozen" in t:
        return "high"
    if t.startswith("add "):
        return "low"
    return "normal"


if __name__ == "__main__":
    for title in TITLES:
        print(f"{title} -> {triage(title)}")
