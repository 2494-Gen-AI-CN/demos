"""Extract the ticket desk's MySQL tables into files for our Data Warehouse"""

import csv 
import json
from pathlib import Path

from db import connect

EXPORTS = Path("exports") # This will be a directory to hold my table csv files
TABLES = ("priorities", "customers", "agents", "tickets")

def read_table(conn, table):
    """Return every row of a given table in our db as a list of dictionaries"""
    cursor = conn.cursor(dictionary=True) # Rather than manually wrangling stuff into dict, output as dict
    cursor.execute(f"SELECT * FROM {table}") # Using an f-string because a Table name can't be a parameter
    rows = cursor.fetchall() # rows is what holds our dictionaries (in an outer list)
    
    cursor.close()
    conn.commit() # ends the underlying transaction that the connection creates
    
    return rows # don't forget the return 
    
    
def write_csv(rows, path):
    """Write rows to a CSV file, with a header row containing column names"""
    with open(path, "w", newline="", encoding="utf-8") as f:
        # Let's write the CSV's
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader() # writing our header row 
        writer.writerows(rows)
        
        
def write_jsonl(rows, path):
    """Write rows to a JSON-lines file, one JSON-L object per line"""
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, default=str) + "\n") 
            
def main():
    """Export our four tables into CSV files, and the event history to JSON-lines"""
    EXPORTS.mkdir(exist_ok=True) # if the folder exists, just continue w/o Exception (no overwrite)
    
    conn = connect() # create that SQL connection
    
    # Write our 4 tables to CSV
    for table in TABLES:
        rows = read_table(conn, table)
        write_csv(rows, EXPORTS / f"{table}.csv") 
        print(table, len(rows))
    
    # Write ticket_events to JSON-L
    events = read_table(conn, "ticket_events")
    write_jsonl(events, EXPORTS / "ticket_events.jsonl") 
    print("ticket_events", len(events)) # confirmation print
    conn.close()
    

if __name__ == "__main__":
    main() # I want to be able to run this file