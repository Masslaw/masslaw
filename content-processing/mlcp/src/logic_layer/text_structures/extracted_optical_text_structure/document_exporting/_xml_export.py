from typing import IO
from xml.etree import ElementTree

from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import hierarchy_level_to_element_class
from logic_layer.text_structures.extracted_optical_text_structure._structure_element import OpticalTextStructureElement
from logic_layer.text_structures.extracted_optical_text_structure._structure_root import OpticalTextStructureRoot
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._assertions import assert_export_output_file
from logic_layer.text_structures.extracted_optical_text_structure.structure_calculations import StructureGeometryCalculator


def export_document_to_xml_format(optical_text_document: ExtractedOpticalTextDocument, output_file: IO):
    assert_export_output_file(file=output_file, expected_type='xml')
    document_element = _document_to_xml_element(optical_text_document=optical_text_document)
    element_tree = ElementTree.ElementTree(document_element)
    element_tree.write(output_file, encoding='utf-8', xml_declaration=True)


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
    for child in structure_root.get_children(): xml_element.append(_structure_element_to_xml_element(child))
    return xml_element


def _structure_element_to_xml_element(structure_element: OpticalTextStructureElement) -> ElementTree.Element:
    xml_element = ElementTree.Element(structure_element.__class__.get_label())
    _handle_element_bounding_rect(structure_element, xml_element)
    _load_structure_element_children_to_xml_element(structure_element, xml_element)
    _load_element_properties_to_xml_element(structure_element, xml_element)
    return xml_element


def _handle_element_bounding_rect(structure_element: OpticalTextStructureElement, xml_element: ElementTree.Element):
    if not structure_element.is_leaf(): return
    _load_element_rectangle_to_xml_element(structure_element, xml_element)


def _load_element_rectangle_to_xml_element(structure_element: OpticalTextStructureElement, xml_element: ElementTree.Element):
    geometry_calculator = StructureGeometryCalculator(structure_element)
    bounding_rectangle = geometry_calculator.calculate_bounding_rect()
    bounding_rectangle_expression = "-".join([str(int(x)) for x in bounding_rectangle])
    xml_element.set('r', bounding_rectangle_expression)


def _load_structure_element_children_to_xml_element(structure_element: OpticalTextStructureElement, xml_element: ElementTree.Element):
    if structure_element.is_leaf():
        element_text = structure_element.get_value()
        element_text = _filter_valid_xml_characters(element_text)
        xml_element.text = element_text
        return
    element_children = structure_element.get_children()
    for child in element_children:
        child_xml_element = _structure_element_to_xml_element(child)
        xml_element.append(child_xml_element)


def _load_element_properties_to_xml_element(structure_element: OpticalTextStructureElement, xml_element: ElementTree.Element):
    element_properties = structure_element.get_properties() or {}
    for key, value in element_properties.items():
        key = key.replace(' ', '-')
        xml_element.set(f'p-{key}', str(value))
    return xml_element


def _filter_valid_xml_characters(text: str) -> str:
    return ''.join(c for c in text if (
        ord(c) == 0x9 or
        ord(c) == 0xA or
        ord(c) == 0xD or
        0x20 <= ord(c) <= 0xD7FF or
        0xE000 <= ord(c) <= 0xFFFD or
        0x10000 <= ord(c) <= 0x10FFFF
    ))
