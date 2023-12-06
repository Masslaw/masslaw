import logging
import os
from typing import Dict
from typing import List
from typing import Optional

from gremlin_python.driver.protocol import GremlinServerError
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.traversal import T
from gremlin_python.statics import long

from src.modules.aws_clients.neptune_client._data_parsing import get_edge_object_from_edge
from src.modules.aws_clients.neptune_client._data_parsing import get_edge_object_from_traversal
from src.modules.aws_clients.neptune_client._data_parsing import get_id_in_correct_type
from src.modules.aws_clients.neptune_client._data_parsing import get_multiple_edge_objects_from_traversal
from src.modules.aws_clients.neptune_client._data_parsing import get_multiple_node_objects_from_traversal
from src.modules.aws_clients.neptune_client._data_parsing import get_node_object_from_traversal
from src.modules.aws_clients.neptune_client._data_parsing import get_node_object_from_vertex
from src.modules.aws_clients.neptune_client._neptune_connection import NeptuneConnection
from src.modules.aws_clients.neptune_client._neptune_edge import NeptuneEdge
from src.modules.aws_clients.neptune_client._neptune_node import NeptuneNode
from src.modules.dictionary_utils import dictionary_utils


def retry_on_gremlin_server_error(connections: List[NeptuneConnection | None]):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except GremlinServerError as e:
                logger = logging.getLogger(os.environ['FUNCTION_NAME'])
                self.logger.info("Gremlin Server Error Occurred. Retrying...")
                self.logger.debug(f"Error: {e}")
                for connection in connections:
                    if not connection: continue
                    connection.close_connection()
                    connection.establish_connection()
                result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


class NeptuneClient:
    """
    Note: Multiple calls for functions of a single instance of this class are not thread-safe since it maintains
    a single connection to the Neptune database which doesn't support test_concurrency_utils.
    """

    _read_connection: NeptuneConnection = None
    _write_connection: NeptuneConnection = None

    def __init__(self, read_connection: NeptuneConnection, write_connection: NeptuneConnection):
        self.logger = logging.getLogger(os.environ['FUNCTION_NAME'])
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
        self.logger.info("Connections Established Successfully")

    def _get_read_traversal_source(self):
        return traversal().with_remote(self._read_connection.get_connection())

    def _get_write_traversal_source(self):
        return traversal().with_remote(self._write_connection.get_connection())

    @retry_on_gremlin_server_error(connections=[_read_connection, _write_connection])
    def set_node(self, label: str, properties: Dict, node_id: long | str = None) -> NeptuneNode:
        g = self._get_write_traversal_source()
        t = g.add_v(label)
        if node_id:
            t = t.property(T.id, node_id)
        properties = properties.copy()
        dictionary_utils.ensure_flat(properties)
        for key, value in properties.items():
            t = t.property(key, value)
        new_node = t.next()
        node_object = get_node_object_from_vertex(vertex=new_node)
        return node_object

    @retry_on_gremlin_server_error(connections=[_read_connection, _write_connection])
    def set_edge(self, edge_label: str, from_node: long | str, to_node: long | str, properties: Dict, edge_id: long | str = None) -> NeptuneEdge:
        g = self._get_write_traversal_source()
        t = g.add_e(edge_label).from_(__.V(get_id_in_correct_type(from_node))).to(__.V(to_node))
        if edge_id:
            t = t.property(T.id, get_id_in_correct_type(edge_id))
        properties = properties.copy()
        dictionary_utils.ensure_flat(properties)
        for key, value in properties.items():
            t = t.property(key, value)
        new_edge = t.next()
        edge_object = get_edge_object_from_edge(edge=new_edge)
        return edge_object

    @retry_on_gremlin_server_error(connections=[_read_connection, _write_connection])
    def load_properties_to_node(self, node_id: long | str, properties: Dict):
        g = self._get_write_traversal_source()
        t = g.V(get_id_in_correct_type(node_id))
        properties = properties.copy()
        dictionary_utils.ensure_flat(properties)
        for key, value in properties.items():
            t = t.property(key, value)
        t.next()

    @retry_on_gremlin_server_error(connections=[_read_connection, _write_connection])
    def load_properties_to_edge(self, edge_id: long | str, properties: Dict):
        g = self._get_write_traversal_source()
        t = g.E(get_id_in_correct_type(edge_id))
        properties = properties.copy()
        dictionary_utils.ensure_flat(properties)
        for key, value in properties.items():
            t = t.property(key, value)
        t.next()

    @retry_on_gremlin_server_error(connections=[_read_connection, _write_connection])
    def delete_node_if_exists(self, node_id: long | str):
        g = self._get_write_traversal_source()
        try:
            g.V(get_id_in_correct_type(node_id)).drop().next()
        except StopIteration:
            pass

    @retry_on_gremlin_server_error(connections=[_read_connection, _write_connection])
    def delete_edge_if_exists(self, edge_id: long | str):
        g = self._get_write_traversal_source()
        try:
            g.E(get_id_in_correct_type(edge_id)).drop().next()
        except StopIteration:
            pass

    @retry_on_gremlin_server_error(connections=[_read_connection, _write_connection])
    def get_node_by_id(self, node_id: long | str) -> Optional[NeptuneNode]:
        g = self._get_read_traversal_source()
        try:
            node = g.V(get_id_in_correct_type(node_id))
            node_object = get_node_object_from_traversal(node)
            return node_object
        except StopIteration:
            return None

    @retry_on_gremlin_server_error(connections=[_read_connection, _write_connection])
    def get_edge_by_id(self, edge_id: long | str) -> Optional[NeptuneEdge]:
        g = self._get_read_traversal_source()
        try:
            edge = g.E(get_id_in_correct_type(edge_id))
            edge_object = get_edge_object_from_traversal(edge)
            return edge_object
        except StopIteration:
            return None

    @retry_on_gremlin_server_error(connections=[_read_connection, _write_connection])
    def get_nodes_by_properties(self, properties: Dict, label=None) -> List[NeptuneNode]:
        g = self._get_read_traversal_source()
        t = g.V()
        if label:
            t = t.has_label(label)
        properties = properties.copy()
        dictionary_utils.ensure_flat(properties)
        for key, value in properties.items():
            t = t.has(key, value)
        node_objects = get_multiple_node_objects_from_traversal(traversal=t)
        return node_objects

    @retry_on_gremlin_server_error(connections=[_read_connection, _write_connection])
    def get_edges_by_properties(self, properties: Dict, label=None, from_node: long | str = None, to_node: long | str = None) -> List[NeptuneEdge]:
        g = self._get_read_traversal_source()
        t = g.E()
        properties = properties.copy()
        dictionary_utils.ensure_flat(properties)
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

    @retry_on_gremlin_server_error(connections=[_read_connection, _write_connection])
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
