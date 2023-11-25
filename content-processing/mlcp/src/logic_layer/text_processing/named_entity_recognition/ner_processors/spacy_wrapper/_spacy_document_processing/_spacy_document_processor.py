import matplotlib.pyplot as plt
import networkx as nx
from spacy.tokens.doc import Doc

from logic_layer.knowledge_record import KnowledgeRecord
from logic_layer.text_processing.named_entity_recognition.ner_processors.spacy_wrapper._spacy_document_processing._coreferences_resolver import SpacyCoreferencesResolver
from logic_layer.text_processing.named_entity_recognition.ner_processors.spacy_wrapper._spacy_document_processing._entities_extractor import SpacyEntitiesExtractor
from logic_layer.text_processing.named_entity_recognition.ner_processors.spacy_wrapper._spacy_document_processing._relations_extractor import SpacyRelationsExtractor
from logic_layer.text_processing.named_entity_recognition.ner_processors.spacy_wrapper._spacy_document_processing._structures import SpacyDocumentData


class SpacyDocumentProcessor:

    def __init__(self, spacy_document: Doc):
        self._document_data = SpacyDocumentData(spacy_document)
        self._knowledge_record = KnowledgeRecord()

    def process_document(self) -> KnowledgeRecord:
        self._resolve_coreferences()
        self._extract_entities()
        self._extract_relations()
        self._inflate_document_data()
        self._build_knowledge_record()
        return self._knowledge_record

    def _resolve_coreferences(self):
        coreference_resolver = SpacyCoreferencesResolver(self._document_data)
        coreference_resolver.resolve_coreferences()

    def _extract_entities(self):
        coreference_resolver = SpacyEntitiesExtractor(self._document_data)
        coreference_resolver.extract_entities()

    def _extract_relations(self):
        relations_extractor = SpacyRelationsExtractor(self._document_data)
        relations_extractor.extract_relations()

    def _inflate_document_data(self):
        pass

    def _build_knowledge_record(self):
        pass
