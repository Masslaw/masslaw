from typing import Type


class StructureElementInvalidDefinitionException(Exception):
    def __init__(self, property_name: str, structure_element_class: str):
        super().__init__(f'Invalid property "{property_name}" in structure hierarchy '
                         f'level implementation: "{structure_element_class}"')


class DuplicateLevelsInStructureHierarchyFormationException(ValueError):
    def __init__(self):
        super().__init__('A structure element has been initialized with a '
                         'hierarchy structure that contains duplicate types')


class EmptyStructureHierarchyFormationException(ValueError):
    def __init__(self):
        super().__init__('Provided an empty structure hierarchy formation list')


class InvalidChildTypeException(ValueError):
    def __init__(self, expected_type: Type, provided_type: Type):
        super().__init__(f'Te provided child has the type "{provided_type}" which is different '
                         f'than the expected type "{expected_type}')
