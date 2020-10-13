from decimal import Decimal
import datetime as dt
import re
from typing import List, Tuple, NamedTuple

from dateutil import parser


DATE_REGEX = r"[1-2][9|0]\d\d-\d\d-\d\d"


class ValidationError(Exception):
    pass


class Transaction(NamedTuple):
    date: dt.date
    source: str
    target: str
    amount: Decimal


def ingest(transaction_strings: List[str]):
    """
    Parse comma-separated strings into Transactions.
    Build `entities` dictionary, with keys of entity names and values of
     lists of tuples, 0-date 1-amount
    """
    transactions = []
    entity_names = set()
    for transaction_string in transaction_strings:
        date, source, target, amount = parse_and_validate_transaction_string(
            transaction_string
        )
        transaction = Transaction(date, source, target, amount)
        transactions.append(transaction)
        entity_names.update((source, target))

    global entities
    entities = {entity_name: [] for entity_name in entity_names}

    for t in sorted(transactions, key=lambda t: t.date):
        entities[t.source].append((t.date, -t.amount))
        entities[t.target].append((t.date, t.amount))


def _get_transactions():
    """for testing"""
    return [item for sublist in list(entities.values()) for item in sublist]


def get_balance(entity_name: str, on_date: dt.date = None) -> Decimal:
    """
    Get the balance _at closing_ of a given date. If no date is given,
    all transactions are summed -> "current balance".
    """
    return sum(
        amount
        for date, amount in entities[entity_name]
        if not on_date or date <= on_date
    )


def parse_and_validate_transaction_string(
    transaction_string: str,
) -> Tuple[dt.date, str, str, Decimal]:

    try:
        date_string, source, target, amount_string = transaction_string.split(",")
    except ValueError:
        raise ValidationError(
            f"Please provide a date, source, target and amount: {transaction_string}"
        )

    if not all((date_string, source, target, amount_string)):
        raise ValidationError(f"All items must have a value: {transaction_string}")

    if not re.match(DATE_REGEX, date_string):
        raise ValidationError(f"date is invalid: {date_string}")

    date = parser.parse(date_string).date()
    amount = Decimal(amount_string)

    return date, source, target, amount
