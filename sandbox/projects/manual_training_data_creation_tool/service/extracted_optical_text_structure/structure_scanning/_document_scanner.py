from typing import List

from service.extracted_optical_text_structure import ExtractedOpticalTextDocument
from service.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from service.extracted_optical_text_structure import OpticalTextStructureElement
from service.extracted_optical_text_structure._hierarchy_levels import hierarchy_level_to_element_class
from service.extracted_optical_text_structure.structure_scanning._element_tree_traverse_logic import collect_all_nested_children_of_type


class OpticalDocumentStructureScanner:
    def __init__(self, document: ExtractedOpticalTextDocument):
        self._document = document

    def collect_all_nested_children_of_type(self, elements_type: OpticalStructureHierarchyLevel) -> List[OpticalTextStructureElement]:
        element_class = hierarchy_level_to_element_class(elements_type)
        nested_children = []
        for structure_child in self._document.get_structure_root().get_children():
            if structure_child.get_type() == element_class: nested_children.append(structure_child)
            nested_children += collect_all_nested_children_of_type(structure_child, elements_type)
        return nested_children

    def count_all_nested_children_of_type(self, elements_type: OpticalStructureHierarchyLevel) -> int:
        return len(self.collect_all_nested_children_of_type(elements_type))