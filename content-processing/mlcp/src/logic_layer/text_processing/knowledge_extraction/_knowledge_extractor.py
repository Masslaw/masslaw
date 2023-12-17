from abc import abstractmethod
from typing import List

from logic_layer.knowledge_record import KnowledgeRecord
from logic_layer.knowledge_record.data_merging import RecordMerger
from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from shared_layer.file_system_utils import file_system_utils
from shared_layer.mlcp_logger import logger
from shared_layer.mlcp_logger import common_formats


class KnowledgeExtractor:

    def __init__(self, languages: List[str]):
        self._languages = languages
        logger.info(f"Knowledge extractor initialized with languages: {self._languages}")
        self._knowledge_record = KnowledgeRecord()
        self.__knowledge_record_merger = RecordMerger(self._knowledge_record)

    def get_record(self) -> KnowledgeRecord:
        return self._knowledge_record

    @logger.process_function("Knowledge Extractor - Merging data from record")
    def _merge_data_from_record(self, another_record: KnowledgeRecord):
        self.__knowledge_record_merger.merge_entities_from_another_record(another_record)
        self.__knowledge_record_merger.merge_connections_in_record(bidirectional=True, ignore_properties=True)

    @logger.process_function("Knowledge Extractor - Processing text")
    def load_text(self, text: str):
        self._process_text(text)

    @logger.process_function("Knowledge Extractor - Processing optical text document")
    def load_optical_text_document(self, document: ExtractedOpticalTextDocument):
        self._process_optical_text_document(document)

    @logger.process_function("Knowledge Extractor - Loading file")
    def load_file(self, file_path: str):
        file_type = file_system_utils.get_file_type(file_path).replace(".", "")
        logger.debug(f"Loading file {common_formats.value(file_path)} of type {common_formats.value(file_type)}")
        if file_type in ('txt', 'text'):
            with open(file_path, 'r') as f:
                self._process_text(f.read())
                return
        if file_type in ('xml',):
            # to be implemented when the document structure loading functionality is implemented
            # self._process_optical_text_document(...)
            raise NotImplementedError
        raise ValueError(f"Unsupported file type: {file_type}")

    @abstractmethod
    def _process_text(self, text: str):
        pass

    @abstractmethod
    def _process_optical_text_document(self, document: ExtractedOpticalTextDocument):
        pass
