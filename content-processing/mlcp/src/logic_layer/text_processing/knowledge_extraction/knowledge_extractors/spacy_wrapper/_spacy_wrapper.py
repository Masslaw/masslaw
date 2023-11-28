from typing import List

from spacy.tokens.doc import Doc

from logic_layer.text_processing.knowledge_extraction._knowledge_extractor import KnowledgeExtractor
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._models import load_spacy_model_for_language
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing import SpacyDocumentProcessor
from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from shared_layer.mlcp_logger import common_formats
from shared_layer.mlcp_logger import logger


class SpacyWrapper(KnowledgeExtractor):

    def __init__(self, languages: List[str]):
        super().__init__(languages)
        logger.info(f'Initialized knowledge extractor is a {common_formats.value("SpacyWrapper")}')
        self._spacy_models = {}
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
    def _process_text(self, text: str):
        for language in self._spacy_models.keys():
            self._process_text_in_language(text, language)

    @logger.process_function("Spacy Wrapper - Processing text in a single language")
    def _process_text_in_language(self, text: str, language: str):
        logger.info(f"Processing text in language {common_formats.value(language)}")
        spacy_document = self._load_spacy_document_in_language(text, language)
        if not spacy_document: return
        logger.info(f'Processing text for language {common_formats.value(language)}.')
        document_processor = SpacyDocumentProcessor(spacy_document)
        knowledge_record = document_processor.process_document()
        self._merge_data_from_record(knowledge_record)

    @logger.process_function("Loading spacy document")
    def _load_spacy_document_in_language(self, text: str, language: str) -> Doc|None:
        logger.info(f"Loading a spacy document in language {common_formats.value(language)}.")
        spacy_model = self._spacy_models.get(language)
        if not spacy_model:
            logger.warn(f'Trying to process text in a language that failed loading: {common_formats.value(language)}.')
            return
        spacy_document = spacy_model(text)
        return spacy_document

    @logger.process_function("Spacy Wrapper - Processing an optical text document")
    def _process_optical_text_document(self, document: ExtractedOpticalTextDocument):
        document_structure = document.get_structure_root()
        document_text = ''.join([child.get_value() for child in document_structure.get_children()])
        self._process_text(document_text)
