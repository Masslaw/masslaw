import unittest

from logic_layer.knowledge_record import KnowledgeRecord
from logic_layer.knowledge_record import KnowledgeRecordEntity
from logic_layer.knowledge_record._record_compnents_matching._entity_matching import find_matching_entity_in_record


class TestFunctionFindMatchingEntityInRecord(unittest.TestCase):
    def test_find_matching_entity_with_unique_properties(self):
        record = KnowledgeRecord()
        unique_properties = ['name']
        entity_in_record = KnowledgeRecordEntity(entity_id='e1', label='Person', properties={'name': 'Alice'}, unique_properties=unique_properties)
        record.add_entities([entity_in_record])

        matching_entity = KnowledgeRecordEntity(entity_id='e2', label='Person', properties={'name': 'Alice'}, unique_properties=unique_properties)

        found_entity = find_matching_entity_in_record(matching_entity, record)

        self.assertIsNotNone(found_entity)
        self.assertEqual(found_entity.get_id(), entity_in_record.get_id())

    def test_find_matching_entity_with_no_unique_properties_match(self):
        record = KnowledgeRecord()
        unique_properties = ['name']
        entity_in_record = KnowledgeRecordEntity(entity_id='e1', label='Person', properties={'name': 'Alice'}, unique_properties=unique_properties)
        record.add_entities([entity_in_record])

        non_matching_entity = KnowledgeRecordEntity(entity_id='e2', label='Person', properties={'name': 'Bob'}, unique_properties=unique_properties)

        found_entity = find_matching_entity_in_record(non_matching_entity, record)

        self.assertIsNone(found_entity)

    def test_find_matching_entity_with_no_label_match(self):
        record = KnowledgeRecord()
        unique_properties = ['name']
        entity_in_record = KnowledgeRecordEntity(entity_id='e1', label='Person', properties={'name': 'Alice'}, unique_properties=unique_properties)
        record.add_entities([entity_in_record])

        non_matching_entity = KnowledgeRecordEntity(entity_id='e2', label='Employee', properties={'name': 'Alice'}, unique_properties=unique_properties)

        found_entity = find_matching_entity_in_record(non_matching_entity, record)

        self.assertIsNone(found_entity)
