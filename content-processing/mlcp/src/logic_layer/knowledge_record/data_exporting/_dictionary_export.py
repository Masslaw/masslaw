from typing import Dict

from logic_layer.knowledge_record._connection import KnowledgeRecordConnection
from logic_layer.knowledge_record._entity import KnowledgeRecordEntity
from logic_layer.knowledge_record._record import KnowledgeRecord


def entity_to_dictionary(entity: KnowledgeRecordEntity) -> Dict:
    entity_data = {
        'id': entity.get_id(),
        'label': entity.get_label(),
        'properties': entity.get_properties()
    }
    return entity_data


def connection_to_dictionary(connection: KnowledgeRecordConnection):
    connection_data = {
        'id': connection.get_id(),
        'label': connection.get_label(),
        'from_entity_id': connection.get_from_entity().get_id(),
        'to_entity_id': connection.get_to_entity().get_id(),
        'properties': connection.get_properties(),
    }
    return connection_data


def record_to_dictionary(record: KnowledgeRecord):
    record_data = {
        'entities': [entity_to_dictionary(entity) for entity in record.get_entities()],
        'connections': [connection_to_dictionary(connection) for connection in record.get_connections()],
    }
    return record_data
