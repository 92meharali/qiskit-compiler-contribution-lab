"""Commands for running and checking the contribution lab."""

import argparse
import os
import platform
import subprocess
import sys
from importlib.metadata import version
from pathlib import Path

from qclab.labs import LABS


def main():
    parser = argparse.ArgumentParser(prog="qclab", description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("doctor", help="Verify Python, Qiskit, and circuit/DAG conversion")
    commands.add_parser("demo", help="Inspect a real circuit and its operation nodes")
    check = commands.add_parser("check", help="Run a lab's acceptance tests")
    check.add_argument("--lab", choices=LABS, default="01", help="Lab number (default: 01)")
    target = check.add_mutually_exclusive_group()
    target.add_argument("--reference", action="store_true", help="Check the instructor solution")
    target.add_argument("--solution", type=Path, help="Path to your Python solution")
    args = parser.parse_args()
    if args.command == "doctor":
        from qiskit import QuantumCircuit
        from qiskit.converters import circuit_to_dag, dag_to_circuit

        circuit = QuantumCircuit(1)
        circuit.h(0)
        print(f"Python {platform.python_version()} ({platform.system()})")
        print(f"Qiskit {version('qiskit')}")
        print(f"pytest {version('pytest')}")
        if dag_to_circuit(circuit_to_dag(circuit)) != circuit:
            print("Circuit/DAG round trip: FAILED", file=sys.stderr)
            return 1
        print("Circuit/DAG round trip: OK")
        return 0
    if args.command == "demo":
        from qiskit import QuantumCircuit
        from qiskit.circuit import Measure, Reset
        from qiskit.converters import circuit_to_dag

        from qclab.reference import select_op_nodes

        circuit = QuantumCircuit(2, 2)
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.measure(1, 0)
        circuit.reset(1)
        circuit.measure(1, 1)
        dag = circuit_to_dag(circuit)
        try:
            "┌─┐╥┤".encode(sys.stdout.encoding or "utf-8")
        except UnicodeEncodeError:
            print("Circuit diagram requires UTF-8; showing the operation list below.")
        else:
            print(circuit.draw(output="text"))
        print(f"Operation nodes: {len(dag.op_nodes())}")
        for node in dag.op_nodes():
            qubits = [dag.find_bit(bit).index for bit in node.qargs]
            clbits = [dag.find_bit(bit).index for bit in node.cargs]
            print(f"  {node.name}: qubits={qubits}, clbits={clbits}")
        names = [node.name for node in select_op_nodes(dag, [Measure, Reset])]
        print("Selected: " + ", ".join(names))
        print("Demo uses the reference. Your exercise is checked by: qclab check")
        return 0
    export, filename = LABS[args.lab]
    suite = Path(__file__).parent / "checks" / filename
    command = [sys.executable, "-m", "pytest", str(suite), "-q", "--tb=short"]
    if not args.reference:
        solution = (args.solution or Path(f"exercises/lab{args.lab}.py")).resolve()
        if not solution.is_file():
            parser.error(
                f"Solution file not found: {solution}. Run from the project root or use --solution."
            )
        if solution.suffix != ".py":
            parser.error(f"The solution must be a .py file exporting {export}.")
        command.extend(["--solution", str(solution)])
        print(f"Checking Lab {args.lab}: {solution}", flush=True)
    else:
        print(f"Checking Lab {args.lab}: instructor reference", flush=True)
    env = os.environ.copy()
    env.pop("PYTEST_ADDOPTS", None)
    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    try:
        result = subprocess.run(command, env=env, timeout=30)
    except subprocess.TimeoutExpired:
        print("The checker timed out after 30 seconds. Look for an infinite loop.", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        return 130
    if result.returncode == 0:
        print("All acceptance checks passed. Next: write your own test and explain the change.")
    elif result.returncode == 1:
        print("Checks did not pass. Start with the first named failure in the output above.")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
