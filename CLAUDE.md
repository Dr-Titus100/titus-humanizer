# Working on titus-humanizer

## Branches
- Push every change to the `dev` branch. Don't create a new branch for each change.
- Before you start, bring `dev` up to date with `main`.
- When the tests pass on `dev` (both `test (3.9)` and `test (3.13)` on that commit), move `main` to the same commit with `git push origin dev:main`. This needs no pull request and no approval from the repository owner.
- `main` is protected. GitHub blocks force pushes and deletion, and a commit reaches `main` only after its tests pass. If GitHub rejects the push because `main` has moved, merge `main` into `dev`, push `dev`, wait for the tests and push again. Never force-push.
- The repository owner publishes releases.

## Writing
- Everything you write here follows the skill itself: no em dashes, no semicolons, no "not X, but Y" framing and no slogans. Run new text through `python3 skills/titus-humanizer/scripts/titus_tools.py score FILE`.

## Checks before you push
- `python3 -m unittest discover -s tests` (the suite also runs on Python 3.9 in CI)
- `python3 tests/update_expected.py --check`. When a script change is intended, run it without `--check`, review the diff and commit the stored output.
- Remove `__pycache__` folders before you commit.
- A change to the scoring script needs a CHANGELOG entry under "Unreleased", and the titus-web site pins each release by tag and checksum.
