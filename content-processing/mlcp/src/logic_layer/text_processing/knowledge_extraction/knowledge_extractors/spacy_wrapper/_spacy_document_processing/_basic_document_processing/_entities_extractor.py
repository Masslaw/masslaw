from typing import Set

from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._structures import DocumentEntity
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._structures import SpacyDocumentData


class SpacyEntitiesExtractor:
    def __init__(self, document_data: SpacyDocumentData):
        self._document_data = document_data
        self._entities: Set[DocumentEntity] = set()

    def extract_entities(self):
        self._load_entities()
        self._load_entities_coreference_chains()
        self._resolve_entity_appearances()
        self._document_data.document_entities = self._entities

    def _load_entities(self):
        spacy_document = self._document_data.spacy_document
        for entity_span in spacy_document.ents:
            document_entity = DocumentEntity()
            document_entity.entity_spans = {entity_span}
            document_entity.entity_type = entity_span.label_
            document_entity.entity_data = {}
            self._entities.add(document_entity)

    def _load_entities_coreference_chains(self):
        for entity in self._entities:
            entity.coreference_chains = set()
            for chain in self._document_data.coreference_chains:
                if entity.entity_spans & chain.chain_entities:
                    entity.coreference_chains.add(chain)

    def _resolve_entity_appearances(self):
        for entity in self._entities:
            entity.entity_appearances = set([span.root for span in entity.entity_spans])
            for chain in entity.coreference_chains:
                entity.entity_appearances.update([token for token in chain.chain_tokens if token.pos_ == "PRON"])
