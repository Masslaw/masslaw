import unittest

from logic_layer.text_extraction.optical_character_recognition.text_document_building._construction_logic import extracted_element_groups_to_optical_structure_entry_groups


class TestFunctionExtractedElementGroupsToOpticalStructureEntryGroups(unittest.TestCase):
    def test_valid(self):
        element_groups = [
            [
                ("Hi", (0, 0, 10, 10)),
                ("There!", (10, 0, 20, 10)),
                ("How Are You?", (0, 10, 20, 20)),
            ],
            [
                ("שלום", (0, 0, 10, 10)),
                ("לך", (10, 0, 20, 10)),
                ("איך אתה?", (0, 10, 10, 20)),
            ],
        ]

        entry_groups = extracted_element_groups_to_optical_structure_entry_groups(element_groups)

        self.assertEqual(entry_groups, [
            [
                ("Hi", (0, 0, 10, 10)),
                ("There!", (10, 0, 20, 10)),
                ("How Are You?", (0, 10, 20, 20)),
            ],
            [
                ("שלום", (0, 0, 10, 10)),
                ("לך", (10, 0, 20, 10)),
                ("איך אתה?", (0, 10, 10, 20)),
            ],
        ])
