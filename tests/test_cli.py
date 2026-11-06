"""Exercise the installed command through a real subprocess and Qiskit."""

import os
import subprocess
import sys
from pathlib import Path

import pytest


def run_cli(*args, cwd=None, extra_env=None):
    env = os.environ.copy()
    env.pop("PYTEST_ADDOPTS", None)
    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    env.update(extra_env or {})
    return subprocess.run(
        [sys.executable, "-m", "qclab.cli", *args],
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        timeout=45,
    )


def test_reference_passes_from_outside_the_repository(tmp_path):
    result = run_cli("check", "--reference", cwd=tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "passed" in result.stdout


def test_lab02_reference_passes_from_outside_the_repository(tmp_path):
    result = run_cli("check", "--lab", "02", "--reference", cwd=tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Checking Lab 02" in result.stdout
    assert "passed" in result.stdout


def test_lab02_starter_fails_with_actionable_test_names():
    root = Path(__file__).resolve().parents[1]
    result = run_cli("check", "--lab", "02", cwd=root)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "test_counts_operations_and_idle_wires_not_only_gates" in result.stdout


@pytest.mark.parametrize(
    ("old", "new", "caught_by"),
    [
        (
            "isinstance(node.op, Gate) and len(node.qargs) == 2",
            "len(node.qargs) == 2",
            "test_two_qubit_gate_count_uses_type_and_arity_not_names",
        ),
        (
            "counts.get(node.name, 0) + 1",
            "1",
            "test_repeated_gate_occurrences_are_counted_separately",
        ),
        (
            "counts = {}",
            "counts = self.property_set.get('circuit_report', {}).get('operation_counts', {})",
            "test_reusing_pass_replaces_report_without_changing_previous_result",
        ),
        (
            "    def run(self, dag):",
            "    def run(self, dag):\n"
            "        for node in list(dag.op_nodes()):\n"
            "            if node.name == 'barrier':\n"
            "                dag.remove_op_node(node)",
            "test_run_preserves_dag_structure_parameters_wires_and_metadata",
        ),
    ],
    ids=["arity-only", "unique-names", "accumulating-counts", "mutating-dag"],
)
def test_lab02_checker_rejects_plausible_mistakes(tmp_path, old, new, caught_by):
    source = Path(__file__).resolve().parents[1] / "src/qclab/reference02.py"
    solution = tmp_path / "analysis solution.py"
    solution.write_text(source.read_text().replace(old, new), encoding="utf-8")
    result = run_cli("check", "--lab", "02", "--solution", str(solution), cwd=tmp_path)
    assert result.returncode == 1, result.stdout + result.stderr
    assert caught_by in result.stdout


def test_starter_fails_with_actionable_test_names():
    root = Path(__file__).resolve().parents[1]
    result = run_cli("check", cwd=root)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "test_list_of_types_selects_measure_and_reset" in result.stdout
    assert "failed" in result.stdout


def test_missing_solution_reports_setup_error_without_traceback(tmp_path):
    result = run_cli("check", "--solution", str(tmp_path / "missing.py"))
    assert result.returncode == 2
    assert "Solution file not found" in result.stderr
    assert "Traceback" not in result.stdout + result.stderr


def test_doctor_confirms_the_pinned_environment():
    result = run_cli("doctor")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Qiskit 2.6.0" in result.stdout
    assert "Circuit/DAG round trip: OK" in result.stdout


def test_demo_shows_operations_and_classical_wires():
    result = run_cli("demo")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Operation nodes: 5" in result.stdout
    assert "measure: qubits=[1], clbits=[0]" in result.stdout
    assert "reset: qubits=[1], clbits=[]" in result.stdout
    assert "Selected: measure, reset, measure" in result.stdout


def test_demo_works_with_an_ascii_only_terminal():
    result = run_cli("demo", extra_env={"PYTHONIOENCODING": "ascii"})
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Selected: measure, reset, measure" in result.stdout


def test_explicit_solution_with_spaces_passes(tmp_path):
    source = Path(__file__).resolve().parents[1] / "src/qclab/reference.py"
    solution = tmp_path / "my solution.py"
    solution.write_text(source.read_text(), encoding="utf-8")
    result = run_cli("check", "--solution", str(solution), cwd=tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "passed" in result.stdout


@pytest.mark.parametrize(
    ("body", "caught_by"),
    [
        (
            "if operation_types is None: return list(dag.op_nodes())\n"
            "    types = ([operation_types] if isinstance(operation_types, type) "
            "else operation_types)\n"
            "    return [n for n in dag.op_nodes() if any(isinstance(n.op, t) for t in types)]",
            "test_generator_is_not_consumed_again_for_each_node",
        ),
        (
            "if operation_types is None: return list(dag.op_nodes())\n"
            "    types = ((operation_types,) if isinstance(operation_types, type) "
            "else tuple(operation_types))\n"
            "    return [n for n in dag.op_nodes() if type(n.op) in types]",
            "test_superclass_matches_custom_gate_and_standard_gates",
        ),
        (
            "if operation_types is None: return list(dag.op_nodes())\n"
            "    types = ((operation_types,) if isinstance(operation_types, type) "
            "else tuple(operation_types))\n"
            "    return [n for t in types for n in dag.op_nodes() if isinstance(n.op, t)]",
            "test_repeated_types_do_not_duplicate_nodes",
        ),
        (
            "if operation_types is None: return list(dag.op_nodes())\n"
            "    types = ((operation_types,) if isinstance(operation_types, type) "
            "else tuple(operation_types))\n"
            "    return [n for n in dag.op_nodes() if isinstance(n.op, types)]",
            "test_invalid_later_type_is_rejected_even_after_a_match",
        ),
        (
            "if operation_types is None: return list(dag.op_nodes())\n"
            "    types = ((operation_types,) if isinstance(operation_types, type) "
            "else tuple(operation_types))\n"
            "    return [n for n in dag.op_nodes(include_directives=False) "
            "if isinstance(n.op, types)]",
            "test_directives_are_selected_like_other_operations",
        ),
        (
            "if operation_types is None: return list(dag.op_nodes())\n"
            "    types = ((operation_types,) if isinstance(operation_types, type) "
            "else tuple(operation_types))\n"
            "    return [n for n in dag.topological_op_nodes() if isinstance(n.op, types)]",
            "test_order_follows_op_nodes_across_independent_wires",
        ),
    ],
    ids=[
        "consumed-generator",
        "exact-type",
        "duplicated-nodes",
        "lazy-validation",
        "skips-directives",
        "topological-order",
    ],
)
def test_checker_rejects_plausible_wrong_solutions(tmp_path, body, caught_by):
    solution = tmp_path / "wrong.py"
    solution.write_text(
        "def select_op_nodes(dag, operation_types=None):\n    " + body + "\n",
        encoding="utf-8",
    )
    result = run_cli("check", "--solution", str(solution))
    assert result.returncode == 1
    assert caught_by in result.stdout, result.stdout + result.stderr


def test_missing_export_cannot_pass_the_checker(tmp_path):
    solution = tmp_path / "empty.py"
    solution.write_text("# No solution yet\n", encoding="utf-8")
    result = run_cli("check", "--solution", str(solution))
    assert result.returncode != 0
    assert "must export a callable select_op_nodes" in result.stdout


def test_broken_python_cannot_pass_the_checker(tmp_path):
    solution = tmp_path / "syntax_error.py"
    solution.write_text("def broken(\n", encoding="utf-8")
    result = run_cli("check", "--solution", str(solution))
    assert result.returncode != 0
    assert "SyntaxError" in result.stdout


def test_infinite_solution_stops_with_timeout_message(tmp_path):
    solution = tmp_path / "infinite.py"
    solution.write_text(
        "def select_op_nodes(dag, operation_types=None):\n    while True: pass\n",
        encoding="utf-8",
    )
    result = run_cli("check", "--solution", str(solution))
    assert result.returncode == 2
    assert "timed out after 30 seconds" in result.stderr
