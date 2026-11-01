# Focused review: does this help a first-time Qiskit contributor?

This is an independent contribution-workflow prototype with two optional Python
foundation labs, not an official Qiskit course. The
intended learner knows Python functions/classes and basic quantum circuits but
has not contributed to Qiskit. The goal is to help them move toward a first useful
contribution, not generate PR volume or claim that finishing a notebook is enough.

## Specialist reviewer profile

For a focused technical review, we seek a current Qiskit maintainer or active
contributor with recent synthesis or transpiler work and demonstrated experience
with Python/Rust integration, source builds and regression tests. Relevant upstream
work matters more than a particular team title. The reviewer should be independent
of the teaching material's authorship; no specialist reviewer is appointed yet.

The review should check the source map and Python/Rust boundary against the pinned
historical case, and check development instructions against the relevant source
revision and [Qiskit's contribution guidance](https://github.com/Qiskit/qiskit/blob/main/CONTRIBUTING.md).
Record concrete findings and unresolved gaps, not an endorsement or certification.
The future source-development companion is not implemented yet; assess it only
when available. This profile does not restrict general learner or educator feedback.

## What to inspect

Start with the [README](../README.md), then the
[contribution-workflow notebook](../notebooks/00-contribution-workflow.ipynb).
It applies contribution rules, reproduces a resolved synthesis bug, traces a
Python/Rust boundary, and prepares a practice review. It does not teach core Rust
development or a complete transpiler pass. If relevant, inspect a foundation:

- [Lab 01: circuit DAGs and operation selection](../notebooks/01-circuit-dag.ipynb).
- [Lab 02: an analysis pass and report state](../notebooks/02-analysis-pass.ipynb).

The instructor notebooks are linked from the README. For a technical review,
inspect them and the checks directly. For a usability attempt, try the learner
exercise first and record whether you consulted hints or the reference. Review
comments are not treated as an independent learner outcome.

Read the [case guide](contribution-case.md), [practice-review template](practice-review.md),
and [roadmap](roadmap.md). The old Lab 03/04 plan is paused while this direction is
evaluated. The installed teaching package is not a Qiskit source-build environment.
No learner outcome for the new walkthrough is claimed. Instructor answers are
[separate](../notebooks/instructor/00-contribution-workflow-guide.ipynb).

## Three questions

1. **Accuracy:** Is any contract, example, test, or explanation misleading? Please
   name the file/cell, a counterexample if possible, and the expected behavior.
2. **Contribution pathway:** Does the workflow-first case provide useful practice
   beyond linking CONTRIBUTING.md? Does it accurately distinguish Python API use,
   Python implementation, and Rust-backed code? What remains before a useful,
   appropriately scoped contribution, and what should be removed or simplified?
3. **Overlap and reuse:** Which existing Qiskit resource should this link to
   instead of recreating it? Could you run one exercise from the guide, and what
   would prevent you from doing so?

Even one concrete finding is useful; a full course review is not expected. A
15-20-minute skim is an invitation size, not a claimed exercise completion time.
An optional installation attempt can take longer; record the actual time.

## Suggested feedback format

- What you inspected: lab, file/cell, and commit or version.
- What you tried: reading, running the reference, or attempting the learner task.
- One technical issue or missing prerequisite, with an example.
- One useful element and one thing to cut, replace, or link elsewhere.
- What remains before a learner should attempt an upstream task.
- If you ran it: OS, Python/Qiskit versions, commands, and sanitized errors.

Use a repository issue or reply privately to the person who invited your review.
Do not post participant records or identifying screenshots. The author will ask
before quoting a private reply or naming someone in a grant application. A review
is feedback on the inspected scope, not an endorsement by the reviewer or Qiskit.

No submission to Qiskit is requested as part of this review. Actual contributions
must follow the current upstream policies and be understood and owned by the
human contributor.
