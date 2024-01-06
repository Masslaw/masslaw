import unittest

from logic_layer.knowledge_record import KnowledgeRecord
from logic_layer.knowledge_record import KnowledgeRecordConnection
from logic_layer.knowledge_record import KnowledgeRecordEntity
from logic_layer.knowledge_record.record_merging import RecordMergingConfiguration
from logic_layer.knowledge_record.record_merging._record_merger import RecordMerger


class TestClassRecordMerger(unittest.TestCase):

    def test_merge_records(self):
        merge_to_record = KnowledgeRecord()
        to_merge_record = KnowledgeRecord()

        entity_to_merge = KnowledgeRecordEntity(entity_id='1', label='Entity1', properties={
            'name': 'John Doe'
        })
        matching_entity = KnowledgeRecordEntity(entity_id='2', label='Entity1', properties={
            'name': 'John Doe'
        })
        non_matching_entity = KnowledgeRecordEntity(entity_id='3', label='Entity2', properties={
            'name': 'Jane Smith'
        })

        merge_to_record.set_entities([matching_entity])
        to_merge_record.set_entities([entity_to_merge, non_matching_entity])

        connection_to_merge_in = KnowledgeRecordConnection(connection_id='c1', label='connection', from_entity=non_matching_entity, to_entity=entity_to_merge)
        connection_to_merge_out = KnowledgeRecordConnection(connection_id='c2', label='connection', from_entity=entity_to_merge, to_entity=non_matching_entity)
        to_merge_record.set_connections([connection_to_merge_in, connection_to_merge_out])

        def entity_mergeability_check_function(e1: KnowledgeRecordEntity, e2: KnowledgeRecordEntity):
            if e1.get_label() != e2.get_label(): return False
            if e1.get_properties().get('name', '') != e2.get_properties().get('name', ''): return False
            return True

        def connection_mergeability_check_function(e1: KnowledgeRecordConnection, e2: KnowledgeRecordConnection):
            if e1.get_label() != e2.get_label(): return False
            if e1.get_properties().get('name', '') != e2.get_properties().get('name', ''): return False
            return True

        merge_configuration = RecordMergingConfiguration(entity_mergeability_check_function, connection_mergeability_check_function)
        merger = RecordMerger(merge_to_record, merge_configuration)
        merger.merge_record(to_merge_record)

        self.assertIn(non_matching_entity, merge_to_record.get_entities())

        self.assertNotIn(entity_to_merge, merge_to_record.get_entities())
