"""Public Lab 02 contract, shared by notebook and terminal learners."""

from copy import deepcopy

import pytest
from qiskit import QuantumCircuit
from qiskit.circuit import Gate, Instruction, Parameter
from qiskit.converters import circuit_to_dag, dag_to_circuit
from qiskit.transpiler import AnalysisPass, PassManager


def test_empty_circuit_publishes_a_report_in_the_property_set(report_pass):
    analysis = report_pass()
    assert isinstance(analysis, AnalysisPass)
    manager = PassManager(analysis)
    manager.run(QuantumCircuit())
    assert manager.property_set["circuit_report"] == {
        "num_qubits": 0,
        "num_clbits": 0,
        "operation_counts": {},
        "num_two_qubit_gates": 0,
    }


def test_counts_operations_and_idle_wires_not_only_gates(report_pass):
    circuit = QuantumCircuit(3, 2)
    circuit.h(0)
    circuit.h(1)
    circuit.cx(0, 1)
    circuit.barrier(0, 1)
    circuit.measure(1, 0)
    circuit.reset(1)
    circuit.delay(10, 0)
    manager = PassManager(report_pass())
    manager.run(circuit)
    assert manager.property_set["circuit_report"] == {
        "num_qubits": 3,
        "num_clbits": 2,
        "operation_counts": {
            "h": 2,
            "cx": 1,
            "barrier": 1,
            "measure": 1,
            "reset": 1,
            "delay": 1,
        },
        "num_two_qubit_gates": 1,
    }


@pytest.mark.parametrize(
    ("operation", "expected"),
    [
        (Gate("custom_pair", 2, []), 1),
        (Gate("barrier", 2, []), 1),
        (Instruction("cx", 2, 0, []), 0),
        (Gate("custom_triple", 3, []), 0),
    ],
    ids=["custom-gate", "gate-with-misleading-name", "instruction-not-gate", "three-qubit-gate"],
)
def test_two_qubit_gate_count_uses_type_and_arity_not_names(report_pass, operation, expected):
    circuit = QuantumCircuit(3)
    circuit.append(operation, range(operation.num_qubits))
    manager = PassManager(report_pass())
    manager.run(circuit)
    report = manager.property_set["circuit_report"]
    assert report["num_two_qubit_gates"] == expected
    assert report["operation_counts"] == {operation.name: 1}


def test_repeated_gate_occurrences_are_counted_separately(report_pass):
    circuit = QuantumCircuit(2)
    circuit.cx(0, 1)
    circuit.cx(0, 1)
    circuit.cz(1, 0)
    circuit.swap(0, 1)
    manager = PassManager(report_pass())
    manager.run(circuit)
    assert manager.property_set["circuit_report"]["num_two_qubit_gates"] == 4
    assert manager.property_set["circuit_report"]["operation_counts"] == {
        "cx": 2,
        "cz": 1,
        "swap": 1,
    }


def test_control_flow_is_counted_at_top_level_not_as_executed_gates(report_pass):
    circuit = QuantumCircuit(2, 1)
    with circuit.if_test((circuit.clbits[0], True)):
        circuit.cx(0, 1)
        circuit.h(0)
    manager = PassManager(report_pass())
    manager.run(circuit)
    assert manager.property_set["circuit_report"] == {
        "num_qubits": 2,
        "num_clbits": 1,
        "operation_counts": {"if_else": 1},
        "num_two_qubit_gates": 0,
    }


def test_composite_gate_is_not_decomposed(report_pass):
    inner = QuantumCircuit(2, name="pair_block")
    inner.cx(0, 1)
    inner.cx(0, 1)
    circuit = QuantumCircuit(2)
    circuit.append(inner.to_gate(), [0, 1])
    manager = PassManager(report_pass())
    manager.run(circuit)
    assert manager.property_set["circuit_report"]["operation_counts"] == {"pair_block": 1}
    assert manager.property_set["circuit_report"]["num_two_qubit_gates"] == 1


def test_run_preserves_dag_structure_parameters_wires_and_metadata(report_pass):
    circuit = QuantumCircuit(3, 2, name="preserve_me", global_phase=Parameter("phase"))
    circuit.metadata = {"lesson": {"labels": ["original"]}}
    circuit.rx(Parameter("angle"), 1)
    circuit.cx(1, 2)
    circuit.barrier(1, 2)
    circuit.measure(2, 1)
    dag = circuit_to_dag(circuit)
    before = deepcopy(dag)
    analysis = report_pass()
    analysis.property_set["another_pass"] = {"keep": True}
    returned = analysis.run(dag)
    assert returned is None, "AnalysisPass.run should publish properties, not return a replacement."
    assert dag == before
    assert dag.name == before.name
    assert dag.metadata == before.metadata
    assert dag.global_phase == before.global_phase
    assert dag.qubits == before.qubits and dag.clbits == before.clbits
    assert dag_to_circuit(dag) == circuit
    assert analysis.property_set["another_pass"] == {"keep": True}


def test_pass_manager_output_preserves_the_circuit(report_pass):
    circuit = QuantumCircuit(2, 1, name="preserve_output", global_phase=0.25)
    circuit.metadata = {"purpose": "regression"}
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure(1, 0)
    before = deepcopy(circuit)
    output = PassManager(report_pass()).run(circuit)
    assert output == before and circuit == before
    assert output.name == before.name
    assert output.metadata == before.metadata
    assert output.global_phase == before.global_phase


def test_later_analysis_pass_can_consume_the_report(report_pass):
    class ReadReport(AnalysisPass):
        def run(self, dag):
            self.property_set["observed_pair_count"] = self.property_set["circuit_report"][
                "num_two_qubit_gates"
            ]

    circuit = QuantumCircuit(2)
    circuit.cx(0, 1)
    manager = PassManager([report_pass(), ReadReport()])
    manager.run(circuit)
    assert manager.property_set["observed_pair_count"] == 1


def test_reusing_pass_replaces_report_without_changing_previous_result(report_pass):
    circuit = QuantumCircuit(2)
    circuit.cx(0, 1)
    analysis = report_pass()
    analysis.run(circuit_to_dag(circuit))
    old = analysis.property_set["circuit_report"]
    analysis.run(circuit_to_dag(QuantumCircuit(1, 2)))
    assert analysis.property_set["circuit_report"] == {
        "num_qubits": 1,
        "num_clbits": 2,
        "operation_counts": {},
        "num_two_qubit_gates": 0,
    }
    assert old == {
        "num_qubits": 2,
        "num_clbits": 0,
        "operation_counts": {"cx": 1},
        "num_two_qubit_gates": 1,
    }


def test_reusing_manager_does_not_accumulate_counts(report_pass):
    circuit = QuantumCircuit(2)
    circuit.cx(0, 1)
    manager = PassManager(report_pass())
    manager.run(circuit)
    manager.run(QuantumCircuit(4))
    assert manager.property_set["circuit_report"] == {
        "num_qubits": 4,
        "num_clbits": 0,
        "operation_counts": {},
        "num_two_qubit_gates": 0,
    }
