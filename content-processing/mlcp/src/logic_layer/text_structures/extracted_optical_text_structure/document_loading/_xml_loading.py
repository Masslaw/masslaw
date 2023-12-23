import xml.etree.ElementTree as ET
from typing import IO
from typing import Type

from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureElementBoundingRectangle
from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import hierarchy_level_to_element_class
from logic_layer.text_structures.extracted_optical_text_structure._structure_element import OpticalTextStructureElement
from logic_layer.text_structures.extracted_optical_text_structure._structure_root import OpticalTextStructureRoot
from logic_layer.text_structures.extracted_optical_text_structure.document_loading._assertions import assert_load_input_file
from shared_layer.list_utils import list_utils


def load_document_from_xml_format(input_file: IO) -> ExtractedOpticalTextDocument:
    assert_load_input_file(file=input_file, expected_type='xml')
    tree = ET.parse(input_file)
    root = tree.getroot()
    return _xml_element_to_document(root)


def _xml_element_to_document(xml_element: ET.Element) -> ExtractedOpticalTextDocument:
    optical_text_document = ExtractedOpticalTextDocument()
    for child in xml_element:
        if child.tag == 'textStructure':
            structure_root = _xml_element_to_structure_root(child)
            optical_text_document.set_structure_root(structure_root)
        elif child.tag == 'metadata':
            metadata = _xml_element_to_metadata(child)
            optical_text_document.set_metadata(metadata)
    return optical_text_document


def _xml_element_to_structure_root(xml_element: ET.Element) -> OpticalTextStructureRoot:
    structure_root = OpticalTextStructureRoot()
    child_elements = []
    for child in xml_element:
        structure_element = _xml_element_to_structure_element(child)
        child_elements.append(structure_element)
    structure_root.set_children(child_elements)
    return structure_root


def _xml_element_to_structure_element(xml_element: ET.Element) -> OpticalTextStructureElement:
    element_type = _determine_element_type_from_xml_element(xml_element)
    structure_element = element_type()
    if 'v' in xml_element.attrib:
        structure_element.set_children(list(xml_element.get('v', '')))
        bounding_rect = _extract_bounding_rect_from_attribute(xml_element.get('r', '0-0-0-0'))
        structure_element.set_bounding_rect(bounding_rect)
    else:
        children = [_xml_element_to_structure_element(child) for child in xml_element]
        structure_element.set_children(children)
    properties = {k[2:]: v for k, v in xml_element.attrib.items() if k.startswith('p-')}
    structure_element.set_properties(properties)
    return structure_element


def _determine_element_type_from_xml_element(xml_element: ET.Element) -> Type[OpticalTextStructureElement]:
    for hierarchy_level in OpticalStructureHierarchyLevel:
        hierarchy_level_class = hierarchy_level_to_element_class(hierarchy_level)
        hierarchy_level_label = hierarchy_level_class.get_label()
        if hierarchy_level_label == xml_element.tag: return hierarchy_level_class


def _extract_bounding_rect_from_attribute(attribute: str) -> OpticalStructureElementBoundingRectangle:
    split_rect_attr = attribute.split('-')
    return (
        int(list_utils.get_element_at(split_rect_attr, 0, default=0)),
        int(list_utils.get_element_at(split_rect_attr, 1, default=0)),
        int(list_utils.get_element_at(split_rect_attr, 2, default=0)),
        int(list_utils.get_element_at(split_rect_attr, 3, default=0)),
    )


def _xml_element_to_metadata(metadata_xml_element: ET.Element) -> dict:
    def xml_element_to_metadata_item(xml_element: ET.Element) -> dict:
        metadata_item = {}
        label = xml_element.tag
        metadata_item.update(xml_element.attrib)
        metadata_item['__label'] = label
        for child in xml_element:
            metadata_child_item = xml_element_to_metadata_item(child)
            metadata_item[child.tag] = metadata_child_item
        return metadata_item
    metadata = {}
    for child in metadata_xml_element:
        metadata[child.tag] = xml_element_to_metadata_item(child)
    return metadata
