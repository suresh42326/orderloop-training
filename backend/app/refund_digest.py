"""Daily refund digest for the support lead.

This module is the change under review in Lab 14. It is not wired into the API yet.

Inputs are plain dicts:
  refunds:   {"id": str, "customer_id": str, "amount_cents": int, "reason": str}
  customers: {"id": str, "name": str, "email": str}
"""

from app.rules import LEAD_APPROVAL_THRESHOLD_CENTS


def build_digest(refunds, customers):
    total = sum(r["amount_cents"] for r in refunds)
    average_cents = total // len(refunds) if refunds else 0
    customer_ids = {customer["id"] for customer in customers}
    by_customer = {}
    for r in refunds:
        key = r["customer_id"] if r["customer_id"] in customer_ids else "unknown"
        by_customer[key] = by_customer.get(key, 0) + r["amount_cents"]

    large = [r["id"] for r in refunds if r["amount_cents"] > LEAD_APPROVAL_THRESHOLD_CENTS]

    return {
        "count": len(refunds),
        "total_cents": total,
        "average_cents": average_cents,
        "by_customer": by_customer,
        "large": large,
    }
