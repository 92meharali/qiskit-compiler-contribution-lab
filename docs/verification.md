# Public prototype verification

Material version: `contribution-workflow-r1-2026-11-01`.
The historical two-lab baseline below remains `pilot-revision-1-2026-10-22`.

## Walkthrough revision 1 — local checks, 1 November 2026

The revision changes instructional text and assessment guidance, not executable
notebook cells or dependencies. Both workflow notebooks executed in clean kernels
and both fixed-release case tests passed: **4 passed in 3.58 seconds**. Ruff lint
and formatting checks passed; distributed notebook outputs remain cleared.
The instructor's small-positive-time counterexample was also checked on the locked
Qiskit 2.6.0 environment and produced a nonempty expansion as expected.

Before publication, the complete local suite was rerun on revision 1:
**38 passed in 49.53 seconds**. Foundation references also passed **26 + 14**
acceptance cases; Ruff lint/format and 90 local-link checks passed, and all six
notebooks have cleared outputs. Hosted CI for this publication must be checked
against its exact commit in the workflow history below; it is not established
by these local results. No human evaluation of revision 1 is claimed. Existing
ZIP packages are historical snapshots and do not automatically include revisions.

## Contribution-workflow implementation — local checks, 1 November 2026

- Full project suite: **38 passed** in 51.05 seconds on the local macOS environment.
  This includes two new public-QDrift-API regressions and clean-kernel execution
  of the learner and instructor workflow notebooks, in addition to the original
  34 tests. All six distributed notebooks have cleared outputs/execution counts.
- The two regressions fail on isolated Qiskit 2.5.2 at the invalid arithmetic and
  pass on Qiskit 2.6.0. NumPy error handling exposes the zero-time defect even
  though the old release can return an empty list. The fixed release also passes
  in a separate wheel environment; direct comparison commands are in the
  [case guide](contribution-case.md).
- Foundation references still pass all **26 + 14** acceptance cases. Their
  notebooks and exercise contracts are unchanged. No teaching dependency or
  lockfile was changed. Ruff lint and format checks pass.
- Local Markdown/notebook links were checked for existing targets. Upstream
  case source links use pinned commits; see [case evidence](walkthrough-case-research.md).

These are local software checks, not a new hosted CI run, a source build, a
learner session, or an external review of the redesign. The notebook deliberately
leaves human review pending. There is no automated contribution-readiness grade.
The historical comparison installs pinned direct dependencies in isolated
environments but does not lock all transitive packages. It is not part of the
ordinary fixed-release CI job.

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
  The new walkthrough demonstrates a Python synthesis regression and source
  navigation of a later Rust boundary, not Rust editing. Labs 03–04 are paused
  pending evaluation; the former Labs 05–06 remain unimplemented future ideas.
- Private learner records, grant drafts, budgets, and application attachments are
  excluded from the public repository.
