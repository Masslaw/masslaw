import unittest

from logic_layer.remote_graph_database import GraphDatabaseNode
from logic_layer.remote_graph_database.neptune_manager._neptune_data_parsing import parse_raw_neptune_node_object
from resources_layer.aws.neptune_client import NeptuneNode


class TestFunctionParseRawNeptuneNodeObject(unittest.TestCase):

    def test_parse_valid_neptune_node_object(self):
        neptune_node = NeptuneNode(123, 'label', {'key': 'value'})
        result = parse_raw_neptune_node_object(neptune_node)

        self.assertIsInstance(result, GraphDatabaseNode)
        self.assertEqual(result.get_id(), '123')
        self.assertEqual(result.get_label(), 'label')
        self.assertEqual(result.get_properties(), {'key': 'value'})

    def test_parse_with_empty_properties(self):
        neptune_node = NeptuneNode(123, 'label', {})
        result = parse_raw_neptune_node_object(neptune_node)

        self.assertIsInstance(result, GraphDatabaseNode)
        self.assertEqual(result.get_id(), '123')
        self.assertEqual(result.get_label(), 'label')
        self.assertEqual(result.get_properties(), {})

    def test_parse_with_multiple_properties(self):
        properties = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
        neptune_node = NeptuneNode(123, 'label', properties)
        result = parse_raw_neptune_node_object(neptune_node)

        self.assertIsInstance(result, GraphDatabaseNode)
        self.assertEqual(result.get_id(), '123')
        self.assertEqual(result.get_label(), 'label')
        self.assertEqual(result.get_properties(), properties)
