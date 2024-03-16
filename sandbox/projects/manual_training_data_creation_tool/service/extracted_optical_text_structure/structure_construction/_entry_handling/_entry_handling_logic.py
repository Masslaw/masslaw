from typing import List

from service.bidi._bidi_text_handling_logic import get_text_direction
from service.bidi._bidi_text_handling_logic import swap_ordering_between_read_direction_and_ltr
from service.extracted_optical_text_structure import OpticalElementRawDataEntry
from service.extracted_optical_text_structure import OpticalStructureElementOrderDirection
from service.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from service.extracted_optical_text_structure._hierarchy_levels import hierarchy_level_to_element_class
from service.extracted_optical_text_structure.structure_construction._entry_handling._entry_wrapper import EntryWrapper


def split_entry_by_element_type(entry: OpticalElementRawDataEntry, element_type: OpticalStructureHierarchyLevel) -> List[OpticalElementRawDataEntry]:
    element_class = hierarchy_level_to_element_class(element_type)
    direction = element_class.get_children_order_direction()
    separator = element_class.get_children_separator()
    if direction == OpticalStructureElementOrderDirection.HORIZONTAL:
        return split_entry_with_separator_horizontally(entry, separator)

    if direction == OpticalStructureElementOrderDirection.VERTICAL:
        return split_entry_with_separator_vertically(entry, separator)

    return [entry]


def split_entry_with_separator_horizontally(entry: OpticalElementRawDataEntry, separator: str) -> List[OpticalElementRawDataEntry]:
    entry_value, (x1, y1, x2, y2) = entry

    separator_length = 0 if separator == '\n' else len(separator)

    child_parts = separator and entry_value.split(separator) or list(entry_value)
    text_direction = get_text_direction(child_parts[0])
    child_parts = swap_ordering_between_read_direction_and_ltr(child_parts, text_direction)

    total_width = x2 - x1
    single_char_width = total_width / (len(entry_value) - entry_value.count('\n'))

    child_entries = []
    current_x = x1
    for part in child_parts:
        part_width = len(part) * single_char_width
        part_x2 = current_x + part_width
        child_entries.append((part, (current_x, y1, part_x2, y2)))
        current_x = part_x2 + separator_length * single_char_width

    wrappers = [EntryWrapper(entry) for entry in child_entries]
    reordered_wrappers = swap_ordering_between_read_direction_and_ltr(wrappers, text_direction)
    child_entries = [wrapper.get_entry() for wrapper in reordered_wrappers]

    return child_entries


def split_entry_with_separator_vertically(entry: OpticalElementRawDataEntry, separator: str) -> List[OpticalElementRawDataEntry]:
    entry_value, (x1, y1, x2, y2) = entry

    separator_length = 0 if separator == '\n' else len(separator)

    child_parts = entry_value.split(separator)

    total_height = y2 - y1
    single_line_height = total_height / len(child_parts)

    child_entries = []
    current_y = y1
    for part in child_parts:
        part_y2 = current_y + single_line_height
        child_entries.append((part, (x1, current_y, x2, part_y2)))
        current_y = part_y2 + separator_length * single_line_height

    return child_entries
