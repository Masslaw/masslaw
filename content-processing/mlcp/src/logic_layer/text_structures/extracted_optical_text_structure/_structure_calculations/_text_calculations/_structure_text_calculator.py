from logic_layer.text_structures.extracted_optical_text_structure._structure_calculations._text_calculations._bidirectional_calculations import calculate_element_text_direction
from logic_layer.text_structures.extracted_optical_text_structure._structure_element import OpticalTextStructureElement


class StructureTextCalculator:
    def __init__(self, structure_element: OpticalTextStructureElement):
        self._structure_element = structure_element

    def calculate_text_direction(self):
        return calculate_element_text_direction(self._structure_element)
