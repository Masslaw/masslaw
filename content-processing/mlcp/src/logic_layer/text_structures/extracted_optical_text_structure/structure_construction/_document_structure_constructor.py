from typing import List

from logic_layer.text_structures.extracted_optical_text_structure._document import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure._types import OpticalElementRawDataEntry
from logic_layer.text_structures.extracted_optical_text_structure.structure_construction._structure_constructor import StructureConstructor


class OpticalTextStructureConstructor:
    def __init__(self, document: ExtractedOpticalTextDocument):
        self._document = document
        structure = self._document.get_structure_root()
        self._constructor = StructureConstructor(structure)

    def add_entry_groups_to_structure(self, entry_groups: List[List[OpticalElementRawDataEntry]]):
        self._constructor.add_entry_groups_as_structure_children(entry_groups=entry_groups)

    def add_structured_entry_groups_to_structure(self, structured_entry_groups: List[List]):
        self._constructor.add_structured_entry_groups_to_structure(structured_entry_groups=structured_entry_groups)
