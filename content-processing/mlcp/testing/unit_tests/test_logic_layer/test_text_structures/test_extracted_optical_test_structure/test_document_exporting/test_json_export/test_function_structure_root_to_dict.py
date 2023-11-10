import unittest

from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure._structure_root import OpticalTextStructureRoot
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._json_export import _structure_root_to_dict


class TestStructureRootToDictFunction(unittest.TestCase):

    def setUp(self):
        self.structure_root = OpticalTextStructureRoot(
            hierarchy_formation=[OpticalStructureHierarchyLevel.GROUP, OpticalStructureHierarchyLevel.LINE, OpticalStructureHierarchyLevel.WORD, OpticalStructureHierarchyLevel.CHARACTER, ])

    def test_structure_root_to_dict_valid_conditions(self):
        result_dict = _structure_root_to_dict(self.structure_root)
        self.assertIsInstance(result_dict, dict)
        self.assertIn('type', result_dict)
        self.assertEqual(result_dict['type'], 'optical')

    def test_structure_root_to_dict_children_key_presence(self):
        result_dict = _structure_root_to_dict(self.structure_root)
        self.assertIn('children', result_dict)
        self.assertIsInstance(result_dict['children'], list)

    def test_structure_root_to_dict_empty_children(self):
        result_dict = _structure_root_to_dict(self.structure_root)
        self.assertEqual(len(result_dict['children']), 0)
