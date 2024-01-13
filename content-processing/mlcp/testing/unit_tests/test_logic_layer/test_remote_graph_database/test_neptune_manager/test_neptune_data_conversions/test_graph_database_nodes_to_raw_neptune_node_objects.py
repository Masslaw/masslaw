import unittest

from logic_layer.remote_graph_database import GraphDatabaseNode
from logic_layer.remote_graph_database.neptune_manager._neptune_data_conversions import graph_database_nodes_to_raw_neptune_node_objects
from resources_layer.aws_clients.neptune_client import NeptuneNode


class TestFunctionGraphDatabaseNodesToRawNeptuneNodeObjects(unittest.TestCase):

    def test_convert_on_valid_node_objects(self):
        database_node1 = GraphDatabaseNode('nodeLabel1', {'key': 'value'}, '123')
        database_node2 = GraphDatabaseNode('nodeLabel2',  {'value': 'key'}, '456')
        result = graph_database_nodes_to_raw_neptune_node_objects([database_node1, database_node2])

        self.assertIsInstance(result[0], NeptuneNode)
        self.assertEqual(result[0].get_id(), '123')
        self.assertEqual(result[0].get_label(), 'nodeLabel1')
        self.assertEqual(result[0].get_properties(), {'key': 'value'})

        self.assertIsInstance(result[1], NeptuneNode)
        self.assertEqual(result[1].get_id(), '456')
        self.assertEqual(result[1].get_label(), 'nodeLabel2')
        self.assertEqual(result[1].get_properties(), {'value': 'key'})


    def test_convert_on_nodes_with_empty_properties(self):
        database_node1 = GraphDatabaseNode( 'nodeLabel1', {}, '123')
        database_node2 = GraphDatabaseNode( 'nodeLabel2',  {}, '456')
        result = graph_database_nodes_to_raw_neptune_node_objects([database_node1, database_node2])

        self.assertIsInstance(result[0], NeptuneNode)
        self.assertEqual(result[0].get_id(), '123')
        self.assertEqual(result[0].get_label(), 'nodeLabel1')
        self.assertEqual(result[0].get_properties(), {})

        self.assertIsInstance(result[1], NeptuneNode)
        self.assertEqual(result[1].get_id(), '456')
        self.assertEqual(result[1].get_label(), 'nodeLabel2')
        self.assertEqual(result[1].get_properties(), {})

    def test_convert_on_nodes_with_multiple_properties(self):
        properties = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
        database_node1 = GraphDatabaseNode( 'nodeLabel1', properties, '123')
        database_node2 = GraphDatabaseNode( 'nodeLabel2',  properties, '456')
        result = graph_database_nodes_to_raw_neptune_node_objects([database_node1, database_node2])

        self.assertIsInstance(result[0], NeptuneNode)
        self.assertEqual(result[0].get_id(), '123')
        self.assertEqual(result[0].get_label(), 'nodeLabel1')
        self.assertEqual(result[0].get_properties(), properties)

        self.assertIsInstance(result[1], NeptuneNode)
        self.assertEqual(result[1].get_id(), '456')
        self.assertEqual(result[1].get_label(), 'nodeLabel2')
        self.assertEqual(result[1].get_properties(), properties)
