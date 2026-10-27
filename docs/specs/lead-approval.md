# Spec: Lead approval for large refunds

Status: approved
Risk tier: 3

## 1. Problem

Support agents cannot process refunds above $200 through OrderLoop. They use email instead, leaving leads and finance without a shared record of approvals and creating extra manual work.

## 2. User stories

- US-1: As a support agent, I want to submit a large refund for approval, so that I can track its progress in OrderLoop.
- US-2: As a support lead, I want to approve a pending refund, so that authorized refunds can proceed.
- US-3: As a finance analyst, I want to distinguish pending and approved refunds, so that I can identify money paid out.

## 3. Acceptance criteria

| ID | Criterion | Test | Package | Status |
|---|---|---|---|---|
| AC-1 | WHEN the requested refund amount is above the lead-approval threshold, the rules SHALL report that lead approval is required | test_amount_above_threshold_requires_lead_approval | WP-1 | done |
| AC-2 | WHEN the requested refund amount is exactly the threshold, the rules SHALL report that no lead approval is required | test_amount_exactly_at_threshold_needs_no_approval | WP-1 | done |
| AC-3 | IF the requested amount is not an integer number of cents, THEN the rules SHALL raise TypeError | test_float_amount_is_rejected_as_not_cents | WP-1 | done |
| AC-4 | WHEN an eligible on-time refund above the threshold is submitted, the API SHALL store it with status pending | test_large_refund_is_pending | WP-2 | todo |
| AC-5 | WHILE a refund is pending, the API SHALL reserve its amount against the refundable maximum | test_pending_refund_reserves_amount | WP-2 | todo |
| AC-6 | IF a caller without the lead role attempts approval, THEN the API SHALL respond with HTTP 403 | test_non_lead_cannot_approve | WP-2 | todo |
| AC-7 | WHEN a lead approves a pending refund, the API SHALL store its status as approved | test_lead_approves_pending_refund | WP-2 | todo |
| AC-8 | WHILE a refund is pending, the screen SHALL display the text "Pending lead approval" | test_pending_refund_message | WP-3 | todo |
| AC-9 | WHEN a refund is approved, the screen SHALL display the text "Approved" | test_approved_refund_message | WP-3 | todo |

## 4. Open questions

| ID | Question | Owner | Answer |
|---|---|---|---|
| Q-1 | Is the threshold inclusive? | Support lead | No. Approval is required strictly above 20000 cents. |
| Q-2 | Is the threshold applied to each request or the order total? | Finance analyst | It applies to each request; running totals are out of scope. |
| Q-3 | Do late refunds use this path? | Product owner | No. They remain blocked with late_requires_lead. |
| Q-4 | Who may approve and how is the role supplied? | Security reviewer | A lead may approve; this training build uses the X-Role: lead header. Real authentication is out of scope. |
| Q-5 | Does a pending refund reserve the amount? | Finance analyst | Yes. Pending amounts reduce the refundable maximum but do not count as money paid out. |
| Q-6 | Can an agent approve their own request? | Security reviewer | This is out of scope and requires a follow-up. |

## 5. Design delta

- Rules: add a pure threshold predicate; WP-2 integrates it into the existing decision flow.
- Schema: record pending or approved status and an approval record for each large refund.
- API: submit pending requests, reserve their amounts, and expose lead-only approval and status.
- Screen: display pending and approved states from the API.

## 6. Contracts between work packages

- WP-1 to WP-2: `rules.requires_lead_approval(amount_cents: int) -> bool`. True only when the amount is above `LEAD_APPROVAL_THRESHOLD_CENTS`. Raises TypeError for a non-integer.
- WP-2 to WP-3: refund JSON includes `id`, `amount_cents`, and `status` (`pending` or `approved`); the approval endpoint returns the updated refund.

## 7. Work packages

| ID | Goal | Files | Depends on | Done when |
|---|---|---|---|---|
| WP-1 | Pure threshold rule | backend/app/rules.py, backend/tests/test_rules.py | none | AC-1 to AC-3 tests pass and the suite is green |
| WP-2 | Pending and lead approval API | backend/app/main.py, backend/app/schema.sql, backend/tests/test_api.py | WP-1 | API criteria pass and existing refund behavior remains covered |
| WP-3 | Display refund states | frontend/src/App.tsx, frontend/src/api.ts | WP-2 | Screen criteria pass against the API contract |

## 8. Risk and approval gates

Tier 3 applies because refunds affect money and approval authority.

- G1: A human support lead approves this spec before tests or code are written.
- G2: A human reviews each package's failing tests before implementation starts.
