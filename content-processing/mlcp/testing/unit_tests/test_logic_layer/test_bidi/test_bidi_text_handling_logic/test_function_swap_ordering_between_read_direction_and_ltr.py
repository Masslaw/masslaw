import unittest

from logic_layer.bidi import ReadDirection
from logic_layer.bidi import swap_ordering_between_read_direction_and_ltr


class TestFunctionSwapOrderingBetweenReadDirectionAndLTR(unittest.TestCase):

    def test_on_ltr_text(self):

        text_parts = [
            "This",
            "is",
            "a",
            "test",
        ]

        ltr_text_parts = [
            "This",
            "is",
            "a",
            "test",
        ]

        self.assertEqual(swap_ordering_between_read_direction_and_ltr(text_parts, ReadDirection.LTR), ltr_text_parts)
        self.assertEqual(swap_ordering_between_read_direction_and_ltr(ltr_text_parts, ReadDirection.LTR), text_parts)

    def test_on_rtl_text(self):

        text_parts = [
            "זוהי",
            "עברית",
        ]

        rtl_text_parts = [
            "עברית",
            "זוהי",
        ]

        self.assertEqual(swap_ordering_between_read_direction_and_ltr(text_parts, ReadDirection.RTL), rtl_text_parts)
        self.assertEqual(swap_ordering_between_read_direction_and_ltr(rtl_text_parts, ReadDirection.RTL), text_parts)

    def test_on_bidi_text(self):

        text_parts = [
            'זהו',
            'טקסט',
            'in',
            'english',
            'לבדיקה',
            'בלבד',
        ]

        ltr_text_parts = [
            'בלבד',
            'לבדיקה',
            'in',
            'english',
            'טקסט',
            'זהו',
        ]

        self.assertEqual(swap_ordering_between_read_direction_and_ltr(text_parts, ReadDirection.RTL), ltr_text_parts)
        self.assertEqual(swap_ordering_between_read_direction_and_ltr(ltr_text_parts, ReadDirection.RTL), text_parts)
