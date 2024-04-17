import logging

from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._structures import DocumentEntity
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._structures import SpacyDocumentData
from shared_layer.mlcp_logger import logger
from shared_layer.mlcp_logger import common_formats


class DocumentDataFilterer:

    def __init__(self, document_data: SpacyDocumentData):
        self._document_data = document_data

    def filter_entities(self):
        logger.info(f"Filtering {common_formats.value(len(self._document_data.document_entities))} entities.")
        filtered_entities = {entity for entity in self._document_data.document_entities if not self._determine_entitiy_useless(entity)}
        self._document_data.document_entities = filtered_entities
        logger.info(f"{common_formats.value(len(self._document_data.document_entities))} entities left after filtering.")

    def _determine_entitiy_useless(self, entity: DocumentEntity) -> bool:
        entity_title = entity.entity_data.get('title', '').lower()
        if not entity_title: return True
        if entity.entity_span.label_ in ('LANGUAGE', ): return True
        if entity.entity_span.label_ in ('DATE', 'TIME', ) and not entity.entity_data.get('datetime', {}): return True
        if entity.entity_span.label_ in ('ORDINAL', 'PERCENT', ) and len(entity_title.split(' ')) < 2: return True
        if entity.entity_span.label_ in ('CARDINAL', 'QUANTITY', 'MONEY', ) and sum(c.isdigit() for c in entity_title) < 4: return True
        return False

    def filter_relations(self):
        pass