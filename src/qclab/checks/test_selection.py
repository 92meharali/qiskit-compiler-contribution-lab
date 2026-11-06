"""The learner-visible behavior contract. These tests run on real Qiskit DAGs."""

import pytest
from qiskit import QuantumCircuit
from qiskit.circuit import Barrier, Gate, Instruction, Measure, Reset
from qiskit.circuit.library import HGate
from qiskit.converters import circuit_to_dag, dag_to_circuit


def test_single_type_selects_only_measurements(select_nodes):
    circuit = QuantumCircuit(1, 1)
    circuit.h(0)
    circuit.measure(0, 0)
    nodes = select_nodes(circuit_to_dag(circuit), Measure)
    assert [node.name for node in nodes] == ["measure"]


def test_list_of_types_selects_measure_and_reset(select_nodes):
    circuit = QuantumCircuit(1, 1)
    circuit.h(0)
    circuit.reset(0)
    circuit.measure(0, 0)
    nodes = select_nodes(circuit_to_dag(circuit), [Measure, Reset])
    assert [node.name for node in nodes] == ["reset", "measure"]


def test_none_returns_all_operation_nodes(select_nodes):
    circuit = QuantumCircuit(1, 1)
    circuit.h(0)
    circuit.measure(0, 0)
    dag = circuit_to_dag(circuit)
    assert select_nodes(dag) == list(dag.op_nodes())


def test_invalid_later_type_is_rejected_even_after_a_match(select_nodes):
    circuit = QuantumCircuit(1, 1)
    circuit.measure(0, 0)
    with pytest.raises(TypeError):
        select_nodes(circuit_to_dag(circuit), [Measure, "reset"])


@pytest.mark.parametrize("container", [tuple, set, iter], ids=["tuple", "set", "iterator"])
def test_iterable_filter_matches_multiple_nodes(select_nodes, container):
    circuit = QuantumCircuit(1, 1)
    circuit.h(0)
    circuit.measure(0, 0)
    circuit.reset(0)
    circuit.measure(0, 0)
    nodes = select_nodes(circuit_to_dag(circuit), container([Measure, Reset]))
    assert [node.name for node in nodes] == ["measure", "reset", "measure"]


def test_generator_is_not_consumed_again_for_each_node(select_nodes):
    circuit = QuantumCircuit(1, 1)
    circuit.h(0)  # A non-match can consume the entire filter in a broken implementation.
    circuit.measure(0, 0)
    circuit.reset(0)
    circuit.measure(0, 0)
    types = (cls for cls in [Measure, Reset])
    nodes = select_nodes(circuit_to_dag(circuit), types)
    assert [node.name for node in nodes] == ["measure", "reset", "measure"]


@pytest.mark.parametrize("types", [[], (), set()])
def test_empty_filter_selects_nothing(select_nodes, types):
    circuit = QuantumCircuit(1)
    circuit.h(0)
    assert select_nodes(circuit_to_dag(circuit), types) == []


def test_empty_generator_selects_nothing(select_nodes):
    circuit = QuantumCircuit(1)
    circuit.h(0)
    assert select_nodes(circuit_to_dag(circuit), (cls for cls in [])) == []


def test_repeated_types_do_not_duplicate_nodes(select_nodes):
    circuit = QuantumCircuit(1, 1)
    circuit.measure(0, 0)
    circuit.reset(0)
    circuit.measure(0, 0)
    nodes = select_nodes(circuit_to_dag(circuit), [Measure, Measure, Reset])
    assert [node.name for node in nodes] == ["measure", "reset", "measure"]


def test_superclass_matches_custom_gate_and_standard_gates(select_nodes):
    circuit = QuantumCircuit(1, 1)
    circuit.h(0)
    circuit.append(Gate("custom", 1, []), [0])
    circuit.measure(0, 0)
    nodes = select_nodes(circuit_to_dag(circuit), Gate)
    assert [node.name for node in nodes] == ["h", "custom"]


def test_singleton_gate_matches_its_public_class(select_nodes):
    circuit = QuantumCircuit(1)
    circuit.h(0)
    nodes = select_nodes(circuit_to_dag(circuit), HGate)
    assert [node.name for node in nodes] == ["h"]


def test_custom_instruction_subclass_is_included(select_nodes):
    class TaggedInstruction(Instruction):
        def __init__(self):
            super().__init__("tagged", 1, 0, [])

    circuit = QuantumCircuit(1)
    circuit.append(TaggedInstruction(), [0])
    nodes = select_nodes(circuit_to_dag(circuit), Instruction)
    assert [node.name for node in nodes] == ["tagged"]


@pytest.mark.parametrize("types", [None, Measure, [Measure, Reset]])
def test_empty_dag_returns_empty_list(select_nodes, types):
    assert select_nodes(circuit_to_dag(QuantumCircuit(1)), types) == []


@pytest.mark.parametrize("invalid", [42, "measure", [Measure()], [Measure, "reset"]])
def test_invalid_filter_is_rejected_on_empty_dag(select_nodes, invalid):
    with pytest.raises(TypeError):
        select_nodes(circuit_to_dag(QuantumCircuit(1)), invalid)


def test_filter_order_does_not_reorder_dag_nodes(select_nodes):
    circuit = QuantumCircuit(1, 1)
    circuit.measure(0, 0)
    circuit.reset(0)
    circuit.measure(0, 0)
    nodes = select_nodes(circuit_to_dag(circuit), [Reset, Measure])
    assert [node.name for node in nodes] == ["measure", "reset", "measure"]


def test_query_preserves_original_nodes_wires_and_circuit(select_nodes):
    circuit = QuantumCircuit(2, 2, name="inspection")
    circuit.global_phase = 0.25
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure(1, 0)
    circuit.reset(1)
    dag = circuit_to_dag(circuit)
    expected = [dag.named_nodes("measure")[0], dag.named_nodes("reset")[0]]
    before = dag_to_circuit(dag)
    nodes = select_nodes(dag, [Measure, Reset])
    assert isinstance(nodes, list)
    assert nodes == expected
    assert nodes[0].qargs == (dag.qubits[1],)
    assert nodes[0].cargs == (dag.clbits[0],)
    assert dag_to_circuit(dag) == before


def test_no_matching_type_returns_empty_list(select_nodes):
    circuit = QuantumCircuit(1)
    circuit.h(0)
    assert select_nodes(circuit_to_dag(circuit), Measure) == []


def test_directives_are_selected_like_other_operations(select_nodes):
    circuit = QuantumCircuit(1)
    circuit.h(0)
    circuit.barrier(0)
    dag = circuit_to_dag(circuit)
    assert [node.name for node in select_nodes(dag, Barrier)] == ["barrier"]
    assert [node.name for node in select_nodes(dag, Instruction)] == ["h", "barrier"]


def test_order_follows_op_nodes_across_independent_wires(select_nodes):
    circuit = QuantumCircuit(2)
    circuit.h(1)
    circuit.h(0)
    dag = circuit_to_dag(circuit)
    assert select_nodes(dag, HGate) == list(dag.op_nodes())
