from typing import List

from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy._common import sort_tokens
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy._common import traverse_downward
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._structures import DocumentEntityRelation
from shared_layer.dictionary_utils import dictionary_utils


def inflate_relations_data(relations: List[DocumentEntityRelation]):
    _write_relations_strength_to_data(relations)
    _fill_relation_sentence_data(relations)


def _write_relations_strength_to_data(relations: List[DocumentEntityRelation]):
    for relation in relations: relation.relation_data['strength'] = relation.relation_strength
    

def _fill_relation_sentence_data(relations: List[DocumentEntityRelation]):
    for relation in relations: _set_relation_sentence_data(relation)


def _set_relation_sentence_data(relation: DocumentEntityRelation):
    relating_tokens = relation.relating_tokens
    relating_sentence = list(relating_tokens)[0].sent
    relation_indices = []
    for token in relating_tokens:
        token_start, token_end = _get_token_start_and_end_indices(token)
        relation_indices += [token_start-relating_sentence.start_char, token_end-relating_sentence.start_char]
    dictionary_utils.set_at(relation.relation_data, ['text', 'sents', relating_sentence.text], relation_indices)

    
def _get_token_start_and_end_indices(token):
    token_sub_tree = traverse_downward(token, lambda _: False)
    sorted_subtree_tokens = sort_tokens(token_sub_tree)
    token_start = sorted_subtree_tokens[0].idx
    token_end = sorted_subtree_tokens[-1].idx+len(sorted_subtree_tokens[-1].text)
    return token_start, token_end
    
