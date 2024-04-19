import re
from types import SimpleNamespace
from typing import List
from typing import Set
from typing import Tuple

from spacy.tokens.span import Span
from spacy.tokens.token import Token

from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy._common import sort_tokens
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy._common import traverse_downward
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._structures import DocumentEntity
from shared_layer.dictionary_utils import dictionary_utils


def inflate_entity_data(entities: List[DocumentEntity]|Set[DocumentEntity]):
    for entity in entities: _load_entity_appearances(entity)


def _load_entity_appearances(entity: DocumentEntity):
    entity_appearances = entity.entity_appearances
    appearances_data = {}
    for appearance in entity_appearances:
        sentence = appearance.sent
        appearance_sub_tree = traverse_downward(appearance, lambda _: False)
        sorted_subtree_tokens = sort_tokens(appearance_sub_tree)
        appearance_start = sorted_subtree_tokens[0].idx
        appearance_end = sorted_subtree_tokens[-1].idx+len(sorted_subtree_tokens[-1].text)
        appearances_data[sentence.text] = appearances_data.get(sentence.text, [])
        appearances_data[sentence.text] += [appearance_start-sentence.start_char, appearance_end-sentence.start_char]
    dictionary_utils.set_at(entity.entity_data, ['text', 'aprs'], appearances_data)


def _group_appearances_tokens_into_same_sentences(appearances: Set[Token | Token]) -> List[Tuple[Span, List[Token]]]:
    sentences_to_appearances_in_it = {}
    for appearance in appearances: sentences_to_appearances_in_it[appearance.sent] = sentences_to_appearances_in_it.get(appearance.sent, []) + [appearance]
    pairs = [(s, a) for s, a in sentences_to_appearances_in_it.items()]
    return pairs


def _construct_sentences_with_appearance_representation(appearances_in_sentences: List[Tuple[Span, List[Token]]]):
    appearance_sentences = set()
    for sentence_and_appearances in appearances_in_sentences:
        sentence_text = _construct_appearance_representation_of_sentence(sentence_and_appearances)
        appearance_sentences.add(sentence_text)
    return list(appearance_sentences)


def _construct_appearance_representation_of_sentence(appearances_in_sentence: Tuple[Span, List[Token]]) -> str:
    sentence = [token for token in appearances_in_sentence[0]] + [SimpleNamespace(text='', ent_type=-1, i=-1)]
    sentence_appearances = appearances_in_sentence[1]
    sentence_text = ''
    current_span = {'type': 0, 'text': '', 'is_target': False}
    for sentence_token in sentence:
        token_entity_type = sentence_token.ent_type
        is_token_in_appearances = (sentence_token.text and sentence_token in sentence_appearances)
        if token_entity_type == current_span['type']:
            current_span['text'] += ' ' + sentence_token.text
            current_span['is_target'] = current_span['is_target'] or is_token_in_appearances
            continue
        span_text = " ".join(current_span['text'].split())
        span_text = (' <t>{}</t>' if current_span['is_target'] else ' <e>{}</e>' if current_span['type'] else ' {}').format(span_text)
        sentence_text += span_text
        current_span = {'text': sentence_token.text, 'type': token_entity_type, 'is_target': is_token_in_appearances}
    sentence_text = " ".join(sentence_text.split())
    return sentence_text
