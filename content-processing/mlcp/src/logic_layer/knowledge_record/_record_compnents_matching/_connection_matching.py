from concurrent.futures import ThreadPoolExecutor
from typing import List

from logic_layer.knowledge_record import KnowledgeRecord
from logic_layer.knowledge_record._connection import KnowledgeRecordConnection
from logic_layer.remote_graph_database import GraphDatabaseManager
from logic_layer.knowledge_record.data_loading import graph_database_loading


def compare_connections(connection1: KnowledgeRecordConnection, connection2: KnowledgeRecordConnection) -> int:
    return 0


def fetch_matching_connections_in_database(graph_database_manager: GraphDatabaseManager, connection: KnowledgeRecordConnection, ) -> List[KnowledgeRecordConnection]:
    connection_label = connection.get_label()
    connection_from_entity_id = connection.get_from_entity().get_id()
    connection_to_entity_id = connection.get_to_entity().get_id()
    connection_unique_properties = connection.get_unique_properties()
    with ThreadPoolExecutor() as executor:
        one_way_query_future = executor.submit(graph_database_manager.get_edges_by_properties, connection_unique_properties, connection_label, connection_from_entity_id, connection_to_entity_id)
        opposite_way_query_future = executor.submit(graph_database_manager.get_edges_by_properties, connection_unique_properties, connection_label, connection_to_entity_id, connection_from_entity_id)
        matching_edges = one_way_query_future.result() + opposite_way_query_future.result()
    matching_connections = [graph_database_loading.graph_database_edge_to_connection(edge) for edge in matching_edges]
    return matching_connections


def find_matching_connection_in_record(connection: KnowledgeRecordConnection, record: KnowledgeRecord, bidirectional: bool = False, ignore_properties: bool = False) -> KnowledgeRecordConnection:
    for record_connection in record.get_connections():
        if record_connection.get_label() != connection.get_label(): continue
        if bidirectional:
            if connection.get_from_entity() not in (record_connection.get_from_entity().get_id(), record_connection.get_to_entity().get_id()): continue
            if connection.get_to_entity() not in (record_connection.get_from_entity().get_id(), record_connection.get_to_entity().get_id()): continue
        else:
            if record_connection.get_from_entity().get_id() != connection.get_from_entity().get_id(): continue
            if record_connection.get_to_entity().get_id() != connection.get_to_entity().get_id(): continue
        if not ignore_properties:
            for unique_property in connection.get_unique_properties():
                connection_unique_property_value = connection.get_properties().get(unique_property)
                other_connection_unique_property_value = record_connection.get_properties().get(unique_property)
                if connection_unique_property_value and other_connection_unique_property_value and connection_unique_property_value == other_connection_unique_property_value:
                    return record_connection
        else:
            return record_connection
