import itertools
from typing import List

from logic_layer.text_processing.named_entity_recognition.ner_processors.spacy_wrapper._spacy_document_processing._common import find_common_ancestor
from logic_layer.text_processing.named_entity_recognition.ner_processors.spacy_wrapper._spacy_document_processing._structures import DocumentEntityRelation
from logic_layer.text_processing.named_entity_recognition.ner_processors.spacy_wrapper._spacy_document_processing._structures import SpacyDocumentData
from shared_layer.list_utils import list_utils


class SpacyRelationsExtractor:

    def __init__(self, document_data: SpacyDocumentData):
        self._document_data = document_data
        self._relations: List[DocumentEntityRelation] = []

    def extract_relations(self):
        self._load_relations_by_crossing_coref_chains()
        self._load_relations_by_common_ancestor()
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
                relation.relating_tokens = [token for token in connecting_chain.chain_tokens if token.pos_ in ("PRON",)]
                self._relations.append(relation)

    def _load_relations_by_common_ancestor(self):
        for entity1, entity2 in itertools.permutations(self._document_data.document_entities, 2):
            for entity1_span, entity2_span in itertools.product(entity1.entity_spans, entity2.entity_spans):
                common_ancestor = find_common_ancestor(entity1_span.root, entity2_span.root)
                if not common_ancestor: continue
                relation = DocumentEntityRelation()
                relation.from_entity = entity1
                relation.to_entity = entity2
                relation.relation_data = {}
                relation.relating_tokens = {common_ancestor}
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
        return merged_relation
