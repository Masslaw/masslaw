import unittest

from logic_layer.knowledge_record import KnowledgeRecord
from logic_layer.knowledge_record import KnowledgeRecordConnection
from logic_layer.knowledge_record import KnowledgeRecordEntity
from logic_layer.knowledge_record.data_merging._mergers import RecordMerger


class TestClassRecordMerger(unittest.TestCase):

    def test_merge_records(self):
        merge_to_record = KnowledgeRecord()
        to_merge_record = KnowledgeRecord()

        entity_to_merge = KnowledgeRecordEntity(entity_id='1', label='Entity1', properties={'name': 'John Doe'}, unique_properties=['name'])
        matching_entity = KnowledgeRecordEntity(entity_id='2', label='Entity1', properties={'name': 'John Doe'}, unique_properties=['name'])
        non_matching_entity = KnowledgeRecordEntity(entity_id='3', label='Entity2', properties={'name': 'Jane Smith'}, unique_properties=['name'])

        merge_to_record.set_entities([matching_entity])
        to_merge_record.set_entities([entity_to_merge, non_matching_entity])

        connection_to_merge_in = KnowledgeRecordConnection(connection_id='c1', label='connection', from_entity=non_matching_entity, to_entity=entity_to_merge)
        connection_to_merge_out = KnowledgeRecordConnection(connection_id='c2', label='connection', from_entity=entity_to_merge, to_entity=non_matching_entity)
        to_merge_record.set_connections([connection_to_merge_in, connection_to_merge_out])

        merger = RecordMerger(merge_to_record)
        merger.merge_entities_from_another_record(to_merge_record)

        self.assertIn(non_matching_entity, merge_to_record.get_entities())

        self.assertNotIn(entity_to_merge, merge_to_record.get_entities())

        for connection in merge_to_record.get_connections():
            if connection.get_to_entity() == entity_to_merge:
                self.assertEqual(connection.get_to_entity(), matching_entity)
            if connection.get_from_entity() == entity_to_merge:
                self.assertEqual(connection.get_from_entity(), matching_entity)
