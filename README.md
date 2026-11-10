# titus-humanizer

titus-humanizer is an editing skill for Claude and ChatGPT. It rewrites text so it reads like a careful, plain-spoken person wrote it, and it keeps every fact, number and name from the original. Before rewriting, it strips hidden characters such as zero-width spaces. After rewriting, it scores the original and the new version from 0 to 1 for AI-writing patterns, so you can see what changed. It can also review a draft and list each pattern it finds, with a plainer version of each line.

It works on emails, reports, slide decks, resumes, papers, cover letters, personal statements, blog posts and fiction.

You can also try it without installing anything at [dr-titus100.github.io/titus-web](https://dr-titus100.github.io/titus-web/tools/titus-humanizer/). The checker there scores text in your browser for free, and the rewrite page works with your own Gemini, Claude or OpenAI key.

## What it changes

**Before:**
> In today's fast-paced academic landscape, our new lab notebook template isn't just a form — it's a gateway to more reproducible science, fostering transparency and driving meaningful impact.

**After:**
> The new lab notebook template gives every experiment the same structure, which makes results easier to reproduce.

**Before (email):**
> I hope this message finds you well! I wanted to reach out to touch base regarding the proposal, which was reviewed by our team last week. It's not just a budget request — it's a roadmap for sustainable growth. Please let me know if you have any questions!

**After:**
> Our team reviewed the proposal last week. It sets out the budget we're requesting and what it would cover. I'm happy to walk you through the numbers.

The report under that rewrite, as the script printed it:

```
AI-pattern score: 0.56 (medium) before, not scored (27 words, needs at least 30) after
Patterns before: em dash x1, reject-then-assert x1, passive voice (heuristic) x1, chatbot residue x1
Patterns left after: none
Hidden characters removed: none
Note: the text is short, so the script dampened the score and it is less reliable.
```

**Before (story):**
> Elena stood at the window as the rain fell, mirroring the storm inside her. Her chest tightened, ice crawled down her spine, and the scent of wet earth and old memories filled her lungs. She realized, at last, that letting go was not the same as forgetting. It was a way of carrying him with her.

**After:**
> Elena stood at the window and watched the rain. She was afraid. She decided she could let him go without forgetting him.

None of the rewrites add facts. When a draft is vague and the details aren't available, the skill writes the plainest honest sentence and, in notes mode, says which detail would help.

## How it works

The skill cleans the text, checks it at three levels, fixes what it finds and then measures the result.

1. Hidden-character cleanup. Text pasted from AI tools, PDFs and web pages often carries characters you can't see: zero-width spaces, byte-order marks, text-direction controls, odd spaces and look-alike letters such as a Cyrillic "а" inside an English word. They break search, spell-check and word counts. The skill removes them and leaves emoji, other alphabets, code, links and file paths as they are.
2. Seven hard rules for patterns that never appear in the output. The punctuation rule bans em dashes, semicolons, en dashes or hyphens used as a break between clauses, dots and vertical bars used to separate items on one line, and arrows in prose. The other six cover "it's not X, it's Y" framing, passive voice that hides who acted, command-style titles, slogans, hedges such as "illustrative" on real numbers, and chatbot lines such as "I hope this helps".
3. Judgment calls on wording, sorted into five categories: awkward, flowery, vague, unnecessary and illogical. Each category comes with a test, such as "would you say this out loud to a colleague?", and examples of wording that passes and wording that fails. The skill also cuts inflated significance ("a pivotal moment"), promotional tone, unnamed authorities ("experts say"), stock AI vocabulary such as "delve", "leverage" and "seamless", and formulaic habits such as stock openers, canned endings and reflexive lists of three.
4. Story-level patterns for narrative and reflective writing. AI-written stories tend to state their moral, show fear through a stack of body sensations, make the weather match the mood and tie up every thread. The skill cuts these, keeps the writer's real names and odd details, and suggests bigger structural changes without making them unless you ask.
5. An AI-pattern score from 0 to 1, run on the original and on the rewrite. Most of the score comes from how densely the text uses the patterns above. Sentence rhythm, repeated sentence openings and word variety make up the rest. Scores of 0.60 and up count as high, and the skill takes another pass at the flagged spots when the rewrite still scores high.

Each rewrite ends with a self-check against the original, so no fact, number, name or real qualification goes missing.

Date ranges such as "Jul 2020 – Jun 2021" and bullets at the start of a line pass the punctuation rules, so resumes come through intact.

Quoted text stays exactly as written. Text in quotation marks, block quotes and dialogue keeps its wording and punctuation, whoever wrote it, including you. The skill rewrites only the text around a quote and mentions any problem inside one in its notes. The score skips quoted text too, so a quotation full of AI phrasing doesn't count against your rewrite. The script counts a quotation only when it finds an opening mark after a space or the start of a line and a closing mark before a space or punctuation, in the same paragraph. So it still scores apostrophes, as in "don't" and "students'", and inch marks, as in "a 12" tablet". Quotes nested inside other quotes work too, as long as the levels alternate between double and single marks.

The script has two known limits. In both, part of a quotation may count toward the score, but the rewrite still leaves the whole quotation untouched.

- Three levels of quotes that reuse straight double quotes, as in "Ama said, 'Kofi said "fine" twice.'"
- A straight double quote used as an inch mark inside a quotation, as in "the 12" model is robust". The script reads 12" as the end of the quotation.

The skill aims at clear, specific writing. The score counts patterns. It doesn't measure quality, it isn't the output of GPTZero, Turnitin or any other detector, and a low score doesn't prove a person wrote the text. The cleanup removes invisible characters only. It doesn't remove AI watermarks or file metadata.

## Using it

Once it's installed, ask in plain words. The skill loads when the request fits.

| You ask | You get |
| --- | --- |
| "Humanize this:" followed by your text | The rewritten text and a short report: the scores before and after, the patterns left and the hidden characters removed |
| "Rewrite this and tell me what you changed" | The rewrite, then a short list of what changed and why |
| "Does this sound like AI?" or "Review this" | The score, then a list of problems, each quoted with its location, category and a plainer version |
| "Here's my revised draft" after a review | Old and new scores, plus which problems the revision fixed, which remain and which are new |
| "Do a deeper rewrite of this story" | A rewrite that may also reorder or trim scenes, using only material already in the draft |

## Installation

The simplest way to install is to copy this repository's link, https://github.com/Dr-Titus100/titus-humanizer.git, into Claude, Claude Code, ChatGPT or Codex and ask it to help you install the skill. It will handle the installation for you, or walk you through any step it can't do itself. To install it yourself, follow the steps below.

Each release on the [Releases page](https://github.com/Dr-Titus100/titus-humanizer/releases) includes `titus-humanizer.zip`. The same zip works in claude.ai, the Claude desktop app and ChatGPT. Upload it as it is, without unzipping it.

### Claude (claude.ai and the desktop app)

1. In Settings, open Capabilities, and turn on Create and edit files ("Code execution and file creation" in older layout).
2. Open [Customize > Skills](https://claude.ai/customize/skills), choose "Upload a skill" and select `titus-humanizer.zip`.
3. Turn the skill on in your skills list.

Team and Enterprise owners may need to allow user-created skills first. Anthropic's guide is [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

### Claude Code

Add this repository as a plugin marketplace and install the plugin:

```
/plugin marketplace add Dr-Titus100/titus-humanizer
/plugin install titus-humanizer@titus-humanizer
```

You can also copy the skill folder in by hand:

```
git clone https://github.com/Dr-Titus100/titus-humanizer.git
cp -r titus-humanizer/skills/titus-humanizer ~/.claude/skills/
```

### ChatGPT

In the ChatGPT app, go to Skills, select Create, then select "Upload from your computer" and choose `titus-humanizer.zip`. OpenAI lists skills for Business, Enterprise, Healthcare and Edu workspaces, and a workspace admin may need to turn them on. OpenAI's guide is [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt).

### Codex

Codex loads skills from `~/.agents/skills` in your home folder, or from `.agents/skills` inside a project:

```
git clone https://github.com/Dr-Titus100/titus-humanizer.git
mkdir -p ~/.agents/skills
cp -r titus-humanizer/skills/titus-humanizer ~/.agents/skills/
```

OpenAI's guide is [Build skills](https://developers.openai.com/codex/build-skills).

### A Custom GPT, or any other chat assistant

If your plan doesn't support skills, build a Custom GPT:

1. Paste the contents of [chatgpt/gpt-instructions.md](chatgpt/gpt-instructions.md) into the Instructions field. It fits within the 8,000-character limit.
2. Upload [SKILL.md](skills/titus-humanizer/SKILL.md) and [titus_tools.py](skills/titus-humanizer/scripts/titus_tools.py) as Knowledge files.
3. Turn on Code Interpreter under Capabilities, so the GPT can run the cleanup and the score.

For Gemini, Copilot or another assistant, paste the contents of `SKILL.md` at the start of a chat or into the assistant's custom instructions. Without a way to run Python, the assistant applies the rules by hand and reports the score as not available.

## Repository layout

```
titus-humanizer/
├── skills/titus-humanizer/
│   ├── SKILL.md                      the rules and workflow
│   └── scripts/titus_tools.py        hidden-character cleanup and the AI-pattern score
├── .claude-plugin/                   Claude Code plugin and marketplace files
├── chatgpt/gpt-instructions.md       short instructions for a Custom GPT
├── tests/                            checks for the script, with resume and prose examples
├── .github/workflows/tests.yml       runs the tests on every push and pull request
├── .github/workflows/release.yml     builds titus-humanizer.zip for each release
├── CHANGELOG.md
└── LICENSE
```

The skill folder holds everything the skill needs. The plugin files point to it and the release workflow zips it, so a change to the rules or the script happens in that folder only. The script uses only the Python standard library. The release zip leaves out `tests/`.

## Sources

The rules draw on three sources.

- Professional writing standards for editing AI-generated text: a five-category taxonomy of weak wording (awkward, flowery, vague, unnecessary and illogical) and a set of AI-isms that always count as problems. All of the skill's examples are original.
- Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), which WikiProject AI Cleanup maintains. The skill paraphrases its patterns and copies no text from it.
- Russell, Rajendhran, Pham, Iyyer and Wieting, [StoryScope: Investigating idiosyncrasies in AI fiction](https://arxiv.org/abs/2604.03136) (COLM 2026). The study compared 10,272 human-written stories with stories that five models wrote from the same prompts, and it supplies the story-level patterns and the percentages quoted in Part 6 of the skill.

## Contributing

Issues and pull requests are welcome. Make every change on the `dev` branch, and open pull requests against `dev`. Changes go to `main` only after the tests pass on `dev`. A useful report includes a before-and-after pair: a draft, the skill's output, and what you expected instead. A new rule fits best when it comes with an example of the pattern and its plainer version.

If you change `scripts/titus_tools.py`, run the tests first:

```
python3 -m unittest discover -s tests
```

When a change moves a score or a pattern count, the tests print a diff of the old and new output, and `python3 tests/update_expected.py` saves the new output for your pull request. A bug report that names a fixture and a line, such as `tests/fixtures/resume/ai_resume.txt` line 15, is the quickest to fix. [tests/README.md](tests/README.md) explains the examples and how to add one.

## License

[MIT](LICENSE), © 2026 Titus Nyarko Nde.
