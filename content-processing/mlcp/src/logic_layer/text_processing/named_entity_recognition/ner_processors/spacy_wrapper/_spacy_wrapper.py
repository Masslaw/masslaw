from typing import List

from logic_layer.text_processing.named_entity_recognition._ner_processor import NERProcessor
from logic_layer.text_processing.named_entity_recognition.ner_processors.spacy_wrapper._spacy_model_wrapper import SpacyModelWrapper
from logic_layer.text_processing.named_entity_recognition.ner_processors.spacy_wrapper._models import load_spacy_model_for_language
from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from shared_layer.mlcp_logger import logger
from shared_layer.mlcp_logger import common_formats


class SpacyWrapper(NERProcessor):

    def __init__(self, languages: List[str]):
        super().__init__(languages)
        self._model_wrappers = {}

    def _load_languages(self):
        for language in self._languages:
            logger.info(f'Loading model for language {common_formats.value(language)}.')
            spacy_model = load_spacy_model_for_language(language)
            if spacy_model is None:
                logger.warning(f'No model found for language {common_formats.value(language)}.')
                continue
            knowledge_extractor = SpacyModelWrapper(spacy_model)
            self._model_wrappers[language] = knowledge_extractor

    def _process_text(self, text: str):
        for language in self._model_wrappers.keys():
            self._process_text_in_language(text, language)

    def _process_text_in_language(self, text: str, language: str):
        model_wrapper = self._model_wrappers.get(language)
        if not model_wrapper:
            logger.warning(f'Trying to process text in a language that failed loading: {common_formats.value(language)}.')
            return
        logger.info(f'Processing text for language {common_formats.value(language)}.')
        extracted_record = model_wrapper.process_text(text)
        self._merge_data_from_record(extracted_record)

    def _process_optical_text_document(self, document: ExtractedOpticalTextDocument):
        document_structure = document.get_structure_root()
        document_text = ''.join([child.get_value() for child in document_structure.get_children()])
        self._process_text(document_text)