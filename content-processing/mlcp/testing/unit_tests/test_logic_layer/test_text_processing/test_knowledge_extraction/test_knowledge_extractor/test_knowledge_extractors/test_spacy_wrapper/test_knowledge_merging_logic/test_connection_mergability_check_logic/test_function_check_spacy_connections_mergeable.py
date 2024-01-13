import unittest

from logic_layer.knowledge_record import KnowledgeRecordConnection
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._knowledge_merging_logic._connection_mergability_check_logic import check_spacy_connections_mergeable


class TestFunctionCheckSpacyConnectionsMergable(unittest.TestCase):

    def test_check_spacy_connections_mergeable_with_person_typed_entities_with_same_id(self):
        connection1 = KnowledgeRecordConnection()
        connection1.set_id("1")
        connection1.set_label("FRIEND")
        connection1.set_from_entity("Alice")
        connection1.set_to_entity("Bob")
        connection2 = KnowledgeRecordConnection()
        connection2.set_id("1")
        connection2.set_label("ENEMY")
        connection2.set_from_entity("John")
        connection2.set_to_entity("Mary")
        self.assertTrue(check_spacy_connections_mergeable(connection1, connection2))

    def test_check_spacy_connections_mergeable_with_connection_in_same_direction(self):
        connection1 = KnowledgeRecordConnection()
        connection1.set_id("1")
        connection1.set_label("CONNECTED")
        connection1.set_from_entity("John")
        connection1.set_to_entity("Mary")
        connection2 = KnowledgeRecordConnection()
        connection2.set_id("2")
        connection2.set_label("CONNECTED")
        connection2.set_from_entity("John")
        connection2.set_to_entity("Mary")
        self.assertTrue(check_spacy_connections_mergeable(connection1, connection2))

    def test_check_spacy_connections_mergeable_with_connection_in_opposite_direction(self):
        connection1 = KnowledgeRecordConnection()
        connection1.set_id("1")
        connection1.set_label("CONNECTED")
        connection1.set_from_entity("John")
        connection1.set_to_entity("Mary")
        connection2 = KnowledgeRecordConnection()
        connection2.set_id("2")
        connection2.set_label("CONNECTED")
        connection2.set_from_entity("Mary")
        connection2.set_to_entity("John")
        self.assertTrue(check_spacy_connections_mergeable(connection1, connection2))

    def test_check_spacy_connections_mergeable_with_connection_in_same_direction_and_different_entities(self):
        connection1 = KnowledgeRecordConnection()
        connection1.set_id("1")
        connection1.set_label("CONNECTED")
        connection1.set_from_entity("John")
        connection1.set_to_entity("Mary")
        connection2 = KnowledgeRecordConnection()
        connection2.set_id("2")
        connection2.set_label("CONNECTED")
        connection2.set_from_entity("John")
        connection2.set_to_entity("Bob")
        self.assertFalse(check_spacy_connections_mergeable(connection1, connection2))
