import unittest

from logic_layer.knowledge_record._entity import KnowledgeRecordEntity


class TestClassKnowledgeRecordEntity(unittest.TestCase):

    def setUp(self):
        self.entity = KnowledgeRecordEntity()
        self.sample_properties = {
            "property1": "value1",
            "property2": "value2"
        }

    def test_init(self):
        self.assertEqual(self.entity.get_id(), '')
        self.assertEqual(self.entity.get_label(), '')
        self.assertEqual(self.entity.get_properties(), {})

    def test_set_and_get_id(self):
        self.entity.set_id("test_id")
        self.assertEqual(self.entity.get_id(), "test_id")

    def test_set_and_get_label(self):
        self.entity.set_label("test_label")
        self.assertEqual(self.entity.get_label(), "test_label")

    def test_set_and_get_properties(self):
        self.entity.set_properties(self.sample_properties)
        self.assertEqual(self.entity.get_properties(), self.sample_properties)

    def test_properties_immutable_to_outside_modifications(self):
        properties = self.entity.get_properties()
        properties["newKey"] = "newValue"
        self.assertNotEqual(properties, self.entity.get_properties())
