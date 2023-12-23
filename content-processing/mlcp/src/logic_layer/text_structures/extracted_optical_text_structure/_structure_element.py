from typing import Dict
from typing import List
from typing import Optional
from typing import Type

from logic_layer.text_structures.extracted_optical_text_structure._exceptions import StructureElementInvalidDefinitionException
from logic_layer.text_structures.extracted_optical_text_structure._types import OpticalStructureElementBoundingRectangle
from logic_layer.text_structures.extracted_optical_text_structure._types import OpticalStructureElementOrderDirection


class OpticalTextStructureElement:
    _label: str = 'el'
    _children_separator: str = ''
    _children_order_direction: OpticalStructureElementOrderDirection = OpticalStructureElementOrderDirection.HORIZONTAL

    _children: List = []
    _bounding_rect: OpticalStructureElementBoundingRectangle = (0, 0, 0, 0)
    _properties: dict = {}

    def __init__(self, children: List = None, bounding_rect: OpticalStructureElementBoundingRectangle = None, properties: Dict = None) -> object:
        children and self.set_children(children)
        bounding_rect and self.set_bounding_rect(bounding_rect)
        self._properties = properties or {}

    @classmethod
    def get_label(cls) -> str:
        return cls._label

    @classmethod
    def get_children_separator(cls) -> str:
        return cls._children_separator

    @classmethod
    def get_children_order_direction(cls) -> OpticalStructureElementOrderDirection:
        return cls._children_order_direction

    def get_type(self):
        return self.__class__

    def set_children(self, children):
        self._children = children

    def get_children(self) -> List['OpticalTextStructureElement']:
        return self._children

    def is_empty(self) -> bool:
        return len(self._children) == 0

    def get_children_type(self) -> Optional[Type]:
        return len(self._children) > 0 and self._children[0].__class__ or None

    def set_bounding_rect(self, bounding_rect: OpticalStructureElementBoundingRectangle):
        if not self.is_leaf(): return None
        self._bounding_rect = bounding_rect

    def get_bounding_rect(self) -> Optional[OpticalStructureElementBoundingRectangle]:
        if not self.is_leaf(): return None
        return self._bounding_rect

    def get_value(self) -> str:
        return self.get_children_separator().join([str(child) for child in self.get_children()])

    def is_leaf(self):
        return not issubclass(self.get_children_type() or str, OpticalTextStructureElement)

    def get_property(self, property_name: str) -> Optional[any]:
        return self._properties.get(property_name)

    def set_property(self, property_name: str, property_value: any):
        self._properties[property_name] = property_value

    def delete_property(self, property_name: str):
        self._properties.pop(property_name, None)

    def get_properties(self) -> dict:
        return self._properties

    def set_properties(self, properties: dict):
        self._properties = properties

    def __str__(self):
        return self.get_value()

    @classmethod
    def assert_class_properties(cls):
        if cls.get_children_order_direction() not in [OpticalStructureElementOrderDirection.HORIZONTAL.value, OpticalStructureElementOrderDirection.VERTICAL.value]:
            raise StructureElementInvalidDefinitionException(property_name='children_order_direction', structure_element_class=cls.__name__)
