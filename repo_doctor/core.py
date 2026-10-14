"""Core types and the check registry.

To add a new check, write a function in ``repo_doctor/checks.py`` and decorate
it with ``@check("my-check-id", "Human readable title")``. That's it.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Callable, Dict, List, Optional

PASS = "pass"
WARN = "warn"
FAIL = "fail"

# How much each status contributes to the score (out of 1.0 per check).
SCORE_WEIGHTS = {PASS: 1.0, WARN: 0.5, FAIL: 0.0}


@dataclass
class Result:
    id: str
    title: str
    status: str
    message: str
    hint: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


CheckFn = Callable[[Path], Result]


@dataclass
class Check:
    id: str
    title: str
    fn: CheckFn


REGISTRY: Dict[str, Check] = {}


def check(check_id: str, title: str):
    """Register a check function under ``check_id``."""

    def decorator(fn: Callable[[Path], tuple]):
        def wrapped(root: Path) -> Result:
            status, message, *rest = fn(root)
            hint = rest[0] if rest else None
            return Result(check_id, title, status, message, hint)

        if check_id in REGISTRY:
            raise ValueError(f"duplicate check id: {check_id}")
        REGISTRY[check_id] = Check(check_id, title, wrapped)
        return fn

    return decorator


def run_checks(root: Path, only: Optional[List[str]] = None,
               skip: Optional[List[str]] = None) -> List[Result]:
    # Importing registers all built-in checks.
    from repo_doctor import checks  # noqa: F401

    selected = []
    for cid, c in REGISTRY.items():
        if only and cid not in only:
            continue
        if skip and cid in skip:
            continue
        selected.append(c)
    return [c.fn(root) for c in selected]


def score(results: List[Result]) -> int:
    """Return a 0-100 health score."""
    if not results:
        return 100
    total = sum(SCORE_WEIGHTS[r.status] for r in results)
    return round(100 * total / len(results))
