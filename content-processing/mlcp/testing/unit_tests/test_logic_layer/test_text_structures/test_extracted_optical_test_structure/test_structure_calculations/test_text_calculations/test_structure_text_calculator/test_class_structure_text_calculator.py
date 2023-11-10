import unittest

from logic_layer.bidi import ReadDirection
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureLine
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from logic_layer.text_structures.extracted_optical_text_structure._structure_calculations import StructureTextCalculator


class TestClassStructureTextCalculator(unittest.TestCase):

    def test_calculate_text_direction_on_ltr_text(self):
        line_element = OpticalTextStructureLine(
            children=[
                OpticalTextStructureWord(list("Hi")),
                OpticalTextStructureWord(list("There!")),
            ]
        )

        calculator = StructureTextCalculator(line_element)

        self.assertEqual(calculator.calculate_text_direction(), ReadDirection.LTR)

    def test_calculate_text_direction_on_rtl_text(self):
        line_element = OpticalTextStructureLine(
            children=[
                OpticalTextStructureWord(list("שלום")),
                OpticalTextStructureWord(list("לך!")),
            ]
        )

        calculator = StructureTextCalculator(line_element)

        self.assertEqual(calculator.calculate_text_direction(), ReadDirection.RTL)

    def test_calculate_text_direction_on_bidi_text(self):
        rtl_line_element = OpticalTextStructureLine(
            children=[
                OpticalTextStructureWord(list("שלום")),
                OpticalTextStructureWord(list("לך")),
                OpticalTextStructureWord(list("John")),
                OpticalTextStructureWord(list("Doe")),
                OpticalTextStructureWord(list("איך")),
                OpticalTextStructureWord(list("אתה?")),
            ]
        )
        ltr_line_element = OpticalTextStructureLine(
            children=[
                OpticalTextStructureWord(list("Hi")),
                OpticalTextStructureWord(list("There")),
                OpticalTextStructureWord(list("יוסי")),
                OpticalTextStructureWord(list("כהן")),
                OpticalTextStructureWord(list("How")),
                OpticalTextStructureWord(list("are")),
                OpticalTextStructureWord(list("you?")),
            ]
        )

        calculator = StructureTextCalculator(rtl_line_element)
        self.assertEqual(calculator.calculate_text_direction(), ReadDirection.RTL)

        calculator = StructureTextCalculator(ltr_line_element)
        self.assertEqual(calculator.calculate_text_direction(), ReadDirection.LTR)

    def test_calculate_text_direction_on_empty_text(self):
        line_element = OpticalTextStructureLine(
            children=[]
        )

        calculator = StructureTextCalculator(line_element)

        self.assertEqual(calculator.calculate_text_direction(), ReadDirection.AMBIGUOUS)
