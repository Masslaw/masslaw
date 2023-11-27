import unittest
from unittest.mock import patch

from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._models._model_loading import load_spacy_model_for_language


class TestFunctionLoadSpacyModelForLanguage(unittest.TestCase):

    def setUp(self):
        self.spacy_load_patch = patch('logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._models._model_loading.spacy.load')
        self.spacy_load_mock = self.spacy_load_patch.start()
        self.spacy_load_mock.side_effect = lambda model_name: model_name

    def tearDown(self):
        self.spacy_load_patch.stop()

    def test_on_a_valid_language(self):
        with patch('logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._models._model_loading.models_config') as mock_models_config:
            mock_models_config.get.side_effect = lambda language: ({'en': 'en_model', 'fr': 'fr_model'}).get(language)
            self.assertEqual(load_spacy_model_for_language('en'), 'en_model')
            self.assertEqual(load_spacy_model_for_language('fr'), 'fr_model')

    def test_on_an_invalid_language(self):
        with patch('logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._models._model_loading.models_config') as mock_models_config:
            mock_models_config.get.side_effect = lambda language: ({'en': 'en_model', 'fr': 'fr_model'}).get(language)
            self.assertEqual(load_spacy_model_for_language('sp'), None)