import itertools
from typing import List

from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy._common import get_dependency_distance_between_tokens
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._structures import DocumentEntityRelation
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._structures import SpacyDocumentData
from shared_layer.mlcp_logger import logger
from shared_layer.mlcp_logger import common_formats

RELATING_PRONOUN_RELATION_STRENGTH = 5
COMMON_ANCESTOR_DISTANCE_RELATION_STRENGTH = 2
SENTENCE_SHARING_RELATION_STRENGTH = 0.5


class SpacyRelationsExtractor:

    def __init__(self, document_data: SpacyDocumentData):
        self._document_data = document_data
        self._relations: List[DocumentEntityRelation] = []

    def extract_relations(self):
        self._load_relations_by_sentence_sharing()
        self._document_data.document_relations = self._relations
        logger.info(f"{common_formats.value(len(self._relations))} relations extracted.")

    def _load_relations_by_sentence_sharing(self):
        for entity1, entity2 in itertools.permutations(self._document_data.document_entities, 2):
            for entity1_appearance in entity1.entity_appearances:
                for entity2_appearance in entity2.entity_appearances:
                    if entity1_appearance.sent != entity2_appearance.sent: continue
                    relation = DocumentEntityRelation()
                    relation.from_entity = entity1
                    relation.to_entity = entity2
                    relation.relation_data = {}
                    relation.relating_tokens = {entity1_appearance, entity2_appearance}
                    relation.relation_strength = SENTENCE_SHARING_RELATION_STRENGTH
                    self._relations.append(relation)
