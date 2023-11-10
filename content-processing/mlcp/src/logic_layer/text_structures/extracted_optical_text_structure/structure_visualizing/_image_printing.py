import colorsys
import math
from typing import List

import cv2
import numpy as np

from logic_layer.text_structures.extracted_optical_text_structure._structure_calculations import StructureGeometryCalculator
from logic_layer.text_structures.extracted_optical_text_structure._structure_calculations._geometry_calculations._rectangle_utils import get_rectangles_enclosing_rectangle
from logic_layer.text_structures.extracted_optical_text_structure._structure_element import OpticalTextStructureElement
from logic_layer.text_structures.extracted_optical_text_structure._structure_root import OpticalTextStructureRoot
from logic_layer.text_structures.extracted_optical_text_structure._types import OpticalStructureElementBoundingRectangle
from logic_layer.text_structures.extracted_optical_text_structure.structure_visualizing._assertions import assert_number_of_images_matches_number_of_structure_groups
from logic_layer.text_structures.extracted_optical_text_structure.structure_visualizing._assertions import assert_real_image


def print_structure_children_to_images(structure_root: OpticalTextStructureRoot, image_directories: List[str], line_thickness: int = 4):
    assert_number_of_images_matches_number_of_structure_groups(structure_root, image_directories)
    for num, group in enumerate(structure_root.get_children()):
        image_directory = image_directories[num]
        image = cv2.imread(image_directory)
        assert_real_image(image)
        image = print_structure_element_to_image(group, image, line_thickness)
        cv2.imwrite(image_directory, image)


def print_structure_element_to_image(structure_element: OpticalTextStructureElement, target_image: np.array, line_thickness: int = 1, _hue: float = 0) -> np.array:
    assert_real_image(target_image)
    display_rect = get_display_rect_for_structure_element(structure_element, line_thickness=line_thickness)
    color = tuple(c * 255 for c in colorsys.hsv_to_rgb(_hue, 1, 1))
    target_image = cv2.rectangle(target_image, (int(display_rect[0]), int(display_rect[1])), (int(display_rect[2]), int(display_rect[3])), color, line_thickness)
    if not structure_element.is_leaf():
        for child in structure_element.get_children():
            target_image = print_structure_element_to_image(child, target_image, line_thickness, (_hue + 0.3) % 1)
    return target_image


def get_display_rect_for_structure_element(structure_element: OpticalTextStructureElement, line_thickness: int = 1) -> OpticalStructureElementBoundingRectangle:
    if structure_element.is_leaf(): return structure_element.get_bounding_rect()
    element_children = structure_element.get_children()
    children_rectangles = [get_display_rect_for_structure_element(child, line_thickness) for child in element_children]
    element_rect = get_rectangles_enclosing_rectangle(children_rectangles)
    element_rect = (element_rect[0] - line_thickness, element_rect[1] - line_thickness, element_rect[2] + line_thickness, element_rect[3] + line_thickness)
    return element_rect
