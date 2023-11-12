from typing import List
from typing import Tuple

import numpy as np

from logic_layer.text_structures.extracted_optical_text_structure._types import OpticalStructureElementBoundingRectangle
from logic_layer.text_structures.extracted_optical_text_structure._types import OpticalStructureElementOrderDirection


def get_rectangles_enclosing_rectangle(rectangles: List[OpticalStructureElementBoundingRectangle]) -> OpticalStructureElementBoundingRectangle:
    np_rectangles = np.array(rectangles)

    min_x = np.min(np_rectangles[:, 0])
    min_y = np.min(np_rectangles[:, 1])
    max_x = np.max(np_rectangles[:, 2])
    max_y = np.max(np_rectangles[:, 3])

    enclosing_rectangle = (min_x, min_y, max_x, max_y)
    return enclosing_rectangle


def split_rect_by_direction(rect: OpticalStructureElementBoundingRectangle, direction: OpticalStructureElementOrderDirection, count: int) -> List[OpticalStructureElementBoundingRectangle]:
    _width = get_rectangle_width(rect)
    _height = get_rectangle_height(rect)
    if direction == OpticalStructureElementOrderDirection.HORIZONTAL:
        return [(rect[0] + (_width * i / count), rect[1], rect[0] + (_width * (i + 1) / count), rect[3]) for i in range(count)]
    elif direction == OpticalStructureElementOrderDirection.VERTICAL:
        return [(rect[0], rect[1] + (_height * i / count), rect[2], rect[1] + (_height * (i + 1) / count)) for i in range(count)]
    else:
        return [rect]


def get_average_dimensions_of_rectangles(rectangles: List[OpticalStructureElementBoundingRectangle]) -> Tuple[float, float]:
    if len(rectangles) < 1: return 0, 0
    widths = [get_rectangle_width(rectangle) for rectangle in rectangles]
    heights = [get_rectangle_height(rectangle) for rectangle in rectangles]
    sum_widths = sum(widths)
    sum_heights = sum(heights)
    average_width = sum_widths / len(rectangles)
    average_height = sum_heights / len(rectangles)
    return average_width, average_height


def get_rectangle_width(rect: OpticalStructureElementBoundingRectangle) -> float:
    return abs(rect[2] - rect[0])


def get_rectangle_height(rect: OpticalStructureElementBoundingRectangle) -> float:
    return abs(rect[3] - rect[1])
