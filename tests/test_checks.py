import json

from repo_doctor.cli import main
from repo_doctor.core import FAIL, PASS, REGISTRY, run_checks, score


def by_id(results):
    return {r.id: r for r in results}


def test_empty_repo_fails_most_checks(tmp_path):
    results = by_id(run_checks(tmp_path))
    assert results["readme"].status == FAIL
    assert results["license"].status == FAIL
    assert results["ci"].status == FAIL
    assert score(list(results.values())) < 30


def test_good_repo_scores_high(tmp_path):
    (tmp_path / "README.md").write_text("x" * 300)
    (tmp_path / "LICENSE").write_text("MIT")
    (tmp_path / ".gitignore").write_text("*.pyc")
    (tmp_path / "CONTRIBUTING.md").write_text("hi")
    (tmp_path / "CODE_OF_CONDUCT.md").write_text("be nice")
    (tmp_path / "SECURITY.md").write_text("email us")
    (tmp_path / "tests").mkdir()
    wf = tmp_path / ".github" / "workflows"
    wf.mkdir(parents=True)
    (wf / "ci.yml").write_text("name: ci")
    (tmp_path / ".github" / "ISSUE_TEMPLATE").mkdir()
    (tmp_path / ".github" / "PULL_REQUEST_TEMPLATE.md").write_text("## What")
    results = run_checks(tmp_path)
    assert all(r.status == PASS for r in results), [r for r in results if r.status != PASS]
    assert score(results) == 100


def test_short_readme_warns(tmp_path):
    (tmp_path / "README.md").write_text("# hi")
    assert by_id(run_checks(tmp_path))["readme"].status == "warn"


def test_only_and_skip(tmp_path):
    only = run_checks(tmp_path, only=["readme"])
    assert [r.id for r in only] == ["readme"]
    skipped = run_checks(tmp_path, skip=["readme"])
    assert "readme" not in [r.id for r in skipped]


def test_registry_ids_unique_and_documented():
    run_checks(__import__("pathlib").Path("."), only=["readme"])
    assert len(REGISTRY) >= 9
    for c in REGISTRY.values():
        assert c.title


def test_cli_json_output(tmp_path, capsys):
    (tmp_path / "README.md").write_text("x" * 300)
    code = main([str(tmp_path), "--format", "json"])
    data = json.loads(capsys.readouterr().out)
    assert code == 0
    assert "score" in data and isinstance(data["results"], list)


def test_cli_min_score_exit_code(tmp_path):
    assert main([str(tmp_path), "--min-score", "90"]) == 1
    assert main([str(tmp_path), "--min-score", "0"]) == 0


def test_cli_bad_path(tmp_path):
    assert main([str(tmp_path / "nope")]) == 2


def test_cli_list(capsys):
    assert main(["--list"]) == 0
    assert "readme" in capsys.readouterr().out
