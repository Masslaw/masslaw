from typing import Dict
from typing import List

from gremlin_python.process import graph_traversal
from gremlin_python.process.graph_traversal import GraphTraversal
from gremlin_python.statics import long
from gremlin_python.structure.graph import Edge
from gremlin_python.structure.graph import Vertex

from resources_layer.aws.neptune_client._neptune_edge import NeptuneEdge
from resources_layer.aws.neptune_client._neptune_node import NeptuneNode


def parse_raw_neptune_node_data(raw_data: Dict) -> NeptuneNode:
    node_id = long(raw_data['id'])
    node_label = raw_data['label']
    node_properties = raw_data.get('properties', {})
    node = NeptuneNode(node_id=node_id, label=node_label, properties=node_properties)
    return node


def get_node_object_from_vertex(vertex: Vertex) -> NeptuneNode:
    node_id = long(vertex.id)
    node_label = str(vertex.label)
    node_properties = {p.key: p.value for p in vertex.properties or {}}
    node = NeptuneNode(node_id=node_id, label=node_label, properties=node_properties)
    return node


def _node_data_traversal_projection(traversal: GraphTraversal) -> GraphTraversal:
    t = traversal.project('id', 'label', 'properties')
    t = t.by(graph_traversal.id_())
    t = t.by(graph_traversal.label())
    t = t.by(graph_traversal.valueMap().by(graph_traversal.unfold()))
    return t


def get_node_data_from_traversal(traversal: GraphTraversal) -> Dict:
    t = _node_data_traversal_projection(traversal=traversal)
    node_data = t.next()
    return node_data


def get_multiple_nodes_data_from_traversal(traversal: GraphTraversal) -> Dict:
    t = _node_data_traversal_projection(traversal=traversal)
    nodes_data = t.to_list()
    return nodes_data


def get_node_object_from_traversal(traversal: GraphTraversal) -> NeptuneNode:
    node_data = get_node_data_from_traversal(traversal=traversal)
    node_object = parse_raw_neptune_node_data(raw_data=node_data)
    return node_object


def get_multiple_node_objects_from_traversal(traversal: GraphTraversal) -> List[NeptuneNode]:
    node_data = get_multiple_nodes_data_from_traversal(traversal=traversal)
    node_objects = [parse_raw_neptune_node_data(raw_data=node_data) for node_data in node_data]
    return node_objects


def parse_raw_neptune_edge_data(raw_data: Dict) -> NeptuneEdge:
    edge_id = long(raw_data['id'])
    edge_label = str(raw_data['label'])
    from_edge = long(raw_data['outV'])
    to_edge = long(raw_data['inV'])
    edge_properties = raw_data.get('properties', {})
    edge = NeptuneEdge(edge_id=edge_id, label=edge_label, from_node=from_edge, to_node=to_edge, properties=edge_properties)
    return edge


def get_edge_object_from_edge(edge: Edge) -> NeptuneEdge:
    edge_id = long(edge.id)
    edge_label = str(edge.label)
    from_edge = long(edge.outV.id)
    to_edge = long(edge.inV.id)
    edge_properties = {p.key: p.value for p in edge.properties or {}}
    edge = NeptuneEdge(edge_id=edge_id, label=edge_label, from_node=from_edge, to_node=to_edge, properties=edge_properties)
    return edge


def _edge_data_traversal_projection(traversal: GraphTraversal) -> GraphTraversal:
    t = traversal.project('id', 'label', 'outV', 'inV', 'properties')
    t = t.by(graph_traversal.id_())
    t = t.by(graph_traversal.label())
    t = t.by(graph_traversal.out_v().id_())
    t = t.by(graph_traversal.in_v().id_())
    t = t.by(graph_traversal.valueMap().by(graph_traversal.unfold()))
    return t


def get_edge_data_from_traversal(traversal: GraphTraversal) -> Dict:
    t = _edge_data_traversal_projection(traversal=traversal)
    edge_data = t.next()
    return edge_data


def get_multiple_edges_data_from_traversal(traversal: GraphTraversal) -> Dict:
    t = _edge_data_traversal_projection(traversal=traversal)
    edges_data = t.to_list()
    return edges_data


def get_edge_object_from_traversal(traversal: GraphTraversal) -> NeptuneEdge:
    edge_data = get_edge_data_from_traversal(traversal=traversal)
    edge_object = parse_raw_neptune_edge_data(raw_data=edge_data)
    return edge_object


def get_multiple_edge_objects_from_traversal(traversal: GraphTraversal) -> List[NeptuneEdge]:
    edge_data = get_multiple_edges_data_from_traversal(traversal=traversal)
    edge_objects = [parse_raw_neptune_edge_data(raw_data=edge_data) for edge_data in edge_data]
    return edge_objects
