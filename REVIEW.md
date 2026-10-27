# Review: Add 5% goodwill credit for late deliveries

Verdict: **request changes**. The change risks duplicate credits, exposes personal data, changes a refund boundary, and the new endpoint cannot run.

## High

- **Boundary test weakened** (`backend/tests/test_rules.py:19`, `backend/app/rules.py:67`). The `not el.late` assertion was removed while `>` changed to `>=`, contrary to the existing 30-day rule and the claim that tests did not change. Restore both the boundary and its assertion.
- **Personal data logged** (`backend/app/main.py:137`). Names, email, phone and free-text refund reason enter logs, contrary to the privacy rule. Log only non-sensitive operational identifiers.
- **Missing idempotency** (`backend/app/main.py:162`, `backend/app/main.py:177`). A timestamp-based key changes on every request, allowing retries to create duplicate payments. Require a stable idempotency key and replay existing results.

## Medium

- **Missing helper** (`backend/app/main.py:173`). `rules.round_to_cents` is undefined, so the endpoint raises an exception. Implement the calculation using a defined integer-cents rule and test the endpoint.
- **Float money** (`backend/app/rules.py:102`). The calculation converts cents to floating-point dollars, contrary to the integer-cents rule. Calculate and round using integer arithmetic with an explicit policy.
- **No eligibility check** (`backend/app/main.py:171`). The endpoint credits orders regardless of whether delivery was late. Enforce the intended condition and cover it with tests.
- **Missing endpoint tests** (`backend/app/main.py:162`). No added test exercises the new endpoint, leaving its failure and retry behavior undetected. Add success, eligibility and replay tests.

## Low

- **Undisclosed dependency** (`backend/pyproject.toml:9`). `arrow` is added despite the description's no-new-dependencies claim. Remove it or disclose and justify it.

## Tool results and false positives

- The diff and checklist were reviewed manually, with the course solution consulted as a reference. The interactive `/code-review` and `/security-review` commands were not run, so their findings, misses and false positives were not measured.
- No tool false positives were assessed. Claims about unchanged tests and dependencies were checked against the diff; the missing helper was checked against the branch contents.
