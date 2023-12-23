import unittest

from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureGroup
from logic_layer.text_structures.extracted_optical_text_structure._structure_root import OpticalTextStructureRoot


class TestOpticalTextStructureRoot(unittest.TestCase):

    def test_children_setting_and_retrieval(self):
        root = OpticalTextStructureRoot()

        self.assertEqual(root.get_children(), [])

        children_elements = [OpticalTextStructureGroup(), OpticalTextStructureGroup()]
        root.set_children(children_elements)
        self.assertEqual(root.get_children(), children_elements)
