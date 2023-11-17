from logic_layer.remote_graph_database._graph_database_edge import GraphDatabaseEdge
from logic_layer.remote_graph_database._graph_database_node import GraphDatabaseNode
from resources_layer.aws_clients.neptune_client._neptune_edge import NeptuneEdge
from resources_layer.aws_clients.neptune_client._neptune_node import NeptuneNode


def parse_raw_neptune_node_object(neptune_node: NeptuneNode) -> GraphDatabaseNode:
    node_id = str(neptune_node.get_id())
    node_label = str(neptune_node.get_label())
    node_properties = neptune_node.get_properties()
    node = GraphDatabaseNode(node_id=node_id, label=node_label, properties=node_properties)
    return node


def parse_raw_neptune_edge_object(raw_data: NeptuneEdge) -> GraphDatabaseEdge:
    edge_id = str(raw_data.get_id())
    edge_label = str(raw_data.get_label())
    from_edge = str(raw_data.get_from_node())
    to_edge = str(raw_data.get_to_node())
    edge_properties = raw_data.get_properties()
    edge = GraphDatabaseEdge(edge_id=edge_id, edge_label=edge_label, from_node=from_edge, to_node=to_edge, properties=edge_properties)
    return edge
