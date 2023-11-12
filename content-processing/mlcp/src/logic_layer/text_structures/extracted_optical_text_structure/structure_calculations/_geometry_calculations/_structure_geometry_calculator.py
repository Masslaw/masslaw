from typing import Tuple

from logic_layer.text_structures.extracted_optical_text_structure.structure_calculations._geometry_calculations._geometry_calculations import get_average_gap_between_child_elements
from logic_layer.text_structures.extracted_optical_text_structure.structure_calculations._geometry_calculations._geometry_calculations import get_average_gap_between_nested_child_elements
from logic_layer.text_structures.extracted_optical_text_structure.structure_calculations._geometry_calculations._geometry_calculations import get_element_children_average_size
from logic_layer.text_structures.extracted_optical_text_structure.structure_calculations._geometry_calculations._geometry_calculations import get_element_nested_children_average_size
from logic_layer.text_structures.extracted_optical_text_structure.structure_calculations._geometry_calculations._geometry_calculations import get_element_bounding_rectangle
from logic_layer.text_structures.extracted_optical_text_structure._structure_element import OpticalTextStructureElement
from logic_layer.text_structures.extracted_optical_text_structure._types import OpticalStructureElementBoundingRectangle
from logic_layer.text_structures.extracted_optical_text_structure._types import OpticalStructureHierarchyLevel


class StructureGeometryCalculator:
    def __init__(self, structure_element: OpticalTextStructureElement):
        self._structure_element = structure_element

    def calculate_bounding_rect(self) -> OpticalStructureElementBoundingRectangle:
        return get_element_bounding_rectangle(self._structure_element)

    def calculate_element_children_average_size(self) -> Tuple[float, float]:
        return get_element_children_average_size(self._structure_element)

    def calculate_element_nested_children_average_size(self, element_type: OpticalStructureHierarchyLevel) -> Tuple[float, float]:
        return get_element_nested_children_average_size(self._structure_element, element_type)

    def calculate_average_gap_between_child_elements(self) -> Tuple[float, float]:
        return get_average_gap_between_child_elements(self._structure_element)

    def calculate_average_gap_between_nested_child_elements(self, element_type: OpticalStructureHierarchyLevel) -> Tuple[float, float]:
        return get_average_gap_between_nested_child_elements(self._structure_element, element_type)
