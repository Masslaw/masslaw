import unittest

from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureLine
from logic_layer.text_structures.extracted_optical_text_structure.document_loading._json_loading import _determine_child_type


class TestFunctionDetermineChildType(unittest.TestCase):

    def test_determine_child_type_with_non_leaf(self):
        child_type = _determine_child_type({
            'ln': [{'v': 'hey'}, {'v': 'there!'}]
        })
        self.assertEqual(child_type, OpticalTextStructureLine)

    def test_determine_child_type_with_leaf(self):
        child_type = _determine_child_type({
            'v': 'hey'
        })
        self.assertEqual(child_type, str)

    def test_determine_child_type_with_empty_dict(self):
        child_type = _determine_child_type({})
        self.assertIsNone(child_type)

    def test_determine_child_type_with_invalid_tag(self):
        child_type = _determine_child_type({
            'wooooooo': [{'v': 'hey'}, {'v': 'there!'}]
        })
        self.assertIsNone(child_type)
