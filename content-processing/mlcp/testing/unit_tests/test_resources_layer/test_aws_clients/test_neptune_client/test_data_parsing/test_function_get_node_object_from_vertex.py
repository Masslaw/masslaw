import unittest
from unittest.mock import MagicMock

from gremlin_python.structure.graph import Vertex

from resources_layer.aws_clients.neptune_client._data_parsing import get_node_object_from_vertex


class TestFunctionGetNodeObjectFromVertex(unittest.TestCase):

    def test_valid_vertex(self):
        vertex = Vertex(id=456, label="TestVertex")
        propertyA = MagicMock()
        propertyA.key = "keyA"
        propertyA.value = "valueA"
        propertyB = MagicMock()
        propertyB.key = "keyB"
        propertyB.value = "valueB"
        vertex.properties = [propertyA, propertyB]

        node = get_node_object_from_vertex(vertex)

        self.assertEqual(node.get_id(), 456)
        self.assertEqual(node.get_label(), "TestVertex")
        self.assertEqual(node.get_properties(), {'keyA': 'valueA', 'keyB': 'valueB'})

    def test_no_properties(self):
        vertex = Vertex(id=789, label="NoPropsVertex")

        node = get_node_object_from_vertex(vertex)

        self.assertEqual(node.get_id(), 789)
        self.assertEqual(node.get_label(), "NoPropsVertex")
        self.assertEqual(node.get_properties(), {})
