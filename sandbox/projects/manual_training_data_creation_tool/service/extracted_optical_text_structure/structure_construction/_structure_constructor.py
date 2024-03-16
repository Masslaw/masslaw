from typing import List

from service.extracted_optical_text_structure._structure_element import OpticalTextStructureElement
from service.extracted_optical_text_structure._structure_root import OpticalTextStructureRoot
from service.extracted_optical_text_structure._types import OpticalElementRawDataEntry
from service.extracted_optical_text_structure.structure_construction._construction import construction_logic
from service.extracted_optical_text_structure.structure_construction._structure_hierarchy_formation import OpticalStructureHierarchyFormation
from service.concurrency_utils import run_thread_batch


class StructureConstructor:
    def __init__(self, structure: OpticalTextStructureRoot, hierarchy_formation: OpticalStructureHierarchyFormation):
        self._structure = structure
        self._hierarchy_formation = hierarchy_formation

    def add_entry_groups_as_structure_children(self, entry_groups: List[List[OpticalElementRawDataEntry]]):
        element_groups = run_thread_batch(func=self.convert_entries_to_elements, batch_inputs=entry_groups)
        structure_new_children = run_thread_batch(func=self.construct_structure_child_from_element_group, batch_inputs=element_groups)
        structure_children = self._structure.get_children()
        self._structure.set_children(structure_children + structure_new_children)

    def construct_structure_child_from_element_group(self, element_group: List[OpticalTextStructureElement]) -> OpticalTextStructureRoot:
        constructed_element = construction_logic.construct_element_with_hierarchy(structure_elements=element_group, hierarchy_formation=self._hierarchy_formation)
        return constructed_element

    def convert_entries_to_elements(self, entries: List[OpticalElementRawDataEntry]) -> List[OpticalTextStructureElement]:
        elements = run_thread_batch(func=self.get_appropriate_element, batch_inputs=entries)
        return elements

    def get_appropriate_element(self, text_element_entry: OpticalElementRawDataEntry) -> OpticalTextStructureElement:
        text_element = construction_logic.get_appropriate_element_for_entry_in_structure_hierarchy(entry=text_element_entry, hierarchy_formation=self._hierarchy_formation)
        return text_element

    def add_structured_entry_groups_to_structure(self, structured_entry_groups: List[List]):
        constructed_children = run_thread_batch(func=self.construct_structure_child_from_structured_entries, batch_inputs=structured_entry_groups)
        structure_children = self._structure.get_children()
        self._structure.set_children(structure_children + constructed_children)

    def construct_structure_child_from_structured_entries(self, structured_entries: List) -> OpticalTextStructureElement:
        constructed_element = construction_logic.construct_element_from_structured_entries(structured_entries=structured_entries, hierarchy_formation=self._hierarchy_formation)
        return constructed_element
