from typing import IO
from xml.etree import ElementTree

from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure._structure_element import OpticalTextStructureElement
from logic_layer.text_structures.extracted_optical_text_structure._structure_root import OpticalTextStructureRoot
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._assertions import assert_export_output_file


def export_document_to_xml_format(optical_text_document: ExtractedOpticalTextDocument, output_file: IO):
    assert_export_output_file(file=output_file, expected_type='xml')
    document_element = _document_to_xml_element(optical_text_document=optical_text_document)
    ElementTree.ElementTree(document_element).write(output_file, encoding='utf-8', xml_declaration=True)


def _document_to_xml_element(optical_text_document: ExtractedOpticalTextDocument) -> ElementTree.Element:
    document_xml_element = ElementTree.Element('extractedTextDocument')
    document_xml_element.set('type', 'optical')
    structure_xml_element = _structure_root_to_xml_element(optical_text_document.get_structure_root())
    document_xml_element.append(structure_xml_element)
    metadata_xml_element = optical_text_document.get_metadata()
    document_xml_element.append(metadata_xml_element)
    return document_xml_element


def _structure_root_to_xml_element(structure_root: OpticalTextStructureRoot) -> ElementTree.Element:
    xml_element = ElementTree.Element('textStructure')
    xml_element.set('type', 'optical')
    for child in structure_root.get_children():
        xml_element.append(_structure_element_to_xml_element(child))
    return xml_element


def _structure_element_to_xml_element(structure_element: OpticalTextStructureElement) -> ElementTree.Element:
    xml_element = ElementTree.Element(structure_element.__class__.get_label())

    child_type = structure_element.get_children_type() or str
    element_properties = structure_element.get_properties() or {}
    if child_type == str:
        xml_element.set('v', structure_element.get_value())
        bounding_rectangle = structure_element.get_bounding_rect()
        bounding_rectangle_expression = "-".join([str(int(x)) for x in bounding_rectangle])
        xml_element.set('r', bounding_rectangle_expression)
    else:
        element_children = structure_element.get_children()
        for child in element_children:
            child_xml_element = _structure_element_to_xml_element(child)
            xml_element.append(child_xml_element)
    for key, value in element_properties.items():
        key = key.replace(' ', '-')
        xml_element.set(f'p-{key}', str(value))

    return xml_element
