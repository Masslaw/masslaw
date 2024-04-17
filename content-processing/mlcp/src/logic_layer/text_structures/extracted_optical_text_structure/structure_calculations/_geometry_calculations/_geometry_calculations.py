from typing import List
from typing import Tuple

import numpy as np

from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import hierarchy_level_to_element_class
from logic_layer.text_structures.extracted_optical_text_structure._structure_element import OpticalTextStructureElement
from logic_layer.text_structures.extracted_optical_text_structure._types import OpticalStructureElementBoundingRectangle
from logic_layer.text_structures.extracted_optical_text_structure._types import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure.structure_calculations._geometry_calculations._rectangle_utils import get_average_dimensions_of_rectangles
from logic_layer.text_structures.extracted_optical_text_structure.structure_calculations._geometry_calculations._rectangle_utils import get_rectangles_enclosing_rectangle
from logic_layer.text_structures.extracted_optical_text_structure.structure_scanning import OpticalTextStructureScanner
from shared_layer.concurrency_utils import run_thread_batch


def get_element_bounding_rectangle(element: OpticalTextStructureElement) -> OpticalStructureElementBoundingRectangle:
    bounding_rectangle = element.get_bounding_rect()
    if bounding_rectangle: return bounding_rectangle
    children_rectangles = batch_convert_elements_to_rectangles(element.get_children())
    return get_rectangles_enclosing_rectangle(children_rectangles)


def get_element_children_average_size(element: OpticalTextStructureElement) -> Tuple[float, float]:
    if element.is_leaf(): return 0, 0
    children = element.get_children()
    children_rectangles = batch_convert_elements_to_rectangles(children)
    average_size = get_average_dimensions_of_rectangles(children_rectangles)
    return average_size


def get_element_nested_children_average_size(element: OpticalTextStructureElement, element_type: OpticalStructureHierarchyLevel) -> Tuple[float, float]:
    scanner = OpticalTextStructureScanner(element)
    nested_elements = scanner.collect_all_nested_children_of_type(element_type)
    nested_element_rectangles = batch_convert_elements_to_rectangles(nested_elements)
    average_size = get_average_dimensions_of_rectangles(nested_element_rectangles)
    return average_size


def get_average_gap_between_child_elements(element: OpticalTextStructureElement) -> Tuple[float, float]:
    children = element.get_children()
    average_gap = get_average_gap_between_elements(children)
    return average_gap


def get_average_gap_between_nested_child_elements(element: OpticalTextStructureElement, element_type: OpticalStructureHierarchyLevel) -> Tuple[float, float]:
    if element.is_leaf(): return 0, 0
    children = element.get_children()
    if element.get_children_type() == hierarchy_level_to_element_class(element_type):
        average_gap = get_average_gap_between_elements(children)
    else:
        gaps = [get_average_gap_between_nested_child_elements(child, element_type) for child in children]
        average_gap = mean_of_tuples(gaps)
    return average_gap


def get_average_gap_between_elements(elements: List[OpticalTextStructureElement]) -> Tuple[float, float]:
    def get_gap(elements: Tuple[OpticalTextStructureElement, OpticalTextStructureElement]):
        rect1 = get_element_bounding_rectangle(elements[0])
        rect2 = get_element_bounding_rectangle(elements[1])
        return (max(0.0, rect2[0] - rect1[2], rect1[0] - rect2[2]), max(0.0, rect2[1] - rect1[3], rect1[1] - rect2[3]))

    if len(elements) < 2: return 0, 0
    element_pairs = [(elements[i], elements[i + 1]) for i in range(len(elements) - 1)]
    gaps = run_thread_batch(func=get_gap, batch_inputs=element_pairs)
    average = mean_of_tuples(gaps)
    return average


def mean_of_tuples(tuples: List[Tuple[float, float]]) -> Tuple[float, float]:
    if len(tuples) == 0: return 0, 0
    return tuple(np.mean(np.array(tuples), axis=0))


def batch_convert_elements_to_rectangles(elements: List[OpticalTextStructureElement]) -> List[OpticalStructureElementBoundingRectangle]:
    return run_thread_batch(func=get_element_bounding_rectangle, batch_inputs=elements)
