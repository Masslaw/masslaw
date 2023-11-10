import unittest

from logic_layer.text_extraction.optical_character_recognition.text_document_building._construction_logic import ocr_extracted_element_to_optical_structure_entry


class TestFunctionOcrExtractedElementToOpticalStructureEntry(unittest.TestCase):
    def test_valid(self):
        extracted_element = ("Hi", (0, 0, 10, 10))
        entry = ocr_extracted_element_to_optical_structure_entry(extracted_element)

        self.assertEqual(entry, ("Hi", (0, 0, 10, 10)))
