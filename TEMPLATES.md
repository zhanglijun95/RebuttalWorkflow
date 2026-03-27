# Templates

Copy the relevant block into a paper folder such as `Rebuttal/papers/icml2026_paper_02/` and fill it in.

## `REBUTTAL_STATE.md`

```md
# Rebuttal State

- Venue: ICML
- Hard limit:
- Response format: text-only
- Current round: initial rebuttal
- New experiments allowed for rebuttal use: no
- Drafting allowed: no
- Current phase: initialize
- Last updated:
- Notes:
```

## `README.md`

```md
# Paper Rebuttal Workspace

- Paper folder:
- Venue:
- Current status:

## What to place here

- submitted PDF
- venue rules
- raw reviews
- approved extra evidence

## Main files

- `REBUTTAL_STATE.md`
- `VENUE_RULES.md`
- `PAPER_NOTES.md`
- `REVIEWS_RAW.md`
- `USER_CONFIRMED_EVIDENCE.md`
- `ISSUE_BOARD.md`
- `STRATEGY_PLAN.md`
- `REBUTTAL_DRAFT_v1.md`
- `REBUTTAL_DRAFT_rich.md`
- reviewer-specific `PASTE_READY_<reviewer_id>.md`

## Suggested Codex prompt

```text
Use Rebuttal/WORKFLOW.md and Rebuttal/STYLE_GUIDE.md with this folder. First normalize the inputs and generate ISSUE_BOARD.md plus STRATEGY_PLAN.md. Do not draft yet.
```
```

## `VENUE_RULES.md`

```md
# Venue Rules

- Venue: ICML
- Hard character limit:
- Response format: text-only
- Can include markdown formatting?: no
- Can upload revised PDF?: no
- Can cite appendix / supplement?: 
- Can mention planned revisions?: only if explicitly approved
- Deadline:
- Official rule notes:
```

## `PAPER_NOTES.md`

```md
# Paper Notes

## One-paragraph summary

## Main claims
- C1:
- C2:

## Key evidence already in the paper
- E1:
- E2:

## Important quantitative results
- Table/Figure:
  - What it shows:
  - Exact numbers:

## Baselines / comparisons already covered

## Limitations we can acknowledge safely

## Review-sensitive facts
- novelty anchors
- theoretical assumptions
- runtime / complexity
- ablations
- dataset / setup details
```

## `REVIEWS_RAW.md`

```md
# Raw Reviews

## Reviewer 1
[paste verbatim]

## Reviewer 2
[paste verbatim]

## Reviewer 3
[paste verbatim]

## Meta Reviewer / Area Chair
[paste verbatim if applicable]
```

## `USER_CONFIRMED_EVIDENCE.md`

```md
# User Confirmed Evidence

Only place facts here that are safe to use in the rebuttal but are not already easy to recover from the submitted paper text.

## Approved additional results
- Result:
  - Source file / experiment:
  - Exact wording allowed:

## Approved commitments
- Commitment:
  - Scope:
  - Allowed wording:

## Explicitly blocked items
- Do not claim:
- Do not promise:
```

## `ISSUE_BOARD.md`

```md
# Issue Board

| issue_id | reviewer | round | raw_anchor | issue_type | severity | reviewer_stance | response_mode | evidence_source | status | notes |
|---|---|---|---|---|---|---|---|---|---|---|
| R1-C1 | R1 | initial | "..." | novelty | major | swing | nearest_work_delta | paper | open | |
| R1-C2 | R1 | initial | "..." | empirical_support | critical | negative | grounded_evidence | user_confirmed_result | open | |
```

## `STRATEGY_PLAN.md`

```md
# Strategy Plan

## Global themes
- Theme 1:
- Theme 2:

## Reviewer priorities
- R1:
- R2:
- R3:

## Character budget
- Opener:
- R1:
- R2:
- R3:
- Closing:

## Blocked claims
- 

## Evidence gaps
- 

## Concessions to make
- 

## Risks
- 
```

## `REBUTTAL_DRAFT_v1.md`

```md
# Rebuttal Draft v1

Thank you for the thoughtful reviews. [2-4 sentence opener with global clarifications.]

R1.
1. [Direct answer]
2. [Grounded evidence]
3. [Implication for the paper]

R2.
1. [Direct answer]
2. [Grounded evidence]
3. [Implication for the paper]

R3.
1. [Direct answer]
2. [Grounded evidence]
3. [Implication for the paper]

Closing.
[Short acceptance case / resolution summary.]
```

## `REBUTTAL_DRAFT_rich.md`

```md
# Rebuttal Draft Rich

Same structure as the compact draft, but include fuller reasoning and mark optional paragraphs with:

[OPTIONAL - cut if over limit]
```

## `FOLLOWUP_LOG.md`

```md
# Follow-Up Log

## Round 1

### Reviewer 1
- New comment:
- Linked issue IDs:
- Draft delta reply:

### Reviewer 2
- New comment:
- Linked issue IDs:
- Draft delta reply:
```

## `MCP_STRESS_TEST.md`

```md
# Stress Test Notes

## Unsupported or weak claims
- 

## Missing issue coverage
- 

## Risky promises
- 

## Tone problems
- 

## Minimal grounded fixes
- 

## Verdict
- safe to submit / needs revision
```

## `PASTE_READY_<reviewer_id>.md`

```md
Thank you for the review and for the specific questions on [topic].

**W1:** [weakness text]
**A1:** [direct answer in the first sentence. then evidence. then implication.]

**W2:** [weakness text]
**A2:** [direct answer]

**Q1:** [question text]
**A3:** [direct answer]
```
