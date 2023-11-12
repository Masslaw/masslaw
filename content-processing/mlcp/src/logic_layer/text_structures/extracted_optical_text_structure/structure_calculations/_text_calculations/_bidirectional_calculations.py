from typing import List

from logic_layer.bidi import ReadDirection
from logic_layer.bidi import get_text_direction
from logic_layer.text_structures.extracted_optical_text_structure._structure_element import OpticalTextStructureElement


def calculate_element_text_direction(element: OpticalTextStructureElement) -> ReadDirection:
    if element.is_leaf():
        return get_text_direction(element.get_value())
    element_children = element.get_children()
    return calculate_elements_overall_direction(element_children)


def calculate_elements_overall_direction(elements: List[OpticalTextStructureElement], dominance_threshold=0.6) -> ReadDirection:
    if not len(elements):
        return ReadDirection.LTR

    num_directional = 0
    sum_directional = 0
    for elem in elements:
        c_dir = calculate_element_text_direction(elem)
        dir_value = int(c_dir.value)
        sum_directional += dir_value
        num_directional += abs(dir_value)

    if num_directional == 0:
        return ReadDirection.AMBIGUOUS

    direction_dominance = sum_directional / num_directional

    if calculate_element_text_direction(elements[-1]) == ReadDirection.RTL and direction_dominance < -dominance_threshold:
        return ReadDirection.RTL

    if calculate_element_text_direction(elements[0]) == ReadDirection.LTR and direction_dominance > dominance_threshold:
        return ReadDirection.LTR

    if direction_dominance == 0:
        return ReadDirection.AMBIGUOUS

    return ReadDirection(int(direction_dominance / abs(direction_dominance)))
