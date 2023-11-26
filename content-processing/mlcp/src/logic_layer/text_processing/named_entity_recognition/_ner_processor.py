from abc import abstractmethod
from typing import List

from mlcp.src.logic_layer.knowledge_record import KnowledgeRecord
from mlcp.src.logic_layer.knowledge_record.data_merging import RecordMerger
from mlcp.src.logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument


class NERProcessor:

    def __init__(self, languages: List[str]):
        self._languages = languages
        self._knowledge_record = KnowledgeRecord()
        self.__knowledge_record_merger = RecordMerger(self._knowledge_record)

    def get_record(self) -> KnowledgeRecord:
        return self._knowledge_record

    def _merge_data_from_record(self, another_record: KnowledgeRecord):
        self.__knowledge_record_merger.merge_data_from_another_record(another_record)

    def load_text(self, text: str):
        self._process_text(text)

    def load_optical_text_document(self, document: ExtractedOpticalTextDocument):
        self._process_optical_text_document(document)

    @abstractmethod
    def _process_text(self, text: str):
        pass

    @abstractmethod
    def _process_optical_text_document(self, document: ExtractedOpticalTextDocument):
        pass
