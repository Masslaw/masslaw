import unittest
from logic_layer.knowledge_record._entity import KnowledgeRecordEntity

class TestClassKnowledgeRecordEntity(unittest.TestCase):

    def setUp(self):
        self.entity = KnowledgeRecordEntity()
        self.sample_properties = {
            "property1": "value1",
            "property2": "value2"
        }
        self.sample_unique_properties = ["property1"]

    def test_init(self):
        self.assertEqual(self.entity.get_id(), '')
        self.assertEqual(self.entity.get_label(), '')
        self.assertEqual(self.entity.get_properties(), {})
        self.assertEqual(self.entity.get_unique_properties(), {})

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

    def test_set_and_get_unique_properties(self):
        self.entity.set_properties(self.sample_properties)
        for prop in self.sample_unique_properties:
            self.entity.set_property_as_unique(prop)
        unique_properties_dict = {key: self.sample_properties[key] for key in self.sample_unique_properties}
        self.assertEqual(self.entity.get_unique_properties(), unique_properties_dict)

    def test_set_property_as_unique_non_existent(self):
        self.entity.set_properties(self.sample_properties)
        self.entity.set_property_as_unique("non_existent")
        self.assertNotIn("non_existent", self.entity.get_properties())
