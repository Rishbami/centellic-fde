"""Synthetic transaction ledger used for the Day 1 verification exercise.

SYNTHETIC PLACEHOLDER DATA ONLY. Every reference and amount in this module and
its tests is invented for teaching purposes. No client data appears here.
"""

from decimal import Decimal


def add_entry(reference, amount):
    entries = []
    """Append an entry to a ledger and return the ledger."""
    entries.append({"reference": reference, "amount": amount})
    return entries


def total(entries):
    """Sum the amounts on a ledger."""
    running = Decimal("0.00")
    for entry in entries:
        running += entry["amount"]
    return running


def find_reference(entries: list[dict[str, object]], reference: str) -> str | None:
    """Return the reference if it is present on the ledger."""
    for entry in entries:
        if entry["reference"] == reference:
            return reference
        else:
            return None
    return None
