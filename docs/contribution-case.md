# Case 00: a historical QDrift regression

**Scope:** reproduce a resolved bug, navigate a mixed-language repository, and
prepare a practice review. This is not a new upstream issue, a transpiler-pass
implementation, or a Rust programming exercise. No message or PR is requested.

Start with the [learner notebook](../notebooks/00-contribution-workflow.ipynb).
Read the [workflow guide](contribution-workflow.md) and Qiskit's current contribution
rules before the case. Instructor answers are in the separate
[instructor notebook](../notebooks/instructor/00-contribution-workflow-guide.ipynb).

## Predict before viewing the repair

For time evolution `exp(-i t H)`, zero H or zero t means identity. The public
`QDrift.expand` API should return no sampled rotations for these cases, without
invalid numerical operations. An empty expansion does not mean zero circuit width.
The historical zero-time case returned `[]` even while emitting numerical warnings:
checking the result alone would miss the problem.

```python
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp
from qiskit.synthesis import QDrift

evolution = PauliEvolutionGate(SparsePauliOp("Z", coeffs=[0.0]), time=2.0)
print(QDrift(seed=7).expand(evolution))
```

This is an original local teaching example of the public behavior reported in
[issue #17113](https://github.com/Qiskit/qiskit/issues/17113) by `rishabhhP` and
repaired in [PR #17117](https://github.com/Qiskit/qiskit/pull/17117) by `davidfcohen`.
Naming the original authors is attribution, not an endorsement or a claim that
they helped build this lesson. Do not copy the upstream repair into a new PR.

## Run the historical comparison

Run from the QCLAB repository root. These commands use separate uv-managed
environments, not the teaching `.venv`; Python/package downloads need internet.
They install released wheels, not source checkouts. Do not downgrade the project's
locked dependencies. Exact direct versions are pinned; transitive dependencies
in these comparison environments are resolved by uv and are not a full lockfile.

```sh
# Expected RED: two identity-case tests fail due to invalid arithmetic.
uv run --no-project --python 3.12 --with qiskit==2.5.2 --with pytest==9.1.1 python -m pytest tests/test_contribution_case.py -q

# Expected GREEN: both tests pass on the fixed release.
uv run --no-project --python 3.12 --with qiskit==2.6.0 --with pytest==9.1.1 python -m pytest tests/test_contribution_case.py -q

# The ordinary locked project also uses the fixed release.
uv run --locked python -m pytest tests/test_contribution_case.py -q
```

The local tests make NumPy's divide/invalid operations raise `FloatingPointError`
using `np.errstate`. Without that setting the zero-operator case produces a warning
and `ValueError`, while zero time can return `[]` with warnings. Do not confuse
those different presentations of the same numerical defect. Installation/network
failures, missing files, and import errors do not count as reproducing this bug.

Record the two failing steps separately: zero operator weight fails at
`weights / lambd` (invalid normalization), while zero time with nonzero weight
fails at `2 * lambd / num_gates * time` (division by zero during rescaling).
Do not summarize both as failures at the rescaling line.

After predicting your own regression, inspect the bundled tests. If writing an
original test, save it in a separate local file, replace the test-file argument
in both commands with that path, and record help/reference exposure. Include a
nonzero control so an always-empty implementation would not satisfy your claim.
The instructor demonstrates a deterministic single-term control; neither it nor
these two regressions proves general randomized synthesis correctness.

## Source navigation

Use these pinned files to avoid silently studying a moving version:

| Layer | File / snapshot | What to find |
|---|---|---|
| Old Python implementation | [qdrift.py, Qiskit 2.5.2](https://github.com/Qiskit/qiskit/blob/c1c01ada399af13e495c27b9b22b4ff942bbad7e/qiskit/synthesis/evolution/qdrift.py#L98-L134) | Normalization and time rescaling that can divide by zero |
| Fixed Python implementation | [qdrift.py, Qiskit 2.6.0](https://github.com/Qiskit/qiskit/blob/65094a013073e4bda53c2b341056ab9ade0eb1bd/qiskit/synthesis/evolution/qdrift.py#L98-L138) | Handling the identity cases before either division |
| Upstream tests | [test_evolution_gate.py](https://github.com/Qiskit/qiskit/blob/65094a013073e4bda53c2b341056ab9ade0eb1bd/test/python/circuit/library/test_evolution_gate.py#L293-L301) | Separate zero-time and zero-operator tests; inspect neighboring coverage too |
| Later Python-to-Rust call | [product_formula.py](https://github.com/Qiskit/qiskit/blob/65094a013073e4bda53c2b341056ab9ade0eb1bd/qiskit/synthesis/evolution/product_formula.py#L129-L151) | `synthesize` first calls `expand`, then uses `pauli_evolution` in its default path |
| Rust binding | [pauli_evolution.rs](https://github.com/Qiskit/qiskit/blob/65094a013073e4bda53c2b341056ab9ade0eb1bd/crates/circuit_library/src/pauli_evolution.rs#L53-L60) | `py_pauli_evolution` exported as `pauli_evolution` |

Explain why the repair is in Python and why `expand` alone does not execute the
later Rust synthesis call. Trace the binding without claiming Rust proficiency.
The two releases contain other changes too: examine the
[exact repair diff](https://github.com/Qiskit/qiskit/commit/32c1f79e6133d3d0c8c65e9f8e7721038cd24152)
to isolate what this fix changed. The immediate parent is
`f6924453021a254624d01a0bedc3b917c3d3ed0c`, not the 2.5.2 release commit.

## From this packet to future work

Complete the [practice review](practice-review.md) and obtain a human explanation
check. Do not present replaying this repair as a new Qiskit contribution. A real
task needs current scope discussion, a separate source-development environment,
relevant upstream checks, and human ownership. Follow the current official build
instructions, not a historical installation recipe from this notebook.

Verified here: released-wheel behavior and notebook execution. Not verified:
building the historical source revisions, running Qiskit's full test suite,
learner understanding, Rust-editing readiness, or maintainer acceptance. See the
[case evidence](walkthrough-case-research.md) for provenance and policy checks.
