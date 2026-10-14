# Good first issues

Copy any of these into GitHub Issues with the labels `good first issue` and
`help wanted`, or just grab one and open a PR.

## New checks (each is ~10 lines + a test)
- [ ] `changelog`: warn if no CHANGELOG.md / CHANGES.md
- [ ] `editorconfig`: warn if no .editorconfig
- [ ] `readme-sections`: warn if README lacks an install/usage heading
- [ ] `dependabot`: warn if no `.github/dependabot.yml`
- [ ] `codeowners`: warn if no CODEOWNERS file
- [ ] `pre-commit`: warn if no `.pre-commit-config.yaml`
- [ ] `large-files`: warn if any tracked file is bigger than 5 MB
- [ ] `secrets-in-repo`: fail if a `.env` file is committed (not in .gitignore)
- [ ] `language-config`: detect package.json / pyproject.toml / Cargo.toml / go.mod and check for a lockfile

## CLI improvements
- [ ] `--format markdown` output, handy for pasting into issues
- [ ] `--fix` that creates missing boilerplate files from templates
- [ ] `--config` to read settings from `repo-doctor.toml`
- [ ] A shields.io-style badge generator for the score

## Docs & project
- [ ] Add a GIF/screenshot of the CLI output to the README
- [ ] Publish to PyPI (maintainer help available)
- [ ] Add a GitHub Action wrapper so people can use `uses: .../repo-doctor@v1`
