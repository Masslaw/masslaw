import unittest

from logic_layer.bidi import ReadDirection
from logic_layer.bidi import get_text_direction


class TestFunctionGetTextDirection(unittest.TestCase):

    def test_get_text_direction_with_ltr_text(self):
        text = "This is a test text"
        self.assertEqual(get_text_direction(text), ReadDirection.LTR)

    def test_get_text_direction_with_rtl_text(self):
        text = "זוהי עברית"
        self.assertEqual(get_text_direction(text), ReadDirection.RTL)

    def test_get_text_direction_with_mixed_text(self):
        text = "This is a test text זוהי עברית"
        self.assertEqual(get_text_direction(text), ReadDirection.AMBIGUOUS)
