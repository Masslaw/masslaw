import unittest

from logic_layer.text_structures.extracted_optical_text_structure.structure_calculations._geometry_calculations._geometry_calculations import batch_convert_elements_to_rectangles
from logic_layer.text_structures.extracted_optical_text_structure._structure_element import OpticalTextStructureElement

class TestFunctionBatchConvertElementsToRectangles(unittest.TestCase):
    def test_batch_convert_elements_to_rectangles(self):
        elements = [
            OpticalTextStructureElement(bounding_rect=(5, 5, 50, 50)),
            OpticalTextStructureElement(bounding_rect=(55, 5, 100, 50)),
            OpticalTextStructureElement(bounding_rect=(5, 55, 50, 100)),
            OpticalTextStructureElement(bounding_rect=(55, 55, 100, 100))
        ]

        expected = [
            (5, 5, 50, 50),
            (55, 5, 100, 50),
            (5, 55, 50, 100),
            (55, 55, 100, 100)
        ]

        result = batch_convert_elements_to_rectangles(elements)
        self.assertEqual(result, expected)
