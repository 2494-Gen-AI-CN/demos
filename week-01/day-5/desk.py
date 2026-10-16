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

