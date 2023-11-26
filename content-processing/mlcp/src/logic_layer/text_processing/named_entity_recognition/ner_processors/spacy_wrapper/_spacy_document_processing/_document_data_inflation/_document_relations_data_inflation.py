from typing import List

from logic_layer.text_processing.named_entity_recognition.ner_processors.spacy_wrapper._spacy_document_processing._structures import DocumentEntityRelation


def inflate_relations_data(relations: List[DocumentEntityRelation]):
    _collect_evidence_for_relations(relations)


def _collect_evidence_for_relations(relations: List[DocumentEntityRelation]):
    for relation in relations:
        relation_evidence_sentences = set()
        for relating_token in relation.relating_tokens:
            relation_evidence_sentences.add(relating_token.sent)
        relation.relation_data['evidences'] = [{'t': sentence.text, 's': sentence.start_char, 'e': sentence.end_char} for sentence in relation_evidence_sentences]