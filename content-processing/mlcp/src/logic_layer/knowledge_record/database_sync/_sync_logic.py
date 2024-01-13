from typing import Dict
from typing import List
from typing import Tuple

from logic_layer.knowledge_record import KnowledgeRecordConnection
from logic_layer.knowledge_record import KnowledgeRecordEntity
from logic_layer.knowledge_record._record import KnowledgeRecord
from logic_layer.knowledge_record.data_exporting._graph_database_exporting import connections_to_graph_database_edges
from logic_layer.knowledge_record.data_exporting._graph_database_exporting import entities_to_graph_database_nodes
from logic_layer.knowledge_record.data_loading._graph_database_loading import graph_database_edge_to_connection
from logic_layer.knowledge_record.data_loading._graph_database_loading import graph_database_node_to_entity
from logic_layer.knowledge_record.record_merging import RecordMerger
from logic_layer.knowledge_record.record_merging import RecordMergingConfiguration
from logic_layer.remote_graph_database._graph_database_manager import GraphDatabaseManager
from shared_layer.mlcp_logger import logger


MAX_NUMBER_OF_ENTITIES_SUBMITTED = 150
MAX_NUMBER_OF_CONNECTIONS_SUBMITTED = 5000


@logger.process_function('Syncing knowledge record with graph database')
def sync_record_with_graph_database(record: KnowledgeRecord, graph_database_manager: GraphDatabaseManager, merging_configuration: RecordMergingConfiguration):
    graph_record = _load_knowledge_record_from_database(graph_database_manager)
    record_merger = RecordMerger(record, merging_configuration)
    record_merger.merge_record(graph_record)
    _filter_knowledge_components(record, graph_database_manager)
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


@logger.process_function("Filtering knowledge components")
def _filter_knowledge_components(record: KnowledgeRecord, graph_database_manager: GraphDatabaseManager):
    entities_to_delete, connections_to_delete = _resolve_deletable_components(record)
    record.set_entities([entity for entity in record.get_entities() if entity not in entities_to_delete])
    record.set_connections([connection for connection in record.get_connections() if connection not in connections_to_delete])
    _delete_entities(entities_to_delete, graph_database_manager)
    _delete_connections(connections_to_delete, graph_database_manager)


@logger.process_function("Resolving deletable components")
def _resolve_deletable_components(record: KnowledgeRecord) -> Tuple[List[KnowledgeRecordEntity], List[KnowledgeRecordConnection]]:
    sorted_entities, sorted_connections = _sort_entities_and_connections_by_contribution_and_strength(record.get_entities(), record.get_connections())
    entities_to_delete = []
    connections_to_delete = []
    if len(sorted_entities) > MAX_NUMBER_OF_ENTITIES_SUBMITTED:
        entities_to_delete += sorted_entities[MAX_NUMBER_OF_ENTITIES_SUBMITTED:]
        for entity_to_delete in entities_to_delete:
            entity_connections = record.get_entity_ingoing_connections(entity_to_delete) + record.get_entity_outgoing_connections(entity_to_delete)
            connections_to_delete += entity_connections
    if len(sorted_connections) > MAX_NUMBER_OF_CONNECTIONS_SUBMITTED:
        connections_to_delete += sorted_connections[MAX_NUMBER_OF_CONNECTIONS_SUBMITTED:]
    return entities_to_delete, connections_to_delete


def _sort_entities_and_connections_by_contribution_and_strength(entities: List[KnowledgeRecordEntity], connections: List[KnowledgeRecordConnection]) -> Tuple[List[KnowledgeRecordEntity], List[KnowledgeRecordConnection]]:
    entity_contributions, connection_strengths = _resolve_entity_contributions_and_connection_strength(connections)
    sorted_entities = sorted(entities, key=lambda entity: entity_contributions.get(entity.__hash__(), 0), reverse=True)
    sorted_connections = sorted(connections, key=lambda connection: connection_strengths.get(connection.__hash__(), 0), reverse=True)
    return sorted_entities, sorted_connections


def _resolve_entity_contributions_and_connection_strength(connections: List[KnowledgeRecordConnection]) -> Tuple[Dict, Dict]:
    entity_contributions = {}
    connection_strengths = {}
    for connection in connections:
        connection_strength = connection.get_properties().get('strength', 0)
        from_entity = connection.get_from_entity()
        to_entity = connection.get_to_entity()
        connection_strengths[connection.__hash__()] = connection_strengths.get(connection.__hash__(), 0) + connection_strength
        entity_contributions[from_entity.__hash__()] = entity_contributions.get(from_entity.__hash__(), 0) + connection_strength
        entity_contributions[to_entity.__hash__()] = entity_contributions.get(to_entity.__hash__(), 0) + connection_strength
    return connection_strengths, entity_contributions


@logger.process_function('Deleting filtered knowledge components from database')
def _delete_entities(entities: List[KnowledgeRecordEntity], graph_database_manager: GraphDatabaseManager):
    entity_ids = [entity.get_id() for entity in entities]
    graph_database_manager.delete_nodes_if_exist(entity_ids)


@logger.process_function('Deleting filtered knowledge components from database')
def _delete_connections(connections: List[KnowledgeRecordConnection], graph_database_manager: GraphDatabaseManager):
    connection_ids = [connection.get_id() for connection in connections]
    graph_database_manager.delete_edges_if_exist(connection_ids)


@logger.process_function('Loading record data to database')
def _load_record_data_to_database(record: KnowledgeRecord, graph_database_manager: GraphDatabaseManager):
    record_entities = record.get_entities()
    _put_entities_in_database(record_entities, graph_database_manager)
    record_connections = record.get_connections()
    _put_connections_in_database(record_connections, graph_database_manager)


@logger.process_function('Putting entities in database')
def _put_entities_in_database(record_entities: List[KnowledgeRecordEntity], graph_database_manager: GraphDatabaseManager):
    # new_entities, existing_entities = _separate_entities_to_new_and_existing(record_entities)
    _load_new_entities_to_database(record_entities, graph_database_manager)
    # _load_existing_entities_to_database(existing_entities, graph_database_manager)


@logger.process_function('Putting connections in database')
def _put_connections_in_database(record_connections: List[KnowledgeRecordConnection], graph_database_manager: GraphDatabaseManager):
    # new_connections, existing_connections = _separate_connections_to_new_and_existing(record_connections)
    _load_new_connections_to_database(record_connections, graph_database_manager)
    # _load_existing_connections_to_database(existing_connections, graph_database_manager)


def _separate_entities_to_new_and_existing(entities: List[KnowledgeRecordEntity]) -> Tuple[List[KnowledgeRecordEntity], List[KnowledgeRecordEntity]]:
    new_entities = []
    existing_entities = []
    for entity in entities:
        if entity.get_id(): existing_entities.append(entity)
        else: new_entities.append(entity)
    return new_entities, existing_entities


def _separate_connections_to_new_and_existing(connections: List[KnowledgeRecordConnection]) -> Tuple[List[KnowledgeRecordConnection], List[KnowledgeRecordConnection]]:
    new_connections = []
    existing_connections = []
    for connection in connections:
        if connection.get_id(): existing_connections.append(connection)
        else: new_connections.append(connection)
    return new_connections, existing_connections


def _load_new_entities_to_database(new_entities: List[KnowledgeRecordEntity], graph_database_manager: GraphDatabaseManager) -> List[KnowledgeRecordEntity]:
    graph_database_nodes = entities_to_graph_database_nodes(new_entities)
    new_nodes = graph_database_manager.set_nodes(graph_database_nodes)
    for idx, entity in enumerate(new_entities): entity.set_id(new_nodes[idx].get_id())


def _load_new_connections_to_database(new_connections: List[KnowledgeRecordConnection], graph_database_manager: GraphDatabaseManager) -> List[KnowledgeRecordConnection]:
    graph_database_edges = connections_to_graph_database_edges(new_connections)
    new_edges = graph_database_manager.set_edges(graph_database_edges)
    for idx, connection in enumerate(new_connections): connection.set_id(new_edges[idx].get_id())


def _load_existing_entities_to_database(existing_entities: List[KnowledgeRecordEntity], graph_database_manager: GraphDatabaseManager):
    entity_property_updates = {entity.get_id(): entity.get_properties() for entity in existing_entities}
    graph_database_manager.load_properties_to_nodes(entity_property_updates)


def _load_existing_connections_to_database(existing_connections: List[KnowledgeRecordConnection], graph_database_manager: GraphDatabaseManager):
    connection_property_updates = {connection.get_id(): connection.get_properties() for connection in existing_connections}
    graph_database_manager.load_properties_to_edges(connection_property_updates)
