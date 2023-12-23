from typing import List
from typing import Type

from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel

# the last element in the hierarchy will always be a string value (it won't be specified in the hierarchy formation)
OpticalStructureHierarchyFormation: Type = List[OpticalStructureHierarchyLevel]
