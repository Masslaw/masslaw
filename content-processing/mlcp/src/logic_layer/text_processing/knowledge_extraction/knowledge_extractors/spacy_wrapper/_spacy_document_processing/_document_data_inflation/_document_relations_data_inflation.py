from typing import List

from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._structures import DocumentEntityRelation


def inflate_relations_data(relations: List[DocumentEntityRelation]):
    _write_relations_strength_to_data(relations)


def _write_relations_strength_to_data(relations: List[DocumentEntityRelation]):
    for relation in relations: relation.relation_data['strength'] = relation.relation_strength
