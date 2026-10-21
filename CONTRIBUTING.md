# Contributing to the lab

The project is in its first prototype stage. Read the README and Lab 01, try the
starter, and report a reproducible problem or concrete improvement.

For a focused technical or teaching review, use the
[reviewer guide](docs/reviewer-guide.md). Do not include participant identities,
private session notes, access tokens, or personal file paths in public issues.

For code changes, run:

```sh
uv sync --locked
uv run qclab check --reference
uv run qclab check --lab 02 --reference
uv run python -m pytest
uv run ruff check .
uv run ruff format --check .
```

Keep the learner starter deliberately incomplete. Normal project tests check that
it fails; do not replace it with the reference to make the learner command green.
New exercises need a clear public contract, passing reference, intentionally failing
starter, useful hints, and evidence that the checker rejects plausible mistakes.

Notebooks are the primary learner format. Keep cell IDs stable, tag the learner
function as `learner-solution` and the check cell as `acceptance-check`, and clear
outputs/execution counts before committing. Add clean-kernel execution tests for
both the unfinished and completed paths. Keep shared grading logic in `src/qclab`
so CLI and notebook checks cannot silently diverge.

Explain why a change helps a learner. Keep exercises accessible on ordinary
laptops and make any dependency on quantum hardware optional. Separate completed
software checks from observed human outcomes. Include attribution and describe
substantial AI assistance in contributions to this project.

Changes to Qiskit itself follow [Qiskit's own policy](docs/upstream.md), not this
repository's workflow. Exercise completion should never generate an upstream PR
automatically.
