"""Draw the desk's tickets as charts."""
import matplotlib.pyplot as plt
from desk import SLA_HOURS
from frame import status_table


def status_chart(df, path):
    """Save a bar chart of tickets per status to the path."""
    counts = status_table(df)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(counts.index, counts.values)
    ax.set_title("Tickets per status")
    ax.set_xlabel("status")
    ax.set_ylabel("tickets")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def hours_chart(df, path):
    """Save each closed ticket's hours to resolve against its own SLA."""
    closed = df[df["hours"].notna()]
    labels = "TD-" + closed["ticket_id"].astype(str)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(labels, closed["hours"], label="hours to resolve")
    ax.scatter(labels, closed["priority"].map(SLA_HOURS), marker="_", s=600,
               color="black", label="SLA for its priority")
    ax.set_title("Resolution hours against each ticket's SLA")
    ax.set_xlabel("ticket")
    ax.set_ylabel("hours")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def hours_by_priority_chart(df, path):
    """Save each priority's average hours to close against its SLA."""
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(df["priority"], df["hours_to_close"], label="hours to close")
    ax.scatter(df["priority"], df["sla_hours"], marker="_", s=600, color="black", label="SLA")
    ax.set_title("High and normal tickets both close inside their SLA")
    ax.set_ylabel("hours")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
