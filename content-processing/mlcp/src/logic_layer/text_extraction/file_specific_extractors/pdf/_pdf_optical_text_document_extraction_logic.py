from typing import List

import pdfplumber

from logic_layer.bidi import correct_ltr_sequenced_text
from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure import OpticalElementRawDataEntry
from logic_layer.text_structures.extracted_optical_text_structure.structure_construction._structure_hierarchy_formation import OpticalStructureHierarchyFormation
from logic_layer.text_structures.extracted_optical_text_structure.structure_construction import OpticalTextStructureConstructor
from logic_layer.text_structures.extracted_optical_text_structure.structure_manipulation import OpticalTextStructureManipulator
from shared_layer.mlcp_logger import logger


@logger.process_function("Extracting an optical text document from a PDF file")
def pdf_document_to_optical_text_document(file_path: str, hierarchy_formation: OpticalStructureHierarchyFormation) -> ExtractedOpticalTextDocument:
    pdf_text_elements_entries = extract_element_entries(file_path)
    document = ExtractedOpticalTextDocument()
    constructor = OpticalTextStructureConstructor(document, hierarchy_formation)
    constructor.add_entry_groups_to_structure(pdf_text_elements_entries)
    polish_document(document)
    return document


@logger.process_function("Extracting element entries")
def extract_element_entries(file_path: str) -> List[List[OpticalElementRawDataEntry]]:
    with pdfplumber.open(file_path) as pdf:
        return [get_text_elements_from_page(page) for page in pdf.pages]


def get_text_elements_from_page(page) -> List[OpticalElementRawDataEntry]:
    text_elements = []
    for text_element in page.extract_text_lines():
        text = text_element['text']
        text = correct_ltr_sequenced_text(text)
        bounding_rect = (text_element['x0'] / page.width, text_element['top'] / page.height, text_element['x1'] / page.width, text_element['bottom'] / page.height)
        text_elements.append((text, bounding_rect))
    return text_elements


@logger.process_function("Polishing PDF extracted optical document")
def polish_document(document: ExtractedOpticalTextDocument):
    manipulator = OpticalTextStructureManipulator(document)
    manipulator.merge_mergeable_structure_children_sequentially()
    manipulator.clean_document_structure()
