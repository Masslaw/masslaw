from typing import Type

from service.extracted_optical_text_structure._structure_element import OpticalTextStructureElement
from service.extracted_optical_text_structure.structure_construction._structure_hierarchy_formation import OpticalStructureHierarchyFormation


class StructureConstructionElementNestingException(TypeError):
    def __init__(self, hierarchy_formation: OpticalStructureHierarchyFormation, child_class: Type[OpticalTextStructureElement]):
        super().__init__(f'Element of type "{child_class.__name__}" is not a nested child in hierarchy: "{hierarchy_formation}')


class StructureConstructionInvalidElementTypeException(TypeError):
    def __init__(self, expected_type: Type, child_class: Type[OpticalTextStructureElement]):
        super().__init__(f'Element of type "{child_class.__name__}" is does not match '
                         f'the expected type "{expected_type.__class__}"')


class EmptyConstructionStructureHierarchyFormationException(ValueError):
    def __init__(self):
        super().__init__('An empty structure hierarchy formation has been provided')
