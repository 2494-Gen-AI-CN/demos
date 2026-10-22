"""Draw the desk's tickets as charts"""
import matplotlib.pyplot as plt
from desk import SLA_HOURS
from frame import status_table


def status_chart(df, path):
    """Save a bar chart of tickets per status to a specified file path"""
    
    counts = status_table(df)
    
    # Create a 6x4 figure with one axes (plot) inside of it
    fig, ax = plt.subplots(figsize=(6, 4))
    
    ax.bar(counts.index, counts.values)
    ax.set_title("Tickets per status")
    ax.set_xlabel("status")
    ax.set_ylabel("tickets")

    fig.tight_layout()

    # This saves the figure to my disk 
    fig.savefig(path)
    plt.close(fig) # I can close the figure once the method ends. If I don't do this, 
    # the chart window persists until the overall python program ends.


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
