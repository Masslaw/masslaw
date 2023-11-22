from abc import abstractmethod
from typing import Dict
from typing import List
from typing import Tuple

from mlcp.src.logic_layer.knowledge_record import KnowledgeRecord
from mlcp.src.logic_layer.knowledge_record.data_merging import RecordMerger
from mlcp.src.logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from mlcp.src.logic_layer.text_structures.extracted_optical_text_structure._structure_root import OpticalTextStructureRoot


class NERProcessor:

    def __init__(self, languages: List[str]):
        self._languages = languages
        self._knowledge_record = KnowledgeRecord()
        self.__knowledge_record_merger = RecordMerger(self._knowledge_record)

    def load_text(self, text: str):
        extracted_record = self._process_text(text)
        self.__knowledge_record_merger.merge_data_from_another_record(extracted_record)

    def load_optical_text_document(self, document: ExtractedOpticalTextDocument):
        extracted_record = self._process_optical_text_document(document)
        self.__knowledge_record_merger.merge_data_from_another_record(extracted_record)

    @abstractmethod
    def _process_text(self, text: str) -> KnowledgeRecord:
        pass

    @abstractmethod
    def _process_optical_text_document(self, document: ExtractedOpticalTextDocument) -> KnowledgeRecord:
        pass


