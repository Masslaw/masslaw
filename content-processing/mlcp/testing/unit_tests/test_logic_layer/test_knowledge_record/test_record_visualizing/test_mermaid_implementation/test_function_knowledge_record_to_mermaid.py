import unittest
from unittest.mock import patch, mock_open
from logic_layer.knowledge_record._record import KnowledgeRecord
from logic_layer.knowledge_record._entity import KnowledgeRecordEntity
from logic_layer.knowledge_record._connection import KnowledgeRecordConnection
from logic_layer.knowledge_record.record_visualizing._mermaid_implementation import knowledge_record_to_mermaid


class TestFunctionKnowledgeRecordToMermaid(unittest.TestCase):

    def setUp(self):
        self.record = KnowledgeRecord()

        entity1 = KnowledgeRecordEntity()
        entity1.set_id("e1")
        entity1.set_properties({"value": "Entity One"})

        entity2 = KnowledgeRecordEntity()
        entity2.set_id("e2")
        entity2.set_properties({"value": "Entity Two"})

        connection = KnowledgeRecordConnection(label="Related")
        connection.set_from_entity(entity1)
        connection.set_to_entity(entity2)

        self.record.set_entities([entity1, entity2])
        self.record.set_connections([connection])

    @patch("builtins.open", new_callable=mock_open)
    def test_knowledge_record_to_mermaid(self, mock_file):
        knowledge_record_to_mermaid(self.record, 'test.mermaid', lambda e: e.get_properties().get('value', e.get_id()))

        expected_script = (
            "graph LR\n"
            "e1(\"Entity One\")\n"
            "e2(\"Entity Two\")\n"
            "e1 -->|Related| e2\n"
        )

        mock_file().write.assert_called_once_with(expected_script)

    @patch("builtins.open", new_callable=mock_open)
    def test_knowledge_record_to_mermaid_with_untitled(self, mock_file):
        untitled_entities = []
        for entity in self.record.get_entities():
            properties = entity.get_properties()
            del properties['value']
            entity.set_properties(properties)
            untitled_entities.append(entity)
        self.record.set_entities(untitled_entities)

        knowledge_record_to_mermaid(self.record, 'test_untitled.mermaid', lambda e: e.get_properties().get('value', e.get_id()))

        expected_script = (
            "graph LR\n"
            "e1(\"e1\")\n"
            "e2(\"e2\")\n"
            "e1 -->|Related| e2\n"
        )

        mock_file().write.assert_called_once_with(expected_script)
