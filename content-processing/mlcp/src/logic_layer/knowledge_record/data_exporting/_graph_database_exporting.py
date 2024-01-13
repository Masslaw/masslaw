from typing import List

from logic_layer.knowledge_record._connection import KnowledgeRecordConnection
from logic_layer.knowledge_record._entity import KnowledgeRecordEntity
from logic_layer.remote_graph_database._graph_database_edge import GraphDatabaseEdge
from logic_layer.remote_graph_database._graph_database_node import GraphDatabaseNode


def entities_to_graph_database_nodes(entities: List[KnowledgeRecordEntity]) -> List[GraphDatabaseNode]:
    return [entity_to_graph_database_node(entity) for entity in entities]


def entity_to_graph_database_node(entity: KnowledgeRecordEntity) -> GraphDatabaseNode:
    node_id = entity.get_id()
    node_label = entity.get_label()
    node_properties = entity.get_properties()
    node = GraphDatabaseNode(node_id=node_id, label=node_label, properties=node_properties)
    return node


def connections_to_graph_database_edges(connections: List[KnowledgeRecordConnection]) -> List[GraphDatabaseEdge]:
    return [connection_to_graph_database_edge(connection) for connection in connections]


def connection_to_graph_database_edge(connection: KnowledgeRecordConnection) -> GraphDatabaseEdge:
    edge_id = connection.get_id()
    edge_label = connection.get_label()
    from_edge = connection.get_from_entity().get_id()
    to_edge = connection.get_to_entity().get_id()
    edge_properties = connection.get_properties()
    edge = GraphDatabaseEdge(edge_id=edge_id, edge_label=edge_label, from_node=from_edge, to_node=to_edge, properties=edge_properties)
    return edge
