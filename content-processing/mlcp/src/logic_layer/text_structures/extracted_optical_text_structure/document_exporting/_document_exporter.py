from typing import IO, List

from logic_layer.text_structures.extracted_optical_text_structure._document import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._html_export import export_document_to_html_format
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._json_export import export_document_to_json_format
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._txt_export import export_document_to_txt_format
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._xml_export import export_document_to_xml_format
from shared_layer.memory_utils.storage_cached_image import StorageCachedImage


class DocumentExporter:

    def __init__(self, document: ExtractedOpticalTextDocument):
        self._document = document

    def export_json(self, opened_json_file: IO):
        export_document_to_json_format(optical_text_document=self._document, output_file=opened_json_file)

    def export_xml(self, opened_xml_file: IO):
        export_document_to_xml_format(optical_text_document=self._document, output_file=opened_xml_file)

    def export_text(self, opened_txt_file: IO):
        export_document_to_txt_format(optical_text_document=self._document, output_file=opened_txt_file)

    def export_html(self, opened_html_file: IO, structure_children_background_images: List[StorageCachedImage] = None):
        export_document_to_html_format(optical_text_document=self._document, output_file=opened_html_file, structure_children_background_images=structure_children_background_images)
