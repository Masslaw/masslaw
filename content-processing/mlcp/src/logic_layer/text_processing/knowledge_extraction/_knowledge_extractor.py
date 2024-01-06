from abc import abstractmethod
from typing import List

from logic_layer.knowledge_record import KnowledgeRecord
from logic_layer.knowledge_record.record_merging import RecordMerger
from logic_layer.knowledge_record.record_merging import RecordMergingConfiguration
from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure.document_loading import DocumentLoader
from shared_layer.file_system_utils import file_system_utils
from shared_layer.mlcp_logger import common_formats
from shared_layer.mlcp_logger import logger


class KnowledgeExtractor:

    def __init__(self, languages: List[str]):
        self._languages = languages
        logger.info(f"Knowledge extractor initialized with languages: {self._languages}")
        self._knowledge_record = KnowledgeRecord()
        self._knowledge_record_merger = RecordMerger(self._knowledge_record, RecordMergingConfiguration())

    def get_record(self) -> KnowledgeRecord:
        return self._knowledge_record

    def set_knowledge_merging_configuration(self, merge_configuration: RecordMergingConfiguration):
        self._knowledge_record_merger.set_merge_configuration(merge_configuration)

    @logger.process_function("Knowledge Extractor - Merging data from record")
    def _merge_data_from_record(self, another_record: KnowledgeRecord):
        self._knowledge_record_merger.merge_record(another_record)

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
            document_loader = DocumentLoader()
            with open(file_path, 'r') as f:
                extracted_optical_text_document = document_loader.load_xml(f)
                self._process_optical_text_document(extracted_optical_text_document)
                return
        if file_type in ('json',):
            document_loader = DocumentLoader()
            with open(file_path, 'r') as f:
                extracted_optical_text_document = document_loader.load_json(f)
                self._process_optical_text_document(extracted_optical_text_document)
                return
        raise ValueError(f"Unsupported file type: {file_type}")

    @abstractmethod
    def _process_text(self, text: str):
        pass

    @abstractmethod
    def _process_optical_text_document(self, document: ExtractedOpticalTextDocument):
        pass
