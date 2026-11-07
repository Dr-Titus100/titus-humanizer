# titus-humanizer

titus-humanizer is an editing skill for Claude and ChatGPT. It rewrites text so it reads like a careful, plain-spoken person wrote it, and it keeps every fact, number and name from the original. It can also review a draft and list each AI-writing pattern it finds, with a plainer version of each line.

It works on emails, reports, slide decks, papers, cover letters, personal statements, blog posts and fiction.

## What it changes

**Before:**
> In today's fast-paced digital landscape, our new onboarding checklist isn't just a tracker — it's a gateway to a more seamless experience, fostering alignment and driving meaningful impact.

**After:**
> The new onboarding checklist shows new hires which setup steps they have finished.

**Before (email):**
> I hope this message finds you well! I wanted to reach out to touch base regarding the proposal, which was reviewed by our team last week. It's not just a budget request — it's a roadmap for sustainable growth. Please let me know if you have any questions!

**After:**
> Our team reviewed the proposal last week. It sets out the budget we're requesting and what it would cover. I'm happy to walk you through the numbers.

**Before (story):**
> Elena stood at the window as the rain fell, mirroring the storm inside her. Her chest tightened, ice crawled down her spine, and the scent of wet earth and old memories filled her lungs. She realized, at last, that letting go was not the same as forgetting. It was a way of carrying him with her.

**After:**
> Elena stood at the window and watched the rain. She was afraid. She decided she could let him go without forgetting him.

None of the rewrites add facts. When a draft is vague and the details aren't available, the skill writes the plainest honest sentence and, in notes mode, says which detail would help.

## How it works

The skill checks a draft at three levels and fixes what it finds.

1. Seven hard rules for patterns that never appear in the output. They cover em dashes and semicolons, "it's not X, it's Y" framing, passive voice that hides who acted, command-style slide titles, slogans, hedges such as "illustrative" on real numbers, and chatbot phrases such as "I hope this helps".
2. Judgment calls on wording, sorted into five categories: awkward, flowery, vague, unnecessary and illogical. Each category comes with a test, such as "would you say this out loud to a colleague?", and graded examples of text that passes and text that fails.
3. Story-level patterns for narrative and reflective writing. AI-written stories tend to state their moral, show fear through a stack of body sensations, make the weather match the mood and tie up every thread. The skill cuts these, keeps the writer's real names and odd details, and suggests bigger structural changes without making them unless you ask.

Each rewrite ends with a self-check against the original, so no fact, number, name or real qualification goes missing.

The skill aims at clear, specific writing. It makes no promise about how any AI detector will score the result.

## Using it

Once it's installed, ask in plain words. The skill loads when the request fits.

| You ask | You get |
| --- | --- |
| "Humanize this:" followed by your text | The rewritten text and nothing else |
| "Rewrite this and tell me what you changed" | The rewrite, then a short list of what changed and why |
| "Does this sound like AI?" or "Review this" | A list of problems, each quoted with its location, category and a plainer version |
| "Do a deeper rewrite of this story" | A rewrite that may also reorder or trim scenes, using only material already in the draft |

## Installation

Each release on the [Releases page](https://github.com/Dr-Titus100/titus-humanizer/releases) includes `titus-humanizer.zip`. The same zip works in claude.ai, the Claude desktop app and ChatGPT. Upload it as it is, without unzipping it.

### Claude (claude.ai and the desktop app)

1. In Settings, open Capabilities and turn on "Code execution and file creation". Skills need it.
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
2. Upload [skills/titus-humanizer/SKILL.md](skills/titus-humanizer/SKILL.md) as a Knowledge file.

For Gemini, Copilot or another assistant, paste the contents of `SKILL.md` at the start of a chat or into the assistant's custom instructions.

## Repository layout

```
titus-humanizer/
├── skills/titus-humanizer/SKILL.md   the skill itself
├── .claude-plugin/                   Claude Code plugin and marketplace files
├── chatgpt/gpt-instructions.md       short instructions for a Custom GPT
├── .github/workflows/release.yml     builds titus-humanizer.zip for each release
├── CHANGELOG.md
└── LICENSE
```

`SKILL.md` holds all the rules. The plugin files point to it and the release workflow zips it, so a change to the rules needs an edit in that one file only.

## Sources

The rules draw on three sources.

- A set of AI-writing grading guidelines: writing quality instructions, a five-category taxonomy of weak wording, a list of AI-isms and hundreds of graded calibration examples.
- Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), which WikiProject AI Cleanup maintains. The skill paraphrases its patterns and copies no text from it.
- Russell, Rajendhran, Pham, Iyyer and Wieting, [StoryScope: Investigating idiosyncrasies in AI fiction](https://arxiv.org/abs/2604.03136) (COLM 2026). The study compared 10,272 human-written stories with stories that five models wrote from the same prompts, and it supplies the story-level patterns and the percentages quoted in Part 6 of the skill.

## Contributing

Issues and pull requests are welcome. A useful report includes a before-and-after pair: a draft, the skill's output, and what you expected instead. A new rule fits best when it comes with an example of the pattern and its plainer version.

## License

[MIT](LICENSE), © 2026 Titus Nyarko Nde.
