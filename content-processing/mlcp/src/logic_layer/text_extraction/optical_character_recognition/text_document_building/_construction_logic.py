from typing import List
from typing import Tuple

from logic_layer.text_extraction.optical_character_recognition import OcrExtractedElement
from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure import OpticalElementRawDataEntry
from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyFormation
from logic_layer.text_structures.extracted_optical_text_structure.structure_construction import OpticalTextStructureConstructor


def construct_optical_text_document_from_ocr_output_element_groups(structure_hierarchy_formation: OpticalStructureHierarchyFormation, extracted_element_groups: List[List[OcrExtractedElement]]) -> ExtractedOpticalTextDocument:
    document = ExtractedOpticalTextDocument(structure_hierarchy_formation)
    element_entry_groups = extracted_element_groups_to_optical_structure_entry_groups(extracted_element_groups)
    document_constructor = OpticalTextStructureConstructor(document)
    document_constructor.add_entry_groups_to_structure(element_entry_groups)
    return document


def extracted_element_groups_to_optical_structure_entry_groups(extracted_element_groups: List[List[OcrExtractedElement]]) -> List[List[OpticalElementRawDataEntry]]:
    element_entry_groups = []
    for extracted_element_group in extracted_element_groups:
        element_entry_group = []
        for extracted_element in extracted_element_group:
            element_entry = ocr_extracted_element_to_optical_structure_entry(extracted_element)
            element_entry_group.append(element_entry)
        element_entry_groups.append(element_entry_group)
    return element_entry_groups


def construct_optical_text_document_from_structured_ocr_output(structure_hierarchy_formation: OpticalStructureHierarchyFormation, extracted_structured_element_groups) -> ExtractedOpticalTextDocument:
    document = ExtractedOpticalTextDocument(structure_hierarchy_formation)
    structured_element_groups = extracted_structured_elements_to_structured_optical_entries(extracted_structured_element_groups)
    document_constructor = OpticalTextStructureConstructor(document)
    document_constructor.add_structured_entry_groups_to_structure(structured_element_groups)
    return document


def extracted_structured_elements_to_structured_optical_entries(extracted_structured_elements: List[List]) -> List[List]:
    structured_entries = []
    for child_part in extracted_structured_elements:
        if isinstance(child_part, List):
            structured_entry = extracted_structured_elements_to_structured_optical_entries(child_part)
            structured_entries.append(structured_entry)
            continue
        if isinstance(child_part, Tuple):
            entry = ocr_extracted_element_to_optical_structure_entry(child_part)
            structured_entries.append(entry)
            continue
    return structured_entries


def ocr_extracted_element_to_optical_structure_entry(extracted_element: OcrExtractedElement) -> OpticalElementRawDataEntry:
    text: str = extracted_element[0]
    bounding_rect: Tuple[float, float, float, float] = extracted_element[1]
    optical_structure_entry: OpticalElementRawDataEntry = (text, bounding_rect)
    return optical_structure_entry
