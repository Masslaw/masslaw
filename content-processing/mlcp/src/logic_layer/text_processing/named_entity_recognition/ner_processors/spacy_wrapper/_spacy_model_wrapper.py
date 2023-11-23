import spacy
from spacy.tokens.doc import Doc

from logic_layer.knowledge_record import KnowledgeRecord
from logic_layer.text_processing.named_entity_recognition.ner_processors.spacy_wrapper._spacy_document_processor import SpacyDocumentProcessor


class SpacyModelWrapper:

    def __init__(self, spacy_model: spacy.Language):
        self._model = spacy_model
        self._prepare_model()

    def _prepare_model(self):
        self._model.add_pipe('coreferee')

    def process_text(self, text: str) -> KnowledgeRecord:
        spacy_document = self._get_document_for_text(text)
        document_processor = SpacyDocumentProcessor(spacy_document)
        knowledge_record = document_processor.process_document()
        return knowledge_record

    def _get_document_for_text(self, text: str) -> Doc:
        return self._model(text)
