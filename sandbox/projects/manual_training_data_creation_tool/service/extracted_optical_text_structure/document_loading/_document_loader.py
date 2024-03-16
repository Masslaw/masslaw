from typing import IO

from service.extracted_optical_text_structure.document_loading._json_loading import load_document_from_json_format
from service.extracted_optical_text_structure.document_loading._xml_loading import load_document_from_xml_format


class DocumentLoader:

    def load_json(self, opened_json_file: IO):
        return load_document_from_json_format(opened_json_file)

    def load_xml(self, opened_xml_file: IO):
        return load_document_from_xml_format(opened_xml_file)

