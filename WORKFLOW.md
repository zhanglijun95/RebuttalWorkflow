# Rebuttal Workflow

This is the shared workflow for any paper folder under `Rebuttal/papers/`.

Use a paper directory placeholder while working, for example:

- `<paper_dir> = Rebuttal/papers/icml2026_paper_02`

## Core Gates

Three gates must pass before a reviewer-facing response is considered final:

1. Provenance gate
Every factual statement must map to one of:
- the submitted paper
- a reviewer comment
- `<paper_dir>/USER_CONFIRMED_EVIDENCE.md`
- an explicit author-supplied implementation fact that is clearly intended for rebuttal use
- explicitly marked future work

2. Commitment gate
Every promise must be one of:
- already done
- explicitly approved for the rebuttal
- framed as future work only

3. Coverage gate
Every reviewer concern must be tracked in `<paper_dir>/ISSUE_BOARD.md` and end as:
- `answered`
- `deferred_intentionally`
- `needs_user_input`

## Drafting Standard

Apply these rules before writing any reviewer-facing text:

- write in formal academic prose, not conversational explanation
- answer the reviewer's actual concern in the first sentence of each answer
- keep the visible `**W:** / **Q:** / **A:**` structure
- paraphrase reviewer concerns neutrally; do not make the paper sound worse than the review already does
- give each paragraph one clear job
- use the paragraph order: answer, explanation, evidence, supported claim
- when a limitation is real, state it precisely and then explain what the paper still establishes
- do not overclaim, but do not let the answer collapse into pure concession
- use plain professional language; avoid ornate vocabulary and canned filler
- if several points share one underlying issue, merge them only when the merged answer stays easy to follow
- if the user manually rewrites wording, treat that wording as preferred

Compression rules:

- do not compress before the logic is approved
- remove only filler, repetition, redundant transitions, or repeated background
- do not change the logic, stance, evidence, or coverage while compressing
- never delete the sentence that explains why the result still matters

See `Rebuttal/STYLE_GUIDE.md` for the detailed standard.

## Phase 0: Initialize

Make sure these files exist in `<paper_dir>`:

- `README.md`
- `REBUTTAL_STATE.md`
- `VENUE_RULES.md`
- `PAPER_NOTES.md`
- `REVIEWS_RAW.md`
- `USER_CONFIRMED_EVIDENCE.md`
- `AUTHOR_NOTES.md`

Update `REBUTTAL_STATE.md` with:

- venue
- hard limit
- current round
- whether new experiments are allowed
- whether drafting is allowed yet

## Phase 1: Normalize Inputs

Goal: make the source material clean enough for structured drafting.

Tasks:

- keep reviewer text verbatim in `REVIEWS_RAW.md`
- preserve reviewer IDs if available
- record the official limit and reply format in `VENUE_RULES.md`
- extract usable paper anchors into `PAPER_NOTES.md`
- list only approved extra evidence in `USER_CONFIRMED_EVIDENCE.md`
- collect author-side strategy, reviewer-specific attitude, unfinished experiment context, and desired tables in `AUTHOR_NOTES.md`
- if the paper PDF is available, summarize only grounded claims and numbers from it

Suggested Codex prompt:

```text
Read <paper_dir>/VENUE_RULES.md, <paper_dir>/PAPER_NOTES.md, <paper_dir>/REVIEWS_RAW.md, <paper_dir>/USER_CONFIRMED_EVIDENCE.md, and <paper_dir>/AUTHOR_NOTES.md. Normalize the inputs, identify blockers, and do not draft yet.
```

## Phase 2: Atomize Reviewer Concerns

Create or update `<paper_dir>/ISSUE_BOARD.md`.

Each issue should include:

- `issue_id` like `R1-C2`
- `reviewer`
- `round`
- `raw_anchor`
- `issue_type`
- `severity`
- `reviewer_stance`
- `response_mode`
- `evidence_source`
- `status`

Recommended `issue_type` values:

- assumptions
- theorem_rigor
- novelty
- empirical_support
- baseline_comparison
- complexity
- practical_significance
- clarity
- reproducibility
- other

Recommended `response_mode` values:

- direct_clarification
- grounded_evidence
- nearest_work_delta
- assumption_hierarchy
- narrow_concession
- future_work_boundary

Suggested Codex prompt:

```text
Use <paper_dir>/REVIEWS_RAW.md to build <paper_dir>/ISSUE_BOARD.md. Split each review into atomic concerns, preserve reviewer tone, and assign issue_type, severity, reviewer_stance, response_mode, evidence_source, and status.
```

## Phase 3: Build Strategy

Create or update `<paper_dir>/STRATEGY_PLAN.md`.

It should contain:

- 2-4 global themes across reviewers
- per-reviewer priorities
- blocked claims that must not appear
- evidence gaps
- character budget
- a decision on where to clarify, where to concede narrowly, and where to push back

Simple character budget for ICML reviewer replies:

- opener: 5-10%
- point-by-point answers: 85-90%
- closing: 0-5%

Before any drafting, write down for each issue:

- the exact concern
- our stance: agree / clarify / partial agree
- the strongest grounded evidence
- the supported claim after the answer

Suggested Codex prompt:

```text
Use <paper_dir>/ISSUE_BOARD.md plus the source files to write <paper_dir>/STRATEGY_PLAN.md. Identify shared themes, budget the characters, flag blocked claims, and define the strongest grounded answer for each major concern.
```

## Phase 4: Evidence Sprint

Only do this if you have approved new evidence for rebuttal use.

If a reviewer asks for results you do not have:

- do not fabricate
- either add approved new evidence to `USER_CONFIRMED_EVIDENCE.md`
- or switch the issue response toward narrow concession / future-work boundary

If the author notes say a table will likely be needed, prepare the table scaffold with `[TBD]` values even before the numbers are finalized.

Suggested Codex prompt:

```text
Review <paper_dir>/ISSUE_BOARD.md and list which concerns have strong evidence, weak evidence, or no evidence. For weak or missing evidence, recommend either a narrow concession or a future-work boundary.
```

## Phase 5: Draft Reviewer Responses

Create:

- `<paper_dir>/REBUTTAL_DRAFT_v1.md`
- `<paper_dir>/REBUTTAL_DRAFT_rich.md`
- reviewer-facing files such as `<paper_dir>/PASTE_READY_<reviewer_id>.md`

Default reviewer-response structure:

1. short reviewer-facing opener
2. point-by-point responses using `**W1:** / **A1:** / **Q1:** / **A2:**`
3. each listed weakness/question receives a direct answer
4. shared concerns are answered consistently, but tailored to the current reviewer's wording and emphasis

For each answer, force this checklist before writing:

- What is the reviewer's actual concern?
- What is the first sentence that answers that concern?
- What evidence from the paper supports the answer?
- What is the strongest supported claim after acknowledging the limitation?

Writing heuristics:

- start from the paper's value, not from a defensive summary
- state real limitations directly, but do not let the answer stop there
- make the sentence-to-sentence logic explicit
- keep the language plain, professional, and easy to scan
- use tables only when they make comparison easier
- do not use generic filler to sound polite
- answer positive reviewers with a slightly warmer opener, but the same technical rigor

Suggested Codex prompt:

```text
Use Rebuttal/WORKFLOW.md and Rebuttal/STYLE_GUIDE.md to draft reviewer-facing rebuttal files in <paper_dir>. Use AUTHOR_NOTES.md for strategy and tone, but keep every factual claim grounded to the paper, reviews, user-approved facts, or clearly identified revision plans only.
```

## Phase 6: Human Refinement Loop

This phase is expected, not exceptional.

Rules:

- if the user rewrites part of a draft, preserve that wording
- edit only the places the user flags unless explicitly asked to rewrite more
- learn the user's sentence logic and reuse it in later reviewer responses
- do not reintroduce phrases or structures the user has already rejected
- do not compress unless the user asks for compression

Suggested Codex prompt:

```text
Revise only the commented parts of the latest reviewer draft in <paper_dir>. Preserve all user-edited wording unless directly asked to change it.
```

## Phase 7: Stress Test

Use Codex as an internal skeptical reviewer.

Questions to ask:

- Which concerns are still weakly answered?
- Which sentences sound unsupported?
- Which promises sound risky or unapproved?
- Which paragraph fails to explain why the paper is still meaningful?
- Which answer sounds too negative, too defensive, or too vague?
- What are the smallest grounded fixes?

Store the notes in `<paper_dir>/MCP_STRESS_TEST.md`.

Suggested Codex prompt:

```text
Stress-test the current reviewer-facing drafts in <paper_dir> against REVIEWS_RAW.md and ISSUE_BOARD.md. Write MCP_STRESS_TEST.md with unsupported claims, missing coverage, risky promises, tone problems, and minimal grounded fixes.
```

## Phase 8: Finalize And Compress

Produce:

- reviewer-specific markdown drafts such as `PASTE_READY_<reviewer_id>.md`
- paste-safe text files if needed
- a short final summary of remaining risks

Compression order if over limit:

1. remove repeated background
2. shorten repeated conclusions
3. compress transition sentences
4. shorten opener / closer
5. compress tables only if the table is not central

Never compress by removing answer coverage, evidence, or the sentence that states the supported claim.
