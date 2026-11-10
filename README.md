# Qiskit Compiler Contribution Lab

Facilitated practice for developers who know Python and basic Qiskit circuits
but have not worked through a source-level contribution. Use a resolved case to
reproduce behavior, find implementation and tests, and explain a regression for
human review.

The intended setting is a guided workshop or study group. Qiskit's official
documentation explains the process; this project supplies a case to practise,
written artifacts and facilitator prompts. It is not a replacement for that
documentation, an introductory quantum course or a proven self-study curriculum.

This is an independent project by Mehar Ali. It is not
affiliated with or endorsed by IBM, Qiskit, or Unitary Foundation.

The current prototype contains **one contribution-workflow walkthrough and two
optional Python foundation labs**, not a complete compiler/Rust training course.

## Start with the contribution workflow

Read [Qiskit's official contribution guide](https://github.com/Qiskit/qiskit/blob/main/CONTRIBUTING.md)
first, then use our [workflow guide](docs/contribution-workflow.md) and
[learner notebook](notebooks/00-contribution-workflow.ipynb). The official guide
and linked policies are authoritative; we provide practice applying them.

The walkthrough uses an already-resolved QDrift numerical bug to practice
prediction, reproduction, source navigation, and regression reasoning. It
distinguishes Python-facing APIs from Rust implementation boundaries. You will
prepare a local review packet, **not resubmit the historical fix**. A working
Python example does not establish readiness to change core Rust or production
transpiler passes.

## Quick setup

You need Git and [uv](https://docs.astral.sh/uv/getting-started/installation/).
From a terminal:

```sh
git clone https://github.com/92meharali/qiskit-compiler-contribution-lab.git
cd qiskit-compiler-contribution-lab
uv sync --locked
uv run qclab doctor
uv run jupyter lab notebooks/00-contribution-workflow.ipynb
```

Use the project's Python kernel and run cells in order. The locked teaching
environment uses Python 3.12 and Qiskit 2.6.2. Initial installation needs internet;
the notebook needs no quantum hardware or cloud account. Troubleshooting and
kernel selection: [setup checklist](docs/setup.md).

This is a released-wheel teaching environment, not a Qiskit source build.
[Historical comparison commands](docs/contribution-case.md) use separate
environments; they do not downgrade the teaching installation.

## Choose material for your task

| Material | Purpose |
|---|---|
| [Contribution workflow](notebooks/00-contribution-workflow.ipynb) | Apply project rules, reproduce a resolved issue, find code/tests, and prepare a human-review packet |
| [Foundation 01: circuit DAGs](notebooks/01-circuit-dag.ipynb) | Practice operation selection through the Python interface |
| [Foundation 02: analysis passes](notebooks/02-analysis-pass.ipynb) | Practice a bounded Python analysis pass and report-state reasoning |

The foundations are useful when relevant to a chosen task, not mandatory
preparation for every contribution. They do not teach the complete upstream
development process. Their unfinished starters intentionally report `NOT YET`.
[Checker/terminal reference](docs/lab-reference.md) explains their separate
notebook and Python workspaces.

Instructor material: [workflow guide](notebooks/instructor/00-contribution-workflow-guide.ipynb),
[Lab 01 reference](notebooks/instructor/01-circuit-dag-solution.ipynb),
[Lab 02 reference](notebooks/instructor/02-analysis-pass-solution.ipynb).

## Evidence and next steps

Material version: `contribution-workflow-r1-2026-11-01`. This revision
is software-checked, **not yet learner-validated**. Use the
[one-learner observation protocol](docs/contribution-walkthrough-pilot.md) to
record setup, assistance, source navigation, and explanation—not just green tests.
The [foundation facilitation guide](docs/facilitator-guide.md) remains separate.

See [verification](docs/verification.md) for local and hosted-CI boundaries.
The [roadmap](docs/roadmap.md) pauses the old Labs 03–04 plan while this approach
is evaluated. No learning gains, adoption, maintainer endorsement, accepted PR,
or contribution-readiness grade is claimed.

## Review or contribute

Use the [focused reviewer guide](docs/reviewer-guide.md) for concrete feedback,
or [CONTRIBUTING.md](CONTRIBUTING.md) for changes to this learning project.
Keep participant records, private replies, credentials, and personal paths out
of issues and commits. Grant and participant records are not public teaching source.

Original material is MIT licensed; see [LICENSE](LICENSE). Upstream source is
linked with attribution and retains its own license. Run only trusted local code:
the foundation checkers are not security sandboxes.
