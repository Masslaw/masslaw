import unittest
from spacy import load
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy._common import sort_tokens

class TestFunctionSortTokens(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.nlp = load("en_core_web_sm")
        cls.doc = cls.nlp("Johana Jones went to eat dinner with her friend, John Smith, in New York City.")

    def test_sort_random_order_tokens(self):
        tokens = [self.doc[5], self.doc[2], self.doc[8]]
        sorted_tokens = sort_tokens(tokens)
        self.assertEqual([token.i for token in sorted_tokens], [2, 5, 8])

    def test_sort_already_sorted_tokens(self):
        tokens = [self.doc[2], self.doc[5], self.doc[8]]
        sorted_tokens = sort_tokens(tokens)
        self.assertEqual([token.i for token in sorted_tokens], [2, 5, 8])

    def test_sort_empty_list(self):
        tokens = []
        sorted_tokens = sort_tokens(tokens)
        self.assertEqual(sorted_tokens, [])

    def test_sort_single_token(self):
        tokens = [self.doc[2]]  # went
        sorted_tokens = sort_tokens(tokens)
        self.assertEqual(len(sorted_tokens), 1)
        self.assertEqual(sorted_tokens[0], self.doc[2])
