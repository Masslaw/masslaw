from logic_layer.knowledge_record._connection import KnowledgeRecordConnection
from logic_layer.knowledge_record._entity import KnowledgeRecordEntity
from logic_layer.remote_graph_database._graph_database_edge import GraphDatabaseEdge
from logic_layer.remote_graph_database._graph_database_node import GraphDatabaseNode


def graph_database_node_to_entity(node: GraphDatabaseNode) -> KnowledgeRecordEntity:
    entity = KnowledgeRecordEntity(entity_id=node.get_id(), label=node.get_label(), properties=node.get_properties(), )
    return entity


def graph_database_edge_to_connection(edge: GraphDatabaseEdge) -> KnowledgeRecordConnection:
    connection = KnowledgeRecordConnection(connection_id=edge.get_id(), label=edge.get_label(), from_entity=KnowledgeRecordEntity(entity_id=edge.get_from_node()),
        to_entity=KnowledgeRecordEntity(entity_id=edge.get_to_node()), properties=edge.get_properties(), )
    return connection
