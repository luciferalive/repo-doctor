"""Built-in checks. Each returns ``(status, message[, hint])``."""

from __future__ import annotations

from pathlib import Path

from repo_doctor.core import FAIL, PASS, WARN, check


def _first_existing(root: Path, names):
    """Return the first existing path among ``names`` (case-insensitive)."""
    try:
        entries = {p.name.lower(): p for p in root.iterdir()}
    except OSError:
        return None
    for name in names:
        hit = entries.get(name.lower())
        if hit is not None:
            return hit
    return None


@check("readme", "README exists and has substance")
def readme(root: Path):
    p = _first_existing(root, ["README.md", "README.rst", "README.txt", "README"])
    if p is None:
        return FAIL, "No README found.", "Add a README.md explaining what the project does and how to use it."
    size = len(p.read_text(encoding="utf-8", errors="ignore").strip())
    if size < 200:
        return WARN, f"{p.name} is very short ({size} chars).", "Describe install, usage, and how to contribute."
    return PASS, f"{p.name} found ({size} chars)."


@check("license", "LICENSE file present")
def license_(root: Path):
    p = _first_existing(root, ["LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"])
    if p is None:
        return FAIL, "No license file.", "Without a license, nobody is legally allowed to reuse or contribute. Try https://choosealicense.com"
    return PASS, f"{p.name} found."


@check("gitignore", ".gitignore present")
def gitignore(root: Path):
    if (root / ".gitignore").is_file():
        return PASS, ".gitignore found."
    return WARN, "No .gitignore.", "Add one so build artifacts and secrets don't get committed."


@check("contributing", "CONTRIBUTING guide")
def contributing(root: Path):
    for base in (root, root / ".github", root / "docs"):
        if base.is_dir() and _first_existing(base, ["CONTRIBUTING.md", "CONTRIBUTING.rst"]):
            return PASS, "Contributing guide found."
    return FAIL, "No CONTRIBUTING guide.", "Tell newcomers how to set up, test, and open a PR."


@check("code-of-conduct", "Code of Conduct")
def code_of_conduct(root: Path):
    for base in (root, root / ".github", root / "docs"):
        if base.is_dir() and _first_existing(base, ["CODE_OF_CONDUCT.md"]):
            return PASS, "Code of Conduct found."
    return WARN, "No CODE_OF_CONDUCT.md.", "A code of conduct makes new contributors feel safe."


@check("ci", "Continuous integration configured")
def ci(root: Path):
    wf = root / ".github" / "workflows"
    if wf.is_dir() and any(p.suffix in (".yml", ".yaml") for p in wf.iterdir()):
        return PASS, "GitHub Actions workflow found."
    for f in (".gitlab-ci.yml", ".travis.yml", "azure-pipelines.yml", ".circleci"):
        if (root / f).exists():
            return PASS, f"CI config found ({f})."
    return FAIL, "No CI config.", "Add a workflow in .github/workflows/ that runs your tests."


@check("tests", "Tests exist")
def tests(root: Path):
    for d in ("tests", "test", "__tests__", "spec"):
        if (root / d).is_dir():
            return PASS, f"Test directory found ({d}/)."
    hits = list(root.glob("test_*.py")) + list(root.glob("*.test.*")) + list(root.glob("*_test.go"))
    if hits:
        return PASS, "Test files found."
    return FAIL, "No tests found.", "Contributors need tests to know they didn't break anything."


@check("issue-templates", "Issue / PR templates")
def issue_templates(root: Path):
    gh = root / ".github"
    has_issue = (gh / "ISSUE_TEMPLATE").is_dir() or (gh / "ISSUE_TEMPLATE.md").is_file()
    has_pr = _first_existing(gh, ["PULL_REQUEST_TEMPLATE.md"]) is not None if gh.is_dir() else False
    if has_issue and has_pr:
        return PASS, "Issue and PR templates found."
    if has_issue or has_pr:
        return WARN, "Only one of issue/PR templates found.", "Add both to get better bug reports and PRs."
    return WARN, "No issue or PR templates.", "Add .github/ISSUE_TEMPLATE/ and .github/PULL_REQUEST_TEMPLATE.md."


@check("security", "Security policy")
def security(root: Path):
    for base in (root, root / ".github", root / "docs"):
        if base.is_dir() and _first_existing(base, ["SECURITY.md"]):
            return PASS, "SECURITY.md found."
    return WARN, "No SECURITY.md.", "Explain how to privately report vulnerabilities."
