from typing import List

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
    matching_edges = graph_database_manager.get_edges_by_properties(label=connection_label, from_node=connection_from_entity_id, to_node=connection_to_entity_id,
        properties=connection_unique_properties, )
    matching_connections = [graph_database_loading.graph_database_edge_to_connection(edge) for edge in matching_edges]
    return matching_connections
