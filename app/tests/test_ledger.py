import datetime as dt
from decimal import Decimal
from random import choice

import pytest

from app import ledger

ENTITIES = ("mary", "john", "insurance", "supermarket", "lottery", "joe", "gas station")


@pytest.fixture
def ledger_data():
    return (
        "2015-01-16,john,mary,125.00",
        "2015-01-17,john,supermarket,20.00",
        "2015-01-17,mary,insurance,100.00",
    )


@pytest.fixture
def invalid_data_sets():
    return (
        (
            "201-01-16,john,mary,125.00",
            "2015-01-17,john,supermarket,20.00",
            "2015-01-17,mary,insurance,100.00",
        ),
        (
            "2015-01-16,john,,125.00",
            "2015-01-17,john,supermarket,20.00",
            "2015-01-17,mary,insurance,100.00",
        ),
    )


@pytest.fixture
def random_data():
    N = 10_000
    data = []
    for _ in range(N):
        date = f"{choice(range(2014, 2018))}-{choice(range(1, 13)):02}-{choice(range(1, 29)):02}"
        source = choice(ENTITIES)
        target = choice([i for i in ENTITIES if i != source])
        amount = Decimal(choice(range(-500, 250)))
        data.append(f"{date},{source},{target},{amount}")
    return data


@pytest.fixture
def ingest(ledger_data):
    ledger.ingest(ledger_data)


def test_invalid(invalid_data_sets):
    for invalid_data in invalid_data_sets:
        with pytest.raises(ledger.ValidationError):
            ledger.ingest(invalid_data)


def test_ledger_ingest(ingest):
    assert len(ledger._get_transactions()) == 6
    assert len(ledger.entities) == 4
    assert ledger.entities["john"]
    assert ledger.entities["mary"]
    assert ledger.entities["insurance"]
    assert ledger.entities["supermarket"]


def test_get_balance(ingest):
    assert ledger.get_balance("john") == Decimal(-145)
    assert ledger.get_balance("john", dt.date(2015, 1, 16)) == Decimal(-125)
    assert ledger.get_balance("mary", dt.date(2015, 1, 16)) == Decimal(125)
    assert ledger.get_balance("mary", dt.date(2015, 1, 17)) == Decimal(25)
    assert ledger.get_balance("mary") == Decimal(25)


def test_get_balance_random(random_data):
    ledger.ingest(random_data)
    for entity_name, transactions in ledger.entities.items():
        assert ledger.get_balance(entity_name) == sum(t[1] for t in transactions)
        assert ledger.get_balance(entity_name, dt.date(2017, 3, 5)) == sum(
            amount for date, amount in transactions if date <= dt.date(2017, 3, 5)
        )
