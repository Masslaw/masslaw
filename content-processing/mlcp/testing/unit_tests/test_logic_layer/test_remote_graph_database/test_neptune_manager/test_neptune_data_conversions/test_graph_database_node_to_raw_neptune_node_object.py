import unittest

from logic_layer.remote_graph_database import GraphDatabaseNode
from logic_layer.remote_graph_database.neptune_manager._neptune_data_conversions import graph_database_node_to_raw_neptune_node_object
from resources_layer.aws_clients.neptune_client import NeptuneNode


class TestFunctionGraphDatabaseNodeToRawNeptuneNodeObject(unittest.TestCase):

    def test_convert_on_valid_node_object(self):
        database_node = GraphDatabaseNode( 'nodeLabel1', {'key': 'value'}, '123')
        result = graph_database_node_to_raw_neptune_node_object(database_node)

        self.assertIsInstance(result, NeptuneNode)
        self.assertEqual(result.get_id(), '123')
        self.assertEqual(result.get_label(), 'nodeLabel1')
        self.assertEqual(result.get_properties(), {'key': 'value'})

    def test_convert_on_node_with_empty_properties(self):
        database_node = GraphDatabaseNode( 'nodeLabel1', {}, '123')
        result = graph_database_node_to_raw_neptune_node_object(database_node)

        self.assertIsInstance(result, NeptuneNode)
        self.assertEqual(result.get_id(), '123')
        self.assertEqual(result.get_label(), 'nodeLabel1')
        self.assertEqual(result.get_properties(), {})

    def test_convert_on_node_with_multiple_properties(self):
        properties = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
        database_node = GraphDatabaseNode( 'nodeLabel1', properties, '123')
        result = graph_database_node_to_raw_neptune_node_object(database_node)

        self.assertIsInstance(result, NeptuneNode)
        self.assertEqual(result.get_id(), '123')
        self.assertEqual(result.get_label(), 'nodeLabel1')
        self.assertEqual(result.get_properties(), properties)
