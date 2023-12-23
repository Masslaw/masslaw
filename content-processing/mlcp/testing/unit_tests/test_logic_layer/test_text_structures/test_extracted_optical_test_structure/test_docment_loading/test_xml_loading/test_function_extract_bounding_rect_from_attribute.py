import unittest

from logic_layer.text_structures.extracted_optical_text_structure.document_loading._xml_loading import _extract_bounding_rect_from_attribute


class TestFunctionExtractBoundingRectFromAttribute(unittest.TestCase):

    def test_extract_bounding_rect_from_attribute_valid_value(self):
        bounding_rect = _extract_bounding_rect_from_attribute('1-23-456-789')
        self.assertEqual(bounding_rect, (1, 23, 456, 789))

    def test_extract_bounding_rect_from_attribute_short_value(self):
        bounding_rect = _extract_bounding_rect_from_attribute('1-23-456')
        self.assertEqual(bounding_rect, (1, 23, 456, 0))

    def test_extract_bounding_rect_from_attribute_long_value(self):
        bounding_rect = _extract_bounding_rect_from_attribute('1-23-456-789-10')
        self.assertEqual(bounding_rect, (1, 23, 456, 789))
