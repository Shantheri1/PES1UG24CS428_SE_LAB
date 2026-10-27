# Static Code Analysis — Issues Report

## Project
IT Helpdesk Ticket Allocator

## Tools Used
- Pylint
- Flake8
- Bandit

## Baseline Results
- Pylint score: 5.53/10
- Flake8: Reported style and code-quality violations.
- Bandit: Reported 4 security-related findings.

## Identified Issues

| No. | Issue | Tool | Severity / Type | Proposed Fix |
|---|---|---|---|---|
| 1 | Hardcoded administrator password | Bandit | Low; potential security risk | Read credentials from a secure configuration or environment variable. |
| 2 | Command execution uses `shell=True` with a concatenated hostname | Bandit | High; potential command injection | Use an argument list with `shell=False` and validate the hostname. |
| 3 | Bare exception handler with `pass` | Pylint, Flake8, Bandit | Error-handling and maintainability issue | Catch specific exceptions and handle them explicitly. |
| 4 | Mutable list used as a default argument | Pylint | Potential correctness issue | Use `None` as the default and create a new list inside the function. |
| 5 | Missing module and function docstrings | Pylint | Documentation issue | Add meaningful docstrings. |
| 6 | Inconsistent naming conventions | Pylint | Style issue | Use `UPPER_CASE` for constants and `snake_case` for functions and variables. |
| 7 | Long lines and insufficient blank lines | Pylint, Flake8 | Formatting issue | Follow the configured line-length and spacing rules. |
| 8 | Comparison with `None` using `==` | Pylint, Flake8 | Style issue | Use `is None`. |
| 9 | File opened without an explicit encoding or context manager | Pylint | Resource-handling issue | Use `with open(..., encoding="utf-8")` where appropriate. |
| 10 | Unused local variable | Pylint, Flake8 | Code-quality issue | Remove the unused variable or use it if needed. |

## Conclusion
Static analysis identified security, error-handling, documentation, naming, formatting, and resource-management issues. The next stage is to correct the issues, rerun the tools, and compare the results with the baseline.
