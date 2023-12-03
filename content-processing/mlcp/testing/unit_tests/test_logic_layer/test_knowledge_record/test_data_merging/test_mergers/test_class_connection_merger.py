import unittest

from logic_layer.knowledge_record import KnowledgeRecordConnection
from logic_layer.knowledge_record import KnowledgeRecordEntity
from logic_layer.knowledge_record.data_merging import ConnectionMerger


class TestClassConnectionMerger(unittest.TestCase):

    def test_connection_merging(self):
        connection1 = KnowledgeRecordConnection(connection_id='', label='test', properties={
            'title': 'Adam Douglases', 'appearances': ['Adam did this when', 'Adam said'], 'type': 'person',
        }, unique_properties=['value'], )
        connection2 = KnowledgeRecordConnection(connection_id='123', label='some_label', properties={
            'title': 'Adam', 'appearances': ['Adam Douglases was', 'mr. Adam Douglases loves'], 'type': 'person',
        }, from_entity=KnowledgeRecordEntity(), to_entity=KnowledgeRecordEntity(), )

        merger = ConnectionMerger(target_connection=connection1)
        merger.merge_data_from_another_connection(another_connection=connection2)

        self.assertEqual(connection1.get_id(), '123')
        self.assertEqual(connection1.get_label(), 'some_label')
        self.assertEqual(set(connection1.get_properties().get('appearances')), {'Adam said', 'Adam Douglases was', 'mr. Adam Douglases loves', 'Adam did this when'})
        self.assertEqual(connection1.get_properties().get('type'), 'person')
        self.assertEqual(connection1.get_properties().get('title'), 'Adam Douglases')
