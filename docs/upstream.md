# Moving from practice to an upstream contribution

Start with the [contribution workflow](contribution-workflow.md) and its
[historical case notebook](../notebooks/00-contribution-workflow.ipynb). The case
is already resolved and must not be submitted again. This page describes the
additional steps for a genuinely new, useful task.

This project teaches general contribution skills. Passing the lab does not mean a
learner is ready to submit compiler code. Source builds, repository conventions,
domain knowledge, and review are additional work.

1. Read the current [Qiskit contribution guide](https://github.com/Qiskit/qiskit/blob/main/CONTRIBUTING.md).
2. Inspect an issue, check for existing work, and discuss scope with its maintainers.
   An issue label is a starting point, not a guarantee of suitability or availability.
3. Follow that guide to create a separate Qiskit development environment. This lab
   uses a released wheel; it does not set up a Qiskit source build or Rust toolchain.
4. Reproduce the behavior and find the relevant existing tests before changing code.
5. Follow the project's checks, documentation, release-note, and review conventions.
6. Write your own explanation and be ready to discuss each design decision.

## AI assistance and human ownership

As checked on 1 November 2026, Qiskit's guide requires human-driven submissions and
communications, understanding of the submitted code, and disclosure of substantial
AI assistance. It also prohibits generative content for issues labelled
`good first issue`. Read the current policy before choosing a task, because policy
can change. The project should train independent reasoning and reduce review
burden; automatic PR volume is not a success metric.

This local lab scaffold was developed with AI assistance. Exercises are practice
material, not patches for submission to Qiskit. Do not submit the starter or
reference as a new upstream feature: operation selection already exists.

Primary source: [Qiskit's generative AI policy](https://github.com/Qiskit/qiskit/blob/main/CONTRIBUTING.md#use-of-generative-ai).
