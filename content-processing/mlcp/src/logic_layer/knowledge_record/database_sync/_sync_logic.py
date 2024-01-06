from typing import List

from logic_layer.knowledge_record import KnowledgeRecordConnection
from logic_layer.knowledge_record import KnowledgeRecordEntity
from logic_layer.knowledge_record._record import KnowledgeRecord
from logic_layer.knowledge_record.data_loading._graph_database_loading import graph_database_edge_to_connection
from logic_layer.knowledge_record.data_loading._graph_database_loading import graph_database_node_to_entity
from logic_layer.knowledge_record.record_merging import RecordMerger
from logic_layer.knowledge_record.record_merging import RecordMergingConfiguration
from logic_layer.remote_graph_database._graph_database_manager import GraphDatabaseManager
from shared_layer.mlcp_logger import logger


@logger.process_function('Syncing knowledge record with graph database')
def sync_record_with_graph_database(record: KnowledgeRecord, graph_database_manager: GraphDatabaseManager, merging_configuration: RecordMergingConfiguration):
    graph_record = _load_knowledge_record_from_database(graph_database_manager)
    record_merger = RecordMerger(record, merging_configuration)
    record_merger.merge_record(graph_record)
    _load_record_data_to_database(record, graph_database_manager)


@logger.process_function('Loading knowledge record from database')
def _load_knowledge_record_from_database(graph_database_manager: GraphDatabaseManager) -> KnowledgeRecord:
    entities = _fetch_graph_entities(graph_database_manager)
    connections = _fetch_graph_connections(graph_database_manager)
    record = KnowledgeRecord()
    record.set_entities(entities)
    record.set_connections(connections)
    return record


@logger.process_function('Fetching entities from database')
def _fetch_graph_entities(graph_database_manager: GraphDatabaseManager) -> List[KnowledgeRecordEntity]:
    nodes = graph_database_manager.get_nodes_by_properties({})
    entities = [graph_database_node_to_entity(node) for node in nodes]
    return entities


@logger.process_function('Fetching connections from database')
def _fetch_graph_connections(graph_database_manager: GraphDatabaseManager) -> List[KnowledgeRecordConnection]:
    edges = graph_database_manager.get_edges_by_properties({})
    connections = [graph_database_edge_to_connection(edge) for edge in edges]
    return connections


# TODO: Instead of iterating over all components and submitting them one by one - a single database instruction per each - find a gremlin instruction that batch-performs this action - lowering overhead and improving performance
@logger.process_function('Loading record data to database')
def _load_record_data_to_database(record: KnowledgeRecord, graph_database_manager: GraphDatabaseManager):
    for entity in record.get_entities():
        _put_entity_in_database(entity, graph_database_manager)
    for connection in record.get_connections():
        _put_connection_in_database(connection, graph_database_manager)


def _put_entity_in_database(record_entity: KnowledgeRecordEntity, graph_database_manager: GraphDatabaseManager):
    if record_entity.get_id():
        graph_database_manager.load_properties_to_node(node_id=record_entity.get_id(), properties=record_entity.get_properties())
        return
    new_node = graph_database_manager.set_node(label=record_entity.get_label(), properties=record_entity.get_properties(), )
    record_entity.set_id(new_node.get_id())


def _put_connection_in_database(record_connection: KnowledgeRecordConnection, graph_database_manager: GraphDatabaseManager):
    if record_connection.get_id():
        graph_database_manager.load_properties_to_edge(edge_id=record_connection.get_id(), properties=record_connection.get_properties())
        return
    if not record_connection.get_from_entity().get_id(): return
    if not record_connection.get_to_entity().get_id(): return
    new_edge = graph_database_manager.set_edge(edge_label=record_connection.get_label(), from_node=record_connection.get_from_entity().get_id(), to_node=record_connection.get_to_entity().get_id(), properties=record_connection.get_properties(), )
    record_connection.set_id(new_edge.get_id())
