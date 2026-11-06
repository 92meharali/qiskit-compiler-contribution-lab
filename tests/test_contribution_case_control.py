"""Instructor control for the contribution case; kept apart from the learner-visible tests.

The two historical regressions only assert an empty result, so an implementation that
always returns [] would pass them. This control requires sampled rotations for a nonzero
operator and time, without spoiling the learner's step-5 exercise.
"""

from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp
from qiskit.synthesis import QDrift


def test_nonzero_operator_and_time_produce_rotations():
    evolution = PauliEvolutionGate(SparsePauliOp("Z", coeffs=[1.0]), time=1.0)
    assert len(QDrift(seed=7).expand(evolution)) > 0
