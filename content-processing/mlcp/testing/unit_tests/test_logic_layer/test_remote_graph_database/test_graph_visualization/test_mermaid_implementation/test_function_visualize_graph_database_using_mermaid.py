import tempfile
import unittest
from unittest.mock import Mock

from logic_layer.remote_graph_database import GraphDatabaseEdge
from logic_layer.remote_graph_database import GraphDatabaseManager
from logic_layer.remote_graph_database import GraphDatabaseNode
from logic_layer.remote_graph_database.graph_visualization._mermaid_implementation import visualize_graph_database_using_mermaid


class TestClassVisualizeGraphDatabaseUsingMermaid(unittest.TestCase):
    ...

    def setUp(self):
        self.nodes = [GraphDatabaseNode(node_id='1', label='Person', properties={'title': 'Bob'}), GraphDatabaseNode(node_id='2', label='Person', properties={'title': 'Alice'}),
                      GraphDatabaseNode(node_id='3', label='Company', properties={'title': 'Google'}), GraphDatabaseNode(node_id='4', label='Company', properties={'title': 'Facebook'}), ]
        self.connections = [GraphDatabaseEdge(edge_id='1', edge_label='Related', properties={}, from_node='1', to_node='2'),
                            GraphDatabaseEdge(edge_id='1', edge_label='Related', properties={}, from_node='2', to_node='1'),
                            GraphDatabaseEdge(edge_id='2', edge_label='Works', properties={}, from_node='1', to_node='3'),
                            GraphDatabaseEdge(edge_id='3', edge_label='Works', properties={}, from_node='2', to_node='4'),
                            GraphDatabaseEdge(edge_id='4', edge_label='Compete', properties={}, from_node='3', to_node='4'),
                            GraphDatabaseEdge(edge_id='4', edge_label='Compete', properties={}, from_node='4', to_node='3'), ]

        self.graph_database_manager = Mock(GraphDatabaseManager)

        self.graph_database_manager.get_nodes_by_properties.return_value = self.nodes
        self.graph_database_manager.get_edges_by_properties.return_value = self.connections

    def test_mermaid_graph_generation(self):
        mermaid_output = ''

        handle, path = tempfile.mkstemp()

        visualize_graph_database_using_mermaid(self.graph_database_manager, path)

        expected_output = ('graph LR\n' \
                           '1(Bob)\n' \
                           '2(Alice)\n' \
                           '3(Google)\n' \
                           '4(Facebook)\n' \
                           '1 --> | Related | 2\n' \
                           '2 --> | Related | 1\n' \
                           '1 --> | Works | 3\n' \
                           '2 --> | Works | 4\n' \
                           '3 --> | Compete | 4\n'
                           '4 --> | Compete | 3\n')

        with open(path, 'r') as f:
            mermaid_output = f.read()

        self.assertEqual(mermaid_output, expected_output)
