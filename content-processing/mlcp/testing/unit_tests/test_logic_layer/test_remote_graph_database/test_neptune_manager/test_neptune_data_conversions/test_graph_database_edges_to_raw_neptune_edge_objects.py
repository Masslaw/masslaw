import unittest

from logic_layer.remote_graph_database import GraphDatabaseEdge
from logic_layer.remote_graph_database.neptune_manager._neptune_data_conversions import graph_database_edges_to_raw_neptune_edge_objects
from resources_layer.aws_clients.neptune_client import NeptuneEdge


class TestFunctionGraphDatabaseEdgesToRawNeptuneEdgeObjects(unittest.TestCase):

    def test_convert_on_valid_edge_objects(self):
        database_edge1 = GraphDatabaseEdge('edgeLabel1', 'fromNode1', 'toNode1', {
            'key': 'value'
        }, '123')
        database_edge2 = GraphDatabaseEdge('edgeLabel2', 'fromNode2', 'toNode2', {
            'value': 'key'
        }, '456')
        result = graph_database_edges_to_raw_neptune_edge_objects([database_edge1, database_edge2])

        self.assertIsInstance(result[0], NeptuneEdge)
        self.assertEqual(result[0].get_id(), '123')
        self.assertEqual(result[0].get_label(), 'edgeLabel1')
        self.assertEqual(result[0].get_properties(), {
            'key': 'value'
        })

        self.assertIsInstance(result[1], NeptuneEdge)
        self.assertEqual(result[1].get_id(), '456')
        self.assertEqual(result[1].get_label(), 'edgeLabel2')
        self.assertEqual(result[1].get_properties(), {
            'value': 'key'
        })

    def test_convert_on_edges_with_empty_properties(self):
        database_edge1 = GraphDatabaseEdge('edgeLabel1', 'fromNode1', 'toNode1', {}, '123')
        database_edge2 = GraphDatabaseEdge('edgeLabel2', 'fromNode2', 'toNode2', {}, '456')
        result = graph_database_edges_to_raw_neptune_edge_objects([database_edge1, database_edge2])

        self.assertIsInstance(result[0], NeptuneEdge)
        self.assertEqual(result[0].get_id(), '123')
        self.assertEqual(result[0].get_label(), 'edgeLabel1')
        self.assertEqual(result[0].get_properties(), {})

        self.assertIsInstance(result[1], NeptuneEdge)
        self.assertEqual(result[1].get_id(), '456')
        self.assertEqual(result[1].get_label(), 'edgeLabel2')
        self.assertEqual(result[1].get_properties(), {})

    def test_convert_on_edges_with_multiple_properties(self):
        properties = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': 'value3'
        }
        database_edge1 = GraphDatabaseEdge('edgeLabel1', 'fromNode1', 'toNode1', properties, '123')
        database_edge2 = GraphDatabaseEdge('edgeLabel2', 'fromNode2', 'toNode2', properties, '456')
        result = graph_database_edges_to_raw_neptune_edge_objects([database_edge1, database_edge2])

        self.assertIsInstance(result[0], NeptuneEdge)
        self.assertEqual(result[0].get_id(), '123')
        self.assertEqual(result[0].get_label(), 'edgeLabel1')
        self.assertEqual(result[0].get_properties(), properties)

        self.assertIsInstance(result[1], NeptuneEdge)
        self.assertEqual(result[1].get_id(), '456')
        self.assertEqual(result[1].get_label(), 'edgeLabel2')
        self.assertEqual(result[1].get_properties(), properties)
