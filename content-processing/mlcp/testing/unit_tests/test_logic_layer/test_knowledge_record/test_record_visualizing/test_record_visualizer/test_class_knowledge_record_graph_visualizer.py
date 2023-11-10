import unittest
import os
import filecmp
from logic_layer.knowledge_record._record import KnowledgeRecord
from logic_layer.knowledge_record._entity import KnowledgeRecordEntity
from logic_layer.knowledge_record.record_visualizing import KnowledgeRecordGraphVisualizer

class TestKnowledgeRecordGraphVisualizer(unittest.TestCase):
    def setUp(self):
        self.record = KnowledgeRecord()
        entity1 = KnowledgeRecordEntity()
        entity1.set_id("e1")
        entity1.set_properties({"value": "Entity One"})
        self.record.set_entities([entity1])

        self.visualizer = KnowledgeRecordGraphVisualizer(self.record)

    def test_visualize_using_mermaid(self):
        output_script_path = "test_mermaid_output.mermaid"
        self.visualizer.visualize_using_mermaid(output_script_path)
        self.assertTrue(os.path.exists(output_script_path))
        os.remove(output_script_path)
