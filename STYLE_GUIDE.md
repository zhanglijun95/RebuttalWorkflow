# Rebuttal Style Guide

This guide captures the writing standard learned from an actual ICML rebuttal iteration with heavy human refinement.

## Tone

- formal
- professional
- academic
- direct
- collaborative, but not chatty

## What Good Rebuttal Writing Looks Like

- answer the reviewer's actual concern, not a nearby concern
- make the first sentence of each answer do real work
- keep the structure visible
- make paragraph logic easy to follow
- sound like an author defending a paper, not an assistant summarizing notes

## Preferred Reviewer Format

Use:

- `**W1:** ...`
- `**A1:** ...`
- `**Q1:** ...`
- `**A2:** ...`

If several reviewer points are the same underlying concern, merge them explicitly and then answer with subparts such as:

- `**A2:** ...`
- `**A2-1:** ...`
- `**A2-2:** ...`

## Paragraph Logic

Default pattern:

1. topic sentence that directly answers the point
2. concrete explanation
3. grounded evidence or numbers
4. implication for how the paper should be read

Useful moves:

- clarify first if the reviewer misunderstood something
- agree first if the reviewer is right
- use total-then-detail structure
- keep transitions explicit

## Language Rules

Prefer:

- short, clear topic sentences
- precise nouns and verbs
- concise transitions such as `Therefore`, `However`, `Instead`, `In this setting`

Avoid:

- robotic list-like prose
- colon-heavy writing
- filler openings such as `This is a helpful question`
- vague phrases such as `the right way to frame it`
- unexplained abstractions
- overclaiming beyond the actual evidence

## Human-In-The-Loop Rule

If the user manually rewrites a sentence or paragraph:

- treat that wording as preferred
- learn why it was improved
- preserve it unless the user explicitly asks to change it

Do not:

- rewrite user-fixed text back into your own default style
- reintroduce phrases the user has already rejected

## Compression Rule

Only compress after the logic is finalized.

Allowed compression targets:

- repeated background
- repeated conclusions
- filler politeness
- redundant transitions
- longer-than-needed formulations of the same point

Do not compress by:

- deleting a step in the logic
- weakening explicit answers to reviewer concerns
- removing necessary evidence
- changing the stance or implication

## Reviewer-Specific Guidance

- positive reviewers can receive a slightly warmer opener, but the body should remain technical
- low-score reviewers need especially clean logic and full coverage
- if multiple reviewers share a concern, answer it consistently across files
- cross-reference another reviewer only after the current reviewer's question is already clear on its own
