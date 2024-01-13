import unittest

from logic_layer.remote_graph_database import GraphDatabaseEdge
from logic_layer.remote_graph_database.neptune_manager._neptune_data_conversions import parse_raw_neptune_edge_objects
from resources_layer.aws_clients.neptune_client import NeptuneEdge


class TestFunctionParseRawNeptuneEdgeObject(unittest.TestCase):

    def test_parse_valid_neptune_edge_object(self):
        neptune_edge1 = NeptuneEdge('edgeLabel1', 'fromNode1', 'toNode1', {'key': 'value'}, 123)
        neptune_edge2 = NeptuneEdge('edgeLabel2', 'fromNode2', 'toNode2', {'value': 'key'}, 456)
        result = parse_raw_neptune_edge_objects([neptune_edge1, neptune_edge2])

        self.assertIsInstance(result[0], GraphDatabaseEdge)
        self.assertEqual(result[0].get_id(), '123')
        self.assertEqual(result[0].get_label(), 'edgeLabel1')
        self.assertEqual(result[0].get_from_node(), 'fromNode1')
        self.assertEqual(result[0].get_to_node(), 'toNode1')
        self.assertEqual(result[0].get_properties(), {'key': 'value'})

        self.assertIsInstance(result[1], GraphDatabaseEdge)
        self.assertEqual(result[1].get_id(), '456')
        self.assertEqual(result[1].get_label(), 'edgeLabel2')
        self.assertEqual(result[1].get_from_node(), 'fromNode2')
        self.assertEqual(result[1].get_to_node(), 'toNode2')
        self.assertEqual(result[1].get_properties(), {'value': 'key'})

    def test_parse_edge_with_empty_properties(self):
        neptune_edge1 = NeptuneEdge('edgeLabel1', 'fromNode1', 'toNode1', {}, 123)
        neptune_edge2 = NeptuneEdge('edgeLabel2', 'fromNode2', 'toNode2', {}, 456)
        result = parse_raw_neptune_edge_objects([neptune_edge1, neptune_edge2])

        self.assertIsInstance(result[0], GraphDatabaseEdge)
        self.assertEqual(result[0].get_id(), '123')
        self.assertEqual(result[0].get_label(), 'edgeLabel1')
        self.assertEqual(result[0].get_from_node(), 'fromNode1')
        self.assertEqual(result[0].get_to_node(), 'toNode1')
        self.assertEqual(result[0].get_properties(), {})

        self.assertIsInstance(result[1], GraphDatabaseEdge)
        self.assertEqual(result[1].get_id(), '456')
        self.assertEqual(result[1].get_label(), 'edgeLabel2')
        self.assertEqual(result[1].get_from_node(), 'fromNode2')
        self.assertEqual(result[1].get_to_node(), 'toNode2')
        self.assertEqual(result[1].get_properties(), {})



    def test_parse_edge_with_multiple_properties(self):
        properties = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
        neptune_edge1 = NeptuneEdge('edgeLabel1', 'fromNode1', 'toNode1', properties, 123)
        neptune_edge2 = NeptuneEdge('edgeLabel2', 'fromNode2', 'toNode2', properties, 456)
        result = parse_raw_neptune_edge_objects([neptune_edge1, neptune_edge2])

        self.assertIsInstance(result[0], GraphDatabaseEdge)
        self.assertEqual(result[0].get_id(), '123')
        self.assertEqual(result[0].get_label(), 'edgeLabel1')
        self.assertEqual(result[0].get_from_node(), 'fromNode1')
        self.assertEqual(result[0].get_to_node(), 'toNode1')
        self.assertEqual(result[0].get_properties(), properties)

        self.assertIsInstance(result[1], GraphDatabaseEdge)
        self.assertEqual(result[1].get_id(), '456')
        self.assertEqual(result[1].get_label(), 'edgeLabel2')
        self.assertEqual(result[1].get_from_node(), 'fromNode2')
        self.assertEqual(result[1].get_to_node(), 'toNode2')
        self.assertEqual(result[1].get_properties(), properties)
