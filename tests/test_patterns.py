"""Each pattern in PATTERNS: one sentence it must catch and one it must leave alone.

Every label in PATTERNS needs an entry in CASES. A new pattern without one fails
test_every_pattern_has_a_case, so each rule arrives with its own example.
"""
import unittest

from support import tools

# label: (sentences the pattern must catch, sentences it must not catch)
CASES = {
    "em dash": (["The lab closed\u2014fast."], ["The lab closed fast."]),
    "dash used as a break": (
        ["The lab closed in 2020 - and nobody noticed.", "We shipped it \u2013 then it broke."],
        ["Jul 2020 \u2013 Jun 2021", "May 2019 - Aug 2019", "2018 \u2013 Present", "Fall 2018 \u2013 Spring 2020",
         "Q1 \u2013 Q3", "pages 5 - 10", "a well-written report", "2019\u20132021"]),
    "semicolon": (["We left; they stayed."], ["We left, and they stayed.", "Run `a = 1; b = 2` first."]),
    "arrow, bar or inline dot": (
        ["Python \u2022 SQL \u2022 R", "Plan \u2192 Build", "Home | About", "Draft -> Review"],
        ["\u2022 Built a dashboard in Tableau.", "- Ran fatigue tests.", "Python, SQL and R"]),
    "reject-then-assert": (["This isn't just a form, it's a gateway."], ["This form records each experiment."]),
    "not only / not just ... but": (["It is not only fast but also cheap."], ["It is fast and cheap."]),
    "rather than contrast": (["Use email rather than phone."], ["Use email."]),
    "passive voice (heuristic)": (["The budget was approved by the board."], ["The board approved the budget."]),
    "slogan fragment": (["One lab. One mission. Endless discovery."], ["The lab has one research goal."]),
    "illustrative hedging": (["These figures are illustrative."], ["These figures come from the 2024 survey."]),
    "chatbot residue": (["I hope this helps!", "Let me know if you need more."], ["I can send the full data."]),
    "inflated significance": (["The bridge stands as a testament to the town."], ["The town built the bridge in 1931."]),
    "vague authority": (["Experts say the method works."], ["Lee (2022) found that the method works."]),
    "tacked-on -ing clause": (["Sales rose 5%, highlighting strong demand."], ["Sales rose 5%."]),
    "copula avoidance": (["The room serves as a lab."], ["The room is a lab."]),
    "synthetic balance": (["While online classes offer convenience, they also present challenges."],
                          ["Online classes save commuting time."]),
    "canned ending": (["Done. In conclusion, the plan works."], ["Done. The plan cut costs by 8%."]),
    "over-hedging": (["We may potentially move the date."], ["We could move the date."]),
    "bureaucratic filler": (["We met in order to plan."], ["We met to plan."]),
    "AI vocabulary": (["Let's delve into the data.", "We leverage robust tools."], ["Let's look at the data."]),
    "stock opener": (["When it comes to budgets, plan early."], ["Plan budgets early."]),
    "sentence-initial connector": (["It rained. Moreover, it was cold."], ["It rained, and it was cold."]),
    "bold-label bullet": (["- **Speed:** fast"], ["- Fast enough for daily use"]),
    "stated lesson": (["She realized that home was people."], ["She called her sister."]),
    "emotion as body sensation": (["Her chest tightened.", "A chill ran down his spine."], ["She was afraid."]),
    "setting as mirror": (["The fog rolled in, mirroring the doubt inside him."], ["The fog rolled in."]),
    "decorative smell": (["The air smelled of rain."], ["It rained all night."]),
    "tidy inner resolution": (["He made peace with his past."], ["He sold the boat."]),
}


def labels_in(text):
    return {label for label, _, _ in tools.score(text)["patterns"]}


class EachPattern(unittest.TestCase):
    def test_every_pattern_has_a_case(self):
        missing = [label for label, _, _ in tools.PATTERNS if label not in CASES]
        self.assertEqual(missing, [], "add a CASES entry in tests/test_patterns.py for each new pattern")

    def test_catches(self):
        for label, (positives, _) in CASES.items():
            for text in positives:
                with self.subTest(label=label, text=text):
                    self.assertIn(label, labels_in(text))

    def test_leaves_alone(self):
        for label, (_, negatives) in CASES.items():
            for text in negatives:
                with self.subTest(label=label, text=text):
                    self.assertNotIn(label, labels_in(text))


class Score(unittest.TestCase):
    long_slop = ("In today's fast-paced digital landscape, our robust platform stands as a testament to innovation. "
                 "Experts agree it plays a vital role, fostering synergy; it's not just a tool, it's a movement. ") * 4
    plain = ("We moved the reading group to Thursdays because Tuesdays clashed with the methods seminar. "
             "The room is the same, and we still start at four. Bring a question or a complaint. "
             "Snacks are on me this week, and after that we'll take turns again like we used to.")

    def test_under_thirty_words_is_not_scored(self):
        r = tools.score("Too short to score.")
        self.assertIsNone(r["score"])
        self.assertEqual(r["tier"], "not scored")

    def test_score_stays_between_zero_and_one(self):
        for text in (self.long_slop, self.plain):
            s = tools.score(text)["score"]
            self.assertGreaterEqual(s, 0.0)
            self.assertLessEqual(s, 1.0)

    def test_dense_patterns_score_high(self):
        self.assertEqual(tools.score(self.long_slop)["tier"], "high")

    def test_plain_text_scores_low(self):
        self.assertEqual(tools.score(self.plain)["tier"], "low")

    def test_thirty_to_hundred_words_is_dampened(self):
        self.assertTrue(tools.score(self.plain)["dampened"])
        self.assertFalse(tools.score(self.long_slop)["dampened"])

    def test_tiers_match_the_thresholds_in_skill_md(self):
        for text in (self.long_slop, self.plain):
            r = tools.score(text)
            expected = "high" if r["score"] >= 0.6 else "medium" if r["score"] >= 0.35 else "low"
            self.assertEqual(r["tier"], expected)

    def test_quoted_text_is_not_scored(self):
        for text in ('She wrote, "We leverage robust tools; it\'s not just a tool, it\'s a movement."',
                     "She wrote, \u201cWe leverage robust tools; truly a testament.\u201d",
                     "Her note said:\n> Experts agree it plays a vital role; truly pivotal."):
            with self.subTest(text=text):
                self.assertEqual(labels_in(text), set())

    def test_single_quoted_text_is_not_scored(self):
        for text in ("She wrote 'we leverage robust tools; truly a testament.' Then she left.",
                     "She wrote \u2018we leverage robust tools; truly a testament\u2019 and left.",
                     "'We leverage robust tools,' she wrote."):
            with self.subTest(text=text):
                self.assertEqual(labels_in(text), set())

    def test_apostrophes_without_a_partner_are_still_scored(self):
        for text in ("The students' work leverages robust tools.",
                     "Don't leverage robust tools.",
                     "'Tis a robust plan.",
                     "The boys' bikes and the girls' robust bikes.",
                     "We don\u2019t leverage robust tools."):
            with self.subTest(text=text):
                self.assertIn("AI vocabulary", labels_in(text))

    def test_quotes_inside_brackets_dashes_and_other_quotes(self):
        for text in ('("We leverage robust tools.") She left.',
                     'She wrote\u2014"we leverage robust tools"\u2014and left.',
                     "'\"We leverage robust tools,\" she said' was the note."):
            with self.subTest(text=text):
                self.assertNotIn("AI vocabulary", labels_in(text))

    def test_nested_quotes(self):
        for text in ('Ama wrote, "Kofi told me, \'We leverage robust tools; truly pivotal.\' I laughed."',
                     'Ama wrote, "Kofi told me, \'We leverage robust tools.\'"',
                     "Ama wrote, 'Kofi told me, \"We leverage robust tools.\"'",
                     "\u201cKofi said \u2018we leverage robust tools\u2019 and left,\u201d Ama wrote.",
                     'Ama wrote, "Kofi said \'the students\' work is robust\' today."',
                     "\u201cKofi said \u2018we don\u2019t leverage robust tools\u2019 anymore,\u201d Ama wrote.",
                     '("Kofi told me, \'We leverage robust tools.\'") Ama wrote that.',
                     'Ama wrote, "Kofi said \'we leverage robust tools\' twice," and left.',
                     '\u201cAma said, \u2018Kofi wrote \u201cwe leverage robust tools\u201d twice.\u2019\u201d',
                     '"Kofi said \'robust\' and Ama said \'seamless\' in the same meeting."'):
            with self.subTest(text=text):
                self.assertEqual(labels_in(text), set())

    def test_sentence_after_nested_quotes_is_still_a_sentence(self):
        text = 'Ama wrote, "Kofi told me, \'Fine.\'" Moreover, we leverage it.'
        self.assertEqual(labels_in(text), {"sentence-initial connector", "AI vocabulary"})

    def test_inch_and_foot_marks_are_still_scored(self):
        for text in ('A 12" tablet and a 15" laptop are robust.',
                     "He is 5' 11\" tall and robust."):
            with self.subTest(text=text):
                self.assertIn("AI vocabulary", labels_in(text))

    def test_text_around_a_quote_is_still_scored(self):
        self.assertEqual(labels_in('She said "fine." Moreover, we leverage robust tools.'),
                         {"sentence-initial connector", "AI vocabulary"})

    def test_a_quote_does_not_run_past_a_paragraph(self):
        self.assertIn("semicolon", labels_in('An open "quote here.\n\nWe left; they stayed.'))

    def test_code_is_not_scored(self):
        self.assertEqual(labels_in("Run `x = 1; y = 2` and ```\nfoo \u2014 bar; baz\n``` now."), set())


if __name__ == "__main__":
    unittest.main()
