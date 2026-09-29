"""Synthetic transaction ledger. LEARNER STARTER.

SYNTHETIC PLACEHOLDER DATA ONLY. Every reference and amount used with this
module is invented for teaching purposes. No client data appears here.

This module runs. It is also wrong in three ways. Do not go hunting for them
by reading. Run the three gates and let the tools tell you:

    python -m ruff check .
    python -m mypy src tests run.py
    python -m pytest

Then fix what they report, one gate at a time, and run the gate again.
"""

from decimal import Decimal
from dataclasses import dataclass


@dataclass(frozen=True)
class Entry:
    reference: str
    amount: Decimal


def add_entry(reference: str, amount: Decimal, ledger: list[Entry]) -> list[Entry]:
    entries = ledger.copy()
    """Append an entry to a ledger and return the ledger.

    TODO (CA-2): ruff will flag the default value on `entries`. Understand why
    a shared mutable default is a bug before you change it, then decide whether
    this function should mutate its argument or return a new list.
    """
    entries.append(Entry(reference=reference, amount=amount))
    return entries


def total(entries: list[Entry]) -> Decimal:
    """Sum the amounts on a ledger.

    TODO (CA-3): write a test asserting the total of 10.10, 20.20 and 5.05 is
    35.35. When it fails, read the number pytest prints before you touch this
    function. The decision you then have to make is float vs Decimal: floats
    are binary, so 10.10 has no exact representation and the error accumulates.
    """
    running = Decimal("0.0")
    for entry in entries:
        running += entry.amount
    return running


def find_reference(entries: list[Entry], reference: str) -> str | None:
    """Return the reference if it is present on the ledger.

    TODO (CA-2): mypy will flag this. The annotation promises a str on every
    path, and one path returns nothing. Decide what this function should
    honestly return when the reference is absent, and make the type say so.
    """
    for entry in entries:
        if entry.reference == reference:
            return reference
    return None
