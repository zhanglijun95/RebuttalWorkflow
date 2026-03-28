# Rebuttal Style Guide

This guide captures the writing standard learned from the first ICML rebuttal round after heavy human refinement.

## Core Objective

A good rebuttal is not a neutral summary of reviewer concerns. It is a clear, professional argument that does four things at once:

- answers the reviewer's actual concern directly
- shows why the concern does or does not change the paper's main value
- states the real limitation without melodrama or overclaim
- leaves the reviewer with a sharper understanding of what the paper does support

The target tone is formal, calm, persuasive, and easy to read.

## What Good Rebuttal Writing Looks Like

- each answer starts by addressing the exact concern, not a nearby concern
- each paragraph has one job and announces that job clearly
- the logic moves in a visible order: answer, explanation, evidence, supported claim
- the writing sounds like a senior author defending a paper, not like an assistant summarizing notes
- limitations are acknowledged precisely, but the answer still explains why the paper is meaningful

## Preferred Reviewer Format

Use visible reviewer structure:

- `**W1:** ...`
- `**A1:** ...`
- `**Q1:** ...`
- `**A2:** ...`

If several points are one underlying concern, merge them explicitly and answer with subparts only when the subparts are genuinely distinct:

- `**W2 / Q3:** ...`
- `**A2:** ...`
- `**A2-1:** ...`
- `**A2-2:** ...`

Do not remove the visible `W/Q/A` structure once drafting has started unless the user explicitly asks for a different format.

## How To Paraphrase Reviewer Points

Reviewer-point summaries must be neutral and compact.

Prefer:

- `Concern about zero-shot degradation in generative settings`
- `Concern about the training cost and adaptation requirement`
- `Concern about how strongly the current evidence supports generative-task claims`

Avoid:

- paraphrases that make the paper sound worse than the original review does
- emotionally loaded summaries
- summaries that already smuggle in your answer

The reviewer label should orient the reader, not intensify the criticism.

## Default Answer Structure

For most answers, the best structure is:

1. direct topic sentence that answers the concern
2. brief explanation of why that answer is correct
3. concrete paper evidence, numbers, or setup details
4. one sentence on what conclusion is actually supported

This structure matters. The reviewer should know from the first sentence what the paragraph is trying to establish.

## Paragraph Logic

Each paragraph should have a clean internal logic.

Good paragraph behavior:

- first sentence states the point of the paragraph
- middle sentences supply the reason or evidence
- final sentence tells the reader what follows from that evidence

Good transitions are short and functional:

- `However`
- `Therefore`
- `At the same time`
- `In the current submission`
- `For decoder models`
- `In this setting`

Do not write paragraphs that merely stack facts without showing the relation between them.

## How To Handle Limitations

When the reviewer is right:

- say so directly
- define the boundary precisely
- explain what the paper still establishes despite that boundary

When the reviewer is partly right:

- clarify the boundary first
- separate what is truly limited from what is still supported
- avoid turning the whole answer into a concession

When the reviewer misunderstands something:

- clarify the misunderstanding in the first sentence
- then walk back to the evidence in the paper

The answer should never stop at "yes, this is limited." It must also explain what remains meaningful.

## Persuasion Standard

The rebuttal must actively help the reviewer see the paper's value.

That means:

- do not bury the main contribution under a long concession
- do not let a real limitation erase the positive evidence already in the paper
- do not sound defensive
- do not sound like the safest possible summary

A common target form is:

- limitation is real
- evidence is also real
- therefore the supported claim is narrower than the strongest possible claim, but still meaningful

## Language Rules

Use:

- plain academic English
- short, direct topic sentences
- concrete nouns and verbs
- professional wording that is easy to read

Prefer:

- `Therefore`
- `However`
- `This means`
- `The current paper shows`
- `The supported claim is`

Avoid:

- fancy or inflated vocabulary
- vague abstractions
- robotically formal filler
- unexplained meta language
- repeated stock phrases such as `the right interpretation is`, `best read as`, `for this reason`, unless they are truly needed
- empty softeners such as `This is a helpful question`

The goal is not to sound ornate. The goal is to sound precise and credible.

## Formatting Rules

- bold only the `W/Q/A` labels by default
- use extra boldface inside the answer only for a genuinely central sentence
- do not force one bold sentence into every paragraph
- split long paragraphs when readability improves
- use markdown tables only when they help the reviewer see a concrete comparison

If the author notes say a table should be prepared, create the markdown table scaffold even if the values are still `[TBD]`.

## Human-In-The-Loop Rule

If the user manually rewrites a sentence or paragraph:

- treat that wording as preferred
- preserve it unless the user explicitly asks to change it
- learn from why the change improved the logic or tone

Do not:

- rewrite user-fixed text back into your own default style
- flatten the user's sentence logic into a generic summary
- reintroduce phrasing the user has already rejected

## Compression Rule

Only compress after the logic is approved.

Allowed compression targets:

- repeated background
- repeated conclusions
- filler politeness
- redundant transitions
- duplicated explanation across related reviewer answers

Do not compress by:

- deleting a logical step
- softening a direct answer until it becomes vague
- removing the sentence that explains why the paper is still meaningful
- changing the stance or implication

The first pass should optimize logic. Compression is a later pass.

## Reviewer-Specific Guidance

- positive reviewers can receive a slightly warmer opener, but the body should stay technical
- low-score reviewers need the clearest logic and the most careful statement of value
- if multiple reviewers share a concern, keep the underlying reasoning consistent but still tailor the answer to the exact wording of each review
- cross-reference another reviewer only after the current answer stands on its own
