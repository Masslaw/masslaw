import json
from typing import IO

from logic_layer.text_structures.extracted_optical_text_structure._document import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure._structure_element import OpticalTextStructureElement
from logic_layer.text_structures.extracted_optical_text_structure._structure_root import OpticalTextStructureRoot


def load_document_from_json_format(input_file: IO) -> ExtractedOpticalTextDocument:
    document_data = json.load(input_file)
    return _dict_to_document(document_data)


def _dict_to_document(document_data: dict) -> ExtractedOpticalTextDocument:
    structure_data = document_data['textStructure']
    structure_root = _dict_to_structure_root(structure_data)

    document_metadata = document_data['metadata']
    optical_text_document = ExtractedOpticalTextDocument()
    optical_text_document.set_structure_root(structure_root)
    optical_text_document.set_metadata(document_metadata)

    return optical_text_document


def _dict_to_structure_root(structure_data: dict) -> OpticalTextStructureRoot:
    structure_root = OpticalTextStructureRoot()
    for child_data in structure_data['children']:
        structure_element = _dict_to_structure_element(child_data)
        structure_root.add_child(structure_element)
    return structure_root


def _dict_to_structure_element(element_data: dict) -> OpticalTextStructureElement:
    if 'v' in element_data:  # Assuming it's a leaf node
        structure_element = OpticalTextStructureElement(str)
        structure_element.set_value(element_data['v'])
        bounding_rectangle = (element_data['x1'], element_data['y1'], element_data['x2'], element_data['y2'])
        structure_element.set_bounding_rect(bounding_rectangle)
    else:
        # Assuming it's a non-leaf node. Adjust according to actual data structure.
        child_type = ...  # Determine the child type
        structure_element = OpticalTextStructureElement(child_type)
        for child_data in element_data[child_type.get_label()]:
            child = _dict_to_structure_element(child_data)
            structure_element.add_child(child)

    element_properties = element_data.get('p', {})
    structure_element.set_properties(element_properties)

    return structure_element
