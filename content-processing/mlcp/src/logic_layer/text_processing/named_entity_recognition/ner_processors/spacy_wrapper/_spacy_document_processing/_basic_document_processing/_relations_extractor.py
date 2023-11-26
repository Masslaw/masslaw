import itertools
from typing import List

from logic_layer.text_processing.named_entity_recognition.ner_processors.spacy_wrapper._spacy import common
from logic_layer.text_processing.named_entity_recognition.ner_processors.spacy_wrapper._spacy._common import get_dependency_distance_between_tokens
from logic_layer.text_processing.named_entity_recognition.ner_processors.spacy_wrapper._spacy_document_processing._structures import DocumentEntityRelation
from logic_layer.text_processing.named_entity_recognition.ner_processors.spacy_wrapper._spacy_document_processing._structures import SpacyDocumentData
from shared_layer.list_utils import list_utils


RELATING_PRONOUN_RELATION_STRENGTH = 5
COMMON_ANCESTOR_DISTANCE_RELATION_STRENGTH = 2
SENTENCE_SHARING_RELATION_STRENGTH = 0.5


class SpacyRelationsExtractor:

    def __init__(self, document_data: SpacyDocumentData):
        self._document_data = document_data
        self._relations: List[DocumentEntityRelation] = []

    def extract_relations(self):
        self._load_relations_by_crossing_coref_chains()
        self._load_relations_by_common_ancestor()
        self._load_relations_by_sentence_sharing()
        self._merge_relations()
        self._document_data.document_relations = self._relations

    def _load_relations_by_crossing_coref_chains(self):
        for entity1, entity2 in itertools.permutations(self._document_data.document_entities, 2):
            sharing_coref_chains = entity1.coreference_chains & entity2.coreference_chains
            for connecting_chain in sharing_coref_chains:
                relation = DocumentEntityRelation()
                relation.from_entity = entity1
                relation.to_entity = entity2
                relation.relation_data = {}
                relation.relating_tokens = set(token for token in connecting_chain.chain_tokens if token.pos_ in ("PRON",))
                relation.relation_strength = len(relation.relating_tokens) * RELATING_PRONOUN_RELATION_STRENGTH
                self._relations.append(relation)

    def _load_relations_by_common_ancestor(self):
        for entity1, entity2 in itertools.permutations(self._document_data.document_entities, 2):
            for entity1_appearance, entity2_appearance in itertools.product(entity1.entity_appearances, entity2.entity_appearances):
                common_ancestor = common.find_common_ancestor(entity1_appearance, entity2_appearance)
                if not common_ancestor: continue
                relation = DocumentEntityRelation()
                relation.from_entity = entity1
                relation.to_entity = entity2
                relation.relation_data = {}
                relation.relating_tokens = {common_ancestor}
                relation.relation_strength = get_dependency_distance_between_tokens(entity1_appearance, entity2_appearance) * COMMON_ANCESTOR_DISTANCE_RELATION_STRENGTH
                self._relations.append(relation)

    def _load_relations_by_sentence_sharing(self):
        for entity1, entity2 in itertools.permutations(self._document_data.document_entities, 2):
            for entity1_appearance, entity2_appearance in itertools.product(entity1.entity_appearances, entity2.entity_appearances):
                if entity1_appearance.sent != entity2_appearance.sent: continue
                relation = DocumentEntityRelation()
                relation.from_entity = entity1
                relation.to_entity = entity2
                relation.relation_data = {}
                relation.relating_tokens = {entity1_appearance.sent.root}
                relation.relation_strength = abs(entity1_appearance.i - entity2_appearance.i) * SENTENCE_SHARING_RELATION_STRENGTH
                self._relations.append(relation)

    def _merge_relations(self):
        list_utils.merge_mergeable(self._relations, self._mergeable, self._do_merge_relations)

    def _mergeable(self, relation1: DocumentEntityRelation, relation2: DocumentEntityRelation) -> bool:
        if relation1.from_entity != relation2.from_entity: return False
        if relation1.to_entity != relation2.to_entity: return False
        return True

    def _do_merge_relations(self, relation1: DocumentEntityRelation, relation2: DocumentEntityRelation) -> DocumentEntityRelation:
        merged_relation = DocumentEntityRelation()
        merged_relation.from_entity = relation1.from_entity
        merged_relation.to_entity = relation1.to_entity
        merged_relation.relation_data = {}
        merged_relation.relating_tokens = relation1.relating_tokens | relation2.relating_tokens
        merged_relation.relation_strength = relation1.relation_strength + relation2.relation_strength
        return merged_relation
