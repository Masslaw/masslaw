import unittest

from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._knowledge_record_building._knowledge_record_builder import SpacyDocumentKnowledgeRecordBuilder
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._structures import DocumentEntity
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._structures import DocumentEntityRelation
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._structures import SpacyDocumentData


class TestClassSpacyDocumentKnowledgeRecordBuilder(unittest.TestCase):

    def setUp(self):
        entity1 = DocumentEntity()
        entity2 = DocumentEntity()
        entity3 = DocumentEntity()
        relation1 = DocumentEntityRelation()
        relation1.from_entity = entity1
        relation1.to_entity = entity2
        relation2 = DocumentEntityRelation()
        relation2.from_entity = entity2
        relation2.to_entity = entity3
        relation3 = DocumentEntityRelation()
        relation3.from_entity = entity3
        relation3.to_entity = entity1
        self.document = SpacyDocumentData(None)
        self.document.document_entities = [entity1, entity2, entity3]
        self.document.document_relations = [relation1, relation2, relation3]
        self.builder = SpacyDocumentKnowledgeRecordBuilder(self.document)

    def test_full_record_building(self):
        record = self.builder.build_knowledge_record()
        self.assertEqual(len(record.get_entities()), 3)
        self.assertEqual(len(record.get_connections()), 3)

    def test_loading_entities(self):
        self.builder._create_entities()
        self.assertEqual(len(self.builder._knowledge_record.get_entities()), 3)

    def test_loading_relations_without_loading_entities(self):
        with self.assertRaises(KeyError):
            self.builder._create_relations()
