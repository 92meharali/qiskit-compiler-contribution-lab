# Lab 01: Find the operations you actually need

Prefer an interactive experience? Start with the
[Jupyter notebook](../notebooks/01-circuit-dag.ipynb). This document is the optional
terminal-based version of the same exercise.

**Audience:** comfortable with Python functions, classes, iterables, and basic tests.
No quantum hardware, cloud account, Rust compiler, or advanced physics is needed.
**Material version:** pilot-revision-1-2026-10-22; fresh-learner retest pending.
**Pilot timing:** a 75-minute session plus setup; record the exercise state at
40 minutes. This is a session budget, not a promised completion time.
**Outcome:** extend an API while preserving its existing behavior, use a regression
test to catch an iterator bug, and explain the reasoning to a reviewer.

This is a general compiler inspection exercise. Imagine a compiler diagnostic
that needs to find measurement and reset operations together. You will build its
selection helper and make it behave predictably for different callers. This
exercise does not modify your installed Qiskit package. Qiskit already provides
operation selection; reimplementing a small helper lets us practice specification,
testing, and review before working inside a larger codebase.

## 1. See the circuit (5 minutes)

From the project root, run:

```sh
uv sync --locked
uv run qclab doctor
uv run qclab demo
```

A circuit is a sequence of instructions on wires. A `DAGCircuit` represents the
dependencies between those instructions as a directed acyclic graph. It includes
input and output nodes as well as operation nodes. `dag.op_nodes()` returns only
the operation nodes. We use that existing interface to focus on one API change.

In the demo, `h` and `cx` are gates; `reset` and `measure` are instructions we want
to find together. Selecting only gates would omit the operations we need.
Several nodes may contain the same operation type: selecting a type should retain
every matching node, not just one representative.

Before coding, predict which operations a filter for `[Measure, Reset]` should return.
List the measurement's classical bit as well as its qubit. Inspect the printed
node data to check your prediction.

## 2. Reproduce the missing behavior (5 minutes)

```sh
uv run qclab check
```

Some tests pass and others fail. This is intentional: the starter can select one
class, but the user needs several classes in one call. Read the first failure.
The default target is `exercises/lab01.py`; your work belongs in that file.

The public function is:

```python
select_op_nodes(dag, operation_types=None)
```

Its contract is:

| Input | Expected behavior |
|---|---|
| `None` | All operation nodes |
| `Measure` | All measurement nodes |
| `[Measure, Reset]` or `(Measure, Reset)` | Both kinds, each node once |
| `{Measure, Reset}` | Same selection; filter order does not reorder nodes |
| A generator yielding those classes | Same selection on every node |
| An empty iterable | An empty list |
| A Python superclass such as `Instruction` | Match subclasses via `isinstance` |
| A non-iterable such as `42` | Raise `TypeError` |
| Any iterable containing a non-class | Raise `TypeError`, even if the DAG is empty |

Return the original DAG operation nodes in a list, in the relative order returned
by `dag.op_nodes()`. Do not mutate the DAG or return input/output nodes. This lab
does **not** assume that `op_nodes()` is a topological traversal. When scheduling
requires dependency order, investigate `topological_op_nodes()` separately.

## 3. Make the smallest change (15 minutes)

Before coding, read the notebook's worked examples on generator exhaustion and
validation. Reading a generator once consumes it; materialize it once per call
so each node sees the same types. Validate every entry before traversing nodes.
An empty filter on an empty DAG returns `[]`; `[Measure, "reset"]` on that same
DAG must raise `TypeError`. No matches does not mean the request was valid.

Start with a list of two types. Run just that acceptance test while working:

```sh
uv run python -m pytest src/qclab/checks/test_selection.py \
  --solution exercises/lab01.py -k list_of_types -q
```

Then rerun the full checker. Make one behavior pass at a time. Keep the single-type
case working. The checker is intentionally transparent: read its tests to
understand the contract. Don't change them to accommodate your implementation.

<details>
<summary>Hint 1: normalize once</summary>

Treat a single class as a one-element tuple. Materialize an iterable into a tuple
once, before traversing the nodes. `None` is a separate case; it is not an empty
selection.
</details>

<details>
<summary>Hint 2: generators are stateful</summary>

`any(isinstance(node.op, cls) for cls in operation_types)` looks plausible, but if
`operation_types` is a generator, the first node consumes some or all of it.
Later nodes see a different filter. Materializing once makes the selection stable.
</details>

<details>
<summary>Hint 3: matching and validation are different</summary>

`isinstance(value, tuple_of_classes)` supports subclasses. But it may short-circuit
after a matching class, never encountering an invalid later entry. Validate every
entry first, even when the DAG has no operations. Avoid testing exact class
identity: Qiskit's singleton gates may be instances of subclasses.
</details>

## 4. Write your own regression test (10 minutes)

Create a local test with at least two measurements and a reset. Pass a generator
of classes. Explain why an implementation that consumes the generator inside the
node loop would fail. Use literal expected operation names or known nodes, not a
copy of your selection algorithm as the expected value.

Run your test with `uv run python -m pytest path/to/your_test.py`. Passing the
provided checker is necessary; this new test and your explanation demonstrate
that you can reason about a failure independently.

## 5. Explain the contribution (10 minutes)

Fill in [the practice review template](../docs/practice-review.md) in your own words:
the user problem, a minimal failing example, your change, compatibility, tests,
and one limitation. Have another person review it.

Questions you should be able to answer without the reference:

1. Why can a generator work on the first node and fail on the next?
2. Why should `[Measure, "reset"]` fail even when a measurement matches first?
3. Why is matching `type(node.op) == GateType` too restrictive?
4. Why should `[Measure, Measure]` return each measurement node only once?
5. What does this exercise leave out of a real Qiskit contribution?

After your attempt, compare with `src/qclab/reference.py` and run
`uv run qclab check --reference`. This is an open-book practice lab, not a secure
exam; the reference is deliberately available.

## 6. Connect the exercise to upstream work

Read Qiskit's current
[contribution guide](https://github.com/Qiskit/qiskit/blob/main/CONTRIBUTING.md).
Find the implementation of `DAGCircuit.op_nodes` and its tests. Identify where
the Python-facing API crosses into Rust. Choose an already merged change touching
this area and observe how tests, documentation, and review fit together. See
[optional case studies](../docs/case-studies.md) for starting points.

Real upstream work adds source builds, repository-specific checks, review, and
maintainer agreement. Follow the [upstream transition guide](../docs/upstream.md)
before selecting a real issue. The six-lab roadmap is in
[docs/roadmap.md](../docs/roadmap.md).

Primary references:

- [IBM DAGCircuit API](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.dagcircuit.DAGCircuit)
- [IBM circuit-to-DAG conversion](https://quantum.cloud.ibm.com/docs/en/api/qiskit/converters)
- [Python isinstance](https://docs.python.org/3/library/functions.html#isinstance)
