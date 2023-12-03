import unittest

from logic_layer.knowledge_record import KnowledgeRecordEntity
from logic_layer.knowledge_record.data_merging import EntityMerger


class TestClassEntityMerger(unittest.TestCase):

    def test_entity_merging(self):
        entity1 = KnowledgeRecordEntity(entity_id='', label='test', properties={
            'title': 'Adam Douglases', 'appearances': ['Adam did this when', 'Adam said'], 'type': 'person',
        }, unique_properties=['value'], )
        entity2 = KnowledgeRecordEntity(entity_id='123', label='some_label', properties={
            'title': 'Adam', 'appearances': ['Adam Douglases was', 'mr. Adam Douglases loves'], 'type': 'person',
        })

        merger = EntityMerger(target_entity=entity1)
        merger.merge_data_from_another_entity(another_entity=entity2)

        self.assertEqual(entity1.get_id(), '123')
        self.assertEqual(entity1.get_label(), 'some_label')
        self.assertEqual(set(entity1.get_properties().get('appearances')), {'Adam said', 'Adam Douglases was', 'mr. Adam Douglases loves', 'Adam did this when'})
        self.assertEqual(entity1.get_properties().get('type'), 'person')
        self.assertEqual(entity1.get_properties().get('title'), 'Adam Douglases')
