# Foundation labs: execution and checker reference

Start with the [contribution workflow](contribution-workflow.md). These details
support the optional Python foundations; they are not Qiskit's upstream workflow.

## Notebooks and terminal exercises

The learner and instructor notebooks share checks with the CLI: 28 for Lab 01,
14 for Lab 02. Learner starters deliberately report `NOT YET`. Edit the solution
cell, rerun it, then rerun the checker. Write your own regression and explanation,
then restart the kernel and run all cells.

The notebook checker snapshots the current function/class into a fresh process.
It does not overwrite exercise files. Notebook cells and `exercises/lab01.py` or
`lab02.py` are independent workspaces; editing one does not update the other.
For Lab 02 use `check_solution(CircuitReport, lab="02")`, passing the class,
not an instance. Create fresh pass instances after redefining their class.

The notebooks require this repository's installed helper. Copying an `.ipynb`
alone is insufficient. Distributed outputs are cleared; Colab is unverified.

```sh
uv run qclab doctor
uv run qclab demo
uv run qclab check
uv run qclab check --lab 02
# Compare only after attempting the foundation exercise:
uv run qclab check --reference
uv run qclab check --lab 02 --reference
# Run a trusted, separate solution file:
uv run qclab check --solution path/to/solution.py
```

Lab 01's [terminal walkthrough](../labs/01-select-operation-nodes.md) remains
available. Instructor solutions: [01](../notebooks/instructor/01-circuit-dag-solution.ipynb)
and [02](../notebooks/instructor/02-analysis-pass-solution.ipynb).

## Verification commands

```sh
uv run python -m pytest
uv run python -m pytest tests/test_notebooks.py -q
uv run ruff check .
uv run ruff format --check .
# One visible acceptance test against the unfinished starter:
uv run python -m pytest src/qclab/checks/test_selection.py --solution exercises/lab01.py -k list_of_types -q
```

The checker exits 0 for success, 1 for failed checks or solution-load errors,
and 2 for invalid arguments or timeout. Pytest infrastructure errors may use
other nonzero statuses. A green checker is not proof of understanding or a full
clean-kernel run. Neither checker is a security sandbox: run only trusted code;
never load another person's pickle file. Temporary serialized snapshots are
removed after checks. Full project tests include a deliberate 30-second timeout.

## Alternative pip installation

Prefer the locked uv setup in [setup.md](setup.md). For an existing Python 3.12
virtual environment, `python -m pip install -e .` installs the CLI but does not
use `uv.lock` or install development/notebook groups. It is not the verified
notebook setup. Do not install into an unrelated environment to hide kernel errors.
