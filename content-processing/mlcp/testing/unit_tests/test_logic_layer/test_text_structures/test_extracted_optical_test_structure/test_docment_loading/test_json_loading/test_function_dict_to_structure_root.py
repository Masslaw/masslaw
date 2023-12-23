import unittest

from logic_layer.text_structures.extracted_optical_text_structure.document_loading._json_loading import _dict_to_structure_root


class TestFunctionDictToStructureRoot(unittest.TestCase):

    def test_function_dict_to_structure_root(self):
        structure_root = _dict_to_structure_root({
            'ln': [{'v': 'hey'}, {'v': 'there!'}]
        })
        self.assertEqual(len(structure_root.get_children()), 2)