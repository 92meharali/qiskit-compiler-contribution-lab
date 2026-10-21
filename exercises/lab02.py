"""Lab 02 starter: publish a circuit inventory without changing the DAG.

Run: uv run qclab check --lab 02
The primary lesson is notebooks/02-analysis-pass.ipynb.
"""

from qiskit.transpiler import AnalysisPass


class CircuitReport(AnalysisPass):
    """Complete the report; count top-level operations, not nested definitions."""

    def run(self, dag):
        # Wire counts work, but both operation summaries are unfinished.
        self.property_set["circuit_report"] = {
            "num_qubits": dag.num_qubits(),
            "num_clbits": dag.num_clbits(),
            "operation_counts": {},
            "num_two_qubit_gates": 0,
        }
