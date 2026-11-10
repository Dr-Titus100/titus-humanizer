# Tests

These tests check `skills/titus-humanizer/scripts/titus_tools.py`, the script behind the hidden-character cleanup and the AI-pattern score. They use only the Python standard library, so you need Python 3.9 or later and nothing else. GitHub runs them on every push and pull request.

## Running them

From the top of the repository:

```
python3 -m unittest discover -s tests -v
```

## What they check

| File | What it covers |
| --- | --- |
| `test_cleanup.py` | What the cleanup removes (zero-width spaces, text-direction controls, stray tag characters, odd spaces, look-alike letters, including inside quotations) and what it keeps (emoji, flags, Persian and Russian text, code, URLs, aligned resume columns) |
| `test_patterns.py` | One sentence each pattern must catch and one it must leave alone, plus the score's thresholds, the 30-word minimum, the dampening of short texts and the rule that code and quoted text aren't scored. A new pattern without an example here fails the suite. |
| `test_examples.py` | The resume and prose examples in `fixtures/`, compared with the stored output in `expected/`. It also checks that every rewrite scores lower than its original and keeps no hard-rule pattern, and that plain human writing scores low. |

## The examples

`fixtures/resume/` and `fixtures/prose/` hold short documents written for these tests. The people and companies in them are fictional.

- A file ending in `_rewrite.txt` is a hand-edited rewrite of the file with the same name. Each pair has a stored before-and-after report.
- A file starting with `human_` is plain writing that should pass. `human_resume.txt` uses date ranges such as "Fall 2018 – Spring 2020" and bullets at the start of lines, which the punctuation rules allow. `human_pasted_feedback.txt` contains zero-width spaces, a non-breaking space and a Cyrillic "а" inside an English word, so it tests the cleanup on a whole document.
- The other files are drafts full of AI-writing patterns.

For each example, `expected/` stores what the script prints for it, followed by every pattern it found and the line it found it on:

```
Hits by line:
  line 9: AI vocabulary: "robust"
  line 10: semicolon: ";"
```

## When you change the script

If your change moves a score, a pattern count or a hit, `test_examples.py` fails and prints a diff of the stored output against the new output. For example, taking "robust" out of the AI vocabulary list shows:

```
--- tests/expected/resume__ai_resume.score.txt (stored)
+++ tests/expected/resume__ai_resume.score.txt (script now)
-Pattern density: 13.26 per 100 words, sentence-length variation: 0.65, word variety: 0.91
-  AI vocabulary x10, e.g. "leveraging"
+Pattern density: 12.84 per 100 words, sentence-length variation: 0.65, word variety: 0.91
+  AI vocabulary x9, e.g. "leveraging"
```

If the change is what you meant, save the new output and commit it with your change:

```
python3 tests/update_expected.py           # show the diff, then save it
python3 tests/update_expected.py --check   # show the diff and save nothing
```

The diff in `expected/` then becomes the before-and-after record in your pull request.

## Reporting a bug

A bug report is easiest to act on when it names a fixture and a line, for example "`tests/fixtures/resume/ai_resume.txt`, line 15: the script doesn't count 'Additionally' as a sentence opener after a bullet." If the text that shows the bug isn't in a fixture yet, add a short one to `fixtures/` and run `python3 tests/update_expected.py`. A fix then shows up as a change to that line in `expected/`.

To add a new example, put a `.txt` file in `fixtures/resume/` or `fixtures/prose/`, add a `_rewrite.txt` file next to it if you want a before-and-after pair, and run `python3 tests/update_expected.py`.
