"""Command line interface."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from repo_doctor import __version__
from repo_doctor.core import FAIL, PASS, REGISTRY, WARN, run_checks, score

ICONS = {PASS: "✔", WARN: "!", FAIL: "✘"}
COLORS = {PASS: "\033[32m", WARN: "\033[33m", FAIL: "\033[31m"}
RESET = "\033[0m"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="repo-doctor",
        description="Check how healthy and contributor-friendly a repo is.",
    )
    p.add_argument("path", nargs="?", default=".", help="repo to check (default: current dir)")
    p.add_argument("--format", choices=["text", "json"], default="text")
    p.add_argument("--only", action="append", metavar="ID", help="run only this check (repeatable)")
    p.add_argument("--skip", action="append", metavar="ID", help="skip this check (repeatable)")
    p.add_argument("--min-score", type=int, default=0, metavar="N",
                   help="exit with code 1 if the score is below N (useful in CI)")
    p.add_argument("--list", action="store_true", help="list available checks and exit")
    p.add_argument("--no-color", action="store_true")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return p


def _render_text(results, total: int, color: bool) -> str:
    lines = []
    for r in results:
        icon = ICONS[r.status]
        if color:
            icon = f"{COLORS[r.status]}{icon}{RESET}"
        lines.append(f" {icon} {r.title}: {r.message}")
        if r.hint and r.status != PASS:
            lines.append(f"     → {r.hint}")
    lines.append("")
    lines.append(f"Health score: {total}/100")
    return "\n".join(lines)


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)

    if args.list:
        from repo_doctor import checks  # noqa: F401  (registers checks)
        for c in REGISTRY.values():
            print(f"{c.id:<18} {c.title}")
        return 0

    root = Path(args.path).resolve()
    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 2

    results = run_checks(root, only=args.only, skip=args.skip)
    total = score(results)

    if args.format == "json":
        print(json.dumps({"path": str(root), "score": total,
                          "results": [r.to_dict() for r in results]}, indent=2))
    else:
        color = sys.stdout.isatty() and not args.no_color
        print(f"repo-doctor — {root}\n")
        print(_render_text(results, total, color))

    return 1 if total < args.min_score else 0
