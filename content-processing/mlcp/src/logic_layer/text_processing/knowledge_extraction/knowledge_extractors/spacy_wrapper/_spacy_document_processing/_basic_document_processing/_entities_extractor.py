from typing import Set

from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._structures import DocumentEntity
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._structures import SpacyDocumentData
from shared_layer.mlcp_logger import logger
from shared_layer.mlcp_logger import common_formats


class SpacyEntitiesExtractor:
    def __init__(self, document_data: SpacyDocumentData):
        self._document_data = document_data
        self._entities: Set[DocumentEntity] = set()

    def extract_entities(self):
        self._load_entities()
        self._load_entities_coreference_chains()
        self._document_data.document_entities = self._entities

    def _load_entities(self):
        spacy_document = self._document_data.spacy_document
        for entity_span in spacy_document.ents:
            document_entity = DocumentEntity()
            document_entity.entity_span = entity_span
            document_entity.entity_data = {}
            self._entities.add(document_entity)
        logger.info(f"{common_formats.value(len(self._entities))} entities extracted.")

    def _load_entities_coreference_chains(self):
        for entity in self._entities:
            entity.entity_appearances = {entity.entity_span.root}
            for chain in self._document_data.coreference_chains:
                if entity.entity_span not in chain.chain_entities: continue
                for chain_token in chain.chain_tokens:
                    if chain_token.ent_type_: continue
                    entity.entity_appearances.add(chain_token)
