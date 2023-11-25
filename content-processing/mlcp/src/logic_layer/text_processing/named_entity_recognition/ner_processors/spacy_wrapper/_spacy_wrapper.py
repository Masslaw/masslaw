from typing import List

from logic_layer.text_processing.named_entity_recognition._ner_processor import NERProcessor
from logic_layer.text_processing.named_entity_recognition.ner_processors.spacy_wrapper._models import load_spacy_model_for_language
from logic_layer.text_processing.named_entity_recognition.ner_processors.spacy_wrapper._spacy_document_processing import SpacyDocumentProcessor
from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from shared_layer.mlcp_logger import common_formats
from shared_layer.mlcp_logger import logger


class SpacyWrapper(NERProcessor):

    def __init__(self, languages: List[str]):
        super().__init__(languages)
        self._spacy_models = {}

    def _load_languages(self):
        self._load_models()

    def _load_models(self):
        for language in self._languages:
            logger.info(f'Loading model for language {common_formats.value(language)}.')
            spacy_model = load_spacy_model_for_language(language)
            if spacy_model is None:
                logger.warning(f'No model found for language {common_formats.value(language)}.')
                continue
            self._prepare_model(spacy_model)
            self._spacy_models[language] = spacy_model

    def _prepare_model(self, spacy_model):
        spacy_model.add_pipe('coreferee')

    def _process_text(self, text: str):
        for language in self._spacy_models.keys():
            self._process_text_in_language(text, language)

    def _process_text_in_language(self, text: str, language: str):
        spacy_model = self._spacy_models.get(language)
        if not spacy_model:
            logger.warning(f'Trying to process text in a language that failed loading: {common_formats.value(language)}.')
            return
        logger.info(f'Processing text for language {common_formats.value(language)}.')
        spacy_document = spacy_model(text)
        document_processor = SpacyDocumentProcessor(spacy_document)
        knowledge_record = document_processor.process_document()
        self._merge_data_from_record(knowledge_record)

    def _process_optical_text_document(self, document: ExtractedOpticalTextDocument):
        document_structure = document.get_structure_root()
        document_text = ''.join([child.get_value() for child in document_structure.get_children()])
        self._process_text(document_text)
