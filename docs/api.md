# API reference

Money amounts are integer cents. Application errors use the shape `{"detail": {"code": "...", "message": "..."}}`.

## GET /health

Takes no parameters. Returns `{"status": "ok"}`.

## GET /orders

Optional query parameters:

- `q`: search for a substring of the order ID or customer name.
- `status`: filter by exact order status.

Returns an array of orders ordered by ID, with `id`, `status`, `placed_at`, `delivered_at`, `customer_name`, and `total_cents`.

## GET /orders/{id}

The path parameter `id` is an integer order ID. Returns the order, customer, items, refunds, and refund eligibility. An unknown order returns `404` with code `order_not_found`.

## POST /orders/{id}/refunds

The path parameter `id` is an integer order ID. Send an `Idempotency-Key` header and a JSON body with integer `amount_cents` and string `reason`. The trimmed reason must be 3–200 characters and the amount must be positive. A successful request returns `201` with the refund's `id`, `order_id`, `amount_cents`, `reason`, and `replayed`. Reusing a key returns the existing refund with `replayed: true`.

Refunds exclude final-sale items and gift cards, and the maximum is reduced by previous refunds. Refunds more than 30 days after delivery or over 20,000 cents require lead approval, which is not supported yet.

| HTTP status | Error code | Meaning |
| --- | --- | --- |
| 400 | `idempotency_key_missing` | The header is missing or empty. |
| 404 | `order_not_found` | The order does not exist. |
| 409 | `not_eligible` | The order is not delivered, has no refundable items, or has nothing left to refund. |
| 409 | `late_requires_lead` | The refund is more than 30 days after delivery. |
| 409 | `approval_required` | The amount exceeds 20,000 cents. |
| 422 | `reason_invalid` | The trimmed reason is outside the allowed length. |
| 422 | `amount_invalid` | The amount is not positive. |
| 422 | `exceeds_max` | The amount exceeds the refundable maximum. |

FastAPI also returns `422` for request validation errors, such as a missing or invalid body field or a non-integer order ID.

## POST /orders/{id}/reply-draft

The path parameter `id` is an integer order ID. Send a JSON body with a string `message`. Returns a reply draft based on the message and the order's refund eligibility. An unknown order returns `404` with code `order_not_found`.
