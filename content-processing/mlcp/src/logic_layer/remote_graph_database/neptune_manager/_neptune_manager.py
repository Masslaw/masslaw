from typing import Dict
from typing import List

from logic_layer.remote_graph_database._graph_database_edge import GraphDatabaseEdge
from logic_layer.remote_graph_database._graph_database_manager import GraphDatabaseManager
from logic_layer.remote_graph_database._graph_database_node import GraphDatabaseNode
from logic_layer.remote_graph_database.neptune_manager._neptune_data_conversions import graph_database_edge_to_raw_neptune_edge_object
from logic_layer.remote_graph_database.neptune_manager._neptune_data_conversions import graph_database_node_to_raw_neptune_node_object
from logic_layer.remote_graph_database.neptune_manager._neptune_data_conversions import parse_raw_neptune_edge_object
from logic_layer.remote_graph_database.neptune_manager._neptune_data_conversions import parse_raw_neptune_edge_objects
from logic_layer.remote_graph_database.neptune_manager._neptune_data_conversions import parse_raw_neptune_node_object
from logic_layer.remote_graph_database.neptune_manager._neptune_data_conversions import parse_raw_neptune_node_objects
from resources_layer.aws_clients.neptune_client import NeptuneClient
from resources_layer.aws_clients.neptune_client import NeptuneConnection
from shared_layer.mlcp_logger import common_formats
from shared_layer.mlcp_logger import logger


class NeptuneDatabaseManager(GraphDatabaseManager):

    def __init__(self, neptune_read_connection_data: dict, neptune_write_connection_data: dict, subgraph_node_properties: dict = None, subgraph_edge_properties: dict = None, ):
        super().__init__(subgraph_node_properties=subgraph_node_properties, subgraph_edge_properties=subgraph_edge_properties)
        logger.info("Initializing A Neptune Database Manager")
        self._neptune_read_connection_data = neptune_read_connection_data
        self._neptune_write_connection_data = neptune_write_connection_data
        self._neptune_client: NeptuneClient = self._create_neptune_client()

    @logger.process_function("Creating Neptune Client")
    def _create_neptune_client(self):
        logger.info("Creating Neptune Read Connection")
        logger.debug(f"Neptune Read Connection Data: {common_formats.value(self._neptune_read_connection_data)}")
        read_connection = NeptuneConnection(connection_endpoint=self._neptune_read_connection_data.get("endpoint"), connection_protocol=self._neptune_read_connection_data.get("protocol", "ws"), connection_port=self._neptune_read_connection_data.get("port", 8182),
                                            connection_type=self._neptune_read_connection_data.get("type", "gremlin"), )
        logger.info("Creating Neptune Write Connection")
        logger.debug(f"Neptune Write Connection Data: {common_formats.value(self._neptune_write_connection_data)}")
        write_connection = NeptuneConnection(connection_endpoint=self._neptune_write_connection_data.get("endpoint"), connection_protocol=self._neptune_write_connection_data.get("protocol", "ws"), connection_port=self._neptune_write_connection_data.get("port", 8182),
                                             connection_type=self._neptune_write_connection_data.get("type", "gremlin"), )
        client = NeptuneClient(read_connection=read_connection, write_connection=write_connection)
        logger.positive("Neptune Client Created Successfully")
        return client

    def set_nodes(self, nodes: List[GraphDatabaseNode]) -> List[GraphDatabaseNode]:
        neptune_nodes = []
        for node in nodes.copy():
            node_properties = node.get_properties()
            node_properties.update(self._subgraph_node_properties)
            node.set_properties(node_properties)
            neptune_node = graph_database_node_to_raw_neptune_node_object(node)
            neptune_nodes.append(neptune_node)
        new_neptune_nodes = self._neptune_client.set_nodes(neptune_nodes)
        new_graph_database_nodes = parse_raw_neptune_node_objects(new_neptune_nodes)
        return new_graph_database_nodes

    def set_edges(self, edges: List[GraphDatabaseEdge]) -> List[GraphDatabaseEdge]:
        neptune_edges = []
        for edge in edges.copy():
            edge_properties = edge.get_properties()
            edge_properties.update(self._subgraph_edge_properties)
            edge.set_properties(edge_properties)
            neptune_edge = graph_database_edge_to_raw_neptune_edge_object(edge)
            neptune_edges.append(neptune_edge)
        new_neptune_edges = self._neptune_client.set_edges(neptune_edges)
        new_graph_database_edges = parse_raw_neptune_edge_objects(new_neptune_edges)
        return new_graph_database_edges

    def load_properties_to_nodes(self, node_properties: Dict[str, dict]):
        for node_id, properties in node_properties.items(): properties.update(self._subgraph_node_properties)
        self._neptune_client.load_properties_to_nodes(node_properties=node_properties)

    def load_properties_to_edges(self, edge_properties: Dict[str, dict]):
        for edge_id, properties in edge_properties.items(): properties.update(self._subgraph_edge_properties)
        self._neptune_client.load_properties_to_edges(edge_properties=edge_properties)

    def delete_nodes_if_exist(self, node_ids: List[str]):
        self._neptune_client.delete_nodes_if_exist(node_ids)

    def delete_edges_if_exist(self, edge_ids: List[str]):
        self._neptune_client.delete_edges_if_exist(edge_ids)

    def get_nodes_by_ids(self, node_ids: List[str]) -> List[GraphDatabaseNode]:
        neptune_nodes = self._neptune_client.get_nodes_by_ids(node_ids)
        graph_nodes = parse_raw_neptune_node_objects(neptune_nodes)
        return graph_nodes

    def get_edges_by_ids(self, edge_ids: List[str]) -> List[GraphDatabaseEdge]:
        neptune_edges = self._neptune_client.get_edges_by_ids(edge_ids)
        graph_edges = parse_raw_neptune_edge_objects(neptune_edges)
        return graph_edges

    def get_nodes_by_properties(self, properties: Dict, label=None) -> List[GraphDatabaseNode]:
        query_properties = properties.copy()
        query_properties.update(self._subgraph_node_properties)
        neptune_nodes = self._neptune_client.get_nodes_by_properties(properties=query_properties, label=label)
        graph_nodes = [parse_raw_neptune_node_object(neptune_node) for neptune_node in neptune_nodes]
        return graph_nodes

    def get_edges_by_properties(self, properties: Dict, label=None, from_node=None, to_node=None) -> List[GraphDatabaseEdge]:
        query_properties = properties.copy()
        query_properties.update(self._subgraph_edge_properties)
        neptune_edges = self._neptune_client.get_edges_by_properties(properties=query_properties, label=label, from_node=from_node, to_node=to_node)
        graph_edges = [parse_raw_neptune_edge_object(neptune_edge) for neptune_edge in neptune_edges]
        return graph_edges

    def get_edges_by_nodes_connection(self, from_node: str = None, to_node: str = None) -> List[GraphDatabaseEdge]:
        neptune_edges = self._neptune_client.get_edges_by_nodes_connection(from_node=from_node, to_node=to_node)
        graph_edges = [parse_raw_neptune_edge_object(neptune_edge) for neptune_edge in neptune_edges]
        return graph_edges
