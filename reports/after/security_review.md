# Bandit Security Review

## Summary

Bandit was run against `helpdesk_system.py` after the code changes.

- High-severity findings: 0
- Medium-severity findings: 0
- Low-severity findings: 3

## Findings

1. **B404 — subprocess module:** Bandit flags the use of the subprocess module for manual security review.
2. **B607 — partial executable path:** The `ping` executable is invoked by name rather than an explicitly resolved executable path.
3. **B603 — subprocess execution:** Bandit recommends reviewing subprocess calls that receive input, even when `shell=False` is used.

## Mitigations

The updated implementation uses an argument list, sets `shell=False`, validates the hostname, and applies a timeout. These measures reduce command-injection risk, but the remaining findings still require manual review.

## Conclusion

The original high-severity `shell=True` finding no longer appears. The remaining low-severity findings have been documented rather than suppressed.
