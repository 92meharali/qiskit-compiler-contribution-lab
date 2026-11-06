"""Run the actual notebooks from a clean kernel, including the completed learner path."""

import inspect
from pathlib import Path

import nbformat
import pytest
from nbclient import NotebookClient

from qclab.reference import select_op_nodes
from qclab.reference02 import CircuitReport

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    ("relative_path", "complete_learner", "expected_status"),
    [
        ("notebooks/01-circuit-dag.ipynb", False, "NOT YET"),
        ("notebooks/01-circuit-dag.ipynb", True, "PASS"),
        ("notebooks/instructor/01-circuit-dag-solution.ipynb", False, "PASS"),
        ("notebooks/02-analysis-pass.ipynb", False, "NOT YET"),
        ("notebooks/02-analysis-pass.ipynb", True, "PASS"),
        ("notebooks/instructor/02-analysis-pass-solution.ipynb", False, "PASS"),
    ],
    ids=[
        "01-starter",
        "01-completed",
        "01-instructor",
        "02-starter",
        "02-completed",
        "02-instructor",
    ],
)
def test_notebook_runs_from_a_clean_kernel(
    relative_path, complete_learner, expected_status, tmp_path
):
    notebook = nbformat.read(ROOT / relative_path, as_version=4)
    nbformat.validate(notebook)
    # Distributed notebooks should not contain stale results or personal kernel paths.
    for cell in notebook.cells:
        if cell.cell_type == "code":
            assert cell.execution_count is None
            assert cell.outputs == []
    if complete_learner:
        solution = next(
            cell for cell in notebook.cells if "learner-solution" in cell.metadata.get("tags", [])
        )
        reference = CircuitReport if "02-" in relative_path else select_op_nodes
        solution.source = inspect.getsource(reference)
    executed = NotebookClient(
        notebook,
        timeout=60,
        kernel_name="python3",
        resources={"metadata": {"path": str(tmp_path)}},
    ).execute()
    check = next(
        cell for cell in executed.cells if "acceptance-check" in cell.metadata.get("tags", [])
    )
    output = "".join(item.get("text", "") for item in check.outputs)
    assert f"Acceptance status: {expected_status}" in output, output
    if expected_status == "PASS":
        expected_count = 14 if "02-" in relative_path else 28
        assert f"{expected_count} passed" in output
    else:
        expected_failure = (
            "test_counts_operations_and_idle_wires_not_only_gates"
            if "02-" in relative_path
            else "test_list_of_types_selects_measure_and_reset"
        )
        assert expected_failure in output
