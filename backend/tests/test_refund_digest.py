from app.refund_digest import build_digest
from app.rules import LEAD_APPROVAL_THRESHOLD_CENTS

CUSTOMERS = [{"id": "C1", "name": "Asha Verma", "email": "asha.verma@example.test"}]


def test_total_of_two_refunds():
    refunds = [
        {"id": "R1", "customer_id": "C1", "amount_cents": 1000, "reason": "damaged"},
        {"id": "R2", "customer_id": "C1", "amount_cents": 500, "reason": "late"},
    ]
    assert build_digest(refunds, CUSTOMERS)["total_cents"] == 1500


def test_empty_digest():
    assert build_digest([], CUSTOMERS) == {"count": 0, "total_cents": 0, "average_cents": 0, "by_customer": {}, "large": []}


def test_average_uses_integer_floor():
    refunds = [{"id": "1", "customer_id": "C1", "amount_cents": 1}, {"id": "2", "customer_id": "C1", "amount_cents": 2}]
    average = build_digest(refunds, CUSTOMERS)["average_cents"]
    assert type(average) is int and average == 1


def test_unknown_customer_amount_is_included():
    refunds = [{"id": "1", "customer_id": "missing", "amount_cents": 123}]
    assert build_digest(refunds, CUSTOMERS)["by_customer"] == {"unknown": 123}


def test_customer_id_is_the_key():
    refunds = [{"id": "1", "customer_id": "C1", "amount_cents": 100}]
    assert build_digest(refunds, CUSTOMERS)["by_customer"] == {"C1": 100}


def test_large_threshold_is_strict():
    refunds = [{"id": "at", "customer_id": "C1", "amount_cents": LEAD_APPROVAL_THRESHOLD_CENTS},
               {"id": "over", "customer_id": "C1", "amount_cents": LEAD_APPROVAL_THRESHOLD_CENTS + 1}]
    assert build_digest(refunds, CUSTOMERS)["large"] == ["over"]


def test_logs_exclude_customer_identifiers(caplog):
    import logging
    refunds = [{"id": "1", "customer_id": "C1", "amount_cents": 100}]
    with caplog.at_level(logging.INFO, logger="refund_digest"):
        build_digest(refunds, CUSTOMERS)
    assert "Asha Verma" not in caplog.text
    assert "asha.verma@example.test" not in caplog.text
