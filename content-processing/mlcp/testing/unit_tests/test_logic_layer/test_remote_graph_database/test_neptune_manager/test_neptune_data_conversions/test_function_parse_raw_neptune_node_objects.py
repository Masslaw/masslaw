import unittest

from logic_layer.remote_graph_database import GraphDatabaseNode
from logic_layer.remote_graph_database.neptune_manager._neptune_data_conversions import parse_raw_neptune_node_objects
from resources_layer.aws_clients.neptune_client import NeptuneNode


class TestFunctionParseRawNeptuneNodeObject(unittest.TestCase):

    def test_parse_valid_neptune_node_object(self):
        neptune_node1 = NeptuneNode('label1', {
            'key1': 'value1'
        }, 123)
        neptune_node2 = NeptuneNode('label2', {
            'key2': 'value2'
        }, 456)
        result = parse_raw_neptune_node_objects([neptune_node1, neptune_node2])

        self.assertIsInstance(result[0], GraphDatabaseNode)
        self.assertEqual(result[0].get_id(), '123')
        self.assertEqual(result[0].get_label(), 'label1')
        self.assertEqual(result[0].get_properties(), {
            'key1': 'value1'
        })

    def test_parse_with_empty_properties(self):
        neptune_node1 = NeptuneNode('label1', {}, 123)
        neptune_node2 = NeptuneNode('label2', {}, 456)
        result = parse_raw_neptune_node_objects([neptune_node1, neptune_node2])

        self.assertIsInstance(result[0], GraphDatabaseNode)
        self.assertEqual(result[0].get_id(), '123')
        self.assertEqual(result[0].get_label(), 'label1')
        self.assertEqual(result[0].get_properties(), {})

        self.assertIsInstance(result[1], GraphDatabaseNode)
        self.assertEqual(result[1].get_id(), '456')
        self.assertEqual(result[1].get_label(), 'label2')
        self.assertEqual(result[1].get_properties(), {})

    def test_parse_with_multiple_properties(self):
        properties = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': 'value3'
        }
        neptune_node1 = NeptuneNode('label1', properties, 123)
        neptune_node2 = NeptuneNode('label2', properties, 456)
        result = parse_raw_neptune_node_objects([neptune_node1, neptune_node2])

        self.assertIsInstance(result[0], GraphDatabaseNode)
        self.assertEqual(result[0].get_id(), '123')
        self.assertEqual(result[0].get_label(), 'label1')
        self.assertEqual(result[0].get_properties(), properties)

        self.assertIsInstance(result[1], GraphDatabaseNode)
        self.assertEqual(result[1].get_id(), '456')
        self.assertEqual(result[1].get_label(), 'label2')
        self.assertEqual(result[1].get_properties(), properties)
