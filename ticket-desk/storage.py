"""Plain-text files for the desk: read, write, append and delete."""
from pathlib import Path


def read_lines(path):
    """Return the lines of a text file as a list, without line endings."""
    with open(path, encoding="utf-8") as f:
        return f.read().splitlines()


def export_board(desk, path):
    """Write one tab-separated line per ticket, replacing the file."""
    with open(path, "w", encoding="utf-8") as f:
        for t in desk:
            fields = [str(t.ticket_id), t.title, t.priority, t.status]
            f.write("\t".join(fields) + "\n")


def append_line(path, text):
    """Add one line of text to the end of the file."""
    with open(path, "a", encoding="utf-8") as f:
        f.write(text + "\n")


def delete_file(path):
    """Delete the file and return True, or return False if it is missing."""
    try:
        Path(path).unlink()
    except FileNotFoundError:
        return False
    return True
