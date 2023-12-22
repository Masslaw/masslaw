import unittest

from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._json_export import _structure_element_data_to_dict


class TestStructureElementDataToDictFunction(unittest.TestCase):

    def setUp(self):
        self.structure_element = OpticalTextStructureWord()
        self.structure_element.set_children(list("dummy text"))
        self.structure_element.set_property('dummy property', 'dummy value')

    def test_structure_element_data_to_dict_valid_structure(self):
        result_dict = _structure_element_data_to_dict(self.structure_element)
        self.assertIsInstance(result_dict, dict)

    def test_structure_element_data_to_dict_valid_content(self):
        result_dict = _structure_element_data_to_dict(self.structure_element)
        self.assertIn('v', result_dict)
        self.assertEqual(result_dict['v'], 'dummy text')

    def test_structure_element_data_to_dict_with_properties(self):
        result_dict = _structure_element_data_to_dict(self.structure_element)
        self.assertIn('p', result_dict)
        self.assertEqual(result_dict['p'], self.structure_element.get_properties())

    def test_structure_element_data_to_dict_with_bounding_box(self):
        self.structure_element.set_bounding_rect((1, 2, 3, 4))
        result_dict = _structure_element_data_to_dict(self.structure_element)
        self.assertEqual(result_dict['x1'], 1)
        self.assertEqual(result_dict['y1'], 2)
        self.assertEqual(result_dict['x2'], 3)
        self.assertEqual(result_dict['y2'], 4)
