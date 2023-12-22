import json
from typing import IO

from logic_layer.text_structures.extracted_optical_text_structure._document import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure._structure_element import OpticalTextStructureElement
from logic_layer.text_structures.extracted_optical_text_structure._structure_root import OpticalTextStructureRoot
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._assertions import assert_export_output_file


def export_document_to_json_format(optical_text_document: ExtractedOpticalTextDocument, output_file: IO):
    assert_export_output_file(file=output_file, expected_type='json')
    document_data = _document_to_dict(optical_text_document=optical_text_document)
    json.dump(document_data, output_file, ensure_ascii=False)


def _document_to_dict(optical_text_document: ExtractedOpticalTextDocument) -> dict:
    document_data = {}

    structure_data = _structure_root_to_dict(optical_text_document.get_structure_root())
    document_data['textStructure'] = structure_data

    document_metadata = optical_text_document.get_metadata()
    document_data['metadata'] = document_metadata

    return document_data


def _structure_root_to_dict(structure_root: OpticalTextStructureRoot):
    structure_data = {}

    structure_data['children'] = []
    for child in structure_root.get_children():
        structure_data['children'].append(_structure_element_data_to_dict(child))
    structure_data['type'] = 'optical'

    return structure_data


def _structure_element_data_to_dict(structure_element: OpticalTextStructureElement) -> dict:
    element_data = {}

    child_type = structure_element.get_children_type() or str
    element_properties = structure_element.get_properties() or {}
    if child_type == str:
        element_data['v'] = structure_element.get_value()
        bounding_rectangle = structure_element.get_bounding_rect()
        element_data['x1'] = bounding_rectangle[0]
        element_data['y1'] = bounding_rectangle[1]
        element_data['x2'] = bounding_rectangle[2]
        element_data['y2'] = bounding_rectangle[3]
    else:
        children_data = []
        for child in structure_element.get_children():
            child_data = _structure_element_data_to_dict(child)
            children_data.append(child_data)
        element_data[OpticalTextStructureElement(child_type).get_label()] = children_data
    element_data['p'] = element_properties

    return element_data
