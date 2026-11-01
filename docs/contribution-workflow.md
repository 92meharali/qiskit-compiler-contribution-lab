# Start with contribution practice

Audience: developers who know Python and basic quantum circuits but are new to
Qiskit's repository. This is a local practice pathway, not a complete compiler or
Rust course. It does not generate upstream issues or pull requests.

## 1. Read the project's rules before choosing a task

Start with [Qiskit's current CONTRIBUTING.md](https://github.com/Qiskit/qiskit/blob/main/CONTRIBUTING.md)
and follow its links to the developer guide, conduct rules, AI policy, contributor
agreement, testing instructions, and PR checklist. Those documents are authoritative;
this course does not duplicate them or grant permission to submit anything.

Write a short checklist in your own words:

- How will you check for an existing issue, fix, or competing change?
- When should you discuss scope, and what information makes that discussion useful?
- Which build, tests, formatting, and release-note rules apply to your chosen change?
- What help may you use under the current AI policy, and how must it be disclosed?
- What must you understand and be authorized to do before contributing code?

Reading an agreement is not signing it. Practice here requires no CLA submission.
Do not ask a maintainer to review unfinished practice artifacts.

## 2. Locate behavior, implementation, and tests

Use the [contribution-workflow notebook](../notebooks/00-contribution-workflow.ipynb)
for a bounded historical reproduction. Record exact revisions, public API,
implementation file, and relevant test file. Check the language of the actual
implementation instead of assuming a Python API means Python internals.

Qiskit is a mixed Rust/Python project. Its Python API, Rust implementation, and
Python/Rust/C test suites are distinct layers. A Python regression can exercise a
Rust-backed API, but writing it does not demonstrate Rust implementation skills.
Do not claim every task needs a Rust edit or that a Python exercise prepares you
to write production transpiler passes. Use the actual case to establish the scope.

## 3. Reproduce and propose a useful test

Predict expected behavior before running the example. Record what actually
happens and which versions you ran. Identify a test that fails for the old
behavior and passes for the repaired behavior. Explain why the expected result
comes from the behavior contract, not from copying the implementation.

The teaching environment uses released wheels. That can demonstrate an old/new
behavior difference; it does **not** verify a source checkout, a rebuild, or your
own patch. Actual implementation work needs a separate source checkout following
Qiskit's current instructions. Keep build failures separate from exercise failures.

## 4. Prepare a packet for human review

Complete the [practice-review template](practice-review.md): problem, reproducer,
expected/observed results, source/test map, proposed change, regression rationale,
compatibility limits, help used, and remaining preparation. A facilitator selects
a follow-up scenario, checks prior exposure, and records the first answer and any
later prompts separately. A rehearsed or assisted answer is not unaided transfer
evidence; no single answer establishes readiness.

The outcome may be a useful packet, an assisted attempt, or a documented blocker.
None is an accepted upstream contribution. For real work, choose a currently
useful task, discuss scope as required, and follow the official review process;
never resubmit the historical fix.

## Optional foundations and setup

Use [Lab 01](../notebooks/01-circuit-dag.ipynb) for Python DAG inspection and
[Lab 02](../notebooks/02-analysis-pass.ipynb) for Python analysis-pass concepts
when needed. They are not prerequisites for every possible contribution.
Keep setup troubleshooting in [setup.md](setup.md), and checker details in
[lab-reference.md](lab-reference.md). All learner material is AI-assisted;
automated notebook execution is not an assessment of human readiness.
