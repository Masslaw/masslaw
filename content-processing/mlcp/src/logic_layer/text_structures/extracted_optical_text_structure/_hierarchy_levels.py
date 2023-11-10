from typing import Type

from logic_layer.text_structures.extracted_optical_text_structure._structure_element import OpticalTextStructureElement
from logic_layer.text_structures.extracted_optical_text_structure._types import OpticalStructureElementOrderDirection
from logic_layer.text_structures.extracted_optical_text_structure._types import OpticalStructureHierarchyLevel


class OpticalTextStructureGroup(OpticalTextStructureElement):
    _children_separator = '\n\n\n'
    _label = 'gr'
    _children_order_direction = OpticalStructureElementOrderDirection.VERTICAL


class OpticalTextStructureBlock(OpticalTextStructureElement):
    _children_separator = '\n\n'
    _label = 'bl'
    _children_order_direction = OpticalStructureElementOrderDirection.VERTICAL


class OpticalTextStructureParagraph(OpticalTextStructureElement):
    _children_separator = '\n'
    _label = 'pr'
    _children_order_direction = OpticalStructureElementOrderDirection.VERTICAL


class OpticalTextStructureLine(OpticalTextStructureElement):
    _children_separator = ' '
    _label = 'ln'
    _children_order_direction = OpticalStructureElementOrderDirection.HORIZONTAL


class OpticalTextStructureWord(OpticalTextStructureElement):
    _children_separator = ''
    _label = 'wd'
    _children_order_direction = OpticalStructureElementOrderDirection.HORIZONTAL


class OpticalTextStructureCharacter(OpticalTextStructureElement):
    _children_separator = ''
    _label = 'cr'
    _children_order_direction = OpticalStructureElementOrderDirection.HORIZONTAL


def hierarchy_level_to_element_class(hierarchy_level: OpticalStructureHierarchyLevel) -> Type[OpticalTextStructureElement]:
    return {
        OpticalStructureHierarchyLevel.GROUP: OpticalTextStructureGroup,
        OpticalStructureHierarchyLevel.BLOCK: OpticalTextStructureBlock,
        OpticalStructureHierarchyLevel.PARAGRAPH: OpticalTextStructureParagraph,
        OpticalStructureHierarchyLevel.LINE: OpticalTextStructureLine,
        OpticalStructureHierarchyLevel.WORD: OpticalTextStructureWord,
        OpticalStructureHierarchyLevel.CHARACTER: OpticalTextStructureCharacter,
    }.get(hierarchy_level, OpticalTextStructureElement)
