# Focused review: does this help a first-time Qiskit contributor?

This is an independent two-lab prototype, not an official Qiskit course. The
intended learner knows Python functions/classes and basic quantum circuits but
has not contributed to Qiskit. The goal is to help them move toward a first useful
contribution, not generate PR volume or claim that finishing a notebook is enough.

## What to inspect

Start with the [README](../README.md), then choose one learner notebook:

- [Lab 01: circuit DAGs and operation selection](../notebooks/01-circuit-dag.ipynb).
- [Lab 02: an analysis pass and report state](../notebooks/02-analysis-pass.ipynb).

The instructor notebooks are linked from the README. For a technical review,
inspect them and the checks directly. For a usability attempt, try the learner
exercise first and record whether you consulted hints or the reference. Review
comments are not treated as an independent learner outcome.

Read the [upstream handoff](upstream.md), [practice-review template](practice-review.md),
and the planned Lab 03/04 outcomes in the [roadmap](roadmap.md). Those two new labs
and the expanded mentoring workflow are not implemented yet. The installed lab
package is not a Qiskit source-build environment.

## Three questions

1. **Accuracy:** Is any contract, example, test, or explanation misleading? Please
   name the file/cell, a counterexample if possible, and the expected behavior.
2. **Contribution pathway:** What is the most important missing step between
   these exercises and a useful, appropriately scoped first contribution? What
   should be removed or simplified for this audience?
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
