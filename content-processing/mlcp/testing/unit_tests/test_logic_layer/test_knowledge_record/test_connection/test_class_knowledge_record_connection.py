import unittest

from logic_layer.knowledge_record._connection import KnowledgeRecordConnection
from logic_layer.knowledge_record._entity import KnowledgeRecordEntity


class TestClassKnowledgeRecordConnection(unittest.TestCase):

    def setUp(self):
        self.connection = KnowledgeRecordConnection()
        self.entity1 = KnowledgeRecordEntity(entity_id='entity1')
        self.entity2 = KnowledgeRecordEntity(entity_id='entity2')
        self.sample_properties = {
            "prop1": "value1",
            "prop2": "value2"
        }

    def test_set_and_get_id(self):
        self.connection.set_id("test_id")
        self.assertEqual(self.connection.get_id(), "test_id")

    def test_set_and_get_label(self):
        self.connection.set_label("test_label")
        self.assertEqual(self.connection.get_label(), "test_label")

    def test_set_and_get_from_entity(self):
        self.connection.set_from_entity(self.entity1)
        self.assertEqual(self.connection.get_from_entity(), self.entity1)

    def test_set_and_get_to_entity(self):
        self.connection.set_to_entity(self.entity2)
        self.assertEqual(self.connection.get_to_entity(), self.entity2)

    def test_set_and_get_properties(self):
        self.connection.set_properties(self.sample_properties)
        self.assertEqual(self.connection.get_properties(), self.sample_properties)

    def test_properties_immutable_to_outside_modifications(self):
        properties = self.connection.get_properties()
        properties["newKey"] = "newValue"
        self.assertNotEqual(properties, self.connection.get_properties())
