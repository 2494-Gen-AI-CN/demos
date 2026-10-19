""" Support-ticket desk"""
import logging
import math
import re
from datetime import datetime, timedelta

SLA_HOURS = {"high": 4, "normal": 24, "low":72}
NOW = datetime(2026, 10, 19, 14, 0)

TICKET_REF = re.compile(r"\bTD-(\d+)\b") # matches my ticket format
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+") # matches an email I think

# Adding my logger
log = logging.getLogger(__name__)

# Creating logging config
logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(name)s: %(message)s")

class Ticket:
    """Ticket class"""
    def __init__(self, ticket_id, title, priority, opened_at):
        self.ticket_id = ticket_id
        self.title = title
        self.priority = priority
        self.opened_at = opened_at
        self.status = "open"
        self.assignee = None
        self.closed_at = None
    
    def deadline(self):
        return self.opened_at + timedelta(hours=SLA_HOURS[self.priority])
    
    def days_open(self, now=NOW):
        hours = (now - self.opened_at).total_seconds() / 3600
        return math.ceil(hours / 24) # using ceil() from math module
    
    def assign(self, agent):
        self.assignee = agent
        self.status = "assigned"
        log.info("%s assigned to %s", self, agent)
    
    def close(self, at):
        self.status = "closed"
        self.closed_at = at
        log.info("%s closed", self)
        
    def __repr__(self):
        return f"TD-{self.ticket_id} {self.title} [{self.priority}, {self.status}]"
        
class Desk:
    """Represents a help-desk"""
    def __init__(self):
        self.tickets = []
    
    def add(self, ticket):
        self.tickets.append(ticket)
        log.info("added %s", ticket) # Syntax for structured logging
    
    def __len__(self):
        return len(self.tickets)

    # If I want to be able to easily iterate over something - I have to define
    # __iter__ - this is what is used by for loops. Without this, I can't do
    # for thing in collection/object do y.
    def __iter__(self):
        return iter(self.tickets)
    
    def overdue(self, now=NOW):
        """This method gives me all tickets assigned 
            to the desk that are overdue"""
        
        late = []
        for t in self.tickets:
            if t.status != "closed" and now > t.deadline():
                log.warning("%s is past it's SLA", t)
                late.append(t)
        
        return late
    
    def ticket_refs(self, text):
        refs = []
        for match in TICKET_REF.finditer(text):
            refs.append(int(match.group(1)))
        return refs



