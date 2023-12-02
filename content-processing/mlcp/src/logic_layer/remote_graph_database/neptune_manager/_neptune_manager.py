from random import randint
from typing import Dict
from typing import List
from typing import Optional

from logic_layer.remote_graph_database._graph_database_edge import GraphDatabaseEdge
from logic_layer.remote_graph_database._graph_database_manager import GraphDatabaseManager
from logic_layer.remote_graph_database._graph_database_node import GraphDatabaseNode
from logic_layer.remote_graph_database.neptune_manager._neptune_data_parsing import parse_raw_neptune_edge_object
from logic_layer.remote_graph_database.neptune_manager._neptune_data_parsing import parse_raw_neptune_node_object
from resources_layer.aws_clients.neptune_client import NeptuneClient
from resources_layer.aws_clients.neptune_client import NeptuneConnection
from shared_layer.mlcp_logger import logger
from shared_layer.mlcp_logger import common_formats


class NeptuneDatabaseManager(GraphDatabaseManager):

    def __init__(self, neptune_read_connection_data: dict, neptune_write_connection_data: dict, subgraph_node_properties: dict = None, subgraph_edge_properties: dict = None, ):
        super().__init__(subgraph_node_properties=subgraph_node_properties, subgraph_edge_properties=subgraph_edge_properties)
        logger.info("Initializing A Neptune Database Manager")
        self._neptune_read_connection_data = neptune_read_connection_data
        self._neptune_write_connection_data = neptune_write_connection_data
        self._neptune_client = None
        self._create_neptune_client()

    @logger.process_function("Creating Neptune Client")
    def _create_neptune_client(self):
        if self._neptune_client: return
        logger.info("Creating Neptune Read Connection")
        logger.debug(f"Neptune Read Connection Data: {common_formats.value(self._neptune_read_connection_data)}")
        read_connection = NeptuneConnection(connection_endpoint=self._neptune_read_connection_data.get("endpoint"), connection_protocol=self._neptune_read_connection_data.get("protocol", "ws"), connection_port=self._neptune_read_connection_data.get("port", 8182),
                                            connection_type=self._neptune_read_connection_data.get("type", "gremlin"), )
        logger.info("Creating Neptune Write Connection")
        logger.debug(f"Neptune Write Connection Data: {common_formats.value(self._neptune_write_connection_data)}")
        write_connection = NeptuneConnection(connection_endpoint=self._neptune_write_connection_data.get("endpoint"), connection_protocol=self._neptune_write_connection_data.get("protocol", "ws"), connection_port=self._neptune_write_connection_data.get("port", 8182),
                                             connection_type=self._neptune_write_connection_data.get("type", "gremlin"), )
        self._neptune_client = NeptuneClient(read_connection=read_connection, write_connection=write_connection)
        logger.positive("Neptune Client Created Successfully")

    def set_node(self, label: str, properties: Dict, node_id: str = None) -> GraphDatabaseNode:
        node_properties = properties.copy()
        node_properties.update(self._subgraph_node_properties)
        new_neptune_node = self._neptune_client.set_node(node_id=node_id, label=label, properties=node_properties)
        new_graph_database_node = parse_raw_neptune_node_object(new_neptune_node)
        return new_graph_database_node

    def set_edge(self, edge_label: str, from_node: str, to_node: str, properties: Dict, edge_id: str = None):
        edge_properties = properties.copy()
        edge_properties.update(self._subgraph_edge_properties)
        new_neptune_edge = self._neptune_client.set_edge(edge_id=edge_id, edge_label=edge_label, from_node=from_node, to_node=to_node, properties=edge_properties)
        new_graph_database_edge = parse_raw_neptune_edge_object(new_neptune_edge)
        return new_graph_database_edge

    def load_properties_to_node(self, node_id: str, properties: Dict):
        properties.update(self._subgraph_node_properties)
        self._neptune_client.load_properties_to_node(node_id=node_id, properties=properties)

    def load_properties_to_edge(self, edge_id: str, properties: Dict):
        properties.update(self._subgraph_edge_properties)
        self._neptune_client.load_properties_to_edge(edge_id=edge_id, properties=properties)

    def delete_node_if_exists(self, node_id: str = None):
        self._neptune_client.delete_node_if_exists(node_id=node_id)

    def delete_edge_if_exists(self, edge_id: str = None):
        self._neptune_client.delete_edge_if_exists(edge_id=edge_id)

    def get_node_by_id(self, node_id: str) -> Optional[GraphDatabaseNode]:
        neptune_node = self._neptune_client.get_node_by_id(node_id=node_id)
        if not neptune_node:
            return None
        graph_node = parse_raw_neptune_node_object(neptune_node)
        return graph_node

    def get_edge_by_id(self, edge_id: str) -> Optional[GraphDatabaseEdge]:
        neptune_edge = self._neptune_client.get_edge_by_id(edge_id=edge_id)
        if not neptune_edge:
            return None
        graph_edge = parse_raw_neptune_edge_object(neptune_edge)
        return graph_edge

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

    def generate_unique_node_id(self) -> str:
        while True:
            node_id = randint(-2147483647, 2147483646)
            if not self.get_node_by_id(node_id):
                return node_id

    def generate_unique_edge_id(self) -> str:
        while True:
            edge_id = randint(-2147483647, 2147483646)
            if not self.get_edge_by_id(edge_id):
                return edge_id

    def get_edges_by_nodes_connection(self, from_node: str = None, to_node: str = None) -> List[GraphDatabaseEdge]:
        neptune_edges = self._neptune_client.get_edges_by_nodes_connection(from_node=from_node, to_node=to_node)
        graph_edges = [parse_raw_neptune_edge_object(neptune_edge) for neptune_edge in neptune_edges]
        return graph_edges
