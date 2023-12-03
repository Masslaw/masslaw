import unittest

from logic_layer.knowledge_record.data_merging._connection_merging_logic import merge_connection_properties


class TestFunctionMergeConnectionProperties(unittest.TestCase):

    def test_merge_connection_properties_with_unique_property(self):
        connection1_properties = {'title': 'Adam Douglases'}
        connection2_properties = {'title': 'Adam'}
        merged_properties = merge_connection_properties(connection1_properties=connection1_properties, connection2_properties=connection2_properties)
        self.assertEqual(merged_properties.get('title'), 'Adam Douglases')
        merged_properties = merge_connection_properties(connection1_properties=connection2_properties, connection2_properties=connection1_properties)
        self.assertEqual(merged_properties.get('title'), 'Adam Douglases')

    def test_merge_connection_properties_with_non_unique_property(self):
        connection1_properties = {'type': 'person'}
        connection2_properties = {'type': 'person'}
        merged_properties = merge_connection_properties(connection1_properties=connection1_properties, connection2_properties=connection2_properties)
        self.assertEqual(merged_properties.get('type'), 'person')
        merged_properties = merge_connection_properties(connection1_properties=connection2_properties, connection2_properties=connection1_properties)
        self.assertEqual(merged_properties.get('type'), 'person')

    def test_merge_connection_properties_with_list_property(self):
        connection1_properties = {'appearances': ['Adam did this when', 'Adam said']}
        connection2_properties = {'appearances': ['Adam Douglases was', 'mr. Adam Douglases loves']}
        merged_properties = merge_connection_properties(connection1_properties=connection1_properties, connection2_properties=connection2_properties)
        self.assertEqual(set(merged_properties.get('appearances')), {'Adam said', 'Adam Douglases was', 'mr. Adam Douglases loves', 'Adam did this when'})
        merged_properties = merge_connection_properties(connection1_properties=connection2_properties, connection2_properties=connection1_properties)
        self.assertEqual(set(merged_properties.get('appearances')), {'Adam said', 'Adam Douglases was', 'mr. Adam Douglases loves', 'Adam did this when'})

    def test_merge_connection_properties_with_dict_property(self):
        connection1_properties = {'title': {'name': 'Adam Douglases'}}
        connection2_properties = {'title': {'name': 'Adam'}}
        merged_properties = merge_connection_properties(connection1_properties=connection1_properties, connection2_properties=connection2_properties)
        self.assertEqual(merged_properties.get('title').get('name'), 'Adam')
        merged_properties = merge_connection_properties(connection1_properties=connection2_properties, connection2_properties=connection1_properties)
        self.assertEqual(merged_properties.get('title').get('name'), 'Adam Douglases')

    def test_merge_connection_properties_with_multiple_properties(self):
        connection1_properties = {'title': 'Adam Douglases', 'appearances': ['Adam did this when', 'Adam said'], 'type': 'person', }
        connection2_properties = {'title': 'Adam', 'appearances': ['Adam Douglases was', 'mr. Adam Douglases loves'], 'type': 'person', }
        merged_properties = merge_connection_properties(connection1_properties=connection1_properties, connection2_properties=connection2_properties)
        self.assertEqual(merged_properties.get('title'), 'Adam Douglases')
        self.assertEqual(set(merged_properties.get('appearances')), {'Adam said', 'Adam Douglases was', 'mr. Adam Douglases loves', 'Adam did this when'})
        self.assertEqual(merged_properties.get('type'), 'person')
        merged_properties = merge_connection_properties(connection1_properties=connection2_properties, connection2_properties=connection1_properties)
        self.assertEqual(merged_properties.get('title'), 'Adam Douglases')
        self.assertEqual(set(merged_properties.get('appearances')), {'Adam said', 'Adam Douglases was', 'mr. Adam Douglases loves', 'Adam did this when'})
        self.assertEqual(merged_properties.get('type'), 'person')

    def test_merge_connection_with_missing_properties(self):
        connection1_properties = {'title': 'Adam Douglases', 'type': 'person' }
        connection2_properties = {'title': 'Adam', 'appearances': ['Adam Douglases was', 'mr. Adam Douglases loves'] }
        merged_properties = merge_connection_properties(connection1_properties=connection1_properties, connection2_properties=connection2_properties)
        self.assertEqual(merged_properties.get('title'), 'Adam Douglases')
        self.assertEqual(set(merged_properties.get('appearances')), {'Adam Douglases was', 'mr. Adam Douglases loves'})
        self.assertEqual(merged_properties.get('type'), 'person')
        merged_properties = merge_connection_properties(connection1_properties=connection2_properties, connection2_properties=connection1_properties)
        self.assertEqual(merged_properties.get('title'), 'Adam Douglases')
        self.assertEqual(set(merged_properties.get('appearances')), {'Adam Douglases was', 'mr. Adam Douglases loves'})
        self.assertEqual(merged_properties.get('type'), 'person')
