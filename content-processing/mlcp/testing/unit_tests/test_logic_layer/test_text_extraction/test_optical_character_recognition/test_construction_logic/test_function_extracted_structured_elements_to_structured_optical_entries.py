import unittest

from logic_layer.text_extraction.optical_character_recognition.text_document_building._construction_logic import extracted_structured_elements_to_structured_optical_entries


class TestFunctionExtractedStructuredElementsToStructuredOpticalEntries(unittest.TestCase):
    def test_regular(self):
        structured_elements = [
            [
                ('Hello', (0, 0, 50, 10)),
                ('There!', (0, 20, 50, 30))
            ],
            [
                ('How', (0, 0, 50, 10)),
                ('are', (0, 20, 50, 30)),
                ('you?', (0, 40, 50, 50))
            ]
        ]

        structured_optical_entries = extracted_structured_elements_to_structured_optical_entries(extracted_structured_elements=structured_elements)

        self.assertEqual(structured_optical_entries, [
            [
                ('Hello', (0, 0, 50, 10)),
                ('There!', (0, 20, 50, 30))
            ],
            [
                ('How', (0, 0, 50, 10)),
                ('are', (0, 20, 50, 30)),
                ('you?', (0, 40, 50, 50))
            ]
        ])
