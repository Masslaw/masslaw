from typing import List

from logic_layer.knowledge_record import KnowledgeRecord
from logic_layer.knowledge_record._entity import KnowledgeRecordEntity
from logic_layer.remote_graph_database import GraphDatabaseManager
from logic_layer.knowledge_record.data_loading import graph_database_loading


def compare_entities(entity1: KnowledgeRecordEntity, entity2: KnowledgeRecordEntity) -> int:
    return 0


def fetch_matching_entities_in_database(graph_database_manager: GraphDatabaseManager, entity: KnowledgeRecordEntity) -> List[KnowledgeRecordEntity]:
    entity_label = entity.get_label()
    entity_unique_properties = entity.get_unique_properties()
    matching_nodes = graph_database_manager.get_nodes_by_properties(label=entity_label, properties=entity_unique_properties, )
    matching_entities = [graph_database_loading.graph_database_node_to_entity(node) for node in matching_nodes]
    return matching_entities


def find_matching_entity_in_record(entity: KnowledgeRecordEntity, record: KnowledgeRecord) -> KnowledgeRecordEntity:
    record_entities = record.get_entities()
    for record_entity in record_entities:
        if record_entity.get_label() != entity.get_label(): continue
        for unique_property in entity.get_unique_properties():
            entity_unique_property_value = entity.get_properties().get(unique_property)
            other_entity_unique_property_value = record_entity.get_properties().get(unique_property)
            if entity_unique_property_value and other_entity_unique_property_value and entity_unique_property_value == other_entity_unique_property_value:
                return record_entity
