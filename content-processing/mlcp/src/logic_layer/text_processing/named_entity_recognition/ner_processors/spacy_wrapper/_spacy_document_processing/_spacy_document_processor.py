import spacy
from spacy.tokens.doc import Doc
from spacy.tokens.span import Span
from spacy.tokens.token import Token
from spacy import displacy

from logic_layer.knowledge_record import KnowledgeRecord


class SpacyDocumentProcessor:

    def __init__(self, document: Doc):
        self._document: Doc = document
        self._knowledge_record = KnowledgeRecord()
        self._cache = {}

    def process_document(self) -> KnowledgeRecord:
        self._resolve_coreferences()
        self._extract_entities()
        self._extract_relations()
        self._inflate_entity_data()
        return self._knowledge_record

    def _resolve_coreferences(self):
        pass

    def _extract_entities(self):
        pass

    def _extract_relations(self):
        pass

    def _inflate_entity_data(self):
        pass
