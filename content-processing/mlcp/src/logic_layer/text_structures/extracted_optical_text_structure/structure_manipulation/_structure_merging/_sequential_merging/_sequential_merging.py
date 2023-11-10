from typing import List

from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureCharacter
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureLine
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from logic_layer.text_structures.extracted_optical_text_structure._structure_element import OpticalTextStructureElement
from logic_layer.text_structures.extracted_optical_text_structure.structure_manipulation._structure_merging._base_merge_logic import MergeLogicImplementation
from logic_layer.text_structures.extracted_optical_text_structure.structure_manipulation._structure_merging._sequential_merging._continuity_check_functions import line_continuity_check_function
from logic_layer.text_structures.extracted_optical_text_structure.structure_manipulation._structure_merging._sequential_merging._continuity_check_functions import word_continuity_check_function


class SequentialMerging(MergeLogicImplementation):
    @classmethod
    def _merge_line_elements(cls, line_elements: List[OpticalTextStructureLine]) -> List[OpticalTextStructureLine]:
        merged_lines = cls._merge_elements_sequentially(elements=line_elements, continuity_check_function=line_continuity_check_function)

        return merged_lines

    @classmethod
    def _merge_word_elements(cls, word_elements: List[OpticalTextStructureWord]) -> List[OpticalTextStructureWord]:
        merged_words = cls._merge_elements_sequentially(elements=word_elements, continuity_check_function=word_continuity_check_function)

        return merged_words

    @classmethod
    def _merge_character_elements(cls, character_elements: List[OpticalTextStructureCharacter]) -> List[OpticalTextStructureCharacter]:
        return character_elements

    @classmethod
    def _merge_elements_sequentially(cls, elements: List[OpticalTextStructureElement],
            continuity_check_function: "(elements: Tuple[OpticalTextStructureElement, OpticalTextStructureElement]) -> bool") -> List[OpticalTextStructureElement]:
        if len(elements) == 0:
            return []

        mergeable_groups = []
        current_group = [elements[0]]
        for idx in range(1, len(elements)):
            if continuity_check_function(elements[idx - 1], elements[idx]):
                current_group.append(elements[idx])
                continue
            mergeable_groups.append(current_group)
            current_group = [elements[idx]]
        mergeable_groups.append(current_group)

        merged_elements = [cls._merge_elements_to_one(group) for group in mergeable_groups]

        return merged_elements
