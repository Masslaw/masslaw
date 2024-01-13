import traceback
from abc import abstractmethod
from typing import Dict
from typing import List
from typing import Optional

from logic_layer.remote_graph_database._graph_database_edge import GraphDatabaseEdge
from logic_layer.remote_graph_database._graph_database_node import GraphDatabaseNode
from shared_layer.mlcp_logger import logger


class GraphDatabaseManager:

    def __init__(self, subgraph_node_properties: Dict = None, subgraph_edge_properties: Dict = None):
        logger.info("Creating a graph database manager")
        self._subgraph_node_properties = subgraph_node_properties or {}
        self._subgraph_edge_properties = subgraph_edge_properties or {}

    def get_subgraph_node_properties(self):
        return self._subgraph_node_properties.copy()

    def get_subgraph_edge_properties(self):
        return self._subgraph_edge_properties.copy()

    @abstractmethod
    def set_nodes(self, nodes: List[GraphDatabaseNode]) -> List[GraphDatabaseNode]:
        pass

    @abstractmethod
    def set_edges(self, edges: List[GraphDatabaseEdge]) -> List[GraphDatabaseEdge]:
        pass

    @abstractmethod
    def delete_nodes_if_exist(self, node_ids: List[str]):
        pass

    @abstractmethod
    def delete_edges_if_exist(self, edge_ids: List[str]):
        pass

    @abstractmethod
    def load_properties_to_nodes(self, node_properties: Dict[str, Dict]):
        pass

    @abstractmethod
    def load_properties_to_edges(self, edge_properties: Dict[str, Dict]):
        pass

    @abstractmethod
    def get_nodes_by_ids(self, node_ids: List[str]) -> List[GraphDatabaseNode]:
        pass

    @abstractmethod
    def get_edges_by_ids(self, edge_ids: List[str]) -> List[GraphDatabaseEdge]:
        pass

    @abstractmethod
    def get_nodes_by_properties(self, properties: Dict, label=None) -> List[GraphDatabaseNode]:
        pass

    @abstractmethod
    def get_edges_by_properties(self, properties: Dict, label: str = None, from_node: str = None, to_node: str = None) -> List[GraphDatabaseEdge]:
        pass

    @abstractmethod
    def get_edges_by_nodes_connection(self, from_node: str = None, to_node: str = None) -> List[GraphDatabaseEdge]:
        pass
