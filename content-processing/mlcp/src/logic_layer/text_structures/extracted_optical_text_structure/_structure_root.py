from typing import List

from logic_layer.text_structures.extracted_optical_text_structure._assertions import assert_hierarchy_formation
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure._structure_element import OpticalTextStructureElement


class OpticalTextStructureRoot:
    _hierarchy_formation: List[OpticalStructureHierarchyLevel]
    _children: List[OpticalTextStructureElement]

    def __init__(self, hierarchy_formation: List[OpticalStructureHierarchyLevel]) -> object:
        assert_hierarchy_formation(hierarchy_formation=hierarchy_formation)
        self._hierarchy_formation: List[OpticalStructureHierarchyLevel] = hierarchy_formation
        self._children: List[hierarchy_formation[0]] = []

    def set_children(self, children: List[OpticalTextStructureElement]):
        self._children = children

    def get_children(self) -> List[OpticalTextStructureElement]:
        return self._children

    def get_hierarchy_formation(self):
        return self._hierarchy_formation
