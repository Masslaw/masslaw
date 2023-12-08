import unittest
from typing import List
from logic_layer.knowledge_record._connection import KnowledgeRecordConnection
from logic_layer.knowledge_record._entity import KnowledgeRecordEntity
from logic_layer.knowledge_record._record import KnowledgeRecord

class TestClassKnowledgeRecord(unittest.TestCase):

    def setUp(self):
        self.knowledge_record = KnowledgeRecord()
        self.sample_entities = [KnowledgeRecordEntity(), KnowledgeRecordEntity()]
        self.sample_connections = [KnowledgeRecordConnection(), KnowledgeRecordConnection()]

    def test_init(self):
        self.assertEqual(self.knowledge_record.get_entities(), [])
        self.assertEqual(self.knowledge_record.get_connections(), [])

    def test_set_and_get_entities(self):
        self.knowledge_record.set_entities(self.sample_entities)
        self.assertEqual(self.knowledge_record.get_entities(), self.sample_entities)

    def test_set_and_get_entities_with_empty_list(self):
        self.knowledge_record.set_entities([])
        self.assertEqual(self.knowledge_record.get_entities(), [])

    def test_entities_immutable_to_outside_modifications(self):
        entities = self.knowledge_record.get_entities()
        entities.append(KnowledgeRecordEntity())
        self.assertNotEqual(entities, self.knowledge_record.get_entities())

    def test_set_and_get_connections(self):
        self.knowledge_record.set_connections(self.sample_connections)
        self.assertEqual(self.knowledge_record.get_connections(), self.sample_connections)

    def test_set_and_get_connections_with_empty_list(self):
        self.knowledge_record.set_connections([])
        self.assertEqual(self.knowledge_record.get_connections(), [])

    def test_connections_immutable_to_outside_modifications(self):
        connections = self.knowledge_record.get_connections()
        connections.append(KnowledgeRecordConnection())
        self.assertNotEqual(connections, self.knowledge_record.get_connections())
        
    def test_add_entities(self):
        entities = self.knowledge_record.get_entities()
        entities_to_add = [KnowledgeRecordEntity(), KnowledgeRecordEntity()]
        self.knowledge_record.add_entities(entities_to_add)
        self.assertEqual(self.knowledge_record.get_entities(), entities + entities_to_add)
    
    def test_add_connections(self):
        connections = self.knowledge_record.get_connections()
        connections_to_add = [KnowledgeRecordConnection(), KnowledgeRecordConnection()]
        self.knowledge_record.add_connections(connections_to_add)
        self.assertEqual(self.knowledge_record.get_connections(), connections + connections_to_add)
        
    def test_connection_entity_maps(self):
        knowledge_record = KnowledgeRecord()
        entity1 = KnowledgeRecordEntity()
        entity2 = KnowledgeRecordEntity()
        entity3 = KnowledgeRecordEntity()
        connection1 = KnowledgeRecordConnection(from_entity=entity1, to_entity=entity2)
        connection2 = KnowledgeRecordConnection(from_entity=entity2, to_entity=entity3)
        connection3 = KnowledgeRecordConnection(from_entity=entity1, to_entity=entity3)
        connection4 = KnowledgeRecordConnection(from_entity=entity3, to_entity=entity1)
        knowledge_record.add_entities([entity1, entity2, entity3])
        knowledge_record.add_connections([connection1, connection2, connection3, connection4])
        self.assertEqual(knowledge_record.get_entity_outgoing_connections(entity1), [connection1, connection3])
        self.assertEqual(knowledge_record.get_entity_ingoing_connections(entity3), [connection2, connection3])

    def test_batch_updating_entity_properties(self):
        knowledge_record = KnowledgeRecord()
        entity1 = KnowledgeRecordEntity()
        entity1.set_properties({'a': 1})
        entity2 = KnowledgeRecordEntity()
        entity2.set_properties({'a': 2})
        knowledge_record.add_entities([entity1, entity2])
        knowledge_record.batch_update_entity_properties({'b': 1})
        self.assertEqual(entity1.get_properties(), {'a': 1, 'b': 1})
        self.assertEqual(entity2.get_properties(), {'a': 2, 'b': 1})

    def test_batch_updating_connection_properties(self):
        knowledge_record = KnowledgeRecord()
        entity1 = KnowledgeRecordEntity()
        entity2 = KnowledgeRecordEntity()
        connection1 = KnowledgeRecordConnection(from_entity=entity1, to_entity=entity2)
        connection1.set_properties({'a': 1})
        connection2 = KnowledgeRecordConnection(from_entity=entity1, to_entity=entity2)
        connection2.set_properties({'a': 2})
        knowledge_record.add_connections([connection1, connection2])
        knowledge_record.batch_update_connection_properties({'b': 1})
        self.assertEqual(connection1.get_properties(), {'a': 1, 'b': 1})
        self.assertEqual(connection2.get_properties(), {'a': 2, 'b': 1})

    def test_batch_set_entity_properties(self):
        knowledge_record = KnowledgeRecord()
        entity1 = KnowledgeRecordEntity()
        entity1.set_properties({'a': 1})
        entity2 = KnowledgeRecordEntity()
        entity2.set_properties({'a': 2})
        knowledge_record.add_entities([entity1, entity2])
        knowledge_record.batch_set_entity_properties({'b': 1})
        self.assertEqual(entity1.get_properties(), {'b': 1})
        self.assertEqual(entity2.get_properties(), {'b': 1})

    def test_batch_set_connection_properties(self):
        knowledge_record = KnowledgeRecord()
        entity1 = KnowledgeRecordEntity()
        entity2 = KnowledgeRecordEntity()
        connection1 = KnowledgeRecordConnection(from_entity=entity1, to_entity=entity2)
        connection1.set_properties({'a': 1})
        connection2 = KnowledgeRecordConnection(from_entity=entity1, to_entity=entity2)
        connection2.set_properties({'a': 2})
        knowledge_record.add_connections([connection1, connection2])
        knowledge_record.batch_set_connection_properties({'b': 1})
        self.assertEqual(connection1.get_properties(), {'b': 1})
        self.assertEqual(connection2.get_properties(), {'b': 1})
