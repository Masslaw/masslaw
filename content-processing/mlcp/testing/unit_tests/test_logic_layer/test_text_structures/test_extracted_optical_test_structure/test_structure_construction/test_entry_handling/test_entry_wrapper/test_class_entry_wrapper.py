import unittest

from logic_layer.text_structures.extracted_optical_text_structure.structure_construction._entry_handling._entry_wrapper import EntryWrapper


class TestClassEntryWrapper(unittest.TestCase):

    def setUp(self):
        self.entry_data = ("sample_text", (0, 0, 10, 10))
        self.entry_wrapper = EntryWrapper(self.entry_data)

    def test_get_entry(self):
        self.assertEqual(self.entry_wrapper.get_entry(), self.entry_data)

    def test_get_text(self):
        self.assertEqual(self.entry_wrapper.get_text(), "sample_text")

    def test_set_text(self):
        self.entry_wrapper.set_text("new_text")
        self.assertEqual(self.entry_wrapper.get_text(), "new_text")
        self.assertEqual(self.entry_wrapper.get_bounding_rect(), (0, 0, 10, 10))

    def test_get_bounding_rect(self):
        self.assertEqual(self.entry_wrapper.get_bounding_rect(), (0, 0, 10, 10))

    def test_set_bounding_rect(self):
        new_bounding_rect = (5, 5, 15, 15)
        self.entry_wrapper.set_bounding_rect(new_bounding_rect)
        self.assertEqual(self.entry_wrapper.get_bounding_rect(), new_bounding_rect)
        self.assertEqual(self.entry_wrapper.get_text(), "sample_text")

    def test_str_method(self):
        self.assertEqual(str(self.entry_wrapper), "sample_text")
