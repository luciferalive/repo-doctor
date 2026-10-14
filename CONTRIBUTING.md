# Contributing to repo-doctor

Thanks for wanting to help! Every contribution counts, including typo fixes.

## Quick start

```bash
git clone https://github.com/luciferalive/repo-doctor.git
cd repo-doctor
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
repo-doctor .
```

## The easiest way to contribute: add a check

Checks live in `repo_doctor/checks.py`. A check is one small function:

```python
@check("changelog", "CHANGELOG present")
def changelog(root: Path):
    if _first_existing(root, ["CHANGELOG.md", "CHANGES.md"]):
        return PASS, "Changelog found."
    return WARN, "No changelog.", "Keep a CHANGELOG.md so users can see what changed."
```

Return `(status, message)` or `(status, message, hint)` where status is
`PASS`, `WARN`, or `FAIL`. Then:

1. Add a test in `tests/test_checks.py`.
2. Add a row to the checks table in `README.md`.
3. Open a pull request.

See `GOOD_FIRST_ISSUES.md` for ideas.

## Pull request flow

1. Fork the repo and create a branch (`git checkout -b add-changelog-check`).
2. Make your change and keep it focused: one idea per PR.
3. Run `pytest` and make sure it passes.
4. Push and open a PR. Fill in the template.
5. A maintainer will review, usually within a few days. Don't worry about
   getting it perfect; we'll iterate together.

## Guidelines

- Pure standard library only. No runtime dependencies, please.
- Keep checks fast and read-only. They must never modify the repo or use the network.
- Be kind. See `CODE_OF_CONDUCT.md`.

## Not sure where to start?

Open an issue and say hi. We're happy to point you at something.
