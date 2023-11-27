import unittest
from unittest.mock import call
from unittest.mock import patch

from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_wrapper import SpacyWrapper
from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure.structure_construction import OpticalTextStructureConstructor


class TestClassSpacyWrapper(unittest.TestCase):

    def setUp(self):
        self.load_model_patch = patch('logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_wrapper.load_spacy_model_for_language')
        self.load_model_mock = self.load_model_patch.start()
        self.load_model_mock.side_effect = lambda language: ({'en': 'en_model', 'fr': 'fr_model'}).get(language)

        self.prepare_model_patch = patch('logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_wrapper.SpacyWrapper._prepare_model')
        self.prepare_model_mock = self.prepare_model_patch.start()
        self.prepare_model_mock.side_effect = lambda model: None

    def tearDown(self):
        self.load_model_patch.stop()
        self.prepare_model_patch.stop()

    def test_models_loading(self):

        spacy_wrapper = SpacyWrapper(['en', 'fr', 'sp'])
        self.assertEqual(spacy_wrapper._spacy_models, {'en': 'en_model', 'fr': 'fr_model'})
        self.assertEqual(self.load_model_mock.call_args_list, [call('en'), call('fr'), call('sp')])
        self.assertEqual(self.prepare_model_mock.call_args_list, [call('en_model'), call('fr_model')])

    def test_process_text(self):
        with patch('logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_wrapper.SpacyWrapper._process_text_in_language') as mock_process_text_in_language:
            spacy_wrapper = SpacyWrapper(['en', 'fr', 'sp'])
            spacy_wrapper._process_text('This is some text to process.')
            self.assertEqual(mock_process_text_in_language.call_args_list, [call('This is some text to process.', 'en'), call('This is some text to process.', 'fr')])


    def test_process_optical_text_document(self):
        with patch('logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_wrapper.SpacyWrapper._process_text') as mock_process_text:
            optical_text_document = ExtractedOpticalTextDocument([OpticalStructureHierarchyLevel.LINE, OpticalStructureHierarchyLevel.WORD])
            OpticalTextStructureConstructor(optical_text_document).add_entry_groups_to_structure([[('this', (0,0,0,0)), ('is', (0,0,0,1)), ('some', (0,0,0,2)), ('text', (0,0,0,3)), ('to', (0,0,0,4)), ('process', (0,0,0,5))]])
            spacy_wrapper = SpacyWrapper(['en', 'fr', 'sp'])
            spacy_wrapper._process_optical_text_document(optical_text_document)
            self.assertEqual(mock_process_text.call_args_list, [call('this is some text to process')])