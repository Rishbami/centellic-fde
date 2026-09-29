"""Tests written against the ledger's stated behaviour. Synthetic data only."""

from ledger import add_entry, total
from decimal import Decimal


def test_total_sums_amounts() -> None:
    book = [
        {"reference": "SYN-001", "amount": Decimal("10.10")},
        {"reference": "SYN-002", "amount": Decimal("20.20")},
        {"reference": "SYN-003", "amount": Decimal("5.05")},
    ]
    assert total(book) == Decimal("35.35")


def test_add_entry_starts_from_an_empty_ledger() -> None:
    first = add_entry("SYN-001", Decimal("10.10"))
    second = add_entry("SYN-002", Decimal("20.20"))
    assert len(first) == 1
    assert len(second) == 1
