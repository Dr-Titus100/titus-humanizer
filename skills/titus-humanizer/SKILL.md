---
name: "titus-humanizer"
description: "Rewrites text so it reads like a careful, plain-spoken person wrote it, removing AI-writing patterns at the word, sentence and story level while keeping every fact. Cleans hidden characters, scores AI-writing patterns from 0 to 1 before and after, and reviews drafts on request. Use when the user asks to humanize, polish, rewrite, de-slop or check writing for AI patterns, including emails, reports, slides, resumes, essays and stories."
---

# titus-humanizer

This skill makes writing read like a careful, plain-spoken person wrote it. The rules come from professional writing standards for editing AI-generated text (a five-category taxonomy of AI-slop wording and a set of AI-isms that are always flagged), Wikipedia's "Signs of AI writing" page, and the StoryScope study of AI fiction (Russell et al., COLM 2026), which found that AI writing shows in what it chooses to say and how it shapes a story, as well as in its word choice. One question applies to every sentence: **would a plainer, more specific version say the same thing better?**

## Default behavior

- **Text pasted with no other instruction:** return the rewritten text, then the short report from Part 7 (the before and after scores, the patterns left, and the hidden characters removed). Nothing else: no preamble ("Here's a polished version"), no closing offer ("Let me know if..."), no list of changes.
- **The user asks what changed, or for notes:** after the rewrite, add a short list. Each item quotes the original words, names the problem, and gives the fix.
- **The user asks "does this sound AI?", "find the slop", or wants a review:** use Review mode (near the end of this file).
- **Keep the substance.** Every fact, number, name, date, citation, technical term and real qualification survives. Never invent sources, figures or specifics to make vague text concrete. If a sentence can't be made specific without information you don't have, write the plainest honest version. In notes mode you can also say what detail would help.
- **Leave quoted text as it is.** Words inside quotation marks, block quotes (lines that start with >), epigraphs and quoted titles stay exactly as written, with their own wording, spelling and punctuation, even when they break a rule in this file. This holds whoever wrote them: a source, a colleague, a customer or the writer. It covers quoted messages, emails and feedback, and the dialogue in a story. Rewrite only the text around a quote, and keep each quote where it was, with its attribution. If a quote has a problem (a typo, a line of dialogue that reads like a debate), point it out in notes or review mode and change it only if the user asks. The hidden-character cleanup in Part 0 still runs inside quotes, because those characters aren't part of the quoted words.
- **Match the register and the person.** A casual text stays casual, a formal letter stays formal. Keep the writer's point of view (first person stays first person) and their spelling variety. The result is usually shorter than the original, never padded.

## Workflow

1. Clean hidden characters from the user's text first (Part 0) and score the original (Part 7), so the rewrite starts from clean text and you know which patterns to look for.
2. Read the whole text. Work out the audience, purpose, format (email, slide, paper, post) and register.
3. Find problems in this order: hard rules (Part 1), the five taxonomy categories (Part 2), substance and tone (Part 3), vocabulary (Part 4), structure (Part 5). If the text tells a story or reflects on an experience (fiction, personal statements, narrative essays, blog posts, speeches, anecdotes in a cover letter), also check the narrative tells in Part 6.
4. Rewrite sentence by sentence, choosing the plainest accurate wording.
5. Run the self-check near the end of this file and fix anything it catches.
6. Score the rewrite and run the cleanup on it (Part 7). If the after score is still "high", or any Part 1 pattern is left, do one more pass on the flagged spots only. Then deliver the text with the report.

## Part 0. Hidden-character cleanup

Text copied from AI tools, PDFs, web pages and word processors often carries characters you can't see. Some of these are zero-width spaces, stray byte-order marks, soft hyphens, text-direction controls and invisible tag characters. Others are odd spaces (non-breaking, thin, ideographic) and look-alike letters, such as a Cyrillic "а" inside an English word. They break search, spell-check, word counts and pasting into forms, and some tools treat them as a sign of machine-generated text. This step removes them. It's text hygiene for the user's own writing.

**What to remove or fix**
- **Zero-width and invisible marks:** zero-width space (U+200B), word joiner (U+2060), byte-order mark (U+FEFF), soft hyphen (U+00AD), invisible math operators (U+2061–2064), Mongolian vowel separator (U+180E), Hangul fillers (U+115F, U+1160, U+3164, U+FFA0).
- **Zero-width joiner and non-joiner** (U+200D, U+200C) when they sit between ordinary Latin letters or spaces.
- **Text-direction controls:** U+202A–202E, U+2066–2069, U+200E, U+200F, U+061C.
- **Invisible tag characters:** U+E0000–E007F.
- **Variation selectors** (U+FE00–FE0F, U+E0100–E01EF) that don't follow an emoji.
- **Private-use characters and non-characters.**
- **Unusual spaces:** non-breaking, narrow non-breaking, en/em/thin/hair spaces (U+2000–200A), U+205F, U+3000, U+1680. Replace each with a normal space.
- **Look-alike letters:** Cyrillic or Greek letters that look Latin, inside words that are otherwise plain English. Replace them with the Latin letter.

**What to keep**
- Emoji sequences. The joiners and variation selectors inside 👨‍👩‍👧 or ❤️ are part of the emoji.
- Joiners inside Arabic, Persian, Hindi and other scripts that need them for correct spelling.
- Real text in other alphabets. A Russian or Greek word stays exactly as written.
- Anything inside code, commands, URLs, file paths and identifiers.
- Required disclosures and labels, which are visible text and never part of this cleanup.

**How to run it.** When a code tool is available (a shell or Python), use the `clean` command of `scripts/titus_tools.py` in this skill's folder. Run it on the original text and again on the finished rewrite. The Part 7 report lists what it removed. When no code tool is available, retype the text in the rewrite and don't copy characters across, and say in the report that the script couldn't check hidden characters this time. For Word files or PDFs, extract the text first and clean the extracted text. For a .docx the user wants back as a .docx, clean the text inside it and keep the formatting.

**Be honest about what this does.** It removes invisible and look-alike characters. That's all. It doesn't remove statistical watermarks from AI models, it doesn't strip metadata from files, and it can't prove that a person wrote the text. Never describe the result as "undetectable" or "proven human".

## Part 1. Hard rules (never appear in the output)

These patterns count as AI-isms every time they appear, whatever the context. Don't produce them, and remove them from the user's text. Quoted text is the exception. A quotation keeps its own wording and punctuation, semicolons and dashes included (see Default behavior).

**1. Punctuation.** No em dashes (—). No hyphens or en dashes used as dashes to set off an aside or a break ("X - and Y - Z"). No semicolons. No inline dot separators (• · ●) between items on one line. No vertical bars ( | ) as separators. No arrows (→, ->, >, ⇒) in prose, titles or labels.
- Still fine: hyphens inside compound words ("well-written"), commas, periods, question marks, parentheses.
- **Ranges are fine,** with or without spaces around the dash: "pages 5–10", "2019–2021", "Jul 2020 – Jun 2021", "May 2019 - Aug 2019", "2018 – Present", "Fall 2018 – Spring 2020", "Q1 – Q3". A dash only counts as a break when it sets off an aside or joins two clauses, as in "closed in 2020 – and nobody noticed".
- **Bullets at the start of a line are fine** (•, ●, ▪, - or *). They're list markers, as on a resume. The inline-dot rule covers only symbols used between items on the same line, as in "Python • SQL • R". Write those as a comma list ("Python, SQL and R").
- Fix by splitting into two sentences, using a comma with "and", "but", "so" or "because", or using parentheses for a true aside.
- Use colons sparingly. One colon that introduces a real list or a definition is fine. Avoid colon-driven rhythm: "Label: fragment" lines ("Interns: shadow a mentor. Managers: sign off weekly. Everyone: log hours by Friday."), lead-ins such as "Key idea:", "Bottom line:" or "Why it matters:", and colon reveals ("The answer: simplicity").

**2. Reject-then-assert framing.** Any sentence that rejects one thing to assert another, in either order, including across two sentences:
- "It's not X, it's Y", "Do Y, not X", "not just X, but Y", "not only X but also Y", "no X, no Y, just Z", "Y rather than X", "This app isn't just a budget tracker - it's a path to financial freedom", "Customer support is not a cost center. It's the heart of the brand."
- Fix: state the positive claim directly ("The app sorts spending by category and flags bills that are due soon"). When a real correction is the point, state both facts plainly as two statements instead of staging a contrast.

**3. Passive voice.** Name who did the action. "The budget was approved by the board" becomes "The board approved the budget." "The duplicate records were already flagged as invalid" becomes "The import script had already flagged the duplicate records as invalid." Watch for it in technical and methods writing, where it hides easily (in research writing, "we" usually works). Sentences that describe a state are fine ("The office is closed", "The data are noisy"). If the actor is truly unknown, choose a subject the context supports, never an invented one.

**4. Imperative titles.** Slide, page and document titles describe the content or state the finding. They don't give commands. "Fix the intake backlog before hiring more staff" becomes "Intake backlog and staffing needs". Labels follow the same rule: "CUT COSTS NOW" becomes "Planned cost reductions". This applies only to titles. Instructions in a how-to body, or an email asking someone to do something, can use commands normally.

**5. Slogan-like phrasing.** Taglines and buzzword formulas that sound finished but leave nothing a reader could check:
- Rhythm fragments: "One lab. One mission. Endless discovery.", "Costs are up. Output isn't.", "Plan early. Finish strong.", "Always curious, always growing", "Many teams. One campus."
- Buzzword formulas: "turns every patient visit into a long-term loyalty engine", "delivered speed, scale and confidence by unifying the data stack", "converts research spending into compounding impact", "From scattered spreadsheets to a single source of truth."
- Fix: say what happens, with the mechanism or number.

**6. Illustrative hedging.** Never describe a number, chart or visual as "illustrative", "for reference only", "for discussion only", "directional", "sample", "placeholder" or "approximate" because its values aren't supported. Use the real figure with its source and unit, or describe plainly what the data is ("Figures from the 2024 department survey").

**7. Chatbot residue.** No "Certainly!", "Great question", "I hope this helps", "Let me know if you'd like...", "Here is a...", "Below is a polished rewrite", "As an AI", knowledge-cutoff notes, or unfilled template placeholders that the writer didn't put there.

## Part 2. The five taxonomy categories (judgment calls)

Each category applies at three levels: single **words**, **phrases**, and standalone **labels** (headings, column heads, chart titles, tags). A one-word label gets the same scrutiny as a full sentence. One phrase can fit several categories.

**A. Awkward or unnatural wording.** Test: would you say this out loud to a colleague? The words are understandable but assembled mechanically.
- "Campus dining has become more intentional and value-forward." Say "more focused on price".
- "Enrollment softened over the period." Say "decreased".
- "Costs trended upward", "Turnover came in lower", "lift the expense base", "Attendance closed the semester at a reduced level". Say "rose", "fell", "raise expenses", "Attendance fell during the semester".
- Nouns forced into adjectives: "REMOTE-FIRST LEARNER" becomes "Students who study mostly online".
- Syntax inversion: "Only through regular calibration can the sensor produce reliable readings" becomes "The sensor gives reliable readings only when it's calibrated regularly."
- Odd metaphors: "shoppers are voting with their thumbs", "the survey is doing the heavy lifting here" (say "Most of the evidence comes from the survey").
- Odd renderings: "fiscal year twenty twenty-four" becomes "FY2024".

**B. Excessive or flowery wording.** Test: say it in the plainest words you have. If nothing is lost, the original was decoration.
- "strategically orchestrate a dynamic constellation of interdisciplinary competencies that collectively empowers the attainment of elevated results" becomes "bring together people with different skills to get better results".
- "Igniting Collaborative Brilliance" becomes "Team Projects". "A fundamentally recalibrated attendance baseline" becomes "A lasting drop in attendance". "high-end premium laptops" becomes "premium laptops".
- Stacked jargon: correct terms crammed together until the meaning blurs ("cloud-native containerized microservice orchestration capabilities", "agile cross-functional delivery pods").
- Consultant verbs standing in for a plain one: "convert insights into aligned action", "activate the roadmap", "socialize the findings", "drive promising ideas toward scale".

**C. Vague or empty wording.** Test: ask which product, which metric, which outcome. If the text can't answer, the words are empty. Vague lines could sit unchanged in a completely different document.
- "Revenue grew 12% in 2024, with broad-based gains across regions" becomes "with gains in every region" (or name the regions, if the source does).
- "protect the core" becomes "protect the main product line", when that's what the core means. "Key Success Enablers" becomes "Hiring and Training Results", when that's what the section covers. "Smart engagement improves retention" becomes "Weekly check-in emails improve retention", when that's the program.
- Incomplete phrasing: "Shared dashboards improve visibility" (visibility of what, and for whom?).
- Missing causal link: "Cost and convenience lead bike-share use" becomes "Cost and convenience are the main reasons people use bike-share".
- Paired nouns that don't belong together ("speed and community", "safety and growth"), so the reader can't tell which one is meant.

**D. Unnecessary wording.** Test: delete it and reread. If the meaning survives, it did no work.
- Redundant modifiers: "past history", "advance planning", "sudden unexpected spike", "total combined enrollment across all campuses", "delay or postpone the decision".
- Empty tails: "to capture the full picture", "that drives lasting value", "ensuring a frictionless experience".
- Decorative labels: "THE NEXT CHAPTER", "FORWARD MOMENTUM", "UNLEASHING GROWTH", and unrequested tags such as "STRICTLY CONFIDENTIAL" or "Draft for internal alignment".
- Subtitles or headers that repeat the title.
- Framing lead-ins: "Why it matters:", "Bottom line:", "Key takeaway:", "It's worth noting that", "It is important to remember that".
- Unrequested disclaimers: "This overview is not a substitute for a full legal review."

**E. Illogical wording.** Test: restate it as a plain fact. If you have to choose between two readings, it fails.
- "Hire, learn and promote the strongest candidates" (you can't "learn" a candidate) becomes "Hire, train and promote the strongest candidates".
- "62% Ridership back to 2019" becomes "Ridership has recovered to 62% of its 2019 level".
- "Enrollment Gain Loss Shift" becomes "Enrollment Loss".
- "Seed adjacent capabilities that can widen the base" becomes "Build related services that reach more customers", when that's what "widen the base" means.

## Part 3. Substance and tone

- **Inflated significance.** Turning ordinary facts into claims about legacy, pivotal moments, broader trends or "an evolving landscape" ("stands as a testament", "plays a vital role", "marks a shift", "indelible mark", "deeply rooted", "setting the stage for"). State the fact. Explain why it matters only when there's a concrete consequence.
- **Promotional or travel-guide tone.** Unrequested praise and reflexive adjectives: vibrant, rich, renowned, groundbreaking, nestled, in the heart of, boasts, diverse array, commitment to, world-class, cutting-edge, seamless.
- **Vague authorities.** "Experts argue", "observers note", "research consistently shows", "several sources suggest", "industry reports". Name the source or drop the claim. Never call one source "several".
- **Tacked-on -ing clauses.** Sentence-final ", highlighting...", ", underscoring...", ", ensuring...", ", reflecting...", ", contributing to...", ", fostering...". Delete them, or turn them into a real sentence with evidence.
- **Empty abstraction.** "This initiative creates synergy, sparks alignment, and drives real impact." Name the observable change instead ("The new form cuts the approval steps from three to two").
- **Process instead of reason.** "After extensive stakeholder consultation, we landed on a revised approach" tells the reader nothing about why. When the writer knows the reason (here, that the sensors won't arrive until April), state it: "We moved the launch to May because the sensors won't arrive until April." When the reason isn't available, ask for it in notes mode and don't invent one.
- **Synthetic balance.** "While online classes offer convenience, they also come with unique challenges." Keep a contrast only when there's a real, named tradeoff.
- **Canned empathy.** "I truly understand how stressful and overwhelming this must be for you." If acknowledgment is needed, make it short and specific.
- **Canned endings.** "In conclusion", "Overall", "Ultimately", generic "challenges and future outlook" paragraphs, and closing recaps. End on the last real point.
- **Copula avoidance.** "serves as", "stands as", "functions as", "boasts", "features", "offers" where "is", "are" or "has" works.
- **Vague association.** "was associated with leadership of ExampleCorp" becomes "was CEO of ExampleCorp" when you know the relationship.
- **Reflexive lists.** Habitual triads of adjectives or abstract nouns ("bold, fresh and inspiring", "clear, concise and compelling") and long rhythmic catalogues added after the point is made. Real lists of three things are fine.
- **Over-hedging.** Keep only uncertainty that matches a real unknown. "It might perhaps be worth exploring whether we could potentially move the deadline" becomes "We could move the deadline."
- **Bureaucratic wording.** "All relevant parties should be notified of the procedural ramifications of this change" becomes "Tell the people affected what will change for them." "At the present moment, it would be prudent to initiate a review of the policy" becomes "We should review the policy now."
- **Compressed or indirect meaning.** "Capacity remains bounded by a dual seat-and-ratio constraint" becomes "The number of seats and the required staff-to-student ratio limit capacity."
- **Oversimplification.** Never cut a qualifier that carries meaning. "When to stop funding the pilot program" must not shrink to "When to stop".

## Part 4. Vocabulary that signals AI writing

These words are a strong tell when several cluster together or when they decorate a sentence instead of carrying meaning. Prefer the plain alternative. Literal uses are fine (an actual landscape, an underscore character, a real journey).

- **Classic AI words:** delve, tapestry, testament, pivotal, crucial, vital, underscore, showcase, highlight (for importance), foster, cultivate, intricate, interplay, landscape, realm, navigate (figurative), embark, journey (figurative), meticulous, vibrant, enduring, garner, bolster, boasts, align with, resonate, enhance, robust, seamless, holistic, synergy, multifaceted, transformative, groundbreaking, game-changer, paradigm shift, nestled.
- **Business filler:** leverage, harness, unlock, elevate, empower, streamline (when vague), operationalize, drive impact, value creation, best-in-class, actionable insights, key stakeholders.
- **Newer-model tics:** quietly, steady, dependable, echoed, clearer, practical, prioritize, "this matters because", universally.
- **Stock openers and connectors:** "In today's fast-paced world", "When it comes to", "At the end of the day", "First and foremost", "It's important to note", and Additionally, Moreover, Furthermore or Notably repeated at the start of sentences.
- **Inflated swaps:** utilize (use), facilitate (help), commence (start), in order to (to), at this point in time (now), each and every (each), end result (result), whether or not (whether, when "or not" adds nothing).

## Part 5. Structure and formatting

- **Start with the point.** No scene-setting, no restating the request, no meta-announcements.
- **Use the lightest structure that works.** Don't spread a two-sentence answer across headings and bullets.
- **Avoid mechanical bullets.** No "**Label:** explanation" bullets unless the user asked for them or the content really is reference material.
- **Keep emphasis light.** No bold scattered through the text and no emoji as decoration.
- **Headings follow the venue's convention.** Use sentence case by default.
- **Quotes:** use straight quotes and apostrophes in plain text.
- **Vary rhythm naturally.** Removing dashes and semicolons shouldn't turn the text into a string of identical short sentences, because that monotony is now an AI tell too. Mix short and longer sentences, joined with "and", "but", "because", "which" or "so". Vary how sentences open.
- **Repeat the right word.** Don't swap in synonyms just to avoid repetition. Use the same term for the same thing.

## Part 6. Narrative and meaning-level tells (from StoryScope)

The StoryScope study ([arXiv 2604.03136](https://arxiv.org/abs/2604.03136)) compared 10,272 human-written short stories from Books3 with stories that five models (Claude Sonnet 4.6, GPT-5.4, Gemini 3 Flash, DeepSeek V3.2 and Kimi K2.5) wrote from prompts based on those stories. A classifier that used only narrative features, with style features withheld, separated AI from human stories at 93.2% macro-F1. When Gemini rewrote 278 of its own stories to remove clichés, purple prose and redundant exposition, detection fell only from 95.5% to 93.9% macro-F1. So for any text that tells a story or reflects on an experience, fixing sentences isn't enough. The tells below sit in what the text chooses to say. Figures in brackets are how often each pattern appeared in AI stories compared with human ones.

**Two levels of change.** Most items below change only the wording, and you can fix them in any default rewrite. A few would change the content (adding a subplot, reordering the timeline, changing an ending). Those are marked **structural**. Don't make structural changes unless the user asks for a deeper rewrite. In notes or review mode, suggest them. Even in a deeper rewrite, only reorder or trim the writer's existing material. Never invent events, characters, references, brands or places.

### 6A. Over-explaining the meaning

AI spells out what a human writer would leave the reader to infer.

- **Narrators who explain the theme outright** (AI 77% vs human 52%). "Grief, she understood now, was only love with nowhere left to go." "And so he learned that true wealth is measured in friendships." End on the event, the image or the decision, and cut the aphorism that explains it. If the realization is itself a plot event, state it plainly as an action ("She decided she could let him go without forgetting him"). In a personal statement or reflective essay that genuinely needs reflection, keep one concrete sentence about what changed ("I now check every dataset for duplicates before I start"), never a life-lesson aphorism.
- **Moralizing and philosophical weighting.** The text keeps stopping to ponder big questions (what it all means, whether people can change). Cut the pondering unless it is the point of the piece.
- **Dialogue used as philosophical debate** (59% vs 34%). "'Do you think we're defined by our choices or our regrets?' 'Perhaps they are the same thing.'" Make dialogue do work: argue about something specific, dodge, misunderstand, joke, move the plot. If the debate is the writer's content, keep the ideas and make the lines sound like people talking. Dialogue is quoted text, so in a default rewrite, suggest these changes in the notes and leave the lines as written, unless the user asks you to rewrite the dialogue.
- **Everything serves the theme.** Every detail, subplot and image points at one central idea. Let some details just be details. Don't add thematic echoes, and don't rewrite the writer's neutral details to make them symbolic.
- **Vague allusions instead of named references** (72% vs 50%). "Like a figure from some half-remembered myth." If the writer clearly means a specific work, person or event and names it elsewhere, name it here. Otherwise cut the allusion. Never supply a name the writer didn't give.

### 6B. Over-writing the body and the senses

- **Emotion shown through body sensations** (81% vs 38%). "Her throat closed. Ice crawled down her spine. Her heart hammered against her ribs." Humans name feelings plainly far more often (29% vs 8%). Replace stacks of body sensations with the plain emotion ("She was terrified") or one concrete action. One body cue is fine. A string of them is the tell. This reverses the usual "show, don't tell" advice, so don't add body-sensation imagery that isn't there.
- **Setting that mirrors the mood.** "Outside, the storm raged, as restless as the thoughts inside him." Rain at the funeral, the lamp dimming as hope fades. Cut the mirroring link. Weather and rooms can simply be what they are.
- **Smell-heavy, dense sensory description** (smell 82% vs 57%). "The air smelled of rain, old paper and something like regret." Keep the senses that matter to the moment and drop decorative ones, especially smells added for atmosphere and abstract nouns used as scents.
- **Tacked-on nature and ecology.** Moss, birds, seasons and "the earth" turning up in scenes where they do no work. Trim them.
- **Constant access to thoughts.** Every action comes with an explanation of what the character felt and why. Let some actions stand without commentary.

### 6C. Tidy, single-track structure

- **One straight causal chain with no loose ends.** Each clue leads to the next, in order, from the first scene to the reveal. **Structural.** Suggest letting a thread stay open or telling events out of order.
- **Endings resolved by the hero's choice and inner acceptance** (choice 69% vs 46%, internal understanding or acceptance 47% vs 27%). "She finally made peace with who she was." Remove the summary of inner peace and end on what happened. **Structural** if the ending itself would change. Humans more often leave endings open or let outside events settle them.
- **No subplots, or every subplot mirrors the main theme** (no subplots 79% vs 57%). **Structural.** Suggest only.
- **Linear time.** AI rarely uses flashbacks, time jumps, delayed reveals or twists that change the meaning of earlier scenes. **Structural.** If asked for a deeper rewrite, opening on a later moment and moving back to it, using the writer's own scenes, is the main human move.
- **A character introduced with a paragraph of appearance** (52% vs 30%). "Dr. Mara Quinn was a tall woman with silver-streaked hair and sharp green eyes that missed nothing." Introduce people through what they say or do, and spread the physical details the draft provides across the scene instead of front-loading them.
- **An establishing-shot opening and over-precise space.** "The small coastal town of Port Haven sat at the edge of a gray, restless sea." Start closer to the action or the first line of dialogue that the draft already has. Cut room-by-room layout that the story doesn't need.
- **A long warm-up before the trouble starts.** Pages of contentment before the inciting event. Trim the warm-up and get to the problem sooner.
- **Morally clear characters** (humans show ambivalent protagonists 59% vs 38%). Don't add judgments that tell the reader who was right. Keep the moral ambiguity the writer wrote.
- **Front-loaded context and long wrap-ups.** Explaining everything up front, then a long epilogue or "Years later..." coda that ties every thread. Trim explanation the reader can work out, and end closer to the climax. Removing an epilogue counts as **structural**.

### 6D. Generic sameness

AI stories cluster in one narrow region of "narrative space". Human stories are rarer and more varied.

- **Keep the writer's specifics.** Real names, places, brands, books, songs and dates read as human. AI avoids naming real things. Never turn "the Starbucks on Broadway" into "a coffee shop" or "*Things Fall Apart*" into "a classic novel".
- **Keep the writer's odd choices.** Don't smooth unusual details, unexpected turns or an off-beat structure into the safe default. If the draft is the less obvious version, it's the more human one.
- **Keep the writer's asides to the reader.** In informal pieces, essays and blogs, a direct word to the reader is a human trait (28% vs 7%). Don't remove it. In formal writing, follow the venue's norms.
- **Watch for model habits.** Each model has its own pattern:
  - Claude: flat tension, quiet endings with an epilogue or flash-forward, an eerie mood.
  - GPT: rumor and gossip driving the plot, and a narrator looking back "years later".
  - Gemini: bleak, oppressive settings and very tidy endings with long wrap-ups.
  - DeepSeek: a visible narrator, the important background given up front, cyclical seasons.

  When several of these show up in one draft, the text is leaning on model defaults. Use the 6A–6C fixes on them.

### Where Part 6 applies

- **Fiction and creative writing:** all of Part 6.
- **Personal statements, narrative essays, blog posts, speeches:** 6A, 6B and 6D fully. Use 6C mainly for openings, endings and warm-ups.
- **Emails, reports, slides, technical writing:** mostly the moral-closer and specifics rules (6A stated lessons, 6D keep the writer's specifics). The other parts rarely apply.

## Part 7. AI-pattern score and report

The script gives every text a score from 0 to 1 for how strongly it shows the patterns this skill removes. Use it to check the work and to show the user what changed.

**What the score measures**
- **Pattern density.** Weighted hits per 100 words for the patterns in Parts 1 to 6 that a script can find reliably: dashes used as breaks (date and number ranges don't count), semicolons, arrows, bars and dots between items on the same line (bullets at the start of a line don't count), reject-then-assert framing, passive voice, slogans, illustrative hedging, chatbot residue, inflated significance, vague authorities, -ing tails, copula avoidance, canned endings, AI vocabulary, stock openers, bold-label bullets, and the StoryScope tells (stated lessons, body-sensation emotion, setting as mirror, decorative smells, tidy inner resolutions). This is the main part of the score. A text dense with these patterns scores high whatever else is true.
- **Rhythm.** How much sentence lengths vary. Very even lengths, or nearly every sentence falling between 8 and 20 words, push the score up. That catches the flat, chopped-up rhythm that over-edited text falls into.
- **Repeated openings.** Many sentences starting with the same word.
- **Word variety.** A small weight for vocabulary that sits in the narrow band typical of model output.

**How to read it**
- **0.60 to 1.00, "high":** many patterns or a flat rhythm. Rewrite fully.
- **0.35 to 0.59, "medium":** some patterns or uneven spots. Fix what the report lists.
- **0.00 to 0.34, "low":** few measurable patterns. Still apply the rules in Parts 1 to 6, because the script can't see everything (awkward phrasing, vague claims, illogical wording and most structural tells need judgment).
- **Under 30 words:** no score, only the pattern list. From 30 to 100 words the script dampens the score, and the report says so.
- **Code, quoted text, links, file paths and emoji aren't scored.** Patterns inside a quotation belong to the person quoted, so the script skips text in quotation marks and block quotes, as it skips code. It also skips links and file paths, so a word such as "robust" in `https://example.com/robust-guide` doesn't count, and emoji never count as words. The `score` command ends with a line such as "Left as-is and not scored: 2 quotations, 1 link and 1 emoji". A quotation needs an opening and a closing mark in the same paragraph, and the same rule applies to single and double quotes. The opening mark comes after a space, a bracket, a dash, another quote mark or the start of a line. The closing mark comes before a space, punctuation, a bracket, a dash, another quote mark or the end of a line. When one quotation sits inside another, the outer one counts. Marks that don't fit the rule stay in the score: apostrophes, as in "don't" or "the students' work", and inch or foot marks, as in "a 12" tablet" or "5' 11"".

**The score is a gauge, not a verdict.** It counts patterns. It doesn't measure quality or accuracy, and it isn't the output of GPTZero, Turnitin or any other detector, so never present it as one. A low score doesn't prove a person wrote the text. Never invent a score by hand: if no code tool is available, write "Score: not available (no code tool in this chat)" and keep the pattern checks manual.

**How to run it**
1. Save the user's original text to `original.txt`. In the commands below, `titus_tools.py` means `scripts/titus_tools.py` in this skill's folder.
2. Run `python3 titus_tools.py clean original.txt > cleaned.txt` and rewrite from `cleaned.txt`.
3. Save the rewrite to `rewrite.txt`, then run `python3 titus_tools.py report original.txt rewrite.txt`.
4. Use `python3 titus_tools.py score FILE` for a detailed breakdown of one text (density, rhythm, word variety, each pattern with an example).

**The report** goes under the rewrite, in plain lines like these:

> AI-pattern score: 0.80 (high) before, 0.22 (low) after
> Patterns before: AI vocabulary x11, inflated significance x2, tacked-on -ing clause x2, em dash x1, semicolon x1
> Patterns left after: none
> Hidden characters removed: 1 zero-width space

When the text has quotations, code, file paths, links or emoji, the report adds a line saying they came through unchanged, such as "Left as-is: 3 quotations, 1 code snippet and 1 link". Always keep that line, so the user can see those parts weren't touched. If the report has a "Changed in the rewrite" line, restore the items it names from the original and run the report again before you deliver.

If the rewrite had to drop something that carried meaning or rhythm, add one line saying what was lost, so the user can put it back. Keep the report this short in default mode. In notes or review mode, add the detailed `score` breakdown.

**On AI watermarks.** Some AI providers build statistical watermarks into word choice so readers and regulators can tell text came from an AI. This skill doesn't try to remove them and doesn't claim to. A full rewrite in the writer's own words changes wording anyway, but that's a side effect, and no tool here can check for a watermark. Never describe output as watermark-free, undetectable or proven human.

## Slide and label text

When the text is slide content:
- Titles describe the content or state the finding. "Two-thirds of respondents prefer evening classes" says more than "Survey results". Titles are never commands.
- Labels, column heads, legends and chart titles get the same checks as body text.
- Wording copied from a prompt or source isn't exempt. If it's slop, fix it.
- Keep standard domain terms (EBITDA, p-value, net leverage, "the server returns 404 when the page doesn't exist").
- A good slide makes one specific claim, shows the evidence behind it, and uses plain terms.

## Leave these alone

- Accurate technical terms, legal conditions, and uncertainty that comes with a stated reason: "The forecast is provisional because March data isn't in yet." "Either party may end the lease with 60 days' written notice."
- Claims backed by a concrete result, source or constraint: "The March safety inspection found nine blocked exits." "Finance must sign off before the purchase order goes out."
- Framing that narrows scope or helps navigation: "This note covers the two hiring decisions due Thursday."
- Parallel structure that separates a real list or logical relationship: "Green means the test passed, and red means it failed."
- Quoted text: quotations, block quotes, dialogue and quoted titles (see Default behavior).
- Plain sentences that are already fine. Don't rewrite for the sake of change. Lines like "Quarterly Enrollment by College", "Net margin is profit divided by revenue", "Train staff on the new booking system" (as a bullet in a plan) and "35% of respondents said they now shop online every week" need no edit.

## Self-check before delivering

1. Search the output, outside quoted text, for — – ; | → • and for " - " used as a dash. Remove every one that isn't a range (including spaced date ranges such as "Jul 2020 – Jun 2021"), a compound word or a bullet at the start of a line.
2. Search for "not", "n't", "rather than", "instead of", "just" and "only". Remove any reject-then-assert framing.
3. Search for a form of "to be" followed by a past participle (was approved, were delayed, is marked, been reviewed). Name the actor unless the sentence describes a state.
4. Check every title and label. Does any start with a bare command verb? Does any decorate without informing?
5. Check for Part 4 words used as decoration, -ing tail clauses, vague authorities and inflated significance.
6. Check the first and last sentences for framing, recaps, offers or chatbot residue.
7. Read it as the writer speaking to a colleague. Does each sentence say something specific? Does anything sound mechanical?
8. For narrative or reflective text, check Part 6. Look for:
   - a stated moral or life-lesson line
   - a stack of body sensations standing in for a named feeling
   - weather or rooms that mirror the mood
   - decorative smells
   - unnamed allusions
   - a character introduced by an appearance paragraph
   - an ending that sums up inner peace
   - specifics turned generic
9. Compare it with the original. Every fact, number, name, event and real qualifier is still there. You invented nothing and made no structural change unless the user asked for one. Every quotation matches the original word for word.
10. Run the Part 7 report on the original and the finished text. Confirm that the after score is lower, that no Part 1 pattern is left, that hidden characters are gone, and that text in other alphabets came through unchanged. The report's "Left as-is" line covers quotations, code, file paths, links and emoji. If it also has a "Changed in the rewrite" line, fix those items first.

## Review mode

Use this when the user wants a list of flags and no rewrite.

- Quote the exact words, say where they are (slide, paragraph or line number when one exists), name the category, explain in one sentence why it's a problem in this context, and give the plainer wording.
- Use these categories: the five taxonomy names (Awkward/unnatural, Excessive/flowery, Vague/empty, Unnecessary, Illogical) and the AI-isms (Punctuation, "It's not X, it's Y", Passive voice, Imperative title, Slogan-like phrasing, Illustrative hedging). For narrative or reflective text, also use the Part 6 names: Stated lesson, Philosophical dialogue, Over-unified theme, Vague allusion, Embodied emotion, Setting as mirror, Sensory overload, Tidy resolution, Linear single-track plot, Appearance-first introduction, Generic sameness. Name every category that applies, and mark structural suggestions as such.
- Write in the third person. Describe the text, not a reaction to it ("Paragraph 3 repeats the opening claim in different words", not "I don't like paragraph 3").
- When the text is long, group findings under: Formulas and slogans. Vague or unsupported claims. Wordiness. Framing and structure. AI-isms. General notes (accuracy gaps and a suggested rewrite of the weakest line).
- Start with the score line from `python3 titus_tools.py score`, then the findings. The script finds the countable patterns. Judgment finds the rest, so the findings list is always longer than the script's list.
- Note what already works, so it's clear what to keep.
- If the user brings back a revised draft, review the change: give the old and new scores, which findings are fixed, which remain (with the original quote), and which are new. New problems introduced by a revision are easy to miss, so flag them separately.

Example finding:
> Paragraph 2, "Customer support is not a cost center. It's the heart of the brand." This is the "It's not X, it's Y" AI-ism, because it rejects a claim nobody made to assert another. Plainer: "Customer support shapes how people see the brand."

## Worked examples

**Before:** "In today's fast-paced academic landscape, our new lab notebook template isn't just a form — it's a gateway to more reproducible science, fostering transparency and driving meaningful impact."
**After:** "The new lab notebook template gives every experiment the same structure, which makes results easier to reproduce."

**Before:** "Data is cleaned; models are trained; results are reviewed — and the paper moves forward."
**After:** "We clean the data, train the models and review the results before the paper goes out."

**Before:** "Research consistently shows that this robust method gives more stable estimates (Lee, 2022)."
**After:** "Lee (2022) found that the method gives more stable estimates."
(The source was already in the draft, so the rewrite names it. Without a source, cut the claim or ask for one.)

**Before:** "Ridership fell 45% between March and May 2020, then recovered slowly—ending 2023 still below its 2019 level."
**After:** "Ridership fell 45% between March and May 2020, then recovered slowly. At the end of 2023 it was still below its 2019 level."

**Before:** "A three-item touchpoint uses quick 1-5 ratings and one free-text prompt to capture the full picture."
**After:** "The three-question check-in uses a 1-5 scale and one open-ended question."

**Before (email):** "I hope this message finds you well! I wanted to reach out to touch base regarding the proposal, which was reviewed by our team last week. It's not just a budget request — it's a roadmap for sustainable growth. Please let me know if you have any questions!"
**After (email):** "Our team reviewed the proposal last week. It sets out the budget we're requesting and what it would cover. I'm happy to walk you through the numbers."
(The rewrite adds no facts. If the draft had named the amount or timeframe, those details would stay.)

**Before (story):** "Elena stood at the window as the rain fell, mirroring the storm inside her. Her chest tightened, ice crawled down her spine, and the scent of wet earth and old memories filled her lungs. She realized, at last, that letting go was not the same as forgetting. It was a way of carrying him with her."
**After (story):** "Elena stood at the window and watched the rain. She was afraid. She decided she could let him go without forgetting him."
(The rewrite removes the setting-as-mirror line, the stack of body sensations, the decorative smell, the reject-then-assert aphorism and the stated lesson. It keeps her decision, which is the actual event, and names the feeling the body cues pointed to. It doesn't invent a reason for her fear, because the draft gave none.)

## Script

`scripts/titus_tools.py`, in this skill's folder, has three commands: `clean`, `score` and `report`. It uses only the Python standard library, so it runs anywhere Claude or ChatGPT can run Python. If the file is missing, ask the user to install the full skill folder from https://github.com/Dr-Titus100/titus-humanizer.
