"""Load the reference or a learner's Python module for the shared contract."""

import importlib.util
import sys
from pathlib import Path

import pytest


def pytest_addoption(parser):
    parser.addoption("--solution", help="Path to a module exporting the selected lab's solution")


@pytest.fixture(scope="session")
def select_nodes(request):
    return load_solution(request, "select_op_nodes", "qclab.reference")


@pytest.fixture(scope="session")
def report_pass(request):
    return load_solution(request, "CircuitReport", "qclab.reference02")


def load_solution(request, export, reference):
    path = request.config.getoption("--solution")
    if path is None:
        from importlib import import_module

        return getattr(import_module(reference), export)
    path = Path(path).resolve()
    spec = importlib.util.spec_from_file_location("learner_solution", path)
    if spec is None or spec.loader is None:
        raise pytest.UsageError(f"Cannot load Python solution: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    solution = getattr(module, export, None)
    if not callable(solution):
        raise pytest.UsageError(f"Solution must export a callable {export}")
    return solution
