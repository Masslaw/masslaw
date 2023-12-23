import unittest

from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureGroup
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureLine
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from logic_layer.text_structures.extracted_optical_text_structure.document_loading._json_loading import _dict_to_structure_element


class TestFunctionDictToStructureElement(unittest.TestCase):

    def test_function_dict_to_structure_element(self):

        element = _dict_to_structure_element({
            'ln': [{
                'wd': [{'v': 'hello', 'x1': 0, 'x2': 1, 'y1': 2, 'y2': 3}, {'v': 'there', 'x1': 4, 'x2': 5, 'y1': 6, 'y2': 7}]
            }]
        }, OpticalTextStructureGroup)

        self.assertEqual(len(element.get_children()), 1)
        self.assertEqual(element.get_children_type(), OpticalTextStructureLine)
        self.assertEqual(len(element.get_children()[0].get_children()), 2)
        self.assertEqual(element.get_children()[0].get_children_type(), OpticalTextStructureWord)
