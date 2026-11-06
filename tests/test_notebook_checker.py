"""The same checker must work with functions defined interactively."""

from pathlib import Path

import pytest

from qclab.notebook import check_solution
from qclab.reference import select_op_nodes


def test_lab02_notebook_defined_class_passes_the_shared_contract():
    source = Path(__file__).resolve().parents[1] / "src/qclab/reference02.py"
    namespace = {"__name__": "__main__"}
    exec(compile(source.read_text(), "<notebook-cell>", "exec"), namespace)
    result = check_solution(namespace["CircuitReport"], lab="02")
    assert result.passed, result.output
    assert "passed" in result.output


def test_lab02_class_redefinition_is_checked_without_stale_results():
    root = Path(__file__).resolve().parents[1]
    namespace = {"__name__": "__main__"}
    exec(compile((root / "exercises/lab02.py").read_text(), "<notebook-cell>", "exec"), namespace)
    result = check_solution(namespace["CircuitReport"], lab="02")
    assert not result.passed
    assert "test_counts_operations_and_idle_wires_not_only_gates" in result.output
    source = root / "src/qclab/reference02.py"
    exec(compile(source.read_text(), "<notebook-cell>", "exec"), namespace)
    assert check_solution(namespace["CircuitReport"], lab="02").passed


def test_unknown_lab_is_rejected_before_running_a_solution():
    with pytest.raises(ValueError, match="Unknown lab"):
        check_solution(select_op_nodes, lab="99")


def test_reference_function_passes_the_shared_contract():
    result = check_solution(select_op_nodes)
    assert result.passed, result.output
    assert "28 passed" in result.output


def test_notebook_starter_fails_without_throwing_into_the_kernel():
    source = Path(__file__).resolve().parents[1] / "exercises/lab01.py"
    namespace = {"__name__": "__main__"}
    exec(compile(source.read_text(), "<notebook-cell>", "exec"), namespace)
    result = check_solution(namespace["select_op_nodes"])
    assert not result.passed
    assert result.returncode == 1
    assert "test_list_of_types_selects_measure_and_reset" in result.output


def test_rerun_checks_the_new_definition_instead_of_caching_old_results():
    namespace = {"__name__": "__main__"}
    exec("def select_op_nodes(dag, operation_types=None): return []", namespace)
    assert not check_solution(namespace["select_op_nodes"]).passed
    source = Path(__file__).resolve().parents[1] / "src/qclab/reference.py"
    exec(compile(source.read_text(), "<notebook-cell>", "exec"), namespace)
    assert check_solution(namespace["select_op_nodes"]).passed


def test_notebook_globals_are_available_to_the_solution():
    namespace = {"__name__": "__main__"}
    exec(
        "from qclab.reference import select_op_nodes as implementation\n"
        "def select_op_nodes(dag, operation_types=None):\n"
        "    return implementation(dag, operation_types)\n",
        namespace,
    )
    assert check_solution(namespace["select_op_nodes"]).passed


def test_notebook_checker_does_not_accept_a_non_callable():
    with pytest.raises(TypeError, match="function itself"):
        check_solution(None)
