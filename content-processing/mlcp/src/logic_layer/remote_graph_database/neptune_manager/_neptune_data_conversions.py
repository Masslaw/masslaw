from typing import List

from logic_layer.remote_graph_database._graph_database_edge import GraphDatabaseEdge
from logic_layer.remote_graph_database._graph_database_node import GraphDatabaseNode
from resources_layer.aws_clients.neptune_client._neptune_edge import NeptuneEdge
from resources_layer.aws_clients.neptune_client._neptune_node import NeptuneNode


def parse_raw_neptune_node_objects(neptune_nodes: List[NeptuneNode]) -> List[GraphDatabaseNode]:
    return [parse_raw_neptune_node_object(neptune_node) for neptune_node in neptune_nodes]


def parse_raw_neptune_node_object(neptune_node: NeptuneNode) -> GraphDatabaseNode:
    node_id = str(neptune_node.get_id())
    node_label = str(neptune_node.get_label())
    node_properties = neptune_node.get_properties()
    node = GraphDatabaseNode(node_id=node_id, label=node_label, properties=node_properties)
    return node


def parse_raw_neptune_edge_objects(neptune_edges: List[NeptuneEdge]) -> List[GraphDatabaseEdge]:
    return [parse_raw_neptune_edge_object(neptune_edge) for neptune_edge in neptune_edges]


def parse_raw_neptune_edge_object(raw_data: NeptuneEdge) -> GraphDatabaseEdge:
    edge_id = str(raw_data.get_id())
    edge_label = str(raw_data.get_label())
    from_edge = str(raw_data.get_from_node())
    to_edge = str(raw_data.get_to_node())
    edge_properties = raw_data.get_properties()
    edge = GraphDatabaseEdge(edge_id=edge_id, edge_label=edge_label, from_node=from_edge, to_node=to_edge, properties=edge_properties)
    return edge


def graph_database_nodes_to_raw_neptune_node_objects(graph_nodes: List[GraphDatabaseNode]) -> List[NeptuneNode]:
    return [graph_database_node_to_raw_neptune_node_object(graph_node) for graph_node in graph_nodes]


def graph_database_node_to_raw_neptune_node_object(graph_node: GraphDatabaseNode) -> NeptuneNode:
    node_id = graph_node.get_id()
    node_label = graph_node.get_label()
    node_properties = graph_node.get_properties()
    neptune_node = NeptuneNode(node_id=node_id, label=node_label, properties=node_properties)
    return neptune_node


def graph_database_edges_to_raw_neptune_edge_objects(graph_edges: List[GraphDatabaseEdge]) -> List[NeptuneEdge]:
    return [graph_database_edge_to_raw_neptune_edge_object(graph_edge) for graph_edge in graph_edges]


def graph_database_edge_to_raw_neptune_edge_object(graph_edge: GraphDatabaseEdge) -> NeptuneEdge:
    edge_id = graph_edge.get_id()
    edge_label = graph_edge.get_label()
    from_node = graph_edge.get_from_node()
    to_node = graph_edge.get_to_node()
    edge_properties = graph_edge.get_properties()
    neptune_edge = NeptuneEdge(edge_id=edge_id, label=edge_label, from_node=from_node, to_node=to_node, properties=edge_properties)
    return neptune_edge
