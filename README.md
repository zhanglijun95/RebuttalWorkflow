# ICML Rebuttal Workspace

This folder is a local rewrite of the rebuttal workflow from `wanshuiyin/Auto-claude-code-research-in-sleep`, adapted into a reusable multi-paper workspace for Codex.

It is designed for:

- ICML-style rebuttals with strict character limits
- per-reviewer responses
- grounded drafting with no fabrication and no unapproved promises
- iterative human editing and refinement
- follow-up discussion rounds after the initial rebuttal

## Shared Layout

- `WORKFLOW.md`: end-to-end process for any paper folder
- `STYLE_GUIDE.md`: writing standard learned from actual ICML rebuttal iteration
- `TEMPLATES.md`: copy-ready templates for new paper folders
- `tools/rebuttal_check.py`: local validator for required files and character counts
- `papers/`: one subfolder per paper

## Paper Layout

Each paper lives in its own folder under `papers/`, for example:

- `papers/icml2026_forest/`: archived first-paper rebuttal materials
- `papers/icml2026_paper_02/`: fresh scaffold for the next paper

Inside one paper folder, the working files are:

- `README.md`
- `REBUTTAL_STATE.md`
- `VENUE_RULES.md`
- `PAPER_NOTES.md`
- `REVIEWS_RAW.md`
- `USER_CONFIRMED_EVIDENCE.md`
- `AUTHOR_NOTES.md`
- `ISSUE_BOARD.md`
- `STRATEGY_PLAN.md`
- `REBUTTAL_DRAFT_v1.md`
- `REBUTTAL_DRAFT_rich.md`
- `FOLLOWUP_LOG.md`
- `MCP_STRESS_TEST.md`
- reviewer-specific `PASTE_READY_<reviewer_id>.md` / `.txt` files once drafting starts

## Recommended Use

Set a paper directory variable mentally, for example:

- `<paper_dir> = Rebuttal/papers/icml2026_paper_02`

Then:

1. Put the submitted PDF in `<paper_dir>/`.
2. Fill in `<paper_dir>/VENUE_RULES.md`.
3. If you want, leave `<paper_dir>/PAPER_NOTES.md` mostly empty and I can summarize it from the PDF.
4. Paste the raw reviews into `<paper_dir>/REVIEWS_RAW.md`.
5. Add approved extra results to `<paper_dir>/USER_CONFIRMED_EVIDENCE.md`.
6. Put your reviewer-specific thoughts, attitudes, and unfinished experiment notes into `<paper_dir>/AUTHOR_NOTES.md`.
7. Ask Codex:

```text
Use Rebuttal/WORKFLOW.md and Rebuttal/STYLE_GUIDE.md with Rebuttal/papers/icml2026_paper_02/ to generate ISSUE_BOARD.md and STRATEGY_PLAN.md. Do not draft the rebuttal yet.
```

8. After reviewing the plan, ask Codex:

```text
Use Rebuttal/WORKFLOW.md and Rebuttal/STYLE_GUIDE.md to draft reviewer-facing rebuttal files in Rebuttal/papers/icml2026_paper_02/. Use AUTHOR_NOTES.md for strategy and tone, but keep factual claims grounded to the paper, reviews, and USER_CONFIRMED_EVIDENCE.md only.
```

9. When you want the final compact version:

```text
Polish the Final sections / PASTE_READY files in Rebuttal/papers/icml2026_paper_02/, keep each one under the venue limit in VENUE_RULES.md, and preserve full reviewer coverage.
```

## Local Checks

Run:

```bash
python3 Rebuttal/tools/rebuttal_check.py --dir Rebuttal/papers/icml2026_paper_02
```

To also check a specific character limit:

```bash
python3 Rebuttal/tools/rebuttal_check.py --dir Rebuttal/papers/icml2026_paper_02 --limit 5000
```

## Safety Rules

- Never invent experiments, numbers, derivations, citations, or reviewer positions.
- Never promise new experiments or revisions unless you explicitly approve them.
- Every reviewer concern must end in one of: `answered`, `deferred_intentionally`, or `needs_user_input`.
- If evidence is weak, concede narrowly instead of overstating.
- Do not compress text before the logic is approved.
- If the user manually rewrites a sentence, treat that wording as preferred unless asked to change it.
