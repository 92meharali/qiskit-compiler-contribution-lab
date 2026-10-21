"""Lab 02 instructor reference. Try the notebook before reading this file."""

from qiskit.circuit import Gate
from qiskit.transpiler import AnalysisPass


class CircuitReport(AnalysisPass):
    """Publish a top-level operation inventory without modifying the DAG."""

    def run(self, dag):
        counts = {}
        two_qubit_gates = 0
        for node in dag.op_nodes():
            counts[node.name] = counts.get(node.name, 0) + 1
            if isinstance(node.op, Gate) and len(node.qargs) == 2:
                two_qubit_gates += 1
        self.property_set["circuit_report"] = {
            "num_qubits": dag.num_qubits(),
            "num_clbits": dag.num_clbits(),
            "operation_counts": counts,
            "num_two_qubit_gates": two_qubit_gates,
        }
