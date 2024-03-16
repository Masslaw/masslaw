import json
from typing import IO
from typing import Type

from service.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from service.extracted_optical_text_structure._document import ExtractedOpticalTextDocument
from service.extracted_optical_text_structure._hierarchy_levels import hierarchy_level_to_element_class
from service.extracted_optical_text_structure._structure_element import OpticalTextStructureElement
from service.extracted_optical_text_structure._structure_root import OpticalTextStructureRoot
from service.extracted_optical_text_structure.document_loading._assertions import assert_load_input_file


def load_document_from_json_format(input_file: IO) -> ExtractedOpticalTextDocument:
    assert_load_input_file(file=input_file, expected_type='json')
    document_data = json.load(input_file)
    return _dict_to_document(document_data)


def _dict_to_document(document_data: dict) -> ExtractedOpticalTextDocument:
    structure_data = document_data.get('textStructure', {})
    structure_root = _dict_to_structure_root(structure_data)
    document_metadata = document_data.get('metadata', {})
    optical_text_document = ExtractedOpticalTextDocument()
    optical_text_document.set_structure_root(structure_root)
    optical_text_document.set_metadata(document_metadata)
    return optical_text_document


def _dict_to_structure_root(structure_data: dict) -> OpticalTextStructureRoot:
    structure_root = OpticalTextStructureRoot()
    child_elements = []
    child_elements_type = _determine_child_type(structure_data)
    if not child_elements_type: return structure_root
    for child_data in structure_data.get(child_elements_type.get_label(), []):
        structure_element = _dict_to_structure_element(child_data, child_elements_type)
        child_elements.append(structure_element)
    structure_root.set_children(child_elements)
    return structure_root


def _dict_to_structure_element(element_data: dict, element_type: Type[OpticalTextStructureElement]) -> OpticalTextStructureElement:
    child_type = _determine_child_type(element_data) or str
    if child_type is str:
        structure_element = element_type()
        structure_element.set_children(list(element_data.get('v', '')))
        bounding_rectangle = (element_data.get('x1', 0), element_data.get('y1', 0), element_data.get('x2', 0), element_data.get('y2', 0))
        structure_element.set_bounding_rect(bounding_rectangle)
    else:
        structure_element = element_type()
        children = []
        for child_data in element_data[child_type.get_label()]:
            child = _dict_to_structure_element(child_data, child_type)
            children.append(child)
        structure_element.set_children(children)
    element_properties = element_data.get('p', {})
    structure_element.set_properties(element_properties)
    return structure_element


def _determine_child_type(element_data: dict) -> Type[OpticalTextStructureElement] | Type[str]:
    if 'v' in element_data: return str
    for hierarchy_level in OpticalStructureHierarchyLevel:
        hierarchy_level_class = hierarchy_level_to_element_class(hierarchy_level)
        hierarchy_level_label = hierarchy_level_class.get_label()
        if hierarchy_level_label in element_data: return hierarchy_level_class
