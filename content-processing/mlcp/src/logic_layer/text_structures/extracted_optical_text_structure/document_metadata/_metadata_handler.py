from typing import List

from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from shared_layer.dictionary_utils import dictionary_utils


class DocumentMetadataHandler:
    def __init__(self, document: ExtractedOpticalTextDocument):
        self._document = document

    def put_metadata_item(self, metadata_path: List[str], metadata_item_label: str, metadata_item_data: dict):
        metadata = self._document.get_metadata()
        metadata_item_data['__label'] = metadata_item_label
        dictionary_utils.set_at(metadata, metadata_path, metadata_item_data)
        self._document.set_metadata(metadata)
