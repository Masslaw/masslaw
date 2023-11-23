from typing import List

from logic_layer.knowledge_record import KnowledgeRecord
from logic_layer.knowledge_record.data_merging import RecordMerger
from logic_layer.text_processing.named_entity_recognition._ner_processor import NERProcessor
from logic_layer.text_processing.named_entity_recognition.ner_processors.spacy_wrapper._spacy_model_wrapper import SpacyKnowledgeExtractor
from logic_layer.text_processing.named_entity_recognition.ner_processors.spacy_wrapper._models import load_spacy_model_for_language
from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from shared_layer.mlcp_logger import logger
from shared_layer.mlcp_logger import common_formats


class SpacyWrapper(NERProcessor):

    def __init__(self, languages: List[str]):
        super().__init__(languages)
        self._knowledge_extractors = {}

    def _load_languages(self):
        for language in self._languages:
            logger.info(f'Loading model for language {common_formats.value(language)}.')
            spacy_model = load_spacy_model_for_language(language)
            if spacy_model is None:
                logger.warning(f'No model found for language {common_formats.value(language)}.')
                continue
            knowledge_extractor = SpacyKnowledgeExtractor(spacy_model)
            self._knowledge_extractors[language] = knowledge_extractor

    def _process_text(self, text: str):
        for language in self._knowledge_extractors.keys():
            self._process_text_in_language(text, language)

    def _process_text_in_language(self, text: str, language: str):
        extractor = self._knowledge_extractors.get(language)
        if not extractor:
            logger.warning(f'Trying to process text in a language that failed loading: {common_formats.value(language)}.')
            return
        logger.info(f'Processing text for language {common_formats.value(language)}.')
        extractor.load_text(text)
        extracted_record = extractor.get_record()
        self._merge_data_from_record(extracted_record)

    def _process_optical_text_document(self, document: ExtractedOpticalTextDocument):
        document_structure = document.get_structure_root()
        document_text = ''.join([child.get_value() for child in document_structure.get_children()])
        self._process_text(document_text)