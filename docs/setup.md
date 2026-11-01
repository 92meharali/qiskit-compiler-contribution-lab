# Setup checklist — choose the project kernel

Material version: **contribution-workflow-r1-2026-11-01**. Start here if an import fails
or the notebook seems to be using the wrong Python.

## 1. Start in the right folder

Extract the complete project into its own folder. Open a terminal in the folder
containing `pyproject.toml` and `uv.lock`, not inside `notebooks/`. Keep previous
pilot versions in separate folders; do not copy a `.venv` between versions or OSes.

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if necessary.
Then run these commands in order:

```sh
uv sync --locked
uv run qclab doctor
uv run python -c "import sys; print(sys.executable)"
uv run jupyter lab notebooks/00-contribution-workflow.ipynb
```

The project's default dependency groups already include JupyterLab and ipykernel.
No additional group flag is needed. Use `uv run python`, even if `python` alone is
not on your PATH. Doctor should report Qiskit 2.6.0 and a successful circuit/DAG
round trip. Record installation errors before attempting the exercise.

To start a foundation lab, use `notebooks/01-circuit-dag.ipynb` or
`notebooks/02-analysis-pass.ipynb` in the last command. Initial setup needs internet;
running the notebooks needs no hardware
account. Keep the server terminal open while using JupyterLab.

## 2. Confirm the notebook's actual interpreter

The foundation notebooks print `sys.executable` before importing Qiskit. In the
workflow notebook, run `print(sys.executable)` in its environment cell as needed.
Compare that path with the terminal command above. Both should belong to the
same project environment, not system Python or an earlier extracted copy.

| Environment | Typical path ending |
|---|---|
| macOS / Linux / WSL | `<project>/.venv/bin/python` or `python3` |
| Native Windows | `<project>\.venv\Scripts\python.exe` |

A display label such as “Python 3” is not proof of the interpreter location.
After selecting a different kernel, rerun the path cell, then the import cell.

### JupyterLab

Use the browser opened by `uv run jupyter lab` from this project. Select its Python
3 kernel and verify the path. An older server or remembered kernel selection may
point elsewhere. If the path is wrong, save your work and reopen the notebook via
the project launch command; verify the path again before proceeding.

Launching Jupyter through `uv run` supplies the project environment. This project
already installs Jupyter, so it does not need an extra `--with jupyter` dependency.
See the [official uv/Jupyter guide](https://docs.astral.sh/uv/guides/integration/jupyter/).

### VS Code

Open the project folder with Python and Jupyter extensions available. In the
notebook's upper-right **Select Kernel** control, choose **Select Another Kernel →
Python Environments** if necessary, then this project's `.venv`. The terminal's
selected interpreter alone does not establish the notebook's kernel. Verify with
the path cell. See [VS Code's kernel guide](https://code.visualstudio.com/docs/datascience/jupyter-kernel-management).

### Windows with WSL

Choose either native Windows or WSL for a given environment; do not mix their
interpreters. For WSL, run setup in the WSL terminal. With VS Code and its WSL
extension installed, open the project there using `code .`, or use **WSL: Reopen
Folder in WSL**. Check the WSL indicator, then select the WSL project's `.venv`
using the notebook kernel picker. The notebook path should be a Linux path, not
a Windows Python executable. See the [official WSL guide](https://code.visualstudio.com/docs/remote/wsl).

These instructions have been checked against official documentation. Hosted-runner
CI passes on Windows, Linux, and macOS; see the [verification record](verification.md).
Interactive Windows/WSL and VS Code kernel selection have not been independently
tested by the agent. Record real learner setup results separately from CI.

## 3. Fix the environment before editing the exercise

| Symptom | Next check |
|---|---|
| `uv` not found | Finish uv installation and reopen the terminal; follow its installer guidance. |
| `python` not found | Use the documented `uv run python` command. |
| `ModuleNotFoundError: qiskit` or `qclab` | Confirm you extracted the whole project, ran `uv sync --locked`, and selected that project's kernel. |
| Notebook shows a different `.venv` | Select the environment belonging to this copy of the project. |
| Old behavior after an edit | Rerun the definition cell. For Lab 02, also rerun the manager cell to create a new pass instance. |
| `NOT YET` with named acceptance failures | Expected for the starter: setup worked, and the exercise is incomplete. |

Do not fix a wrong-kernel error by installing packages into an unrelated Python.
If the environment is correct but the error persists, record the failing command,
OS, version, and error text for the facilitator. Remove personal paths or secrets
before sharing screenshots or logs. Do not share the Jupyter server's access token.

## 4. Record two separate verification outcomes

1. **Acceptance checker:** does the current solution pass the contract?
2. **Clean notebook run:** save, restart the kernel, and run every cell in order.
   Does the entire notebook complete, including your own regression?

A passing checker does not prove a clean notebook run. These checker statuses
apply to foundation Labs 01–02; the workflow notebook deliberately leaves human
review pending and has no automated readiness grade. The unfinished starter may
run end-to-end successfully while reporting `NOT YET`; completed work should report
`PASS`. Restart an existing kernel after syncing changed dependencies.

## 5. Keep historical reproduction and upstream builds separate

The [case guide](contribution-case.md) runs old/fixed Qiskit wheels in separate
uv-managed environments. It does not change this project's lockfile or `.venv`.
Do not install the old wheel into the notebook kernel. The historical comparison
was locally checked; it is not part of the existing three-platform hosted run.

For actual edits to Qiskit, follow its current source-build instructions in a
separate checkout. Python, Rust tooling, rebuild steps, and upstream checks differ
from this released-wheel teaching setup. No successful source build is claimed here.
