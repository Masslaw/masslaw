from typing import IO

from logic_layer.remote_graph_database._graph_database_manager import GraphDatabaseManager
from logic_layer.remote_graph_database.graph_visualization._matplotlib_implementation import visualize_graph_database_using_matplotlib
from logic_layer.remote_graph_database.graph_visualization._mermaid_implementation import visualize_graph_database_using_mermaid


class GraphDatabaseVisualizer:

    def __init__(self, graph_database_manager: GraphDatabaseManager):
        self._graph_database_manager = graph_database_manager

    def visualize_database_content_using_mermaid(self, output_file: str, node_title_property: str = 'title'):
        visualize_graph_database_using_mermaid(self._graph_database_manager, output_file, node_title_property)

    def visualize_database_content_using_matplotlib(self, output_file: str, node_title_property: str = 'title'):
        visualize_graph_database_using_matplotlib(self._graph_database_manager, output_file, node_title_property)
