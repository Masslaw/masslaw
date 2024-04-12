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
                logger = logging.getLogger()
                logger.info("Gremlin Server Error Occurred. Retrying...")
                logger.debug(f"Error: {e}")
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
        self._read_connection = read_connection
        self._write_connection = write_connection
        self.establish_connections()

    def close_connection(self):
        self._read_connection.close_connection()
        self._write_connection.close_connection()

    def establish_connections(self):
        self._read_connection.establish_connection()
        self._write_connection.establish_connection()
        logging.getLogger().info("Connections Established Successfully")

    def _get_read_traversal_source(self):
        return traversal().with_remote(self._read_connection.get_connection())

    def _get_write_traversal_source(self):
        return traversal().with_remote(self._write_connection.get_connection())

    def set_nodes(self, nodes: List[NeptuneNode]) -> List[NeptuneNode]:
        new_nodes = []
        for node in nodes:
            node_object = self._set_node(node)
            new_nodes.append(node_object or NeptuneNode('', {}))
        return new_nodes

    def _set_node(self, node: NeptuneNode) -> NeptuneNode:
        node_id = node.get_id()
        label = node.get_label()
        properties = node.get_properties()
        g = self._get_write_traversal_source()
        t = g.add_v(label)
        if node_id: t = t.property(T.id, node_id)
        properties = properties.copy()
        dictionary_utils.ensure_flat(properties)
        for key, value in properties.items(): t = t.property(key, value)
        try:
            new_node = t.next()
            node_object = get_node_object_from_vertex(vertex=new_node)
        except GremlinServerError as e:
            node_object = node
        return node_object or node

    def set_edges(self, edges: List[NeptuneEdge]) -> List[NeptuneEdge]:
        new_edges = []
        for edge in edges:
            edge_object = self._set_edge(edge)
            new_edges.append(edge_object)
        return new_edges

    def _set_edge(self, edge: NeptuneEdge) -> NeptuneEdge:
        edge_id = edge.get_id()
        edge_label = edge.get_label()
        from_node = edge.get_from_node()
        to_node = edge.get_to_node()
        properties = edge.get_properties()
        if not from_node or not to_node: return edge
        g = self._get_write_traversal_source()
        t = g.add_e(edge_label).from_(__.V(get_id_in_correct_type(from_node))).to(__.V(to_node))
        if edge_id: t = t.property(T.id, get_id_in_correct_type(edge_id))
        properties = properties.copy()
        dictionary_utils.ensure_flat(properties)
        for key, value in properties.items(): t = t.property(key, value)
        try:
            new_edge = t.next()
            edge_object = get_edge_object_from_edge(edge=new_edge)
        except GremlinServerError as e:
            edge_object = edge
        return edge_object or edge

    def load_properties_to_nodes(self, node_properties: Dict[long | str, Dict]):
        for node_id, properties in node_properties.items():
            print(node_id)
            print(properties)
            g = self._get_write_traversal_source()
            t = g.V(get_id_in_correct_type(node_id))
            properties = properties.copy()
            dictionary_utils.ensure_flat(properties)
            for key, value in properties.items(): t = t.property(key, value)
            t.iterate()

    def load_properties_to_edges(self, edge_properties: Dict[long | str, Dict]):
        for edge_id, properties in edge_properties.items():
            g = self._get_write_traversal_source()
            t = g.E(get_id_in_correct_type(edge_id))
            properties = properties.copy()
            dictionary_utils.ensure_flat(properties)
            for key, value in properties.items(): t = t.property(key, value)
            t.iterate()

    def delete_nodes_if_exist(self, node_ids: List[long | str]):
        g = self._get_write_traversal_source()
        corrected_ids = [get_id_in_correct_type(node_id) for node_id in node_ids]
        corrected_ids = [node_id for node_id in corrected_ids if node_id]
        try:
            g.V(corrected_ids).drop().iterate()
        except StopIteration:
            pass

    def delete_edges_if_exist(self, edge_ids: List[long | str]):
        g = self._get_write_traversal_source()
        corrected_ids = [get_id_in_correct_type(edge_id) for edge_id in edge_ids]
        corrected_ids = [edge_id for edge_id in corrected_ids if edge_id]
        logger.debug(f"Deleting edges with ids: {common_formats.value(corrected_ids)}")
        try:
            g.E(corrected_ids).drop().iterate()
        except StopIteration:
            pass

    def get_nodes_by_ids(self, node_ids: List[long | str]) -> List[NeptuneNode]:
        nodes = []
        for node_id in node_ids:
            g = self._get_read_traversal_source()
            try:
                node = g.V(get_id_in_correct_type(node_id))
                node_object = get_node_object_from_traversal(node)
                nodes.append(node_object)
            except StopIteration:
                nodes.append(None)
        return nodes

    def get_edges_by_ids(self, edge_ids: List[long | str]) -> List[NeptuneEdge]:
        edges = []
        for edge_id in edge_ids:
            g = self._get_read_traversal_source()
            try:
                edge = g.E(get_id_in_correct_type(edge_id))
                edge_object = get_edge_object_from_traversal(edge)
                edges.append(edge_object)
            except StopIteration:
                edges.append(None)
        return edges


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
