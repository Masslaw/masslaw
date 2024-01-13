import unittest
from typing import List

from logic_layer.knowledge_record import KnowledgeRecord
from logic_layer.text_processing.knowledge_extraction._knowledge_extractor import KnowledgeExtractor
from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument


class TestClassKnowledgeExtractor(unittest.TestCase):

    def test_text_processing(self):
        mock_knowledge_record = KnowledgeRecord()
        text_to_process = 'This is some text to process.'

        class KnowledgeExtractorMock(KnowledgeExtractor):
            def _process_texts(self, text: List[str]):
                self._knowledge_record = mock_knowledge_record

        knowledge_extractor_mock = KnowledgeExtractorMock([])
        knowledge_extractor_mock.load_texts([text_to_process])

        self.assertEqual(knowledge_extractor_mock.get_record(), mock_knowledge_record)

    def test_optical_text_document_processing(self):
        mock_knowledge_record = KnowledgeRecord()
        optical_text_document_to_process = ExtractedOpticalTextDocument()

        class KnowledgeExtractorMock(KnowledgeExtractor):
            def _process_optical_text_document(self, document: ExtractedOpticalTextDocument):
                self._knowledge_record = mock_knowledge_record

        knowledge_extractor_mock = KnowledgeExtractorMock([])
        knowledge_extractor_mock.load_optical_text_document(optical_text_document_to_process)

        self.assertEqual(knowledge_extractor_mock.get_record(), mock_knowledge_record)
