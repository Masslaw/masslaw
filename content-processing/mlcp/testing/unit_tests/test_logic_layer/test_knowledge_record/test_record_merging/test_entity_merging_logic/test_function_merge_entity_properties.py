import unittest

from logic_layer.knowledge_record.record_merging._entity_merging_logic import merge_entity_properties


class TestFunctionMergeEntityProperties(unittest.TestCase):

    def test_merge_entity_properties_with_unique_property(self):
        entity1_properties = {'title': 'Adam Douglases'}
        entity2_properties = {'title': 'Adam'}
        merged_properties = merge_entity_properties(entity1_properties=entity1_properties, entity2_properties=entity2_properties)
        self.assertEqual(merged_properties.get('title'), 'Adam Douglases')
        merged_properties = merge_entity_properties(entity1_properties=entity2_properties, entity2_properties=entity1_properties)
        self.assertEqual(merged_properties.get('title'), 'Adam Douglases')

    def test_merge_entity_properties_with_non_unique_property(self):
        entity1_properties = {'type': 'person'}
        entity2_properties = {'type': 'person'}
        merged_properties = merge_entity_properties(entity1_properties=entity1_properties, entity2_properties=entity2_properties)
        self.assertEqual(merged_properties.get('type'), 'person')
        merged_properties = merge_entity_properties(entity1_properties=entity2_properties, entity2_properties=entity1_properties)
        self.assertEqual(merged_properties.get('type'), 'person')

    def test_merge_entity_properties_with_list_property(self):
        entity1_properties = {'appearances': ['Adam did this when', 'Adam said']}
        entity2_properties = {'appearances': ['Adam Douglases was', 'mr. Adam Douglases loves']}
        merged_properties = merge_entity_properties(entity1_properties=entity1_properties, entity2_properties=entity2_properties)
        self.assertEqual(set(merged_properties.get('appearances')), {'Adam said', 'Adam Douglases was', 'mr. Adam Douglases loves', 'Adam did this when'})
        merged_properties = merge_entity_properties(entity1_properties=entity2_properties, entity2_properties=entity1_properties)
        self.assertEqual(set(merged_properties.get('appearances')), {'Adam said', 'Adam Douglases was', 'mr. Adam Douglases loves', 'Adam did this when'})

    def test_merge_entity_properties_with_dict_property(self):
        entity1_properties = {'title': {'name': 'Adam Douglases'}}
        entity2_properties = {'title': {'name': 'Adam'}}
        merged_properties = merge_entity_properties(entity1_properties=entity1_properties, entity2_properties=entity2_properties)
        self.assertEqual(merged_properties.get('title').get('name'), 'Adam')
        merged_properties = merge_entity_properties(entity1_properties=entity2_properties, entity2_properties=entity1_properties)
        self.assertEqual(merged_properties.get('title').get('name'), 'Adam Douglases')

    def test_merge_entity_properties_with_multiple_properties(self):
        entity1_properties = {'title': 'Adam Douglases', 'appearances': ['Adam did this when', 'Adam said'], 'type': 'person', }
        entity2_properties = {'title': 'Adam', 'appearances': ['Adam Douglases was', 'mr. Adam Douglases loves'], 'type': 'person', }
        merged_properties = merge_entity_properties(entity1_properties=entity1_properties, entity2_properties=entity2_properties)
        self.assertEqual(merged_properties.get('title'), 'Adam Douglases')
        self.assertEqual(set(merged_properties.get('appearances')), {'Adam said', 'Adam Douglases was', 'mr. Adam Douglases loves', 'Adam did this when'})
        self.assertEqual(merged_properties.get('type'), 'person')
        merged_properties = merge_entity_properties(entity1_properties=entity2_properties, entity2_properties=entity1_properties)
        self.assertEqual(merged_properties.get('title'), 'Adam Douglases')
        self.assertEqual(set(merged_properties.get('appearances')), {'Adam said', 'Adam Douglases was', 'mr. Adam Douglases loves', 'Adam did this when'})
        self.assertEqual(merged_properties.get('type'), 'person')

    def test_merge_entity_with_missing_properties(self):
        entity1_properties = {'title': 'Adam Douglases', 'type': 'person' }
        entity2_properties = {'title': 'Adam', 'appearances': ['Adam Douglases was', 'mr. Adam Douglases loves'] }
        merged_properties = merge_entity_properties(entity1_properties=entity1_properties, entity2_properties=entity2_properties)
        self.assertEqual(merged_properties.get('title'), 'Adam Douglases')
        self.assertEqual(set(merged_properties.get('appearances')), {'Adam Douglases was', 'mr. Adam Douglases loves'})
        self.assertEqual(merged_properties.get('type'), 'person')
        merged_properties = merge_entity_properties(entity1_properties=entity2_properties, entity2_properties=entity1_properties)
        self.assertEqual(merged_properties.get('title'), 'Adam Douglases')
        self.assertEqual(set(merged_properties.get('appearances')), {'Adam Douglases was', 'mr. Adam Douglases loves'})
        self.assertEqual(merged_properties.get('type'), 'person')
