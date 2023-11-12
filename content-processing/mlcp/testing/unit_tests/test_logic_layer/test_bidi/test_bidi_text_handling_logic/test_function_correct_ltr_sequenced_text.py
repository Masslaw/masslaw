import unittest

from logic_layer.bidi import correct_ltr_sequenced_text


class TestFunctionCorrectLtrSequencedText(unittest.TestCase):

    def test_ltr_text(self):
        text = "This is a test"
        expected = "This is a test"
        self.assertEqual(correct_ltr_sequenced_text(text), expected)

    def test_rtl_text(self):
        text = "טסקט שי"
        expected = "יש טקסט"
        self.assertEqual(correct_ltr_sequenced_text(text), expected)

    def test_bidi_text(self):
        text = "דבלב הקידבל in english טסקט והז"
        expected = "זהו טקסט in english לבדיקה בלבד"
        self.assertEqual(correct_ltr_sequenced_text(text), expected)

    def test_empty_text(self):
        text = ""
        expected = ""
        self.assertEqual(correct_ltr_sequenced_text(text), expected)

    def test_single_word_text(self):
        text = "word"
        expected = "word"
        self.assertEqual(correct_ltr_sequenced_text(text), expected)

    def test_single_rtl_word_text(self):
        text = "הלימ"
        expected = "מילה"
        self.assertEqual(correct_ltr_sequenced_text(text), expected)
