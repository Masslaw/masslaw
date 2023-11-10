import unittest

from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureCharacter
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from logic_layer.text_structures.extracted_optical_text_structure.structure_construction._assertions import assert_element_type
from logic_layer.text_structures.extracted_optical_text_structure.structure_construction._exceptions import StructureConstructionInvalidElementTypeException


class TestFunctionAssertElementType(unittest.TestCase):
    def test_not_raising(self):
        assert_element_type(element_type=OpticalTextStructureWord, element_instance=OpticalTextStructureWord())

    def test_raising(self):
        with self.assertRaises(StructureConstructionInvalidElementTypeException):
            assert_element_type(element_type=OpticalTextStructureWord, element_instance=OpticalTextStructureCharacter())
