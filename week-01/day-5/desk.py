# Control flow - Branching logic
# if / elif / else - picks exactly one branch - the first branch that happens
# to satisfy it's condition check. Subsequent ones are skipped.

from datetime import datetime, timedelta

SLA_HOURS = {"high": 4, "normal": 24, "low": 72}
PRIORITY_RANK = {"high": 1, "normal": 2, "low":3}
NOW = datetime(2026, 10, 16, 14, 0) # fixed so every run prints the same

queue = [
    {"id": 101, "title": "Login page returns 500", "priority":"high", "opened_at": datetime(2026, 10, 16,8,0), "open": True},
    {"id": 102, "title": "Printer Jams", "priority":"normal", "opened_at": datetime(2026, 10, 15, 15, 30), "open": True},
    {"id": 103, "title": "Typo on footer", "priority":"low", "opened_at": datetime(2026, 10, 14, 9, 0), "open": False},
]

print(len(queue), "tickets loaded")

# ===== BRANCHING ====

ticket = queue[1] # grabbing that printer jam ticket
deadline = ticket["opened_at"] + timedelta(hours=SLA_HOURS[ticket["priority"]])
hours_left = (deadline - NOW).total_seconds() / 3600 # I want to see how many hours we have left to resolve the ticket

print(ticket["title"], "hours_left:", hours_left)

if hours_left < 0:
    status = "breached"
elif hours_left < 2:
    status = "at risk"
else: 
    status = "on time"

print("status:", status)


title = ticket["title"] # grabbing ticket title



if title == False:
    print("Ticket lacks a title")

if "Printer" in title:
    print("mentions the printer")

if 0 <= hours_left < 24: #chaining a comparison
    print("Due within a day")

if not ticket["open"]:
    print("closed")
else:
    print("still open")
    
# We can nest these checks if we want to - if you're more than like 2 deep maybe re-evaluate
if ticket["open"]:
    if hours_left < 2:
        if ticket["priority"] != "low":
            print("We should escalate this")
            
state = "open" if ticket["open"] else "closed" # conditional expression for value assignment, saves an if-else
print(state)

#### Loops ####
# for - while

attempts = ["urgent", "med", "HIGH"] # pretend a user typed these in when prompted
tries = 0

# while loop - repeats while a condition stays true. We check before every run through the code in the loop
while tries < len(attempts):
    answer = attempts[tries].strip().lower()
    tries += 1 # shorthand for tries = tries + 1
    
    if answer in SLA_HOURS:
        print("accepted:", answer, "after", tries, "tries")
        break # exiting the loop if we satisfy this
    
    print("not a priority:", answer)
else:
    print("user gave up") # if loop run terminates with no break, we can use an else to run default code 
    
# if I want a an "infinite loop" - I can use 
# while True - this will continue until a break. If I use a variable that is set to False, I can then manually
# set it to true, using it as a completion flag. 
    
# for loops - in python our for loops can look different. Loops in Python are optimized for 
# work with collections

# t represents just an item in my queue list
for t in queue:
    print(t["id"], t["title"])

# index represents the ticket (t)'s place in the list. I used "start" in enumerate() to tell it to count from 1
# rather than 0
for index, t in enumerate(queue, start=1):
    print(f"{index}. {t['title']}")

for priority, hours in SLA_HOURS.items():
    print(f"{priority:<8}-{hours:>4}h")

# lets pretend we have some IT call center agents
agents = ["dana", "lee", "sam"]

for t, agent in zip(queue, agents):
    print(t["id"], "->", agent)
    

for n in range(1, 4): # I can use the range function if I need a loop that fires x number of times exactly
    print("ping", n)
    
print("after the loop n is still", n)
    

# Switch statements in Python
# In python we use match-case - works exactly like a switch in most other languages

# Python does not support C-style case fallthrough - so ending each case with break isn't needed.

match ticket["priority"]:
    case "low":
        print("This ticket is low priority")
    case "high":
        print("This ticket is high priority")
    case _: # This underscore wildcard acts as our default case
        print("Normal ticket?")


# ==== Functions ====
# Functions are reusable bits of logic - we can write them once and call them anywhere else
# we can import functions to other files and reuse them across programs

def deadline_for(ticket):
    """Return the datetime by which this ticket must be closed"""
    return ticket["opened_at"] + timedelta(hours=SLA_HOURS[ticket["priority"]])


print(deadline_for(queue[0]))
print(deadline_for.__doc__)

def describe(ticket):
    """Returns a pre-formatted ticket description"""
    print(f"#{ticket['id']} {ticket['title']} - {ticket['priority']}")

result = describe(queue[0])
print(result) # None: describe just prints, it doesn't return anything. Similar to a void function in C# or Java

# I can give my functions default argument values
def hours_left_for(ticket, now=datetime.now()):
    return (deadline_for(ticket) - now).total_seconds() / 3600

# If I provide a default argument for my function, I can omit it from the function call IF im okay with the default value
print(hours_left_for(queue[1]))

# Here, I provide my own value for "now" - the default is not used
print(hours_left_for(queue[1], now=NOW))

# Finally, if I use argument_name=value, I can put my args in any order
print(hours_left_for(now=NOW, ticket=queue[0]))

# print(hours_left_for(now=NOW))



# More complex function
def status_for(ticket, now=NOW):
    
    """closed, breach, at risk or on time."""
    if not ticket["open"]:
        return "closed"
    
    hours = hours_left_for(ticket, now)
    
    if hours < 0:
        return "breached"
    
    if hours < 2:
        return "at risk"
    
    return "on time"

# A trap about lists (dictionaries and other collections) and functions
def log(entry, history=[]):
    history.append(entry)
    return history

print(log("opened"))
print(log("assigned"))

def log_safely(entry, history=None):
    
    if history is None:
        history = []
    
    history.append(entry)
    return history

# Lambda and sort keys
# Lambdas - builds a one expression function with no name, right where it's used
# Commonly used to satisfy sorting methods (providing comparison logic) and when making API calls

# in general we want to use def to defined named functions
# but python is chill - so this works I guess
double = lambda n: n * 2 # notice no return keyword - whatever the expression evaluates to is assumed to be the return

# Sort by priority
by_text = sorted(queue, key=lambda t: t["priority"])

for t in by_text:
    print(t["priority"], t["title"]) # alphabetical - because what we really asked for above
    # to sort off the value of the strings that correspond to the priority key - not what we actually wanted. 
    # we can revisit comparisons later... 
    
# We've worked with lists - lets see actual python arrays
from array import array 
hours_open = array("d", [6.0, 22.5, 1.5]) # "d" - every item is a float
hours_open.append(9.0) 