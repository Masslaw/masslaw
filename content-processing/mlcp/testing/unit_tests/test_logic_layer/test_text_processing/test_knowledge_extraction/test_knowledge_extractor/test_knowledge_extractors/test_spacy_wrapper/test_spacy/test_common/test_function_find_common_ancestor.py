import unittest

from spacy import load

from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy._common import find_common_ancestor


class TestFunctionFindCommonAncestor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.nlp = load("en_core_web_sm")
        cls.doc = cls.nlp("Johana Jones went to eat dinner with her friend, John Smith, in New York City.")

    def test_common_ancestor(self):
        token1 = self.doc[2]
        token2 = self.doc[6]
        common_ancestor = find_common_ancestor(token1, token2)
        self.assertIsNotNone(common_ancestor)
        self.assertEqual(common_ancestor, self.doc[2])

    def test_one_token_is_ancestor_of_other(self):
        token1 = self.doc[2]
        token2 = self.doc[4]
        common_ancestor = find_common_ancestor(token1, token2)
        self.assertIsNotNone(common_ancestor)
        self.assertEqual(common_ancestor, self.doc[2])

    def test_no_common_ancestor(self):
        token1 = self.doc[0]
        token2 = self.doc[11]
        common_ancestor = find_common_ancestor(token1, token2)
        self.assertIsNotNone(common_ancestor)
        self.assertEqual(common_ancestor.dep_, 'ROOT')

    def test_tokens_are_the_same(self):
        token = self.doc[2]
        common_ancestor = find_common_ancestor(token, token)
        self.assertIsNotNone(common_ancestor)
        self.assertEqual(common_ancestor, token)
