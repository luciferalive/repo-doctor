# 🩺 repo-doctor

Check how healthy and contributor-friendly a git repo is, with one command.
Zero dependencies, fast, and easy to extend.

```text
$ repo-doctor .

repo-doctor — /home/you/my-project

 ✔ README exists and has substance: README.md found (812 chars).
 ✘ LICENSE file present: No license file.
     → Without a license, nobody is legally allowed to reuse or contribute.
 ! CONTRIBUTING guide: No CONTRIBUTING guide.
     → Tell newcomers how to set up, test, and open a PR.
 ...

Health score: 62/100
```

## Install

```bash
pip install git+https://github.com/luciferalive/repo-doctor.git
```

## Usage

```bash
repo-doctor                    # check the current directory
repo-doctor path/to/repo       # check another repo
repo-doctor --format json      # machine-readable output
repo-doctor --only readme --only license
repo-doctor --skip security
repo-doctor --min-score 80     # exit 1 if score < 80 (great for CI)
repo-doctor --list             # show all checks
```

## Checks

| ID | What it looks for |
|----|-------------------|
| `readme` | README exists and isn't a stub |
| `license` | A LICENSE file |
| `gitignore` | A .gitignore |
| `contributing` | A CONTRIBUTING guide |
| `code-of-conduct` | A CODE_OF_CONDUCT.md |
| `ci` | CI config (GitHub Actions, GitLab CI, etc.) |
| `tests` | A tests directory or test files |
| `issue-templates` | Issue and PR templates |
| `security` | A SECURITY.md |

## Use it in CI

```yaml
- run: pip install git+https://github.com/luciferalive/repo-doctor.git
- run: repo-doctor . --min-score 80
```

## Contributing

**Contributions are very welcome**, and adding a check takes about ten lines.
Read [CONTRIBUTING.md](CONTRIBUTING.md) and pick something from
[GOOD_FIRST_ISSUES.md](GOOD_FIRST_ISSUES.md).

## License

[MIT](LICENSE)
