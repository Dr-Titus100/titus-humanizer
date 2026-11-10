"""Resume and prose examples, run through the script and compared with the stored output in tests/expected.

When a change to scripts/titus_tools.py changes any score, pattern count or hit, the failure shows a
before-and-after diff with the fixture name and line number. If the change is intended, refresh the
stored output with:

    python3 tests/update_expected.py
"""
import os
import unittest

from support import (all_snapshots, diff, fixtures, hard_rule_labels, hits_by_line, pairs, quotations,
                     read, tools, FIXTURES)


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
