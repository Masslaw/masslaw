from typing import IO
from xml.etree import ElementTree

from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure._structure_calculations import \
    StructureGeometryCalculator
from logic_layer.text_structures.extracted_optical_text_structure._structure_element import OpticalTextStructureElement
from logic_layer.text_structures.extracted_optical_text_structure._structure_root import OpticalTextStructureRoot
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._assertions import \
    assert_export_output_file


def export_document_to_html_format(optical_text_document: ExtractedOpticalTextDocument, output_file: IO):
    assert_export_output_file(file=output_file, expected_type='html')
    document_element = _document_to_html_element(optical_text_document=optical_text_document)
    ElementTree.ElementTree(document_element).write(output_file, encoding='utf-8', xml_declaration=False)


def _document_to_html_element(optical_text_document: ExtractedOpticalTextDocument) -> ElementTree.Element:
    document_html_element = ElementTree.Element('div')
    document_html_element.set('class', 'ml-document')

    structure_html_element = _structure_root_to_html_element(optical_text_document.get_structure_root())
    document_html_element.append(structure_html_element)

    return document_html_element


def _structure_root_to_html_element(structure_root: OpticalTextStructureRoot) -> ElementTree.Element:
    html_element = ElementTree.Element('div')
    html_element.set('class', 'ml-document-structure')

    for child in structure_root.get_children():
        html_element.append(_structure_element_to_html_element(child))

    return html_element


def _structure_element_to_html_element(structure_element: OpticalTextStructureElement) -> ElementTree.Element:
    html_element = ElementTree.Element('p')
    structure_element_label = structure_element.__class__.get_label()
    html_element.set('class', f'{structure_element_label}')

    child_type = structure_element.get_children_type() or str
    geometry_calculator = StructureGeometryCalculator(structure_element)
    bounding_rect = geometry_calculator.calculate_bounding_rect()
    bounding_rect = [int(v) for v in bounding_rect]
    element_style = f'position: absolute; left: {bounding_rect[0]}; top: {bounding_rect[1]}; width: {bounding_rect[2] - bounding_rect[0]}; height: {bounding_rect[3] - bounding_rect[1]};'
    html_element.set('style', element_style)
    if child_type == str:
        html_element.text = structure_element.get_value()
    else:
        element_children = structure_element.get_children()
        for child in element_children:
            child_html_element = _structure_element_to_html_element(child)
            html_element.append(child_html_element)

    return html_element
