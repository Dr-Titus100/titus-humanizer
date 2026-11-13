# Working on titus-humanizer

## Branches
- Push every change to the `dev` branch. Don't create a new branch for each change.
- When `dev` is ready, open a pull request from `dev` into `main`. Titus merges it and publishes releases.
- Before you start, bring `dev` up to date with `main`.

## Writing
- Everything you write here follows the skill itself: no em dashes, no semicolons, no "not X, but Y" framing and no slogans. Run new text through `python3 skills/titus-humanizer/scripts/titus_tools.py score FILE`.

## Checks before you push
- `python3 -m unittest discover -s tests` (the suite also runs on Python 3.9 in CI)
- `python3 tests/update_expected.py --check`. When a script change is intended, run it without `--check`, review the diff and commit the stored output.
- Remove `__pycache__` folders before you commit.
- A change to the scoring script needs a CHANGELOG entry under "Unreleased", and the titus-web site pins each release by tag and checksum.
