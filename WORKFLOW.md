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

- write in formal academic prose, not chatty explanation
- answer the reviewer's actual question in the first sentence of each answer
- use bold labels such as `**W1:**`, `**A1:**`, `**Q1:**`, `**A2:**`
- keep one concern matched to one answer, or explicitly merge related concerns
- use paragraph logic with a clear topic sentence followed by evidence and implication
- avoid robotic formatting, colon-heavy fact dumps, and filler phrases
- avoid overclaim; if evidence is partial, state the supported conclusion only
- for shared concerns across reviewers, cross-reference only if it truly saves space
- if the user manually rewrites wording, treat that wording as preferred

Compression rules:

- do not compress before the logic is approved
- remove only filler, repetition, redundant transitions, or repeated background
- do not change the logic, stance, or answer coverage while compressing
- never drop a reviewer concern just to save characters

See `Rebuttal/STYLE_GUIDE.md` for the detailed standard.

## Phase 0: Initialize

Make sure these files exist in `<paper_dir>`:

- `README.md`
- `REBUTTAL_STATE.md`
- `VENUE_RULES.md`
- `PAPER_NOTES.md`
- `REVIEWS_RAW.md`
- `USER_CONFIRMED_EVIDENCE.md`

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
- if the paper PDF is available, summarize only grounded claims/numbers from it

Suggested Codex prompt:

```text
Read <paper_dir>/VENUE_RULES.md, <paper_dir>/PAPER_NOTES.md, <paper_dir>/REVIEWS_RAW.md, and <paper_dir>/USER_CONFIRMED_EVIDENCE.md. Normalize the inputs, point out blockers, and do not draft yet.
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

Suggested Codex prompt:

```text
Use <paper_dir>/ISSUE_BOARD.md plus the source files to write <paper_dir>/STRATEGY_PLAN.md. Identify shared themes, budget the characters, flag blocked claims, and propose the strongest space allocation.
```

## Phase 4: Evidence Sprint

Only do this if you have approved new evidence for rebuttal use.

If a reviewer asks for results you do not have:

- do not fabricate
- either add approved new evidence to `USER_CONFIRMED_EVIDENCE.md`
- or switch the issue response toward narrow concession / future-work boundary

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
4. shared concerns are answered once and then reused carefully

Writing heuristics:

- evidence before rhetoric
- clarify first when the reviewer misunderstood something
- agree first when the reviewer is right, but do it cleanly and directly
- keep background paragraphs purposeful
- use tables only when they carry grounded new evidence
- answer positive reviewers too, with a slightly warmer tone but the same rigor

Suggested Codex prompt:

```text
Use Rebuttal/WORKFLOW.md and Rebuttal/STYLE_GUIDE.md to draft reviewer-facing rebuttal files in <paper_dir>. Keep every claim grounded to the paper, reviews, or <paper_dir>/USER_CONFIRMED_EVIDENCE.md only.
```

## Phase 6: Human Refinement Loop

This phase is expected, not exceptional.

Rules:

- if the user rewrites part of a draft, preserve that wording
- only edit the places the user flags, unless explicitly asked to rewrite more
- learn the user's sentence logic and reuse it in later reviewer responses
- do not reintroduce phrases or structures the user has already rejected

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
- Which paragraph may backfire with the meta reviewer?
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

1. remove redundancy
2. shorten repeated background
3. compress opener and transition sentences
4. tighten wording around already-stated claims
5. keep critical answer logic intact

Suggested Codex prompt:

```text
Compress only the Final reviewer responses in <paper_dir> to fit the venue limit. Remove filler and repetition only. Do not change the logic, stance, or reviewer coverage.
```

## Phase 9: Follow-Up Rounds

When discussion opens after the initial rebuttal:

- append new comments to `FOLLOWUP_LOG.md`
- link them to existing issue IDs when possible
- draft delta replies instead of rewriting the full rebuttal
- keep the tone technical, not rhetorical

Suggested Codex prompt:

```text
Use <paper_dir>/FOLLOWUP_LOG.md and the existing rebuttal files to draft only the delta replies for the latest reviewer follow-up. Preserve consistency with the main rebuttal and do not introduce new unsupported claims.
```
