# Facilitating the two-lab prototype

This protocol remains specific to optional foundation Labs 01–02. For the new
contribution-first walkthrough, use the separate
[one-learner protocol](contribution-walkthrough-pilot.md). Do not transfer earlier
foundation outcomes to the new activity.

This is a reusable observation protocol, not a report of completed sessions.
Keep participant-level records private; the public repository contains only
blank templates and teaching source. For a short technical review instead, use
the [reviewer guide](reviewer-guide.md).

## Prepare

- Choose learners who know Python functions/classes and basic quantum circuits.
  Record previous Qiskit experience and exposure to the solutions.
- Freeze a commit/version; verify setup and both reference commands using
  [the verification instructions](verification.md).
- Ask permission for note-taking. Ask separately for recording, quotation, or
  sharing work/screenshots; a learner may decline or stop without penalty.
- Copy the [blank feedback record](feedback-template.md) into a private location.
  Do not commit completed records. Keep contact details and identity mappings
  separate, agree a retention/deletion date, and avoid unrelated screen content.
- Explain: we are testing the material, not judging the learner. Negative feedback
  is useful. Learners may use help; record that help rather than hiding it.

## Suggested session structure

Allow 20-30 minutes for setup and two 75-minute sessions, preferably on separate
days. These are planning windows, not demonstrated completion-time claims.
Separate active troubleshooting from network/download waiting.

For each lab: use five minutes for context, ten for reading/predictions, forty
for the exercise and checks, ten for a fresh explanation and a clean-kernel run,
and ten for feedback. Record the result at the exercise limit; optional extra
time and its outcome belong in separate fields. Lab 02 follows Lab 01; mark any
bridge explanation as assistance. Preserve non-attempts and unfinished work.

For group sessions, observe individual work where possible and label self-reports
separately. Do not claim continuous observation or independently verified work
where it was not observed. Record any adaptations to timing or facilitation.

## Help and outcomes

Use these help labels: **D** documentation; **H** notebook hint; **F** facilitator;
**R** instructor reference; **A** AI/another person. Record what happened and when.
Independent completion permits the main lesson and documentation, but no H/F/R/A
help during the exercise. Assistance is acceptable; it changes the outcome label.

Record these separately:

1. All visible checks pass: 28 for Lab 01, 14 for Lab 02.
2. The learner's own regression fails for an intentional mistake and passes
   after repair; a copied regression is not independent test design.
3. A fresh example is explained, not merely executed or recalled from the lesson.
4. Restart Kernel -> Run All completes, including the learner's regression.

The unfinished starter may run cleanly while correctly reporting `NOT YET`.
A passing checker alone does not establish a clean notebook run or understanding.

## Fresh explanation prompts

- Lab 01: why can consuming a generator repeatedly miss matching nodes?
- Lab 01: why can exact type equality miss a custom gate subclass? Show a test.
- Lab 02: why is a two-wire barrier different from a two-qubit gate?
- Lab 02: what does a top-level control-flow count tell us, and what does it omit?
- Lab 02: why allocate a fresh report and pass instance? How do you test both
  report independence and preservation of the input circuit?

Use examples different from the lesson. Score 0 for a remaining misconception,
1 for a prompted/incomplete explanation, and 2 for an independent explanation
applied to the example. Use N/A when not attempted. Keep the observation and any
prompt alongside the score. This is not a validated educational instrument.

## Feedback and reporting

Ask for the most confusing cell, the first interpretation, whether `NOT YET` was
understood, a useful/unhelpful failure message, and the first change they would
make. Ask what remains before real compiler work. Do not solicit praise.

Summarize counts with denominators, per lab and version: attempts, in-window and
eventual passes, assistance, explanations, regressions, clean runs, and setup
problems. Include withdrawals and missing observations. Distinguish fresh learners
from returning learners; do not treat different cohorts as matched pairs.

Fix setup blockers and recurring misconceptions, then retest a named version.
Before sharing any aggregate, review consent and identification risk. A small
convenience sample does not establish causal learning gains, readiness to submit
upstream patches, or maintainer endorsement.
