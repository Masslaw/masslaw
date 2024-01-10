from concurrent.futures import ThreadPoolExecutor
from typing import Dict
from typing import List

import spacy
from spacy.tokens.doc import Doc

from logic_layer.knowledge_record import KnowledgeRecord
from logic_layer.text_processing.knowledge_extraction._knowledge_extractor import KnowledgeExtractor
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._models import load_spacy_model_for_language
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing import SpacyDocumentProcessor
from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure.structure_scanning import OpticalDocumentStructureScanner
from shared_layer.mlcp_logger import common_formats
from shared_layer.mlcp_logger import logger


PROCESSED_HIERARCHY_LEVEL_IN_DOCUMENT_STRUCTURE = OpticalStructureHierarchyLevel.GROUP


class SpacyWrapper(KnowledgeExtractor):

    def __init__(self, languages: List[str]):
        super().__init__(languages)
        logger.info(f'Initialized knowledge extractor is a {common_formats.value("SpacyWrapper")}')
        self._spacy_models: Dict[str, spacy.language.Language] = {}
        self._load_models()

    @logger.process_function("Loading spacy models")
    def _load_models(self):
        for language in self._languages:
            logger.info(f'Loading model for language {common_formats.value(language)}.')
            spacy_model = load_spacy_model_for_language(language)
            if spacy_model is None:
                logger.warn(f'No model found for language {common_formats.value(language)}.')
                continue
            self._prepare_model(spacy_model)
            self._spacy_models[language] = spacy_model

    @logger.process_function("Preparing spacy model")
    def _prepare_model(self, spacy_model):
        spacy_model.add_pipe('coreferee')

    @logger.process_function("Spacy Wrapper - Processing text")
    def _process_texts(self, texts: List[str]):
        for language in self._spacy_models.keys():
            extracted_knowledge_records = self._process_texts_in_language(texts, language)
            for extracted_knowledge_record in extracted_knowledge_records:
                self._merge_data_from_record(extracted_knowledge_record)

    @logger.process_function("Spacy Wrapper - Processing an optical text document")
    def _process_optical_text_document(self, document: ExtractedOpticalTextDocument):
        document_structure_scanner = OpticalDocumentStructureScanner(document)
        structure_children_to_process = document_structure_scanner.collect_all_nested_children_of_type(PROCESSED_HIERARCHY_LEVEL_IN_DOCUMENT_STRUCTURE)
        texts_to_process = [structure_child_to_process.get_value() for structure_child_to_process in structure_children_to_process]
        self._process_texts(texts_to_process)

    @logger.process_function("Spacy Wrapper - Processing text in a single language")
    def _process_texts_in_language(self, texts: List[str], language: str) -> List[KnowledgeRecord] | None:
        logger.info(f"Processing text in language {common_formats.value(language)}")
        spacy_documents = self._load_spacy_documents_in_language(texts, language)
        if not spacy_documents: return
        logger.info(f'Processing text for language {common_formats.value(language)}.')
        document_processors = [SpacyDocumentProcessor(spacy_document) for spacy_document in spacy_documents]
        knowledge_records = [document_processor.process_document() for document_processor in document_processors]
        knowledge_records = [knowledge_record for knowledge_record in knowledge_records if knowledge_record is not None]
        return knowledge_records

    @logger.process_function("Loading spacy documents")
    def _load_spacy_documents_in_language(self, texts: List[str], language: str) -> List[Doc] | None:
        logger.info(f"Loading a spacy documents for tests in language {common_formats.value(language)}.")
        spacy_model = self._spacy_models.get(language)
        if not spacy_model:
            logger.warn(f'Trying to process text in a language that failed loading: {common_formats.value(language)}.')
            return
        spacy_documents = spacy_model.pipe(texts)
        return [doc for doc in spacy_documents]
