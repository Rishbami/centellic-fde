# Contract layer
# Keeps seperate from deterministic behaviour in test_extract.py

from decimal import Decimal

import pytest

from extract import extract_amount, ModelRefused, ModelContractViolation

from model_client import FakeModel

CALLS = 200


@pytest.mark.contract
def test_every_reply_lands_in_a_handles_case() -> None:
    client = FakeModel()
    outcomes = {"amount": 0, "refused": 0, "violations": 0}

    for _ in range(CALLS):
        try:
            value = extract_amount("total is 35.35", client)
        except ModelRefused:
            outcomes["refused"] += 1
        except ModelContractViolation:
            outcomes["violations"] += 1
        else:
            assert value == Decimal("35.35")
            outcomes["amount"] += 1

    assert sum(outcomes.values()) == CALLS
    assert all(count > 0 for count in outcomes.values()), f"Outcomes: {outcomes}"
