# Changelog

## Unreleased

- The score skips links and file paths, as it already skipped code and quoted text, so a word such as "robust" in `https://example.com/robust-guide` or `~/notes/robust-plan.md` doesn't count. A sentence that ends with a link or path still ends there.
- The `score` command's last line names what it left as-is and didn't score, such as "Left as-is and not scored: 3 quotations, 1 code snippet and 1 link". It replaces the "Quoted text" line.
- New tests check that links, file paths and emoji don't count toward the score and that the score line lists each kind.

## v1.2.0 (2026-11-13)

- The report's "Left as-is" line covers quotations, code snippets, file paths, links and emoji, such as "Left as-is: 3 quotations, 1 code snippet and 1 link". It replaces the "Quoted text" line. The script finds each item in the original and the same kind of item in the rewrite and compares them whole, so a link that changed from `/guide` to `/guide2` counts as changed. When anything changed, a "Changed in the rewrite" line says what to restore. The script counts each piece of text once, so a link inside code counts as code.
- Words with a curly apostrophe, such as "don’t", count as one word, the same as "don't". Before, the script split them in two, which threw off the word count, sentence lengths and word variety.
- The script compares a quotation with any code inside it still in place, so swapping the code inside a quote counts as a change. A link keeps a closing bracket it opened, as in `.../Function_(mathematics)`. A flag such as 🇺🇸 counts as one emoji, so changing it to 🇸🇺 counts as a change.
- New tests check one item of each kind kept and one of each kind changed. They also cover items that only gained characters (`/guide` to `/guide2`), code inside a quote, links that end in a bracket, flags, words with slashes that aren't paths and emoji sequences. Another test checks that curly apostrophes don't change the word count.

## v1.1.0 (2026-11-10)

- Quoted text stays exactly as written. Quotations, block quotes, quoted titles and dialogue keep their wording and punctuation, whoever wrote them. The skill rewrites the text around a quote and mentions problems inside one in its notes.
- The score skips text in quotation marks and block quotes, as it already skipped code. It counts a quotation only when the opening mark comes after a space or the start of a line and the closing mark comes before a space or punctuation, in the same paragraph. Single and double quotes follow the same rule, so apostrophes ("don't", "students'") and inch marks ("a 12" tablet") stay in the score.
- When the text has quotations, the report adds a line saying how many were left as written and not scored. If any changed, it says so.
- Tests for quoted text in the score and the cleanup, including quotes nested inside other quotes, and a before-and-after example (`tests/fixtures/prose/nested_quotes.txt`) whose rewrite must keep every quotation word for word.

## v1.0.0 (2026-11-07)

First public release.

- Rewrite and review modes for AI-writing patterns at the word, sentence and story level.
- Story-level rules (Part 6) based on the StoryScope study of AI fiction.
- Hidden-character cleanup (Part 0). The skill removes zero-width spaces, byte-order marks, text-direction controls, unusual spaces and look-alike letters before it rewrites, and checks the rewrite again afterwards. Emoji, other alphabets, code and URLs stay as they are.
- AI-pattern score and report (Part 7). `scripts/titus_tools.py` scores the original and the rewrite from 0 to 1, and every default rewrite ends with a four-line report. When the rewrite still scores high, the skill takes another pass at the flagged spots.
- Review mode starts with the score and can compare a revised draft with the earlier one.
- Date ranges with spaces ("Jul 2020 – Jun 2021") and bullets at the start of a line pass the punctuation rules, so resumes keep their layout.
- A test suite in `tests/` with resume and prose examples, run on every push and pull request.
- Install options for Claude Code, claude.ai, the ChatGPT app, Codex and Custom GPTs. The Custom GPT instructions run the script through Code Interpreter.
