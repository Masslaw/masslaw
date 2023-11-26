from typing import List

from logic_layer.knowledge_record._connection import KnowledgeRecordConnection
from logic_layer.knowledge_record.data_merging import ConnectionMerger
from logic_layer.knowledge_record.data_merging import EntityMerger
from logic_layer.knowledge_record._entity import KnowledgeRecordEntity
from logic_layer.knowledge_record._record import KnowledgeRecord
from logic_layer.knowledge_record.data_loading import graph_database_loading
from logic_layer.knowledge_record._record_compnents_matching import connection_matching
from logic_layer.knowledge_record._record_compnents_matching import entity_matching
from logic_layer.remote_graph_database._graph_database_manager import GraphDatabaseManager
from shared_layer.mlcp_logger import logger


def sync_record_with_graph_database(graph_database_manager: GraphDatabaseManager, record: KnowledgeRecord):
    record_entities = record.get_entities()
    _sync_entities_with_graph_database(graph_database_manager, record_entities)
    record.set_entities(record_entities)

    record_connections = record.get_connections()
    _sync_connections_with_graph_database(graph_database_manager, record_connections)
    record.set_connections(record_connections)


def _sync_entities_with_graph_database(graph_database_manager: GraphDatabaseManager, record_entities: List[KnowledgeRecordEntity]):
    for record_entity in record_entities:
        _sync_entity_with_graph_database(graph_database_manager, record_entity)


def _sync_entity_with_graph_database(graph_database_manager: GraphDatabaseManager, record_entity: KnowledgeRecordEntity):
    _get_and_merge_matching_entity_if_exists(graph_database_manager, record_entity)
    if record_entity.get_id():
        graph_database_manager.load_properties_to_node(node_id=record_entity.get_id(), properties=record_entity.get_properties())
        return
    new_node = graph_database_manager.set_node(label=record_entity.get_label(), properties=record_entity.get_properties(), )
    record_entity.set_id(new_node.get_id())


def _get_and_merge_matching_entity_if_exists(graph_database_manager: GraphDatabaseManager, record_entity: KnowledgeRecordEntity):
    matching_entities = entity_matching.fetch_matching_entities_in_database(graph_database_manager, record_entity)
    if len(matching_entities) == 0:
        return
    if len(matching_entities) > 1:
        logger.critical(f"More than one matching node found for entity {record_entity.get_properties()}")
    matching_entity = matching_entities[0]
    entity_merger = EntityMerger(record_entity)
    entity_merger.merge_data_from_another_entity(matching_entity)


def _sync_connections_with_graph_database(graph_database_manager: GraphDatabaseManager, record_connections: List[KnowledgeRecordConnection]):
    for record_connection in record_connections:
        _sync_connection_with_graph_database(graph_database_manager, record_connection)


def _sync_connection_with_graph_database(graph_database_manager: GraphDatabaseManager, record_connection: KnowledgeRecordConnection):
    _get_and_merge_matching_connection_if_exists(graph_database_manager, record_connection)
    if record_connection.get_id():
        graph_database_manager.load_properties_to_edge(edge_id=record_connection.get_id(), properties=record_connection.get_properties())
        return
    new_edge = graph_database_manager.set_edge(edge_label=record_connection.get_label(), from_node=record_connection.get_from_entity().get_id(),
        to_node=record_connection.get_to_entity().get_id(), properties=record_connection.get_properties(), )
    record_connection.set_id(new_edge.get_id())


def _get_and_merge_matching_connection_if_exists(graph_database_manager: GraphDatabaseManager, record_connection: KnowledgeRecordConnection):
    matching_connections = connection_matching.fetch_matching_connections_in_database(graph_database_manager, record_connection)
    if len(matching_connections) == 0:
        return
    if len(matching_connections) > 1:
        logger.critical(f"More than one matching edge found for connection {record_connection.get_properties()}")
    matching_connection = matching_connections[0]
    connection_merger = ConnectionMerger(record_connection)
    connection_merger.merge_data_from_another_connection(matching_connection)
