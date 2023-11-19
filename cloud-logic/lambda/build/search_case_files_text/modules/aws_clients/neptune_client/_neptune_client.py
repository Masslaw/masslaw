from typing import Dict
from typing import List
from typing import Optional

from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.traversal import T
from gremlin_python.statics import long

from search_case_files_text.modules.aws_clients.neptune_client._data_parsing import get_edge_object_from_edge
from search_case_files_text.modules.aws_clients.neptune_client._data_parsing import get_edge_object_from_traversal
from search_case_files_text.modules.aws_clients.neptune_client._data_parsing import get_multiple_edge_objects_from_traversal
from search_case_files_text.modules.aws_clients.neptune_client._data_parsing import get_multiple_node_objects_from_traversal
from search_case_files_text.modules.aws_clients.neptune_client._data_parsing import get_node_object_from_traversal
from search_case_files_text.modules.aws_clients.neptune_client._data_parsing import get_node_object_from_vertex
from search_case_files_text.modules.aws_clients.neptune_client._neptune_connection import NeptuneConnection
from search_case_files_text.modules.aws_clients.neptune_client._neptune_edge import NeptuneEdge
from search_case_files_text.modules.aws_clients.neptune_client._neptune_node import NeptuneNode


class NeptuneClient:
    """
    Note: Multiple calls for functions of a single instance of this class are not thread-safe since it maintains
    a single connection to the Neptune database which doesn't support test_concurrency_utils.
    """

    def __init__(self, read_connection: NeptuneConnection, write_connection: NeptuneConnection):
        self._read_connection = read_connection
        self._write_connection = write_connection
        self.establish_connections()

    def __del__(self):
        self.close_connection()

    def close_connection(self):
        self._read_connection.close_connection()
        self._write_connection.close_connection()

    def establish_connections(self):
        self._read_connection.establish_connection()
        self._write_connection.establish_connection()

    def _get_read_traversal_source(self):
        return traversal().with_remote(self._read_connection.get_connection())

    def _get_write_traversal_source(self):
        return traversal().with_remote(self._write_connection.get_connection())

    def set_node(self, label: str, properties: Dict, node_id: long | str = None) -> NeptuneNode:
        g = self._get_write_traversal_source()
        t = g.add_v(label)
        if node_id:
            t = t.property(T.id, node_id)
        for key, value in properties.items():
            t = t.property(key, value)
        new_node = t.next()
        node_object = get_node_object_from_vertex(vertex=new_node)
        return node_object

    def set_edge(self, edge_label: str, from_node: long | str, to_node: long | str, properties: Dict, edge_id: long | str = None) -> NeptuneEdge:
        g = self._get_write_traversal_source()
        t = g.add_e(edge_label).from_(__.V(long(from_node))).to(__.V(to_node))
        if edge_id:
            t = t.property(T.id, long(edge_id))
        for key, value in properties.items():
            t = t.property(key, value)
        new_edge = t.next()
        edge_object = get_edge_object_from_edge(edge=new_edge)
        return edge_object

    def load_properties_to_node(self, node_id: long | str, properties: Dict):
        g = self._get_write_traversal_source()
        t = g.V(long(node_id))
        for key, value in properties.items():
            t = t.property(key, value)
        t.next()

    def load_properties_to_edge(self, edge_id: long | str, properties: Dict):
        g = self._get_write_traversal_source()
        t = g.E(long(edge_id))
        for key, value in properties.items():
            t = t.property(key, value)
        t.next()

    def delete_node_if_exists(self, node_id: long | str):
        g = self._get_write_traversal_source()
        try:
            g.V(long(node_id)).drop().next()
        except StopIteration:
            pass

    def delete_edge_if_exists(self, edge_id: long | str):
        g = self._get_write_traversal_source()
        try:
            g.E(long(edge_id)).drop().next()
        except StopIteration:
            pass

    def get_node_by_id(self, node_id: long | str) -> Optional[NeptuneNode]:
        g = self._get_read_traversal_source()
        try:
            node = g.V(long(node_id))
            node_object = get_node_object_from_traversal(node)
            return node_object
        except StopIteration:
            return None

    def get_edge_by_id(self, edge_id: long | str) -> Optional[NeptuneEdge]:
        g = self._get_read_traversal_source()
        try:
            edge = g.E(long(edge_id))
            edge_object = get_edge_object_from_traversal(edge)
            return edge_object
        except StopIteration:
            return None

    def get_nodes_by_properties(self, properties: Dict, label=None) -> List[NeptuneNode]:
        g = self._get_read_traversal_source()
        t = g.V()
        if label:
            t = t.has_label(label)
        for key, value in properties.items():
            t = t.has(key, value)
        node_objects = get_multiple_node_objects_from_traversal(traversal=t)
        return node_objects

    def get_edges_by_properties(self, properties: Dict, label=None, from_node: long | str = None, to_node: long | str = None) -> List[NeptuneEdge]:
        g = self._get_read_traversal_source()
        t = g.E()
        for key, value in properties.items():
            t = t.has(key, value)
        if label:
            t = t.has_label(label)
        if from_node:
            t = t.where(__.out_v().hasId(from_node))
        if to_node:
            t = t.where(__.in_v().hasId(to_node))
        edge_objects = get_multiple_edge_objects_from_traversal(traversal=t)
        return edge_objects

    def get_edges_by_nodes_connection(self, from_node: long | str = None, to_node: long | str = None) -> List[NeptuneEdge]:
        if (from_node, to_node).count(None) == 2:
            raise ValueError('At least one of the nodes must be specified')
        g = self._get_read_traversal_source()
        if from_node and not to_node:
            t = g.V(from_node).out_e()
        elif to_node and not from_node:
            t = g.V(to_node).in_e()
        else:
            t = g.V(from_node).out_e().where(__.in_v().has_id(to_node))
        edge_objects = get_multiple_edge_objects_from_traversal(traversal=t)
        return edge_objects
