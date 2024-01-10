from logic_layer.knowledge_record import KnowledgeRecord
from logic_layer.knowledge_record import KnowledgeRecordConnection
from logic_layer.knowledge_record import KnowledgeRecordEntity
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._structures import SpacyDocumentData
from shared_layer.mlcp_logger import logger


class SpacyDocumentKnowledgeRecordBuilder:

    def __init__(self, document_data: SpacyDocumentData):
        self._document_data = document_data
        self._knowledge_record = KnowledgeRecord()
        self._document_entities_to_record_entities = {}

    def build_knowledge_record(self) -> KnowledgeRecord:
        self._create_entities()
        self._create_relations()
        return self._knowledge_record

    @logger.process_function("Creating entities")
    def _create_entities(self):
        for entity in self._document_data.document_entities:
            entity_label = entity.entity_span.label_
            entity_properties = entity.entity_data
            record_entity = KnowledgeRecordEntity('', entity_label, entity_properties)
            self._document_entities_to_record_entities[entity] = record_entity
            self._knowledge_record.add_entities(record_entity)

    @logger.process_function("Creating relations")
    def _create_relations(self):
        for relation in self._document_data.document_relations:
            relation_label = relation.relation_type
            relation_properties = relation.relation_data
            from_entity = self._document_entities_to_record_entities[relation.from_entity]
            to_entity = self._document_entities_to_record_entities[relation.to_entity]
            record_connection = KnowledgeRecordConnection('', relation_label, from_entity, to_entity, relation_properties)
            self._knowledge_record.add_connections(record_connection)
