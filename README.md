# demos

Live demo code typed in class, 2494 Gen-AI Python.

## What is here

- `ticket-desk/` — the support-ticket desk. One small project that grows week by week, from week 1 to week 5: Python modules and files now, a MySQL database next, then an ETL job and an LLM. From week 2 on, this is the code typed in class, and every class ends with a commit on `main`.
- `week-01/` — the loose scripts from the first week, one folder per day, kept as they were typed.
- `activities/` — workbooks for in-class activities, one folder per week. Not code and not marked: open them in Excel, Google Sheets or LibreOffice. Each folder has a `README.md` that says what to do with them.

## Run the desk

From a terminal, inside your copy of this repository:

```
cd ticket-desk
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS or Linux
python -m pip install -r requirements.txt
python ticket_desk.py
```

The `.venv` folder is yours alone and is not committed. `requirements.txt` lists what the desk needs; it gains a line whenever a class adds a library, so run the `pip install` line again after you refresh your copy.

## Keep your copy current

The folder changes after every class, so refresh your copy before the next one: `git pull` if you cloned this repository, or copy the files in `ticket-desk/` again from GitHub. Your copy is for following along and is never marked. Exercise hand-ins go in your own `2494-Gen-AI-CN/<FirstnameLastname>` repository, not here.
