from typing import Tuple

from logic_layer.text_structures.extracted_optical_text_structure import OpticalTextStructureElement


def scale_element(element: OpticalTextStructureElement, scale: Tuple[float, float]):
    if element.is_leaf():
        bounding_rect = element.get_bounding_rect()
        bounding_rect = (
            bounding_rect[0] * scale[0],
            bounding_rect[1] * scale[1],
            bounding_rect[2] * scale[0],
            bounding_rect[3] * scale[1]
        )
        element.set_bounding_rect(bounding_rect)
        return
    for child in element.get_children():
        scale_element(child, scale)