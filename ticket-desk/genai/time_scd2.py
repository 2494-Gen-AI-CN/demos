"""Time the desk's apply_scd2 loop against the offered rewrite, at two sizes."""
import timeit
from datetime import date
from decimal import Decimal

import transform
from genai import scd2_fast


def customers(n):
    """Return n current customer rows, shaped like dim_customer."""
    return [{"customer_key": i, "customer_id": i, "name": f"c{i}", "email": f"c{i}@example.com",
             "country": "CA", "monthly_fee": Decimal("49.00"), "effective_from": date(2026, 10, 17),
             "effective_to": transform.OPEN_END, "is_current": True} for i in range(1, n + 1)]


for n, runs in ((4, 200), (100_000, 3)):
    dim = customers(n)
    src = [dict(row) for row in dim]
    src[0]["monthly_fee"] = Decimal("199.00")
    for name, fn in (("loop", transform.apply_scd2), ("rewrite", scd2_fast.apply_scd2)):
        seconds = timeit.timeit(lambda f=fn: f(dim, src, date(2026, 11, 5)), number=runs) / runs
        print(f"{n:>7} customers  {name:<7} {seconds * 1000:9.3f} ms per call")
