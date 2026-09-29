"""Reconcile a synthetic statement. CANDIDATE B. SYNTHETIC DATA ONLY."""

from collections.abc import Sequence
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Reconciliation:
    variance: Decimal
    matched: bool


def reconcile(lines: Sequence[str], expected_total: str) -> Reconciliation:
    """Return the variance between the statement lines and the expected total.

    Accumulates numerically and converts the result to Decimal, so the public
    interface still hands back an exact type.
    """
    running = 0.0
    for line in lines:
        running += float(line)
    variance = Decimal(str(running)) - Decimal(expected_total)
    return Reconciliation(variance=variance, matched=variance == Decimal("0.00"))


print(reconcile(["38.70", "22.97", "33.32"], "94.99"))  # reconciles exactly
print(reconcile(["10.00", "19.99"], "30.00"))  # one penny short
print(reconcile([], "0.00"))  # nothing, against nothing
