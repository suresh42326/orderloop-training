# Spec: Refund summary for one order

Status: Approved
Risk tier: Medium

## Problem
Support agents must inspect individual refund records to know how much was refunded and remains available. This takes time and can make reconciliation harder.

## User stories
- As a support agent, I want an order refund summary so that I can see the refunded and remaining amounts quickly.

## Acceptance criteria
- AC-1: When an order exists, the system shall return order_id, refund_count, refunded_cents, remaining_cents and last_refund_at.
- AC-2: When an order has no refunds, the system shall return zero count and total and a null last_refund_at.
- AC-3: If an order does not exist, then the system shall return 404 with order_not_found.
- AC-4: The system shall exclude refund reasons and customer personal data from the response.
- AC-5: When multiple refunds exist, the system shall report their count, sum and latest timestamp and use the existing eligibility rule for remaining cents.

## Out of scope
- Creating or changing refunds, altering refund rules, or frontend changes.

## Open questions
| # | Question | Owner | Answer |
|---|---|---|---|
| 1 | How is remaining calculated for final-sale items? | Product owner | Use the existing eligibility max_refundable_cents, excluding nonrefundable items. |

## Plan
1. Add API tests for AC-1 through AC-5 in backend/tests/test_capstone_refund_summary.py; verify they fail before implementation.
2. Add a read-only endpoint in backend/app/main.py using existing load_order and eligibility rules; run the backend suite.

## Approval
Approved by: user authorized autonomous review; assistant selected the feature and applied that instruction.
Date: 2026-10-27
