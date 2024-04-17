from logic_layer.text_structures.extracted_optical_text_structure.structure_construction import OpticalStructureHierarchyFormation
from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel

extracted_optical_text_structure_hierarchy_formation: OpticalStructureHierarchyFormation = [
    OpticalStructureHierarchyLevel.GROUP,
    OpticalStructureHierarchyLevel.BLOCK,
    OpticalStructureHierarchyLevel.PARAGRAPH,
    OpticalStructureHierarchyLevel.LINE,
    OpticalStructureHierarchyLevel.WORD,
]
