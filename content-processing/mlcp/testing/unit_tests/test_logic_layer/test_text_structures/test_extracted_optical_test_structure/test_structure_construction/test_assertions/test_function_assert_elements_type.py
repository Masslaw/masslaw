import unittest

from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureCharacter
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from logic_layer.text_structures.extracted_optical_text_structure.structure_construction._assertions import assert_elements_type
from logic_layer.text_structures.extracted_optical_text_structure.structure_construction._exceptions import StructureConstructionInvalidElementTypeException


class TestFunctionAssertElementsType(unittest.TestCase):
    def test_not_raising(self):
        assert_elements_type(elements_type=OpticalTextStructureWord, elements=[OpticalTextStructureWord(), OpticalTextStructureWord(), OpticalTextStructureWord(), ])

    def test_raising(self):
        with self.assertRaises(StructureConstructionInvalidElementTypeException):
            assert_elements_type(elements_type=OpticalTextStructureWord, elements=[OpticalTextStructureWord(), OpticalTextStructureCharacter(), OpticalTextStructureWord(), ])
