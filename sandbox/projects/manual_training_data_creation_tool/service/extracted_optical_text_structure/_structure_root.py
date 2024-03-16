from typing import List
from typing import Type

from service.extracted_optical_text_structure._structure_element import OpticalTextStructureElement


class OpticalTextStructureRoot:
    _children: List[OpticalTextStructureElement]

    def __init__(self):
        self._children = []

    def set_children(self, children: List[OpticalTextStructureElement]):
        self._children = children

    def get_children(self) -> List[OpticalTextStructureElement]:
        return self._children

    def get_children_type(self) -> Type[OpticalTextStructureElement] | None:
        return len(self._children) > 0 and self._children[0].__class__ or None
