"""Tests for the ledger. LEARNER STARTER. Synthetic data only.

CA-3: three of these are written for you as a shape to copy. The rest raise
NotImplementedError. Replace each one with a real assertion.
"""

import pytest
from decimal import Decimal
from ledger import Entry, add_entry, total, find_reference


@pytest.fixture
def sample_ledger():
    """Three synthetic entries whose amounts are chosen to break float maths.

    A fixture exists so the same data is not copy-pasted into six tests. When
    the shape of an entry changes, it changes here once.
    """
    return [
        Entry(reference="SYN-001", amount=Decimal("10.10")),
        Entry(reference="SYN-002", amount=Decimal("20.20")),
        Entry(reference="SYN-003", amount=Decimal("5.05")),
    ]


def test_total_is_exact(sample_ledger):
    """Written for you. Run it and read the number in the failure carefully."""
    assert total(sample_ledger) == Decimal("35.35")


def test_total_of_an_empty_ledger_is_zero():
    """TODO (CA-3): assert the total of an empty ledger."""
    assert total([]) == Decimal("0.00")


def test_add_entry_does_not_leak_between_calls():
    """TODO (CA-3): call add_entry twice with no ledger argument, and assert
    that each call returns a ledger of length 1."""
    assert len(add_entry("SYN-004", Decimal("40.40"), [])) == 1
    assert len(add_entry("SYN-005", Decimal("50.50"), [])) == 1


def test_add_entry_returns_a_new_list(sample_ledger):
    """TODO (CA-3): add an entry to sample_ledger and assert the original is
    still length 3 while the returned ledger is length 4."""
    new_ledger = add_entry("SYN-004", Decimal("40.40"), sample_ledger)
    assert len(sample_ledger) == 3
    assert len(new_ledger) == 4


def test_find_reference_hit(sample_ledger):
    """TODO (CA-3): assert a present reference is found."""
    assert find_reference(sample_ledger, "SYN-002") == "SYN-002"


# def test_find_reference_miss_returns_none(sample_ledger):
#     """TODO (CA-3): assert an absent reference returns None."""
#     assert find_reference(sample_ledger, "SYN-999") is None
