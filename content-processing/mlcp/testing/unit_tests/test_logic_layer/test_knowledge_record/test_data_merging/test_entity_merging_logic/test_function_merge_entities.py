import unittest

from logic_layer.knowledge_record import KnowledgeRecordEntity
from logic_layer.knowledge_record.data_merging._entity_merging_logic import merge_entities


class TestFunctionMergeEntities(unittest.TestCase):
    def test_entity_merging(self):
        entity1 = KnowledgeRecordEntity(entity_id='', label='test', properties={
            'title': 'Adam Douglases', 'appearances': ['Adam did this when', 'Adam said'], 'type': 'person',
        }, unique_properties=['value'], )
        entity2 = KnowledgeRecordEntity(entity_id='123', label='some_label', properties={
            'title': 'Adam', 'appearances': ['Adam Douglases was', 'mr. Adam Douglases loves'], 'type': 'person',
        })

        merge_entities(entity1, entity2)

        self.assertEqual(entity1.get_id(), '123')
        self.assertEqual(entity1.get_label(), 'some_label')
        self.assertEqual(set(entity1.get_properties().get('appearances')), {'Adam said', 'Adam Douglases was', 'mr. Adam Douglases loves', 'Adam did this when'})
        self.assertEqual(entity1.get_properties().get('type'), 'person')
        self.assertEqual(entity1.get_properties().get('title'), 'Adam Douglases')
