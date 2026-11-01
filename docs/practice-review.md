# Practice review

Copy this template into your own notes. Write the answers yourself and have another
person read them. This is not an upstream PR submission.

1. **User problem and status:** Who needs the behavior? Is it currently unresolved,
   or are you replaying a historical fix? Record issue/PR and exact revisions.
2. **Small reproducer:** What is the smallest circuit and input that shows it?
3. **Observed and expected output:** What exactly differs?
4. **Change:** What did you change, and why does it address the cause?
5. **Compatibility:** What existing behavior must continue to work?
6. **Evidence:** Which tests failed before and pass now? Add your own regression test.
7. **Limits:** What does this implementation not cover?
8. **Tools:** What help did you use? What can you explain unaided?
9. **Source map:** Which public API, implementation, and test files are involved?
   Which parts are Python or Rust? Where is the boundary for this case?
10. **Workflow and limits:** Which official contribution-policy revision did you
    consult? Did you run wheels, build a source checkout, or test an actual edit?
    Which checks were not run, and what preparation remains before real work?

Reviewer: identify one strength, one missing case or unclear claim, and one question
about the reasoning. Evaluate understanding and usefulness, not code volume.
