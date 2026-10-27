# Eval results

Six golden cases, two recorded runs each. Version A reads code; version B answers from memory.

## with-code

```text
PASS RATE: 6/6 (100%)
PASS@K:    6/6
RUNS:      12/12 passed
COST:      $0.1767
```

## from-memory

```text
PASS RATE: 1/6 (17%)
PASS@K:    1/6
RUNS:      2/12 passed
COST:      $0.0666
```

## Notes

- day-30-late passed from memory by a lucky guess; one transcript explicitly says the agent did not know the rule. An answer-only grader cannot verify the reasoning or source.
- These figures replay recorded examples and do not measure a new live model run. The runner was taken from the course solution.

Decision: keep with-code for this task because all recorded runs passed and the agent can check the actual rules.
