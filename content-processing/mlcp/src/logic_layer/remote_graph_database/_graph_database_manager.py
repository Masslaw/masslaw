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
    def set_node(self, label: str, properties: Dict, node_id: str = None):
        pass

    @abstractmethod
    def set_edge(self, edge_label: str, from_node: str, to_node: str, properties: Dict, edge_id: str = None):
        pass

    @abstractmethod
    def delete_node_if_exists(self, node_id: str = None):
        pass

    @abstractmethod
    def delete_edge_if_exists(self, edge_id: str = None):
        pass

    @abstractmethod
    def load_properties_to_node(self, node_id: str, properties: Dict):
        pass

    @abstractmethod
    def load_properties_to_edge(self, edge_id: str, properties: Dict):
        pass

    @abstractmethod
    def get_node_by_id(self, node_id: str) -> Optional[GraphDatabaseNode]:
        pass

    @abstractmethod
    def get_edge_by_id(self, edge_id: str) -> Optional[GraphDatabaseEdge]:
        pass

    @abstractmethod
    def get_nodes_by_properties(self, properties: Dict, label=None) -> List[GraphDatabaseNode]:
        pass

    @abstractmethod
    def get_edges_by_properties(self, properties: Dict, label: str = None, from_node: str = None, to_node: str = None) -> List[GraphDatabaseEdge]:
        pass

    @abstractmethod
    def generate_unique_node_id(self) -> str:
        pass

    @abstractmethod
    def generate_unique_edge_id(self) -> str:
        pass

    @abstractmethod
    def get_edges_by_nodes_connection(self, from_node: str = None, to_node: str = None) -> List[GraphDatabaseEdge]:
        pass
