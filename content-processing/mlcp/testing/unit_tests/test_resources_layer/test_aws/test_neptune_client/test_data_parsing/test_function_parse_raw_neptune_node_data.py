import unittest
from typing import Dict

from resources_layer.aws.neptune_client._data_parsing import parse_raw_neptune_node_data


class TestFunctionParseRawNeptuneNodeData(unittest.TestCase):

    def test_valid_input(self):
        raw_data: Dict = {'id': '123', 'label': 'NodeLabel', 'properties': {'key1': 'value1', 'key2': 'value2'}}
        node = parse_raw_neptune_node_data(raw_data)

        self.assertEqual(node.get_id(), 123)
        self.assertEqual(node.get_label(), 'NodeLabel')
        self.assertEqual(node.get_properties(), {'key1': 'value1', 'key2': 'value2'})

    def test_missing_id(self):
        raw_data: Dict = {'label': 'NodeLabel', 'properties': {'key1': 'value1', 'key2': 'value2'}}
        with self.assertRaises(KeyError):
            parse_raw_neptune_node_data(raw_data)

    def test_missing_label(self):
        raw_data: Dict = {'id': '123', 'properties': {'key1': 'value1', 'key2': 'value2'}}
        with self.assertRaises(KeyError):
            parse_raw_neptune_node_data(raw_data)

    def test_missing_properties(self):
        raw_data: Dict = {'id': '123', 'label': 'NodeLabel', }
        node = parse_raw_neptune_node_data(raw_data)
        self.assertEqual(node.get_id(), 123)
        self.assertEqual(node.get_label(), 'NodeLabel')
        self.assertEqual(node.get_properties(), {})
