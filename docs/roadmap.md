# Roadmap: contribution practice before specialization

Updated 1 November 2026. This is an independent learning project for Python
developers with basic circuit knowledge who are new to Qiskit contributions.
The purpose remains a first useful contribution; no upstream acceptance is promised.

## Current entry point

| Stage | Practice artifact | Current status |
|---|---|---|
| Contribution expectations | Learner-written checklist using the official guide | Prompts implemented in the workflow notebook |
| Repository navigation | Public API, implementation, tests, and Python/Rust source map | One pinned historical case implemented |
| Reproduction and regression | Old/fixed observations and a justified local regression | Wheel comparison and reference checks implemented |
| Human review | Explanation, limits, assistance record, and next preparation | Template and protocol ready; no learner review outcome claimed |

Start at the [workflow notebook](../notebooks/00-contribution-workflow.ipynb).
The [QDrift case](contribution-case.md) is a resolved Python synthesis bug with a
later Rust integration boundary to inspect. It is not a transpiler-pass exercise,
a new upstream issue, or evidence of Rust development proficiency. We link to
Qiskit's contribution rules rather than creating competing policy.

## Retain, pause, and defer

- **Retain:** Labs 01–02, their learner/instructor notebook pairs, public checks,
  and explanations as optional Python DAG/analysis-pass foundations. Their
  earlier observations cannot be transferred to the new walkthrough.
- **Pause:** the previously proposed Lab 03 transformation and Lab 04 correctness
  sequence pending evaluation of the contribution-first direction. Neither is
  implemented. Do not treat four workflow stages as four completed or promised labs.
- **Defer:** full Rust instruction, production optimizer development, broader
  regression/mentoring courses, and multiple framework support. The former
  Labs 05–06 remain unimplemented, not funded commitments.

## Evaluation gate for each material revision

Use the [blank protocol](contribution-walkthrough-pilot.md) with one consenting
learner. Freeze the material version, run the historical comparison beforehand,
and record setup separately from learning. Assess the policy checklist, source
map, reproduction, regression rationale, and follow-up explanation. Check prior
question exposure and record initial answers separately from hints. Record assistance,
reference exposure, and unfinished work; do not manufacture a successful PR.

Retain or narrow the approach based on the observed packet and blockers. A
single attempt is a usability check, not proof of causal gains or contribution
readiness. Ask an experienced contributor whether the practice is relevant and
what prerequisites are missing; no response or continuing support is assumed.

After that gate, re-estimate deliverables and workload before revising a grant
proposal. Implementation of this prototype does not itself approve a new grant
scope or budget. Any work completed before application must be described as the
baseline rather than future funded work.

## Release and review boundaries

Keep execution checks separate from human outcomes. Source checkout builds,
Rust edits, full upstream test runs, and live issue suitability are additional
work not established by wheel tests. Recheck
[Qiskit's current contribution guide](https://github.com/Qiskit/qiskit/blob/main/CONTRIBUTING.md)
before real work. Do not submit practice solutions, duplicate resolved fixes,
or use PR volume as success. The [reviewer guide](reviewer-guide.md) asks for
specific findings, not endorsements.
