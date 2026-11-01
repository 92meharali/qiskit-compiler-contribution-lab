# Historical walkthrough case: QDrift identity evolution

Verified 1 November 2026. This is primary-source research for a **local, already-resolved practice case**, not a new upstream issue, contribution opportunity, or demonstration of learner outcomes. No issue, comment, or PR should be submitted for this historical fix.

## Selection and provenance

- [Issue #17113](https://github.com/Qiskit/qiskit/issues/17113), reported by `rishabhhP`, describes invalid arithmetic for zero coefficients and zero evolution time. It is closed and currently labeled `bug`.
- [PR #17117](https://github.com/Qiskit/qiskit/pull/17117), authored by `davidfcohen`, fixes the issue. It merged on 2 October 2026. Its observed labels are `bug`, `stable backport potential`, `Changelog: Fixed`, and `mod: synthesis`. Neither item was labeled `good first issue` when checked. Neither was authored by `92meharali`.
- Author attribution is historical provenance only. It does **not** indicate participation in, review of, or endorsement of this teaching project.
- The issue report discloses AI assistance; the PR author marks the submission as not LLM-generated. Preserve this distinction if discussing provenance; do not describe our walkthrough as independently discovering this bug.

The task is narrow enough for Python/basic-circuit learners **with a short explanation of evolution**: evolution under a zero operator, or for zero time, is the identity, so an empty rotation expansion is appropriate. This is a synthesis API case, not an exercise in implementing a transpiler pass and not a Rust bugfix.

## Exact snapshots

| Snapshot | Commit | Purpose |
| --- | --- | --- |
| Released Qiskit 2.5.2 | `c1c01ada399af13e495c27b9b22b4ff942bbad7e` | Verified failing released-wheel baseline |
| Parent immediately before fix | `f6924453021a254624d01a0bedc3b917c3d3ed0c` | Read-only inspection of the precise pre-fix source |
| Merged fix | `32c1f79e6133d3d0c8c65e9f8e7721038cd24152` | Exact historical change |
| Released Qiskit 2.6.0 | `65094a013073e4bda53c2b341056ab9ade0eb1bd` | Verified fixed released-wheel target; matches the teaching project's baseline |

The release tags are annotated tags; the commits above are the dereferenced commits, not the tag-object IDs. Evidence: [2.5.2 tag object](https://api.github.com/repos/Qiskit/qiskit/git/tags/1c3e6e3514e814a88a187872bbc8aa2c23bbdc8e), [2.6.0 tag object](https://api.github.com/repos/Qiskit/qiskit/git/tags/129637e5494957be48332eb922c397574f8f122b), and [fix commit](https://github.com/Qiskit/qiskit/commit/32c1f79e6133d3d0c8c65e9f8e7721038cd24152).

Do not conflate the 2.5.2 release with the immediate parent of the fix. Wheel comparison changes other code too; the historical diff identifies the relevant change. We have not built either historical source checkout or run Qiskit's complete test suite.

## Minimal behavior and local observations

The public call under investigation is:

```python
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp
from qiskit.synthesis import QDrift

gate = PauliEvolutionGate(SparsePauliOp("X", coeffs=[0]), time=1)
QDrift(seed=123).expand(gate)
```

This reproducer follows the public issue and uses installed released packages, not a copied or monkeypatched implementation. In isolated Python 3.12 environments, created with `uv run --isolated --no-project --python 3.12 --with qiskit==VERSION`, the following outcomes were observed. Warnings were captured using `warnings.catch_warnings(record=True)` and an `always` filter.

| Input `(coefficient, time)` | Qiskit 2.5.2 | Qiskit 2.6.0 |
| --- | --- | --- |
| `(0, 1)` | `ValueError: Probabilities contain NaN`; invalid-divide RuntimeWarning | `[]`, no warnings |
| `(1, 0)` | `[]`; divide-by-zero and invalid-multiply RuntimeWarnings | `[]`, no warnings |
| `(0, 0)` | Same error and warning category as `(0, 1)` | `[]`, no warnings |
| `(1, 1)` | Two `X` rotations on qubit 0, each angle 1.0; no warnings | Same expansion; no warnings |

The important regression lesson is that **checking only `result == []` misses the zero-time failure** on the old version. Include warning behavior in the local test. Numerical warning wording can vary with dependency versions; prefer category and behavior checks over exact strings. The single-term nonzero control cannot establish statistical correctness of randomized sampling in general.

The upstream patch added separate zero-time and zero-coefficient tests; the both-zero and nonzero checks above are additional local coverage, not claims about tests added by that PR. This research note establishes no learner outcome; no successful upstream source build is implied by a wheel-based run.

## Read-only source-navigation route

All links in this section are pinned to fixed commits.

1. **Before the fix:** [QDrift expansion in 2.5.2, lines 98–134](https://github.com/Qiskit/qiskit/blob/c1c01ada399af13e495c27b9b22b4ff942bbad7e/qiskit/synthesis/evolution/qdrift.py#L98-L134). `weights / lambd` at line 123 is invalid for all-zero coefficients; rescaling by `num_gates` at line 126 is invalid at zero time.
2. **After the fix:** [QDrift expansion in 2.6.0, lines 98–138](https://github.com/Qiskit/qiskit/blob/65094a013073e4bda53c2b341056ab9ade0eb1bd/qiskit/synthesis/evolution/qdrift.py#L98-L138). Lines 118–120 return early for zero total absolute weight or zero time, before either division.
3. **Relevant tests:** [test/python/circuit/library/test_evolution_gate.py, lines 293–301](https://github.com/Qiskit/qiskit/blob/65094a013073e4bda53c2b341056ab9ade0eb1bd/test/python/circuit/library/test_evolution_gate.py#L293-L301). Nearby existing tests provide broader context; these two tests should not be presented as exhaustive.
4. **Python/Rust boundary:** [ProductFormula.synthesize, lines 129–151](https://github.com/Qiskit/qiskit/blob/65094a013073e4bda53c2b341056ab9ade0eb1bd/qiskit/synthesis/evolution/product_formula.py#L129-L151) first calls `self.expand` in Python. In its default path it then calls `pauli_evolution`, imported from `qiskit._accelerate.circuit_library` at [line 29](https://github.com/Qiskit/qiskit/blob/65094a013073e4bda53c2b341056ab9ade0eb1bd/qiskit/synthesis/evolution/product_formula.py#L29).
5. **Rust binding:** [crates/circuit_library/src/pauli_evolution.rs, lines 53–60](https://github.com/Qiskit/qiskit/blob/65094a013073e4bda53c2b341056ab9ade0eb1bd/crates/circuit_library/src/pauli_evolution.rs#L53-L60) exposes `py_pauli_evolution` with Python name `pauli_evolution`; [lib.rs, line 30](https://github.com/Qiskit/qiskit/blob/65094a013073e4bda53c2b341056ab9ade0eb1bd/crates/circuit_library/src/lib.rs#L30) registers it.

The learner should identify which layer owns the invalid arithmetic and why modifying Rust would not address this particular failure. This teaches navigation of a mixed-language project, **not Rust development proficiency**. Calling `expand` alone does not exercise the later Rust synthesis call; label any optional `synthesize` integration experiment separately.

## Contribution workflow comes before the case

As of this investigation, current `main` resolved to `0f2d7ddfd262b1fa3afbc27f733e5c9f6cc6426d`. Its [CONTRIBUTING.md](https://github.com/Qiskit/qiskit/blob/0f2d7ddfd262b1fa3afbc27f733e5c9f6cc6426d/CONTRIBUTING.md) identifies Qiskit as mixed Rust/Python, directs contributors to the code of conduct and CLA, explains source builds and tests, and prefers issue discussion before a PR. A wheel environment is adequate for this reproduction but does not prove the learner can build or change Qiskit from source.

The linked [AI policy, lines 289–350](https://github.com/Qiskit/qiskit/blob/0f2d7ddfd262b1fa3afbc27f733e5c9f6cc6426d/docs/devguide/contributing.md#L289-L350) requires human-driven submissions and communications, understanding of submitted work, disclosure of generative tooling, and forbids generative content on `good first issue` items. Learner explanation prompts should elicit the learner's own reasoning, not provide AI-authored text to paste into an upstream PR. Read the [live contribution guide](https://github.com/Qiskit/qiskit/blob/main/CONTRIBUTING.md) again before any genuinely new contribution; a historical snapshot is not a substitute for current policy.

## Attribution and implementation limits

Link to original implementation and tests instead of vendoring them. If the implementation later copies or adapts Qiskit source, preserve the relevant copyright/attribution notices, provide its Apache-2.0 license, and mark changes, following [LICENSE.txt section 4](https://github.com/Qiskit/qiskit/blob/65094a013073e4bda53c2b341056ab9ade0eb1bd/LICENSE.txt) and the source-file header. Do not silently relicense upstream code under this project's license. The pinned release tree inspected here did not contain a `NOTICE` file; recheck notices for any different artifact redistributed.

This note is AI-assisted research and records executed package observations plus linked source evidence. It does not assert independent peer review, suitability for every beginner, general QDrift correctness, accessibility validation, a new contribution, or endorsement by Qiskit or any named contributor.
