from abc import abstractmethod
from typing import List

from service.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureCharacter
from service.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureLine
from service.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from service.extracted_optical_text_structure._structure_element import OpticalTextStructureElement


class MergeLogicImplementation:
    @classmethod
    def merge_mergeable_element_children(cls, element: OpticalTextStructureElement, recursive: bool = True) -> OpticalTextStructureElement:
        children_type = element.get_children_type()

        children = element.get_children()

        if children_type == OpticalTextStructureLine:
            new_children = cls._merge_line_elements(children)
        elif children_type == OpticalTextStructureWord:
            new_children = cls._merge_word_elements(children)
        elif children_type == OpticalTextStructureCharacter:
            new_children = cls._merge_character_elements(children)
        else:
            new_children = children

        if recursive and not element.is_leaf():
            new_children = [cls.merge_mergeable_element_children(element=child, recursive=recursive) for child in new_children]

        element.set_children(new_children)

        return element

    @classmethod
    @abstractmethod
    def _merge_line_elements(cls, line_elements: List[OpticalTextStructureLine]) -> List[OpticalTextStructureLine]:
        return line_elements

    @classmethod
    @abstractmethod
    def _merge_word_elements(cls, word_elements: List[OpticalTextStructureWord]) -> List[OpticalTextStructureWord]:
        return word_elements

    @classmethod
    @abstractmethod
    def _merge_character_elements(cls, character_elements: List[OpticalTextStructureCharacter]) -> List[OpticalTextStructureCharacter]:
        return character_elements

    @classmethod
    def _merge_elements_to_one(cls, elements: List[OpticalTextStructureElement]) -> OpticalTextStructureElement:
        total_children = cls._unpack_children(elements)
        merged_element = elements[0].__class__()
        merged_element.set_children(total_children)
        return merged_element

    @classmethod
    def _unpack_children(cls, elements: List[OpticalTextStructureElement]) -> List[OpticalTextStructureElement]:
        total_children = []
        for element in elements:
            total_children.extend(element.get_children())
        return total_children
