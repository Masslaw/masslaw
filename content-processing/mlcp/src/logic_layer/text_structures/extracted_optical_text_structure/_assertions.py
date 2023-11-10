from typing import Type

from logic_layer.text_structures.extracted_optical_text_structure._exceptions import InvalidChildTypeException
from logic_layer.text_structures.extracted_optical_text_structure._exceptions import DuplicateLevelsInStructureHierarchyFormationException
from logic_layer.text_structures.extracted_optical_text_structure._exceptions import EmptyStructureHierarchyFormationException


def assert_hierarchy_formation(hierarchy_formation: 'StructureHierarchyFormation'):
    if len(hierarchy_formation) == 0:
        raise EmptyStructureHierarchyFormationException()
    _types = set()
    duplicated_types = [_t for _t in hierarchy_formation if _t in _types or _types.add(_t)]
    if len(duplicated_types) > 0:
        raise DuplicateLevelsInStructureHierarchyFormationException()


def assert_child_type(expected_type: Type, provided_type: Type):
    if (expected_type or provided_type) == provided_type: return
    raise InvalidChildTypeException(expected_type=expected_type, provided_type=provided_type)
