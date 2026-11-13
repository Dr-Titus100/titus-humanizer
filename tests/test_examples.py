"""Resume and prose examples, run through the script and compared with the stored output in tests/expected.

When a change to scripts/titus_tools.py changes any score, pattern count or hit, the failure shows a
before-and-after diff with the fixture name and line number. If the change is intended, refresh the
stored output with:

    python3 tests/update_expected.py
"""
import os
import unittest

from support import (all_snapshots, diff, fixtures, hard_rule_labels, hits_by_line, pairs, quotations,
                     read, run_cli, tools, FIXTURES)


class StoredOutput(unittest.TestCase):
    def test_output_matches_tests_expected(self):
        for path, actual in sorted(all_snapshots().items()):
            with self.subTest(expected=os.path.basename(path)):
                self.assertTrue(os.path.exists(path),
                                f"{path} is missing. Run python3 tests/update_expected.py to create it.")
                stored = read(path)
                if stored != actual:
                    self.fail("\n" + diff(stored, actual, path) +
                              "\nIf this change is intended, run python3 tests/update_expected.py")

    def test_no_stale_files_in_tests_expected(self):
        from support import EXPECTED
        wanted = {os.path.basename(p) for p in all_snapshots()}
        stale = sorted(set(os.listdir(EXPECTED)) - wanted)
        self.assertEqual(stale, [], "these stored files have no fixture; delete them")


class BeforeAndAfter(unittest.TestCase):
    def test_every_rewrite_scores_lower(self):
        for original, rewrite in pairs():
            with self.subTest(pair=rewrite):
                before = tools.score(read(os.path.join(FIXTURES, original)))
                after = tools.score(read(os.path.join(FIXTURES, rewrite)))
                self.assertEqual(before["tier"], "high")
                self.assertEqual(after["tier"], "low")
                self.assertLess(after["score"], before["score"])

    def test_every_quotation_survives_word_for_word(self):
        for original, rewrite in pairs():
            with self.subTest(pair=rewrite):
                after = read(os.path.join(FIXTURES, rewrite))
                for quote in quotations(read(os.path.join(FIXTURES, original))):
                    self.assertIn(quote, after)

    def test_report_says_quotations_were_left_as_is(self):
        out, _ = run_cli("report", os.path.join(FIXTURES, "prose", "nested_quotes.txt"),
                         os.path.join(FIXTURES, "prose", "nested_quotes_rewrite.txt"))
        self.assertIn("Left as-is: 3 quotations", out)
        self.assertNotIn("Changed in the rewrite", out)

    def test_report_has_no_left_as_is_line_when_there_is_nothing_to_keep(self):
        out, _ = run_cli("report", os.path.join(FIXTURES, "prose", "email.txt"),
                         os.path.join(FIXTURES, "prose", "email_rewrite.txt"))
        self.assertNotIn("Left as-is", out)
        self.assertNotIn("Changed in the rewrite", out)


class KeptItems(unittest.TestCase):
    """The report's "Left as-is" and "Changed in the rewrite" lines."""
    original = ('She said, "we leverage robust tools." Run `npm run build` and open ~/app/config/settings.yaml. '
                "The guide is at https://example.com/guide. \U0001F389")

    def test_finds_each_kind_once(self):
        found = tools.kept_items(self.original)
        self.assertEqual(found["quotation"], ['"we leverage robust tools."'])
        self.assertEqual(found["code snippet"], ["`npm run build`"])
        self.assertEqual(found["file path"], ["~/app/config/settings.yaml"])
        self.assertEqual(found["link"], ["https://example.com/guide"])
        self.assertEqual(found["emoji"], ["\U0001F389"])

    def test_everything_kept(self):
        self.assertEqual(tools._kept_line(self.original, self.original),
                         ["Left as-is: 1 quotation, 1 code snippet, 1 file path, 1 link and 1 emoji"])

    def test_each_kind_changed(self):
        changes = {
            "quotation": ('"we leverage robust tools."', '"we use good tools."'),
            "code snippet": ("`npm run build`", "`npm run make`"),
            "file path": ("~/app/config/settings.yaml", "~/app/settings.yaml"),
            "link": ("https://example.com/guide", "https://example.com/start"),
            "emoji": ("\U0001F389", ""),
        }
        for kind, (old, new) in changes.items():
            with self.subTest(kind=kind):
                lines = tools._kept_line(self.original, self.original.replace(old, new))
                self.assertIn(f"Changed in the rewrite: 1 of 1 {kind}. Restore them from the original.", lines)

    def test_an_item_that_only_grew_counts_as_changed(self):
        # A substring check would miss these: the old link and path still appear inside the new ones.
        rewrite = self.original.replace("guide", "guide2").replace("settings.yaml", "settings.yaml.bak")
        lines = tools._kept_line(self.original, rewrite)
        self.assertIn("Changed in the rewrite: 1 of 1 file path and 1 of 1 link. Restore them from the original.", lines)

    def test_items_inside_code_or_quotes_count_once(self):
        found = tools.kept_items('Run `curl https://example.com/x` then say "see https://example.com/y \U0001F600".')
        self.assertEqual(found["code snippet"], ["`curl https://example.com/x`"])
        self.assertEqual(len(found["quotation"]), 1)
        self.assertEqual(found["link"], [])
        self.assertEqual(found["emoji"], [])

    def test_code_moved_inside_a_quotation_changes_the_quotation(self):
        original = 'She said "Run `one` then `two`." Then she left.'
        lines = tools._kept_line(original, original.replace("`one` then `two`", "`two` then `one`"))
        self.assertIn("Changed in the rewrite: 1 of 1 quotation. Restore them from the original.", lines)
        self.assertEqual(tools.kept_items(original)["code snippet"], [])

    def test_a_link_keeps_its_own_closing_bracket(self):
        found = tools.kept_items("See https://en.wikipedia.org/wiki/Function_(mathematics). Or (https://example.com/a).")
        self.assertEqual(found["link"], ["https://en.wikipedia.org/wiki/Function_(mathematics)", "https://example.com/a"])
        original = "See https://en.wikipedia.org/wiki/Function_(mathematics) for more."
        lines = tools._kept_line(original, original.replace("(mathematics)", "(mathematics"))
        self.assertIn("Changed in the rewrite: 1 of 1 link. Restore them from the original.", lines)

    def test_a_flag_is_one_emoji(self):
        us, su = "\U0001F1FA\U0001F1F8", "\U0001F1F8\U0001F1FA"
        self.assertEqual(tools.kept_items(f"Go {us} team")["emoji"], [us])
        lines = tools._kept_line(f"Go {us} team", f"Go {su} team")
        self.assertIn("Changed in the rewrite: 1 of 1 emoji. Restore them from the original.", lines)

    def test_words_with_slashes_are_not_paths(self):
        self.assertEqual(tools.kept_items("Pick and/or skip it, 1/2 of the time, with w/o help.")["file path"], [])

    def test_emoji_sequences_stay_whole(self):
        family = "\U0001F468\u200d\U0001F469\u200d\U0001F467"
        self.assertEqual(tools.kept_items(f"Hi {family} and \u2764\ufe0f")["emoji"], [family, "\u2764\ufe0f"])


    def test_nested_quotes_example_keeps_all_three_quotations(self):
        self.assertEqual(len(quotations(read(os.path.join(FIXTURES, "prose", "nested_quotes_rewrite.txt")))), 3)

    def test_no_hard_rule_pattern_left_in_a_rewrite(self):
        hard = set(hard_rule_labels())
        for _, rewrite in pairs():
            with self.subTest(rewrite=rewrite):
                left = [h for h in hits_by_line(read(os.path.join(FIXTURES, rewrite))) if h[1] in hard]
                self.assertEqual(left, [])


class HumanWriting(unittest.TestCase):
    """Text written plainly by a person should pass. These guard against false positives."""

    def human_fixtures(self):
        return [n for n in fixtures() if os.path.basename(n).startswith("human_")]

    def test_human_examples_score_low(self):
        for name in self.human_fixtures():
            with self.subTest(fixture=name):
                self.assertEqual(tools.score(read(os.path.join(FIXTURES, name)))["tier"], "low")

    def test_resume_date_ranges_and_bullets_are_not_flagged(self):
        hits = hits_by_line(read(os.path.join(FIXTURES, "resume", "human_resume.txt")))
        self.assertEqual(hits, [])


if __name__ == "__main__":
    unittest.main()
