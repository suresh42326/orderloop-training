# Capstone: refund summary

## Feature
Feature A adds a read-only per-order refund summary. The spec is docs/specs/refund-summary.md and the tests are backend/tests/test_capstone_refund_summary.py.

## What Claude got wrong
The supplied solution changes rules.py despite the brief forbidding rule changes; this implementation reuses existing eligibility instead. The first local frontend build was run from the repository root and failed because package.json is in frontend; rerunning from the correct directory succeeded.

## Review findings
The response contains only the specified aggregate fields and does not expose refund reason or customer data. The endpoint preserves the existing missing-order error and existing eligibility logic. The interactive Claude code-review and guardrail exercise were not run; this was a manual checklist review.

## Cost
Separate Claude Code review calls: 0. Overall assistant token usage and cost were not measured.

## What I would change
Run the interactive guardrail and review exercises and record their outputs. Add explicit tests for final-sale items and multiple timestamp ordering, and measure model usage.

## Pull request
https://github.com/suresh42326/orderloop-training/pull/1 is open on the user's fork. GitHub CI status must be checked after this retrospective is pushed.
