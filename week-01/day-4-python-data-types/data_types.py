#!/usr/bin/env python3

# Python data types, one support ticket at a time.
# Run the whole file after each section: python data_types.py

# ===== 1. Strings =====
# A string is text. Methods on a string give back a NEW string; the original never changes.

title = "  Login page returns 500  "
print(title.strip())
print(title.strip().lower())
print(title.upper())
print(title)  # still has the spaces - strings are immutable

title = title.strip()  # to keep the change, assign it back

print(title[:5])  # slice: first five characters
print(title[-3:])  # negative index counts from the end
print(len(title))
print(title.startswith("Login"))
print(title.replace("500", "error"))
print("500" in title)  # membership test on text

words = ["Login", "page", "returns", "500"]
print("-".join(words))  # join glues a list of strings into one string

reporter = "Ada Lovelace"
print(f"{title} reported by {reporter}")  # f-string: values dropped into text

# ===== 2. Casting =====
# Casting turns a value of one type into another type.

ticket_id_text = "42"
ticket_id = int(ticket_id_text)
print(ticket_id, type(ticket_id_text), type(ticket_id))

hours_open = float("5.5")
print(hours_open, type(hours_open))

print(str(101) + " tickets")  # str() turns a number into text so + works
# print("500" + 1)            # TypeError: text plus number is not allowed

print(int(5.9))  # int() cuts off the decimal, it does not round
# print(int("3.5"))            # ValueError: "3.5" is not a whole number in text

print("42".isdigit(), "3.5".isdigit())  # check the text before you cast it
# ticket_id = int(input("Ticket id: "))  # what you typed at the terminal comes in as text

# ===== 3. Boolean =====
# bool has two values, True and False. Every value can be asked "are you truthy?"

is_open = True
print(type(is_open))

print(bool(0), bool(1), bool(-7))
print(bool(""), bool("hi"))
print(bool([]), bool([0]))
print(bool("False"))  # True! Any non-empty text is truthy, whatever it says

hours_left = 4 - hours_open
is_breached = is_open and hours_left < 0
print(hours_left, is_breached)
print(not is_breached)

# and / or hand back one of the operands, not always True or False
assignee = "" or "unassigned"
print(assignee)
print(is_open and title)

# if is_open == True:   # works, but just write: if is_open:

# ===== 4. Lists =====
# A list is an ordered, changeable collection. Square brackets.

queue = ["Login page returns 500", "Password reset email missing", "Typo on footer"]
print(type(queue), len(queue))

queue.append("Search is slow")  # changes the list in place
queue.insert(0, "Site is down")
print(queue)

print(queue[0])
print(queue[-1])
print(queue[1:3])  # slice, same idea as strings

removed = queue.pop()  # pop removes the last item and gives it back
print(removed, queue)

print(sorted(queue))  # sorted() gives a NEW sorted list
print(queue)  # the original is untouched
print(queue.sort())  # .sort() sorts in place and returns None
print(queue)

queue_alias = queue  # NOT a copy - two names for the same list
queue_alias.append("Button misaligned")
print(queue)

queue_copy = queue.copy()  # a real copy
queue_copy.append("Only in the copy")
print(queue)
print(queue_copy)

# ===== 5. Tuples =====
# A tuple is an ordered collection that cannot change. Round brackets.

ticket = (101, "Login page returns 500", "high")
print(type(ticket), ticket[0], ticket[-1])
# ticket[2] = "low"   # TypeError: tuples do not support item assignment

ticket_id, title, priority = ticket  # unpacking: one name per slot
print(ticket_id, title, priority)

print(type((1)))  # just an int in brackets
print(type((1,)))  # the comma makes the tuple

ranked = [(3, "Typo on footer"), (1, "Site is down"), (2, "Login page returns 500")]
print(sorted(ranked))  # tuples sort by their first item, then the second

# ===== 6. Range =====
# range gives whole numbers on demand. It does not build a list until you ask.

print(range(5))
print(type(range(5)))
print(list(range(5)))  # 0 up to but not including 5
print(list(range(1, 11, 2)))  # start, stop, step
print(len(range(1, 11, 2)))
print(list(range(10, 0, -3)))

# ===== 7. Sets =====
# A set holds distinct items, no order, no duplicates. Curly brackets.

tags = {"bug", "login", "bug", "urgent"}
print(tags)  # the duplicate "bug" is gone
print(type(tags), len(tags))

tags.add("web")
print("login" in tags)  # membership is fast on a set

reviewed = {"login", "web", "mobile"}
print(tags & reviewed)  # in both
print(tags - reviewed)  # in tags only
print(tags | reviewed)  # in either

print(type({}))  # empty curly brackets is a DICT
print(type(set()))  # the empty set is spelled set()

# ===== 8. Binary types =====
# Text has to become bytes before it is saved to disk or sent over a network.

note = "café"
raw = note.encode("utf-8")
print(raw, type(raw))
print(len(note), len(raw))  # 4 characters, 5 bytes: é takes two

print(raw.decode("utf-8"))

buffer = bytearray(raw)  # bytearray is the changeable version
buffer.append(33)  # 33 is the byte for "!"
print(buffer.decode("utf-8"))

# ===== 9. NoneType =====
# None means "no value here". It is its own type with exactly one value.

assignee = None
print(assignee, type(assignee))
print(assignee is None)  # compare to None with "is", not ==
print(assignee is not None)

result = print("printing returns nothing")
print(result)

# ===== 10. Dictionaries =====
# A dictionary maps keys to values. Lookup by key, not by position.

sla_hours = {"high": 4, "normal": 24, "low": 72}
print(type(sla_hours))
print(sla_hours["high"])
# print(sla_hours["urgent"])   # KeyError: that key is not in the dict
print(sla_hours.get("urgent"))  # .get gives None instead of an error
print(sla_hours.get("urgent", 24))  # or a default you choose

sla_hours["urgent"] = 1  # add a key
sla_hours["low"] = 48  # change a value
print(sla_hours)

print(sla_hours.keys())
print(sla_hours.values())
print(sla_hours.items())
print("normal" in sla_hours)  # "in" checks keys

ticket = {"id": 101, "title": "Login page returns 500", "priority": "high", "open": True}
print(ticket["title"], sla_hours[ticket["priority"]])

tickets_by_id = {101: ticket, 102: {"id": 102, "title": "Typo on footer", "priority": "low", "open": False}}
print(tickets_by_id[102]["title"])

# ===== 11. Numbers =====
# int is a whole number. float has a decimal point. Both are numbers, but not the same type.

print(type(7), type(7.0))
print(7 / 2)  # one slash: always a float
print(7 // 2)  # two slashes: whole number, rounded down
print(7 % 2)  # remainder
print(2 ** 10)  # power

print(0.1 + 0.2)  # floats are approximations, not exact decimals
print(0.1 + 0.2 == 0.3)
print(abs((0.1 + 0.2) - 0.3) < 1e-9)  # compare floats with a tolerance

print(round(2.5), round(3.5))  # banker's rounding: halves go to the even number
print(round(2.675, 2))
print(divmod(27, 24))  # quotient and remainder in one go

from decimal import Decimal

print(Decimal("0.1") + Decimal("0.2"))  # exact, for money

# ===== 12. Datetime =====
# datetime holds a point in time. timedelta holds a length of time.

from datetime import datetime, timedelta

opened = datetime(2026, 10, 14, 16, 0)  # year, month, day, hour, minute
print(opened, type(opened))

sla = timedelta(hours=sla_hours["high"])
due = opened + sla  # datetime plus timedelta gives a datetime
print(due)

now = datetime.now()
age = now - opened  # datetime minus datetime gives a timedelta
print(age, type(age))
print(age.total_seconds() / 3600)

print(opened.isoformat())
print(opened.strftime("%Y-%m-%d %H:%M"))  # format to text the way you want it
print(opened.strftime("%A %d %B"))

parsed = datetime.strptime("2026-10-16 14:00", "%Y-%m-%d %H:%M")  # text to datetime
print(parsed, parsed > opened)

# ===== 13. Namespaces =====
# A namespace is the table of names this file knows right now.

print(dir()[-5:])  # five of the names this file knows (dir sorts them alphabetically)

del hours_left  # remove a name from the table
# print(hours_left)   # NameError: name 'hours_left' is not defined

print(__name__)  # Python names the file being run "__main__"

print(max(3, 9))
max = 3  # shadowing: our name hides the built-in max
print(max)
# print(max(3, 9))   # TypeError: 'int' object is not callable
del max  # remove our name and the built-in is visible again
print(max(3, 9))
