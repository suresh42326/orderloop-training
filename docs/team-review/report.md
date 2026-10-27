# Team review: refund digest

Mode: fallback
Display mode: non-interactive independent reviewers

## Team

| Name | Angle |
|---|---|
| lead | Integration and review |
| privacy | Personal data |
| money | Arithmetic and rules |
| perf-tests | Performance and coverage |

## Findings

### Privacy

- [H] Logging exposes customer names and email addresses.
- [H] Email addresses are used as output keys instead of customer IDs.
- [M] Unknown customers are omitted, preventing reconciliation.

### Money

- [H] Empty input divides by zero; nonempty averages use floating-point cents.
- [H] Unknown customer refunds are omitted from grouped totals.
- [M] The large-refund test includes the threshold and duplicates the rules constant.

### Performance and tests

- [M] The nested customer scan is O(refunds times customers).
- [H] The single test misses privacy, empty input, integer average, unknown customers and the threshold boundary.

## Debate

Challenged finding: Treating every customer ID as forbidden identifying data would conflict with the contract.
Challenged by: privacy, against an overly broad privacy interpretation.
Outcome: kept. The contract explicitly permits customer IDs as keys; prohibit names and email instead. The money reviewer also judged performance severity dependent on data volume, so it remains medium.

## Cost and cleanup

Teammates spawned: 3 independent subagents (fallback; no interactive team).
Teammates shut down: yes, all completed.
Cost note: Three independent reviews consume more resources than one reviewer; actual token cost was not measured.

## Decision

- Fix: remove personal data from logs and use customer IDs as keys.
- Fix: include unknown customers, handle empty inputs, and calculate integer averages.
- Fix: use the shared strict lead-approval threshold.
- Fix: index customers and add regression tests for the reviewed cases.
