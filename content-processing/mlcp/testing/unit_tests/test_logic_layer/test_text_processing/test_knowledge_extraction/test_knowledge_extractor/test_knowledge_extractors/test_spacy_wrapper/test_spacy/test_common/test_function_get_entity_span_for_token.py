import unittest
from spacy import load
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy._common import get_entity_span_for_token

class TestFunctionGetEntitySpanForToken(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.nlp = load("en_core_web_sm")
        # Yes, in unittests we should not rely on the output of other functions. This is a very simple
        # sentence, for which we expect the output of spacy to be consistent across versions.
        # The reason we test using a doc, is that mocking it, will be much harder.
        cls.doc = cls.nlp("New York City is a major city.")

    def test_token_within_entity(self):
        token = self.doc[1]  # York
        entity_span = get_entity_span_for_token(token)
        self.assertIsNotNone(entity_span)
        self.assertEqual(entity_span.text, "New York City")

    def test_token_not_within_entity(self):
        token = self.doc[5]  # major
        entity_span = get_entity_span_for_token(token)
        self.assertIsNone(entity_span)

    def test_token_at_start_of_entity(self):
        token = self.doc[0]  # New
        entity_span = get_entity_span_for_token(token)
        self.assertIsNotNone(entity_span)
        self.assertEqual(entity_span.text, "New York City")

    def test_token_at_end_of_entity(self):
        token = self.doc[2]  # City
        entity_span = get_entity_span_for_token(token)
        self.assertIsNotNone(entity_span)
