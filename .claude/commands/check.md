---
description: Syntax-check Python files changed vs HEAD
allowed-tools: Bash(git diff:*), Bash(python -m py_compile:*)
---
Run `git diff --name-only HEAD -- '*.py'` and `python -m py_compile` on each file listed
(all of app.py run.py agents/*.py utils/*.py if none changed). Report only failures.
