import unittest

from logic_layer.text_structures.extracted_optical_text_structure.structure_construction._entry_handling._entry_handling_logic import split_entry_with_separator_vertically


class TestClassSplitEntryWithSeparatorVertically(unittest.TestCase):
    def test_with_multiple_lines(self):
        entry = ('line one\nline two\nline three', (0, 0, 100, 30))

        split_entry = split_entry_with_separator_vertically(entry, '\n')

        self.assertListEqual(split_entry, [('line one', (0, 0, 100, 10)), ('line two', (0, 10, 100, 20)), ('line three', (0, 20, 100, 30))])
