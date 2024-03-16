import itertools
from typing import List

from service.bidi import ReadDirection
from service.extracted_optical_text_structure.structure_calculations import StructureGeometryCalculator
from service.extracted_optical_text_structure.structure_calculations import StructureTextCalculator
from service.extracted_optical_text_structure._structure_element import OpticalStructureElementOrderDirection
from service.extracted_optical_text_structure._structure_element import OpticalTextStructureElement


def sort_element_hierarchy(element: OpticalTextStructureElement):
    sort_element_immediate_children(element)
    for child in element.get_children():
        if child.is_leaf(): continue
        sort_element_hierarchy(child)


def sort_element_immediate_children(element: OpticalTextStructureElement):
    structure_text_calculator = StructureTextCalculator(element)
    element_text_direction = structure_text_calculator.calculate_text_direction()
    element_children = element.get_children()
    element_order_direction = element.get_children_order_direction()
    if element_order_direction == OpticalStructureElementOrderDirection.HORIZONTAL:
        sorted_elements = sort_elements_horizontally(elements=element_children, direction=element_text_direction)
    elif element_order_direction == OpticalStructureElementOrderDirection.VERTICAL:
        sorted_elements = sort_elements_vertically(elements=element_children)
    else:
        sorted_elements = element_children

    element.set_children(sorted_elements)


def sort_elements_horizontally(elements: List[OpticalTextStructureElement], direction: ReadDirection):
    ltr_sorted = sort_elements_left_to_right(elements=elements)
    sorted_elements = sort_ltr_sorted_elements_by_direction(elements=ltr_sorted, direction=direction)
    return sorted_elements


def sort_elements_vertically(elements: List[OpticalTextStructureElement]):
    sorted_elements = sort_elements_top_to_bottom(elements=elements)
    return sorted_elements


def sort_elements_left_to_right(elements: List[OpticalTextStructureElement]):
    return sorted(elements, key=lambda e: StructureGeometryCalculator(e).calculate_bounding_rect()[0])


def sort_elements_top_to_bottom(elements: List[OpticalTextStructureElement]):
    return sorted(elements, key=lambda e: StructureGeometryCalculator(e).calculate_bounding_rect()[1])


def sort_ltr_sorted_elements_by_direction(elements: List[OpticalTextStructureElement], direction: ReadDirection):
    if not len(elements): return elements

    if direction.value < 0: elements = elements[::-1]

    chunks = itertools.groupby(elements, key=lambda elem: StructureTextCalculator(elem).calculate_text_direction())

    sorted_elements = []
    for chunk_direction, chunk in chunks:
        chunk = list(chunk)
        if chunk_direction != direction:
            chunk = chunk[::-1]
        sorted_elements.extend(chunk)

    return sorted_elements
