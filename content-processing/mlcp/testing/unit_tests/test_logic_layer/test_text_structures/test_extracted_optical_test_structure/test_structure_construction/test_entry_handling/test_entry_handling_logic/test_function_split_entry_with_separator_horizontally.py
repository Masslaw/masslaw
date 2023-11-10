import unittest

from logic_layer.text_structures.extracted_optical_text_structure.structure_construction._entry_handling._entry_handling_logic import split_entry_with_separator_horizontally


class TestClassSplitEntryWithSeparatorHorizontally(unittest.TestCase):
    def test_on_ltr_line(self):
        entry = ('hello there', (0, 0, 110, 10))

        split_entry = split_entry_with_separator_horizontally(entry, ' ')

        self.assertListEqual(split_entry, [('hello', (0, 0, 50, 10)), ('there', (60, 0, 110, 10))])

    def test_on_rtl_line(self):
        entry = ('שלום לך', (0, 0, 70, 10))

        split_entry = split_entry_with_separator_horizontally(entry, ' ')

        self.assertListEqual(split_entry, [('שלום', (30, 0, 70, 10)), ('לך', (0, 0, 20, 10))])

    def test_on_bidi_line(self):
        entry = ('שלום לך John Doe איך אתה?', (0, 0, 250, 10))

        split_entry = split_entry_with_separator_horizontally(entry, ' ')

        self.assertListEqual(split_entry,
            [('שלום', (210, 0, 250, 10)), ('לך', (180, 0, 200, 10)), ('John', (90, 0, 130, 10)), ('Doe', (140, 0, 170, 10)), ('איך', (50, 0, 80, 10)), ('אתה?', (0, 0, 40, 10))])

    def test_on_ltr_word(self):
        entry = ('word', (0, 0, 40, 10))

        split_entry = split_entry_with_separator_horizontally(entry, '')

        self.assertListEqual(split_entry, [('w', (0, 0, 10, 10)), ('o', (10, 0, 20, 10)), ('r', (20, 0, 30, 10)), ('d', (30, 0, 40, 10))])

    def test_on_rtl_word(self):
        entry = ('שלום', (0, 0, 40, 10))

        split_entry = split_entry_with_separator_horizontally(entry, '')

        self.assertListEqual(split_entry, [('ש', (30, 0, 40, 10)), ('ל', (20, 0, 30, 10)), ('ו', (10, 0, 20, 10)), ('ם', (0, 0, 10, 10))])
