import unittest
from spacy import load
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy._common import traverse_downward

class TestFunctionTraverseDownward(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.nlp = load("en_core_web_sm")
        cls.doc = cls.nlp("Johana Jones went to eat dinner with her friend, John Smith, in New York City.")

    def test_stop_condition_met(self):
        token = self.doc[2]
        downward_chain = traverse_downward(token, lambda t: t in token.children)
        self.assertEqual(len(downward_chain), 1 + len(list(token.children)))

    def test_stop_condition_not_met(self):
        token = self.doc[2]
        downward_chain = traverse_downward(token, lambda t: False)
        self.assertGreater(len(downward_chain), 1)

    def test_stop_condition_at_token_itself(self):
        token = self.doc[2]
        downward_chain = traverse_downward(token, lambda t: t == token)
        self.assertEqual(len(downward_chain), 1)
        self.assertIn(token, downward_chain)

    def test_empty_downward_chain_for_leaf_token(self):
        token = self.doc[10]
        downward_chain = traverse_downward(token, lambda t: False)
        self.assertEqual(len(downward_chain), 1)
        self.assertIn(token, downward_chain)