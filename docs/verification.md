# Public prototype verification

Teaching version: `pilot-revision-1-2026-10-22` | Prepared 22 October 2026

## Existing local baseline

The two-lab prototype previously passed 34 local project tests on macOS ARM64,
Python 3.12.13, Qiskit 2.6.0, and pytest 9.1.1. Six test paths execute the learner
starter, completed learner, and instructor notebooks in clean kernels. Lab 01's
reference passes 26 acceptance cases; Lab 02's passes 14. The original verification
record is retained locally; this public document contains software results only.

The local publication check on 22 October 2026 passed all 34 project tests in
49.45 seconds, both references (26 + 14 checks), and Ruff lint/format checks.
Publication changes exclude private records and replace notebook links to private
documents with the public facilitator guide. The six notebook execution paths
also passed again after those link edits (8.08 seconds locally).

## GitHub CI

The [first public CI run](https://github.com/92meharali/qiskit-compiler-contribution-lab/actions/runs/39687908140)
completed successfully on Linux, macOS, and Windows for commit
`fc5e466fdc92273a034c362ce977bf4effe2aa63` on 22 October 2026 (Asia/Karachi).
Each job ran locked installation, environment diagnostics, both reference checks,
the project tests, and Ruff lint/format checks. This is hosted-runner verification,
not proof that every learner's interactive setup works. See the
[live workflow history](https://github.com/92meharali/qiskit-compiler-contribution-lab/actions/workflows/ci.yml)
for later commits rather than assuming their results from this snapshot.

## Reproduce

From the repository root:

```sh
uv sync --locked
uv run qclab doctor
uv run qclab check --reference
uv run qclab check --lab 02 --reference
uv run python -m pytest
uv run ruff check .
uv run ruff format --check .
```

The ordinary learner checker intentionally reports `NOT YET` for the incomplete
starter. The test suite checks both failure and success paths, including rejection
of plausible incorrect implementations and a deliberate 30-second timeout.
Notebook source files must have outputs and execution counts cleared.

## Limits

- Software tests do not establish independent learner understanding, educational
  impact, maintainer endorsement, or readiness for a real upstream contribution.
- Hosted-runner CI does not validate every interactive Jupyter/VS Code/WSL setup.
  Record real setup problems separately. Colab has not been tested.
- The notebook helper and CLI execute trusted local Python; neither is a security
  sandbox. Never run untrusted solution files or serialized snapshots.
- The teaching package uses a released Qiskit wheel, not a Qiskit source build.
  Labs 03-06 are planned, not implemented.
- Private learner records, grant drafts, budgets, and application attachments are
  excluded from the public repository.
