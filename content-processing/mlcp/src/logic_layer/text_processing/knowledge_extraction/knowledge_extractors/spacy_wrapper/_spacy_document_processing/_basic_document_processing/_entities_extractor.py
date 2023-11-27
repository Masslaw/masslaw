from typing import List

from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._structures import DocumentEntity
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._structures import SpacyDocumentData
from shared_layer.list_utils import list_utils


class SpacyEntitiesExtractor:
    def __init__(self, document_data: SpacyDocumentData):
        self._document_data = document_data
        self._entities: List[DocumentEntity] = []

    def extract_entities(self):
        self._load_entities()
        self._release_useless_entities()
        self._load_entities_coreference_chains()
        self._resolve_entity_appearances()
        self._merge_entities()
        self._document_data.document_entities = self._entities

    def _load_entities(self):
        spacy_document = self._document_data.spacy_document
        for entity_span in spacy_document.ents:
            document_entity = DocumentEntity()
            document_entity.entity_spans = {entity_span}
            document_entity.entity_type = entity_span.label_
            document_entity.entity_data = {}
            self._entities.append(document_entity)

    def _release_useless_entities(self):
        self._entities = [entity for entity in self._entities if not self._detereine_entity_useless(entity)]

    def _detereine_entity_useless(self, entity: DocumentEntity) -> bool:
        if entity.entity_type in ("DATE", ) and any(span for span in entity.entity_spans if 'old' in span.text): return True;
        return False

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

    def _merge_entities(self):
        list_utils.merge_mergeable(self._entities, self._mergeable, self._do_merge_entities)

    def _mergeable(self, entity1: DocumentEntity, entity2: DocumentEntity) -> bool:
        if entity1.entity_type != entity2.entity_type:
            return False

        entity1_name_components = set()
        for entity1_span in entity1.entity_spans:
            entity1_name_components.update(entity1_span.text.split(' '))
        entity2_name_components = set()
        for entity2_span in entity2.entity_spans:
            entity2_name_components.update(entity2_span.text.split(' '))
        overlapping_components = entity1_name_components & entity2_name_components
        if len(overlapping_components):
            return True

        return False

    def _do_merge_entities(self, entity1: DocumentEntity, entity2: DocumentEntity) -> DocumentEntity:
        merged_entity = DocumentEntity()
        merged_entity.entity_type = entity1.entity_type
        merged_entity.entity_spans = entity1.entity_spans | entity2.entity_spans
        merged_entity.coreference_chains = entity1.coreference_chains.copy() | entity2.coreference_chains.copy()
        merged_entity.entity_appearances = entity1.entity_appearances.copy() | entity2.entity_appearances.copy()
        merged_entity.entity_data = {**entity1.entity_data, **entity2.entity_data}
        return merged_entity
