from typing import Dict

from logic_layer.knowledge_record._connection import KnowledgeRecordConnection
from logic_layer.knowledge_record._entity import KnowledgeRecordEntity
from logic_layer.knowledge_record._record import KnowledgeRecord
from logic_layer.knowledge_record.data_loading._assertions import assert_connection_dictionary_data_record
from logic_layer.knowledge_record.data_loading._assertions import assert_entity_dictionary_data_record
from logic_layer.knowledge_record.data_loading._assertions import assert_record_dictionary_data_record


def dictionary_to_entity(data: Dict) -> KnowledgeRecordEntity:
    assert_entity_dictionary_data_record(data)
    entity = KnowledgeRecordEntity(entity_id=data.get('id'), label=data.get('label'), properties=data.get('properties'), unique_properties=data.get('unique_properties'), )
    return entity


def dictionary_to_connection(data: Dict) -> KnowledgeRecordConnection:
    assert_connection_dictionary_data_record(data)
    connection = KnowledgeRecordConnection(connection_id=data.get('id'), label=data.get('label'), from_entity=KnowledgeRecordEntity(entity_id=data.get('from_entity_id')),
        to_entity=KnowledgeRecordEntity(entity_id=data.get('to_entity_id')), properties=data.get('properties'), unique_properties=data.get('unique_properties'), )
    return connection


def dictionary_to_record(data: Dict) -> KnowledgeRecord:
    assert_record_dictionary_data_record(data)
    record = KnowledgeRecord(id=data.get('id'), label=data.get('label'), entities=[dictionary_to_entity(entity_data) for entity_data in data.get('entities')],
        connections=[dictionary_to_connection(connection_data) for connection_data in data.get('connections')], )
    return record
