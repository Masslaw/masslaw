from typing import List

from logic_layer.text_structures.extracted_optical_text_structure._structure_element import OpticalTextStructureElement


class OpticalTextStructureRoot:
    _children: List[OpticalTextStructureElement]

    def __init__(self):
        self._children = []

    def set_children(self, children: List[OpticalTextStructureElement]):
        self._children = children

    def get_children(self) -> List[OpticalTextStructureElement]:
        return self._children
