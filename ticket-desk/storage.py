"""Plain-text files for the desk: read, write, append and delete."""
from pathlib import Path

# Creating a read function
def read_lines(path):
    """Return the lines of a text file as a list, without line endings.
        Opens the file (if it exists) and returns the contents, as a list
        of strings. Each line of the file is it's own string in the list."""
    with open(path, encoding="utf-8") as f:
        return f.read().splitlines()

# Function to export the tickets that belong to a specific desk object
def export_board(desk, path):
    """Write one tab-separated line per ticket. NOTE: this replaces the contents
        of the file when it runs."""
    with open(path, "w", encoding='utf-8') as f:
        for t in desk:
            # Represent the ticket as a list of strings
            fields = [str(t.ticket_id), t.title, t.priority, t.status]
            # Write those strings to the file, with a newline char at the end
            f.write("\t".join(fields) + "\n")
            # "2        Sample title    low     closed"
            # "3    etc    etc   etc"       
    
def append_line(path, text):
    """Add one line of text to the end of a file, don't truncate the file"""
    with open(path, "a", encoding='utf-8') as f:
        f.write(text + "\n")
        
def delete_file(path):
    """Deletes the file at a given path and returns True,
        returns False if the file is missing"""
    try:
        Path(path).unlink() # if the file exists, delete it
    except FileNotFoundError:
        return False
    
    return True
    