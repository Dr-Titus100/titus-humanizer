# Changelog

## Unreleased

- Quoted text stays exactly as written. Quotations, block quotes, quoted titles and dialogue keep their wording and punctuation, whoever wrote them. The skill rewrites the text around a quote and mentions problems inside one in its notes.
- The score skips text in quotation marks and block quotes, as it already skipped code. A single-quoted passage counts only when it has both an opening and a closing mark, so apostrophes in words like "don't" and "students'" are still scored.
- Tests for quoted text in the score and the cleanup.

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
