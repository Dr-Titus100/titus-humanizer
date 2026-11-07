"""Hidden-character cleanup: what clean() removes, what it keeps, and how it repairs spacing."""
import unittest

from support import tools, run_cli, FIXTURES

clean = tools.clean


class Removes(unittest.TestCase):
    def check(self, text, expected, label, count=1):
        out, found = clean(text)
        self.assertEqual(out, expected)
        self.assertEqual(found[label], count, dict(found))

    def test_zero_width_space_inside_a_word(self):
        self.check("hid\u200bden", "hidden", "zero-width space")

    def test_byte_order_mark_at_start(self):
        self.check("\ufeffTitle", "Title", "byte-order mark")

    def test_soft_hyphen(self):
        self.check("co\u00adoperate", "cooperate", "soft hyphen")

    def test_word_joiner(self):
        self.check("one\u2060two", "onetwo", "word joiner")

    def test_joiner_between_latin_letters(self):
        self.check("ab\u200dcd", "abcd", "zero-width joiner")

    def test_text_direction_controls(self):
        self.check("\u202eabc\u202c", "abc", "text-direction control", 2)

    def test_stray_tag_characters(self):
        self.check("note\U000E0041\U000E0042", "note", "invisible tag character", 2)

    def test_variation_selector_after_a_letter(self):
        self.check("a\ufe0fb", "ab", "variation selector")

    def test_private_use_character(self):
        self.check("x\ue000y", "xy", "private-use or non-character")

    def test_unusual_spaces_become_normal_spaces(self):
        self.check("10\u00a0kg and 5\u2009mm", "10 kg and 5 mm", "unusual space", 2)

    def test_cyrillic_look_alike_inside_an_english_word(self):
        self.check("the p\u0430per", "the paper", "look-alike letter")


class Keeps(unittest.TestCase):
    def assertUnchanged(self, text):
        out, found = clean(text)
        self.assertEqual(out, text)
        self.assertFalse(found, dict(found))

    def test_family_emoji_with_joiners(self):
        self.assertUnchanged("Family: \U0001F468\u200d\U0001F469\u200d\U0001F467")

    def test_heart_with_variation_selector(self):
        self.assertUnchanged("Thanks \u2764\ufe0f")

    def test_england_flag_tag_sequence(self):
        self.assertUnchanged("Go \U0001F3F4\U000E0067\U000E0062\U000E0065\U000E006E\U000E0067\U000E007F team")

    def test_persian_non_joiner(self):
        self.assertUnchanged("\u0645\u06cc\u200c\u062e\u0648\u0627\u0647\u0645")

    def test_russian_word(self):
        self.assertUnchanged("The word \u043f\u0440\u0438\u0432\u0435\u0442 means hello.")

    def test_greek_word(self):
        self.assertUnchanged("\u03b1\u03bb\u03c6\u03b1 is spelled out.")

    def test_inline_code(self):
        self.assertUnchanged("Run `a\u200bb` first.")

    def test_fenced_code_block(self):
        self.assertUnchanged("Before\n```\nx = 'a\u200bb'\n```\nAfter")

    def test_url(self):
        self.assertUnchanged("See https://example.com/a\u200bb for details.")

    def test_aligned_columns_on_a_resume(self):
        self.assertUnchanged("Data Analyst, Riverbend Health          Jul 2021 \u2013 Present")


class Spacing(unittest.TestCase):
    def test_removal_between_two_spaces_leaves_one_space(self):
        self.assertEqual(clean("word \u200b word")[0], "word word")

    def test_aligned_spaces_survive_a_removal_elsewhere(self):
        text = "Na\u200bme          Date"
        self.assertEqual(clean(text)[0], "Name          Date")

    def test_cleanup_is_idempotent(self):
        text = "p\u0430per \u200b and\u00a0more \U0001F3F4\U000E0067\U000E0062\U000E0065\U000E006E\U000E0067\U000E007F"
        once = clean(text)[0]
        self.assertEqual(clean(once), (once, clean(once)[1]))
        self.assertFalse(clean(once)[1])


class CommandLine(unittest.TestCase):
    def test_clean_command_writes_text_to_stdout_and_counts_to_stderr(self):
        out, err = run_cli("clean", f"{FIXTURES}/resume/human_resume.txt")
        with open(f"{FIXTURES}/resume/human_resume.txt", encoding="utf-8") as f:
            self.assertEqual(out, f.read())
        self.assertEqual(err.strip(), "Hidden characters removed: none")


if __name__ == "__main__":
    unittest.main()
