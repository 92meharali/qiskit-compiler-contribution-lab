# Qiskit Compiler Contribution Lab

A practical path from writing quantum circuits to contributing to a quantum
compiler: understand the representation, write passes, test correctness, diagnose
regressions, and explain changes for review.

This is an independent project by Mehar Ali. It is not
affiliated with or endorsed by IBM, Qiskit, or Unitary Foundation.

**Teaching material version:** `pilot-revision-1-2026-10-22`. This public prototype
contains two working labs, not a complete contributor-training course. See the
[software verification record](docs/verification.md) and
[focused reviewer guide](docs/reviewer-guide.md). Passing checks is not evidence
of independent understanding or readiness to submit a Qiskit change.

## Start Lab 01

The primary learning format is a Jupyter notebook: explanations, live circuit
inspection, an editable exercise, and test feedback in one document.

You need Git and [uv](https://docs.astral.sh/uv/getting-started/installation/).
Clone the repository, then run the setup commands from its root directory:

```sh
git clone https://github.com/92meharali/qiskit-compiler-contribution-lab.git
cd qiskit-compiler-contribution-lab
uv sync --locked
uv run qclab doctor
uv run python -c "import sys; print(sys.executable)"
uv run jupyter lab notebooks/01-circuit-dag.ipynb
```

`uv sync` creates an isolated `.venv`, uses Python 3.12 by default, and installs
locked dependencies including Qiskit 2.6.0. The first setup requires internet;
the labs themselves run locally without quantum hardware or an IBM account.
JupyterLab and the notebook test dependencies are included in the default groups.

Open [the learner notebook](notebooks/01-circuit-dag.ipynb) and select the project's
Python 3 kernel. Compare the notebook's first printed interpreter path with the
terminal's project `.venv`. In VS Code, use the notebook's **Select Kernel** picker;
choosing a terminal interpreter is not enough. Follow the
[setup checklist](docs/setup.md) for JupyterLab, VS Code, and WSL. Run cells from top to
bottom. **The starter's acceptance status is supposed to be NOT YET.** Edit the
function in its cell, rerun that cell, then rerun the checker. When it passes,
write your own regression test and explanation, then restart the kernel and run
all cells to check reproducibility.

After your attempt, compare with [the instructor notebook](notebooks/instructor/01-circuit-dag-solution.ipynb).
Both notebooks use the same 26 acceptance checks as the CLI. The notebook helper
checks a snapshot of the current function in a fresh process and does not
overwrite your exercise files. Saved notebooks ship with outputs cleared.

The notebooks need this repository's installed `qclab` helper; copying only the
`.ipynb` to another environment is not sufficient. Colab has not been tested yet.

For a terminal workflow, the [Markdown walkthrough](labs/01-select-operation-nodes.md)
and `exercises/lab01.py` remain available:

```sh
uv run qclab doctor
uv run qclab demo
uv run qclab check
```

The Python starter and the notebook are independent workspaces; editing one does
not update the other. They share the behavior contract and checker.

If you prefer pip, use Python 3.12 in a virtual environment and run
`python -m pip install -e .`. This does not use `uv.lock`; the uv path is the
reproducible setup used for verification. It installs the CLI, but not the
development/notebook dependency groups. Commands are then `qclab doctor`, etc.

## What exists today

- **Lab 01:** inspect a real circuit DAG and implement a robust operation selector.
- **Lab 02:** write an analysis pass, publish a top-level circuit inventory, and
  preserve the circuit. Includes 14 shared acceptance cases.
- Learner and instructor `.ipynb` files, tested by execution in clean kernels.
- Starter, progressive hints, public acceptance checks, and an instructor reference.
- `doctor`, `demo`, and `check` commands.
- Tests of the checker, including plausible incorrect solutions and a timeout.
- A longer-term [curriculum roadmap](docs/roadmap.md), an
  [upstream transition guide](docs/upstream.md), and a
  [practice-review template](docs/practice-review.md).

Labs 03-06 are planned. Learning outcomes, workshop adoption, and maintainer approval
have not been validated. The current software verification record is in
[docs/verification.md](docs/verification.md). The next proposed milestone adds
Labs 03-04 and a bounded handoff toward an appropriate first Qiskit contribution
attempt. Labs 05-06 are longer-term work, and no accepted upstream PR is promised.
Grant preparation and participant-level records are not part of this repository.

## Continue with Lab 02

Open [the Lab 02 learner notebook](notebooks/02-analysis-pass.ipynb). It introduces
`AnalysisPass`, `PassManager`, the shared property set, and a deliberately bounded
report: top-level operation counts, wire counts, and two-qubit gate counts. It is
not a recursive execution-cost estimate. The separate
[instructor notebook](notebooks/instructor/02-analysis-pass-solution.ipynb) includes
a complete solution and an example regression.

```sh
uv sync --locked
uv run qclab doctor
uv run python -c "import sys; print(sys.executable)"
uv run jupyter lab notebooks/02-analysis-pass.ipynb

# Optional terminal exercise (intentionally incomplete):
uv run qclab check --lab 02
uv run qclab check --lab 02 --reference
```

In the notebook, use `check_solution(CircuitReport, lab="02")`, passing the class
rather than an instance. After editing the class cell, rerun it and the checker.
Restart an existing kernel after syncing updated dependencies. As with Lab 01,
the notebook and `exercises/lab02.py` are independent workspaces.

## Useful commands

```sh
# Check a different self-contained Python solution file:
uv run qclab check --solution path/to/solution.py

# Compare against the reference after trying the exercise:
uv run qclab check --reference

# Run just one public acceptance test against the starter:
uv run python -m pytest src/qclab/checks/test_selection.py --solution exercises/lab01.py -k list_of_types -q

# Verify the checker itself (includes a deliberate 30-second timeout test):
uv run python -m pytest

# Execute learner, completed-learner, and instructor notebook paths:
uv run python -m pytest tests/test_notebooks.py -q

# Formatting and static checks:
uv run ruff check .
uv run ruff format --check .
```

The checker runs your local Python file. It exits with 0 on success, 1 on failed
checks or solution-load errors, and 2 on invalid arguments or the 30-second timeout.
pytest infrastructure errors can return other nonzero statuses. A green result
means the visible behavior contract passes; it is not proof of independent
understanding. This is an open-book practice environment.
Neither checker is a security sandbox: only run trusted local code. Serialized
notebook snapshots are created locally for the current check and then removed;
never load someone else's pickle file.

## Contribute to this learning project

Start with the [contribution guide](CONTRIBUTING.md). We especially need feedback
on installation, confusing explanations, realistic compiler tasks, and independent
learner outcomes. Work through the lab before reading the reference.

The [upstream transition guide](docs/upstream.md) explains how practice differs
from changing Qiskit itself. The author's [past PRs](docs/case-studies.md) are optional
reading; the curriculum is organized around general skills.

## License

Original code and learning material are MIT licensed; see [LICENSE](LICENSE).
Linked third-party projects and documents retain their own licenses.
