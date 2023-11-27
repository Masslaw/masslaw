import unittest
from spacy import load
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy._common import traverse_upward

class TestFunctionTraverseUpward(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.nlp = load("en_core_web_sm")
        # Yes, in unittests we should not rely on the output of other functions. This is a very simple
        # sentence, for which we expect the output of spacy to be consistent across versions.
        # The reason we test using a doc, is that mocking it, will be much harder.
        cls.doc = cls.nlp("Johana Jones went to eat dinner with her friend, John Smith, in New York City.")

    def test_stop_condition_met(self):
        token = self.doc[6]
        upward_chain = traverse_upward(token, lambda t: True)
        self.assertEqual(len(upward_chain), 1)
        self.assertIn(self.doc[6], upward_chain)

    def test_stop_condition_not_met(self):
        token = self.doc[6]
        upward_chain = traverse_upward(token, lambda t: False)
        self.assertEqual(len(upward_chain), 4)

    def test_stop_condition_at_root(self):
        token = self.doc[6]
        upward_chain = traverse_upward(token, lambda t: t.dep_ == 'ROOT')
        self.assertEqual(len(upward_chain), 4)

    def test_stop_condition_at_token_itself(self):
        token = self.doc[6]
        upward_chain = traverse_upward(token, lambda t: t == token)
        self.assertEqual(len(upward_chain), 1)
        self.assertIn(token, upward_chain)
