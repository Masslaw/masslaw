from logic_layer.text_structures.extracted_optical_text_structure._structure_element import OpticalTextStructureElement
from logic_layer.text_structures.extracted_optical_text_structure.structure_calculations import StructureGeometryCalculator


def line_continuity_check_function(element1: OpticalTextStructureElement, element2: OpticalTextStructureElement) -> bool:
    rect1 = StructureGeometryCalculator(element1).calculate_bounding_rect()
    rect2 = StructureGeometryCalculator(element2).calculate_bounding_rect()

    y1_diff = abs(rect1[1] - rect2[1])
    y2_diff = abs(rect1[3] - rect2[3])
    h1 = abs(rect1[3] - rect1[1])
    h2 = abs(rect2[3] - rect2[1])
    h_diff = abs(h1 - h2)
    h_avg = (h1 + h2) / 2

    if h_diff > h_avg * 0.5:
        return False

    if y1_diff + y2_diff > h_avg * 0.5:
        return False

    char_count1 = len(element1.get_value())
    char_count2 = len(element2.get_value())

    if char_count1 == 0 or char_count2 == 0:
        return False

    w1 = abs(rect1[2] - rect1[0])
    w2 = abs(rect2[2] - rect2[0])
    avg_char_width1 = w1 / char_count1
    avg_char_width2 = w2 / char_count2
    avg_char_diff = abs(avg_char_width1 - avg_char_width2)
    avg_char_width = (avg_char_width1 + avg_char_width2) / 2

    if avg_char_diff > avg_char_width / 3:
        return False

    gap = min(abs(rect1[2] - rect2[0]), abs(rect1[0] - rect2[2]))

    if gap > avg_char_width * 5:
        return False

    return True


def word_continuity_check_function(element1: OpticalTextStructureElement, element2: OpticalTextStructureElement) -> bool:
    rect1 = StructureGeometryCalculator(element1).calculate_bounding_rect()
    rect2 = StructureGeometryCalculator(element2).calculate_bounding_rect()

    y1_diff = abs(rect1[1] - rect2[1])
    y2_diff = abs(rect1[3] - rect2[3])
    h1 = abs(rect1[3] - rect1[1])
    h2 = abs(rect2[3] - rect2[1])
    h_diff = abs(h1 - h2)
    h_avg = (h1 + h2) / 2

    if h_diff > h_avg * 0.5:
        return False

    if y1_diff + y2_diff > h_avg * 0.5:
        return False

    char_count1 = len(element1.get_value())
    char_count2 = len(element2.get_value())

    if char_count1 == 0 or char_count2 == 0:
        return False

    w1 = abs(rect1[2] - rect1[0])
    w2 = abs(rect2[2] - rect2[0])
    avg_char_width1 = w1 / char_count1
    avg_char_width2 = w2 / char_count2
    avg_char_diff = abs(avg_char_width1 - avg_char_width2)
    avg_char_width = (avg_char_width1 + avg_char_width2) / 2

    if avg_char_diff > avg_char_width * 0.5:
        return False

    gap = min(abs(rect1[2] - rect2[0]), abs(rect1[0] - rect2[2]))

    if gap > avg_char_width * 0.5:
        return False

    return True
