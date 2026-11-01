"""Historical API regression; runnable separately with Qiskit 2.5.2 and 2.6.0.

Original local teaching test, based on the documented contract in Qiskit #17113
and #17117. This is not an upstream contribution or the upstream test suite.
"""

import numpy as np
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp
from qiskit.synthesis import QDrift


def test_zero_operator_expands_without_invalid_arithmetic():
    """Zero Hamiltonian means identity evolution: no sampled rotations."""
    evolution = PauliEvolutionGate(SparsePauliOp("Z", coeffs=[0.0]), time=2.0)
    with np.errstate(divide="raise", invalid="raise"):
        assert QDrift(seed=7).expand(evolution) == []


def test_zero_time_expands_without_invalid_arithmetic():
    """An empty result alone missed warnings in the historical implementation."""
    evolution = PauliEvolutionGate(SparsePauliOp("Z", coeffs=[1.0]), time=0.0)
    with np.errstate(divide="raise", invalid="raise"):
        assert QDrift(seed=7).expand(evolution) == []
