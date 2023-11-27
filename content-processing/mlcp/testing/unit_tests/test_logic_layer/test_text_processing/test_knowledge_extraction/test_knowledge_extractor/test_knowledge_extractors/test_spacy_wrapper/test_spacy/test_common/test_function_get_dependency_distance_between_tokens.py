import unittest

from spacy import load

from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy._common import get_dependency_distance_between_tokens


class TestFunctionGetDependencyDistanceBetweenTokens(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.nlp = load("en_core_web_sm")
        cls.doc = cls.nlp("Johana Jones went to eat dinner with her friend, John Smith, in New York City.")

    def test_directly_connected_tokens(self):
        token1 = self.doc[2]
        token2 = self.doc[3]
        distance = get_dependency_distance_between_tokens(token1, token2)
        self.assertEqual(distance, 3)

    def test_tokens_with_common_ancestor(self):
        token1 = self.doc[6]
        token2 = self.doc[7]
        distance = get_dependency_distance_between_tokens(token1, token2)
        self.assertEqual(distance, 3)

    def test_one_token_is_ancestor_of_other(self):
        token1 = self.doc[2]
        token2 = self.doc[6]
        distance = get_dependency_distance_between_tokens(token1, token2)
        self.assertEqual(distance, 4)

    def test_tokens_with_no_direct_connection(self):
        token1 = self.doc[0]
        token2 = self.doc[11]
        distance = get_dependency_distance_between_tokens(token1, token2)
        self.assertIsNotNone(distance)
