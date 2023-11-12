from logic_layer.text_extraction.file_specific_extractors.pdf._pdf_optical_text_document_extraction_logic import \
    pdf_document_to_optical_text_document
from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyFormation, \
    ExtractedOpticalTextDocument


class PdfTextExtractor:

    def __init__(self, pdf_file_path: str):
        self._file_path = pdf_file_path

    def extract_optical_text_document(self, hierarchy_formation: OpticalStructureHierarchyFormation) -> ExtractedOpticalTextDocument:
        return pdf_document_to_optical_text_document(self._file_path, hierarchy_formation)