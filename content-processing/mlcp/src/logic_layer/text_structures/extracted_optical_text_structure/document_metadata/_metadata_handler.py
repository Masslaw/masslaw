from typing import List

from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure.document_metadata._metadata_handling_logic import put_metadata_item


class DocumentMetadataHandler:
    def __init__(self, document: ExtractedOpticalTextDocument):
        self._document = document

    def put_metadata_item(self, metadata_path: List[str], metadata_item_label: str, metadata_item_data: dict):
        if not metadata_path: raise ValueError('metadata_path cannot be empty')
        metadata = self._document.get_metadata()
        new_metadata = put_metadata_item(metadata, metadata_path, metadata_item_label, metadata_item_data)
        self._document.set_metadata(new_metadata)
