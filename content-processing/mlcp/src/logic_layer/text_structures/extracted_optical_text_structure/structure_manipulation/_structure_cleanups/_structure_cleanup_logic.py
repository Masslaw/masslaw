from logic_layer.text_structures.extracted_optical_text_structure._structure_element import OpticalTextStructureElement
from logic_layer.text_structures.extracted_optical_text_structure._structure_root import OpticalTextStructureRoot


def cleanup_structure(structure: OpticalTextStructureRoot) -> OpticalTextStructureRoot:
    clean_groups = [cleanup_element(group) for group in structure.get_children()]
    structure.set_children(clean_groups)
    return structure


def cleanup_element(element: OpticalTextStructureElement) -> OpticalTextStructureElement:
    if element.is_leaf():
        return element
    clean_children = [cleanup_element(child) for child in element.get_children() if child is not None]
    real_children = [child for child in clean_children if not child.is_empty()]
    element.set_children(real_children)
    return element
