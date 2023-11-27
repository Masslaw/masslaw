from spacy.tokens.doc import Doc

from logic_layer.knowledge_record import KnowledgeRecord
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._basic_document_processing import SpacyCoreferencesResolver
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._basic_document_processing import SpacyEntitiesExtractor
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._basic_document_processing import SpacyRelationsExtractor
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._document_data_inflation import SpacyDocumentDataInflater
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._knowledge_record_building import SpacyDocumentKnowledgeRecordBuilder
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._structures import SpacyDocumentData
from shared_layer.mlcp_logger import logger


class SpacyDocumentProcessor:

    def __init__(self, spacy_document: Doc):
        self._document_data = SpacyDocumentData(spacy_document)
        self._coreference_resolver = SpacyCoreferencesResolver(self._document_data)
        self._entities_extractor = SpacyEntitiesExtractor(self._document_data)
        self._relations_extractor = SpacyRelationsExtractor(self._document_data)
        self._document_data_inflater = SpacyDocumentDataInflater(self._document_data)
        self._knowledge_record_builder = SpacyDocumentKnowledgeRecordBuilder(self._document_data)
        self._knowledge_record = KnowledgeRecord()

    @logger.process_function("Processing spacy document")
    def process_document(self) -> KnowledgeRecord:
        self._resolve_coreferences()
        self._extract_entities()
        self._inflate_entity_data()
        self._extract_relations()
        self._inflate_relations_data()
        self._build_knowledge_record()
        return self._knowledge_record

    @logger.process_function("Resolving coreferences")
    def _resolve_coreferences(self):
        self._coreference_resolver.resolve_coreferences()

    @logger.process_function("Extracting entities")
    def _extract_entities(self):
        self._entities_extractor.extract_entities()

    @logger.process_function("Inflating entity data")
    def _inflate_entity_data(self):
        self._document_data_inflater.generate_titles_for_entities()
        self._document_data_inflater.inflate_entity_data()

    @logger.process_function("Extracting relations")
    def _extract_relations(self):
        self._relations_extractor.extract_relations()

    @logger.process_function("Inflating relations data")
    def _inflate_relations_data(self):
        self._document_data_inflater.inflate_relations_data()

    @logger.process_function("Building knowledge record")
    def _build_knowledge_record(self):
        self._knowledge_record = self._knowledge_record_builder.build_knowledge_record()
