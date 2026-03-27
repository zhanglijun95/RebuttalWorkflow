#!/usr/bin/env python3
"""Lightweight checks for the local rebuttal workflow."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


PAPER_REQUIRED_FILES = [
    "README.md",
    "REBUTTAL_STATE.md",
    "VENUE_RULES.md",
    "PAPER_NOTES.md",
    "REVIEWS_RAW.md",
    "USER_CONFIRMED_EVIDENCE.md",
    "ISSUE_BOARD.md",
    "STRATEGY_PLAN.md",
    "REBUTTAL_DRAFT_v1.md",
    "REBUTTAL_DRAFT_rich.md",
]

SHARED_REQUIRED_FILES = [
    "README.md",
    "WORKFLOW.md",
    "STYLE_GUIDE.md",
    "TEMPLATES.md",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def nonempty_markdown_sections(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.strip().startswith("## "))


def final_section_text(path: Path) -> str:
    text = read_text(path)
    lines = text.splitlines()
    final_idx = None
    for idx, line in enumerate(lines):
        if line.strip() == "## Final":
            final_idx = idx + 1
    if final_idx is None:
        return text
    return "\n".join(lines[final_idx:]).strip()


def collect_output_counts(root: Path) -> dict[str, int]:
    counts: dict[str, int] = {}

    paste_ready = root / "PASTE_READY.txt"
    if paste_ready.exists():
        counts["PASTE_READY.txt"] = len(read_text(paste_ready))

    for path in sorted(root.glob("PASTE_READY_*.md")):
        counts[path.name] = len(final_section_text(path))

    for path in sorted(root.glob("PASTE_READY_*.txt")):
        counts[path.name] = len(read_text(path))

    return counts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default="Rebuttal", help="rebuttal workspace directory")
    parser.add_argument("--limit", type=int, default=None, help="optional hard character limit")
    args = parser.parse_args()

    root = Path(args.dir)
    shared_root = Path(__file__).resolve().parents[1]

    missing = [name for name in PAPER_REQUIRED_FILES if not (root / name).exists()]
    if missing:
        print("Missing files:")
        for name in missing:
            print(f"- {name}")
        return 1

    missing_shared = [name for name in SHARED_REQUIRED_FILES if not (shared_root / name).exists()]
    if missing_shared:
        print("Missing shared workflow files:")
        for name in missing_shared:
            print(f"- {name}")
        return 1

    reviews_raw = read_text(root / "REVIEWS_RAW.md")
    issue_board = read_text(root / "ISSUE_BOARD.md")
    strategy_plan = read_text(root / "STRATEGY_PLAN.md")
    state_text = read_text(root / "REBUTTAL_STATE.md")
    output_counts = collect_output_counts(root)

    print(f"Workspace: {root}")
    print(f"Review file chars: {len(reviews_raw)}")
    if output_counts:
        print("Output chars:")
        for name, count in output_counts.items():
            print(f"- {name}: {count}")
    else:
        print("Output chars: no PASTE_READY outputs found yet")

    if args.limit is not None:
        if not output_counts:
            print("WARN: no outputs available for limit checking yet")
        else:
            over = {name: count for name, count in output_counts.items() if count > args.limit}
            if over:
                for name, count in over.items():
                    print(f"ERROR: {name} exceeds limit by {count - args.limit} chars")
                return 2
            print(f"Limit check passed for all outputs against {args.limit}")

    if "issue_id" not in issue_board:
        print("WARN: ISSUE_BOARD.md does not look initialized")
    if nonempty_markdown_sections(strategy_plan) == 0:
        print("WARN: STRATEGY_PLAN.md looks empty")
    if "Current phase:" not in state_text:
        print("WARN: REBUTTAL_STATE.md is missing phase tracking")
    if len(reviews_raw.strip()) < 40:
        print("WARN: REVIEWS_RAW.md may still be empty")

    return 0


if __name__ == "__main__":
    sys.exit(main())
