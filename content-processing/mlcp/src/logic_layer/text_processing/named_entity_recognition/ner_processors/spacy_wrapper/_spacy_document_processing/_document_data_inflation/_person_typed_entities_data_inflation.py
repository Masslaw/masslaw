from contextvars import Token
from typing import Dict
from typing import List
from typing import Set

from spacy.tokens.span import Span

from logic_layer.text_processing.named_entity_recognition.ner_processors.spacy_wrapper._spacy_document_processing._structures import DocumentEntity
from shared_layer.list_utils import list_utils


def inflate_person_entity_data(entitise: List[DocumentEntity]|Set[DocumentEntity]):
    person_typed_entities = [entity for entity in entitise if entity.entity_type == "PERSON"]
    _load_entity_titles(person_typed_entities)
    _load_entity_information_items(person_typed_entities)


def _load_entity_titles(person_entities: List[DocumentEntity]):
    for entity in person_entities:
        entity.entity_data['title'] = max(entity.entity_spans, key=lambda span: len(span.text)).text


def _load_entity_information_items(person_entities: List[DocumentEntity]):
    for entity in person_entities:
        entity_information_items = _get_entity_information_items(entity)
        information_items = [{'t': information_item.text, 's': information_item.start_char, 'e': information_item.end_char} for information_item in entity_information_items]
        _merge_mergable_information_items(information_items)
        entity.entity_data['information_items'] = information_items


def _get_entity_information_items(entity: DocumentEntity) -> Set[Span]:
    entity_information_items = set()
    for entity_span in entity.entity_spans:
        entity_information_items |= _get_information_about_a_person(entity_span.root)
    for entity_appearance in entity.entity_appearances:
        entity_information_items |= _get_information_about_a_person(entity_appearance)
    return entity_information_items


def _merge_mergable_information_items(information_items: List[Dict]):
    list_utils.merge_mergeable(information_items, _check_information_items_mergeable, _merge_information_items)

def _check_information_items_mergeable(i1: Dict, i2: Dict) -> bool:
    range_of_one_contains_the_other = not not set(range(i1.get('s'), i1.get('e'))) & set(range(i2.get('s'), i2.get('e')))
    if range_of_one_contains_the_other: return True
    text_of_one_contains_the_other = i1.get('t', '') in i2.get('t', '') or i2.get('t', '') in i1.get('t', '')
    if text_of_one_contains_the_other: return True
    return False

def _merge_information_items(i1: Dict, i2: Dict) -> Dict:
    return max(i1, i2, key=lambda i: len(i.get('t', '')))

def _get_information_about_a_person(person_token: Token) -> Set[Span]:
    information_items = set()
    document = person_token.doc
    for token in person_token.subtree:
        if token.dep_ in ["amod", "appos", "attr"] or token.pos_ in ["NOUN", "ADJ"]:
            information_items.add(document[min(token.subtree, key=lambda t: t.i).i: max(token.subtree, key=lambda t: t.i).i + 1])
    return information_items