import unittest

from spacy import load

from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy._common import get_compound_chain


class TestFunctionGetCompoundChain(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.nlp = load("en_core_web_sm")
        # Yes, in unittests we should not rely on the output of other functions. This is a very simple
        # sentence, for which we expect the output of spacy to be consistent across versions.
        # The reason we test using a doc, is that mocking it, will be much harder.
        cls.doc = cls.nlp("Johana Jones went to eat dinner with her friend, John Smith, in New York City.")

    def test_token_in_compound_chain(self):
        token = self.doc[15]  # York
        compound_chain = get_compound_chain(token)
        self.assertEqual(len(compound_chain), 3)
        self.assertIn(self.doc[14], compound_chain)  # New
        self.assertIn(self.doc[15], compound_chain)  # York
        self.assertIn(self.doc[16], compound_chain)  # City

    def test_token_not_in_compound_chain(self):
        token = self.doc[4]  # eat
        compound_chain = get_compound_chain(token)
        self.assertEqual(len(compound_chain), 1)
        self.assertIn(token, compound_chain)
