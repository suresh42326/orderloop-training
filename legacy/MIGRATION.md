# Migration note: nightly settlement, Python 2 to Python 3

## Risk tier

Tier: high
Why: settlement determines merchant payouts, so changed rounding can move money incorrectly.

## Steps taken

1. Tagged the Python 2 baseline `settle-py2-last`.
2. Committed golden and arithmetic characterization tests before changing the code.
3. Migrated money, loader, and settlement in separate commits, using the course solution as a reference implementation.

## Python 2 behaviour that had to be kept on purpose

- Integer division floors, including for negative amounts; partner shares round halves away from zero.
- Unrated merchants sort first, and names are padded by Unicode characters.
- Output is UTF-8 with normalized newlines.

## Evidence

Both golden dates pass the characterization tests. The job also runs for 2030-02-28; the lab check compares that date to an independent calculation. Before go-live, run old and new jobs side by side on real data over a complete cycle and review the differences.

## Rollback

If a payout or report differs, stop the Python 3 job and restore the prior files with `git checkout settle-py2-last -- legacy` on the old Python 2 server. Keep that server available until two clean runs have passed.
