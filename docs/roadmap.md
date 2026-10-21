# Curriculum: from circuit reader to compiler contributor

**Scope decision, 22 October 2026:** a general pathway through Qiskit compiler
development. No lesson requires familiarity with the author's pull requests.
Past contributions are optional examples. The current implementation delivers
Labs 01 and 02; Labs 03-06 below are planned, not completed or validated.

The course assumes Python and basic circuit literacy. The first release uses
Qiskit to make the learning concrete. Concepts such as intermediate
representations, compiler passes, invariants, regression tests, and review transfer
to other systems; multi-framework support is a possible later extension.

| Lab | Learner outcome | Practical artifact | Status |
|---|---|---|---|
| 01: Read and query a circuit DAG | Separate wires, operation nodes, selection, and traversal order | A tested operation-selection helper | Implemented; see software verification and limitations |
| 02: Analyze without changing | Write an `AnalysisPass`, report useful circuit properties, and preserve the circuit | A top-level operation inventory consumed through a pass manager | Implemented; see software verification and limitations |
| 03: Transform with explicit preconditions | Write a narrow `TransformationPass`, preserve wires and metadata, avoid invalid rewrites | A conservative circuit rewrite on a stated subset | Planned |
| 04: Test correctness and its limits | Check unitary equivalence, account for global phase, and state the limits of matrix simulation | Positive and negative correctness tests on small circuits | Planned |
| 05: Reproduce and fix a regression | Minimize a failing circuit, specify behavior, protect compatibility, and avoid misleading benchmarks | A regression test and repair in a practice repository | Planned |
| 06: Prepare a contribution for review | Navigate source, build locally, read project policy, explain a patch, and respond to feedback | A human-written practice review plus an optional maintainer-approved real issue | Planned |

Each lab should use a learner `.ipynb` and a separate instructor `.ipynb`, including
a runnable starter, a visible behavior contract, progressive hints, shared automated
checks, and an explanation task. Run notebooks in a clean kernel in CI to detect
hidden execution-order dependencies. Keep reusable checker logic in Python modules.
Fixtures should include realistic edge cases, not just an attractive demo.

Labs 01 and 02 form the current software prototype. Pilot Lab 01 first, then offer
Lab 02 as a follow-on once learners can explain the first exercise. Before further
curriculum expansion, validate setup, independent problem-solving, and learners'
ability to explain the boundaries without the reference.

## Questions for external review

- Does this bridge a gap beyond Qiskit's existing tutorials and contribution guide?
- Is compiler contribution the right starting point for intermediate Python users?
- Which lab outcomes do maintainers think would reduce their review burden?
- Can learners install the pinned environment on their own laptops?
- What learning benefit remains when the reference is openly available?

These remain research questions, not established benefits. The
[reviewer guide](reviewer-guide.md) asks for specific feedback on accuracy and
the contribution pathway. No maintainer endorsement or causal learning gain is
claimed. Software checks and their limits are recorded in
[verification.md](verification.md); human-session records are not public here.

The next proposed milestone is four labs in total and a bounded guided
first-contribution handoff using the existing upstream and practice-review
guides. It does not promise the full Labs 05-06 above. Local practice artifacts
and actual upstream contribution stages should be reported separately; helping
first-time contributors remains the pathway's purpose.
