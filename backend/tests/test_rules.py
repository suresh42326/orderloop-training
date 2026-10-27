from datetime import datetime, timedelta

from app import rules
from app.rules import Item

NOW = datetime(2030, 3, 1, 10, 0, 0)


def delivered(days: int) -> datetime:
    return NOW - timedelta(days=days)


def tent() -> Item:
    return Item("TENT", "Tent", 18000, 1)


def test_exactly_thirty_days_is_still_on_time():
    el = rules.eligibility(delivered(30), [tent()], 0, NOW)
    assert el.eligible and not el.late


def test_thirty_one_days_is_late():
    el = rules.eligibility(delivered(31), [tent()], 0, NOW)
    assert el.late


def test_final_sale_and_gift_cards_never_qualify():
    items = [Item("A", "Socks", 1000, 2, final_sale=True), Item("G", "Gift card", 5000, 1, gift_card=True)]
    el = rules.eligibility(delivered(1), items, 0, NOW)
    assert not el.eligible
    assert "no_refundable_items" in el.blockers


def test_earlier_refunds_reduce_the_maximum():
    el = rules.eligibility(delivered(1), [tent()], 5000, NOW)
    assert el.max_refundable_cents == 13000


def test_cannot_refund_more_than_what_remains():
    el = rules.eligibility(delivered(1), [tent()], 0, NOW)
    assert rules.decide(el, 18001, "Too small").code == "exceeds_max"


def test_reason_must_be_three_to_two_hundred_characters():
    el = rules.eligibility(delivered(1), [tent()], 0, NOW)
    assert rules.decide(el, 1000, "ab").code == "reason_invalid"
    assert rules.decide(el, 1000, "x" * 201).code == "reason_invalid"
    assert rules.decide(el, 1000, "abc").ok


def test_undelivered_order_is_not_eligible():
    el = rules.eligibility(None, [tent()], 0, NOW)
    assert "not_delivered" in el.blockers


def opened(unit_price_cents: int, qty: int = 1, **flags) -> Item:
    return Item("O", "Opened thing", unit_price_cents, qty, opened=True, **flags)


def test_restocking_fee_is_ten_percent_of_an_opened_item():
    el = rules.eligibility(delivered(20), [opened(6000)], 0, NOW)
    assert el.restocking_fee_cents == 600
    assert el.max_refundable_cents == 5400


def test_restocking_fee_rounds_down_when_ten_percent_has_a_half_cent():
    el = rules.eligibility(delivered(1), [opened(1005)], 0, NOW)
    assert el.restocking_fee_cents == 100  # 100.5 -> 100
    assert el.max_refundable_cents == 905


def test_restocking_fee_is_zero_when_ten_percent_is_under_one_cent():
    el = rules.eligibility(delivered(1), [opened(9)], 0, NOW)
    assert el.restocking_fee_cents == 0  # 0.9 -> 0
    assert el.max_refundable_cents == 9


def test_restocking_fee_is_one_cent_at_exactly_ten_cents():
    el = rules.eligibility(delivered(1), [opened(10)], 0, NOW)
    assert el.restocking_fee_cents == 1
    assert el.max_refundable_cents == 9


def test_restocking_fee_uses_the_line_total_not_the_unit_price():
    el = rules.eligibility(delivered(1), [opened(2500, qty=3)], 0, NOW)
    assert el.restocking_fee_cents == 750  # 10% of 7500


def test_restocking_fee_rounds_once_per_line_not_per_unit():
    el = rules.eligibility(delivered(1), [opened(105, qty=3)], 0, NOW)
    assert el.restocking_fee_cents == 31  # 10% of 315 -> 31 (per-unit rounding would give 30)


def test_restocking_fee_is_not_charged_on_unopened_items():
    el = rules.eligibility(delivered(1), [tent()], 0, NOW)
    assert el.restocking_fee_cents == 0
    assert el.max_refundable_cents == 18000


def test_restocking_fee_is_not_charged_on_opened_final_sale_items():
    items = [opened(6000, final_sale=True), tent()]
    el = rules.eligibility(delivered(1), items, 0, NOW)
    assert el.restocking_fee_cents == 0
    assert el.max_refundable_cents == 18000


def test_restocking_fee_is_not_charged_on_opened_gift_cards():
    items = [opened(5000, gift_card=True), tent()]
    el = rules.eligibility(delivered(1), items, 0, NOW)
    assert el.restocking_fee_cents == 0
    assert el.max_refundable_cents == 18000


def test_restocking_fee_only_hits_the_opened_line_in_a_mixed_order():
    el = rules.eligibility(delivered(5), [tent(), opened(6000)], 0, NOW)
    assert el.restocking_fee_cents == 600
    assert el.max_refundable_cents == 23400


def test_restocking_fee_is_taken_before_earlier_refunds_are_subtracted():
    el = rules.eligibility(delivered(1), [opened(6000)], 1000, NOW)
    assert el.max_refundable_cents == 4400  # 6000 - 600 - 1000


def test_restocking_fee_still_applies_to_a_late_order():
    el = rules.eligibility(delivered(31), [opened(6000)], 0, NOW)
    assert el.late
    assert el.restocking_fee_cents == 600


def test_restocking_fee_allows_a_refund_of_exactly_the_reduced_maximum():
    el = rules.eligibility(delivered(1), [opened(6000)], 0, NOW)
    assert el.max_refundable_cents == 5400
    assert rules.decide(el, 5400, "Opened it").ok


def test_restocking_fee_rejects_a_refund_one_cent_over_the_reduced_maximum():
    el = rules.eligibility(delivered(1), [opened(6000)], 0, NOW)
    assert rules.decide(el, 5401, "Opened it").code == "exceeds_max"
