"""Grade a model's triage reply against the labels the desk expects."""
import glob
import re
import sys
from pathlib import Path

ALLOWED = ("high", "normal", "low", "unsure")
EXPECTED = {
    "Checkout button frozen": {"high"},
    "Export is missing rows": {"normal"},
    "Invoice PDF is blank": {"normal", "unsure"},
}
LABEL = re.compile(r"\b(high|normal|low|unsure)\b", re.IGNORECASE)


def answer_line(lines, title):
    """Return the line that should hold the label for one title, or None."""
    for i, line in enumerate(lines):
        if title.lower() in line.lower():
            after = line.lower().split(title.lower(), 1)[1].strip(" :-–>|*")
            if after:
                return after
            for nxt in lines[i + 1:]:
                if nxt.strip():
                    return nxt.strip()
    return None


def read_reply(path):
    """Return a reply file's text, whether it was saved as UTF-8 or as UTF-16."""
    data = Path(path).read_bytes()
    if data[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return data.decode("utf-16")
    return data.decode("utf-8-sig")


def grade(text):
    """Return one (title, label found, right, bare word) row per expected title."""
    lines = text.splitlines()
    rows = []
    for title, right in EXPECTED.items():
        line = answer_line(lines, title)
        found = LABEL.search(line or "")
        got = found.group(1).lower() if found else "-"
        bare = line is not None and line.strip() in ALLOWED
        rows.append((title, got, got in right, bare))
    return rows


def main():
    """Print a scoreboard for every reply file named on the command line."""
    paths = [match for arg in sys.argv[1:] for match in sorted(glob.glob(arg)) or [arg]]
    for path in paths:
        rows = grade(read_reply(path))
        print(path)
        for title, got, right, bare in rows:
            verdict = "right" if right else "WRONG"
            shape = "bare word" if bare else "not a bare word"
            print(f"  {title:<24} got {got:<7} {verdict}  {shape}")
        print(f"  score: {sum(r[2] for r in rows)}/3 right, {sum(r[3] for r in rows)}/3 bare words")


if __name__ == "__main__":
    main()