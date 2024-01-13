import unittest

from logic_layer.remote_graph_database import GraphDatabaseEdge
from logic_layer.remote_graph_database.neptune_manager._neptune_data_conversions import graph_database_edge_to_raw_neptune_edge_object
from resources_layer.aws_clients.neptune_client import NeptuneEdge


class TestFunctionGraphDatabaseEdgeToRawNeptuneEdgeObject(unittest.TestCase):

    def test_convert_on_valid_edge_object(self):
        database_edge = GraphDatabaseEdge('edgeLabel1', 'fromEdge1', 'toEdge1', {
            'key': 'value'
        }, '123')
        result = graph_database_edge_to_raw_neptune_edge_object(database_edge)

        self.assertIsInstance(result, NeptuneEdge)
        self.assertEqual(result.get_id(), '123')
        self.assertEqual(result.get_label(), 'edgeLabel1')
        self.assertEqual(result.get_properties(), {
            'key': 'value'
        })

    def test_convert_on_edge_with_empty_properties(self):
        database_edge = GraphDatabaseEdge('edgeLabel1', 'fromEdge1', 'toEdge1', {}, '123')
        result = graph_database_edge_to_raw_neptune_edge_object(database_edge)

        self.assertIsInstance(result, NeptuneEdge)
        self.assertEqual(result.get_id(), '123')
        self.assertEqual(result.get_label(), 'edgeLabel1')
        self.assertEqual(result.get_properties(), {})

    def test_convert_on_edge_with_multiple_properties(self):
        properties = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': 'value3'
        }
        database_edge = GraphDatabaseEdge('edgeLabel1', 'fromEdge1', 'toEdge1', properties, '123')
        result = graph_database_edge_to_raw_neptune_edge_object(database_edge)

        self.assertIsInstance(result, NeptuneEdge)
        self.assertEqual(result.get_id(), '123')
        self.assertEqual(result.get_label(), 'edgeLabel1')
        self.assertEqual(result.get_properties(), properties)
