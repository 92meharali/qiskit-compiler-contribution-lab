"""Check executable walkthroughs, not learner reasoning or readiness."""

from pathlib import Path

import nbformat
import pytest
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    "relative_path",
    [
        "notebooks/00-contribution-workflow.ipynb",
        "notebooks/instructor/00-contribution-workflow-guide.ipynb",
    ],
    ids=["learner", "instructor"],
)
def test_walkthrough_runs_in_clean_kernel(relative_path, tmp_path):
    notebook = nbformat.read(ROOT / relative_path, as_version=4)
    nbformat.validate(notebook)
    for cell in notebook.cells:
        if cell.cell_type == "code":
            assert cell.execution_count is None
            assert cell.outputs == []
    executed = NotebookClient(
        notebook,
        timeout=60,
        kernel_name="python3",
        resources={"metadata": {"path": str(tmp_path)}},
    ).execute()
    output = "".join(
        item.get("text", "")
        for cell in executed.cells
        if cell.cell_type == "code"
        for item in cell.outputs
    )
    assert "Zero-operator expansion: []" in output
    assert "Warnings: 0" in output
    assert "Human review: pending" in output
