"""Guardrails around the triage prompt: what goes in, and what comes out."""
import re

ALLOWED = ("high", "normal", "low", "unsure")
FENCE = re.compile(r"</?titles>", re.IGNORECASE)
SUSPICIOUS = re.compile(r"\b(ignore|disregard|instructions?|system prompt)\b", re.IGNORECASE)


def fence_titles(titles):
    """Return the titles in one <titles> block, with any fence tag inside a title removed."""
    return "<titles>\n" + "\n".join(FENCE.sub("", title) for title in titles) + "\n</titles>"


def looks_like_instructions(title):
    """Return True when a title talks to the model instead of describing a problem."""
    return SUSPICIOUS.search(title) is not None


def check_label(line):
    """Return line when it is exactly one allowed label, or raise ValueError."""
    if line not in ALLOWED:
        raise ValueError(f"not an allowed label: {line!r}")
    return line


def parse_reply(text, titles):
    """Return {title: label} from a reply in the three-line format, or raise ValueError."""
    blocks = [block.splitlines() for block in text.replace("\r\n", "\n").strip().split("\n\n")]
    if len(blocks) != len(titles):
        raise ValueError(f"expected {len(titles)} answers, got {len(blocks)}")
    labels = {}
    for block in blocks:
        if len(block) != 3:
            raise ValueError(f"expected 3 lines, got {len(block)}: {block[0]!r}")
        labels[block[0].strip()] = check_label(block[1].strip())
    if sorted(labels) != sorted(titles):
        raise ValueError(f"titles do not match the tickets sent: {sorted(labels)}")
    return labels


def needs_review(labels, rule):
    """Return the titles whose model label disagrees with the hand-written rule."""
    return [title for title, label in labels.items() if label != rule(title)]