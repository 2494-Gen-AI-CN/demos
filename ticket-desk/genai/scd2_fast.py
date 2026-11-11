"""A rewrite of apply_scd2 that an assistant offered as faster. Not accepted yet."""
import pandas as pd

from transform import OPEN_END, TRACKED


def apply_scd2(dimension, source, as_of):
    """Return the customer dimension with type 2 history applied on as_of."""
    rows = [dict(row) for row in dimension]
    current = {row["customer_id"]: row for row in rows if row["is_current"]}
    next_key = max((row["customer_key"] for row in rows), default=0) + 1
    cur = pd.DataFrame(list(current.values()), columns=["customer_id", *TRACKED])
    merged = pd.DataFrame(source).merge(cur, on="customer_id", how="left")
    changed = pd.Series(False, index=merged.index)
    for col in TRACKED:
        changed |= merged[f"{col}_x"] != merged[f"{col}_y"]
    for src, is_changed in zip(source, changed):
        if not is_changed:
            continue
        old = current.get(src["customer_id"])
        if old is not None:
            old["effective_to"] = as_of
            old["is_current"] = False
        rows.append(dict(src, customer_key=next_key, effective_from=as_of,
                         effective_to=OPEN_END, is_current=True))
        next_key += 1
    return rows
