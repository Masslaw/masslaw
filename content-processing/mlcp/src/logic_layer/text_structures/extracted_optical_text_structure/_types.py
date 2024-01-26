from enum import Enum
from typing import Tuple
from typing import Type


# this indicates the order direction of elements within a text element
class OpticalStructureElementOrderDirection(Enum):
    HORIZONTAL = 'h'
    VERTICAL = 'v'


# this indicates the type of hierarchy element that should exist at a certain level of the structure
class OpticalStructureHierarchyLevel(Enum):
    GROUP = 'group'
    BLOCK = 'block'
    PARAGRAPH = 'paragraph'
    LINE = 'line'
    WORD = 'word'
    CHARACTER = 'char'


# defined as (x1, y1, x2, y2)
OpticalStructureElementBoundingRectangle: Type = Tuple[float, float, float, float]

# will be the shape of a single raw data entry to the construction system (that turns it into a hierarchy element)
OpticalElementRawDataEntry: Type = Tuple[str, OpticalStructureElementBoundingRectangle]

# will be the provided datatype to point to a specific element in the structure
OpticalDocumentElementsPointer: Type = Tuple[int, ...]
