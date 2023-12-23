from typing import List
from typing import Set

from dateutil import parser
from spacy.tokens.span import Span

from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy._common import get_token_dependency_chain
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._structures import DocumentEntity
from shared_layer.list_utils import list_utils


def inflate_datetime_entity_data(entities: List[DocumentEntity] | Set[DocumentEntity]):
    date_typed_entities = [entity for entity in entities if entity.entity_type in ("DATE", "TIME",)]
    _load_entity_titles(date_typed_entities)
    _parse_datetimes(date_typed_entities)
    _merge_mergable_datetime_entities(date_typed_entities)
    _cleanup(date_typed_entities)


def _load_entity_titles(date_entities: List[DocumentEntity]):
    for entity in date_entities:
        entity_spans = entity.entity_spans
        possible_titles = set()
        for datetime_entity_span in entity_spans:
            chain = get_token_dependency_chain(datetime_entity_span.root, ['compound', 'nummod', 'nmod'])
            span_tokens = datetime_entity_span.doc[min(chain[0].i, datetime_entity_span.start):max(datetime_entity_span[-1].i + 1, datetime_entity_span.end)]
            possible_title = ' '.join([token.text for token in span_tokens])
            possible_titles.add(possible_title)
        final_title = max(possible_titles, key=lambda title: len(title))
        entity.entity_data['title'] = final_title
        entity.entity_data['possible_titles'] = possible_titles


def _parse_datetimes(datetime_entities: List[DocumentEntity]):
    for entity in datetime_entities:
        predicted_datetimes = []
        for possible_title in entity.entity_data.get('possible_titles', []):
            datetime_string = _replace_common_unparseable_expressions_with_parsable_text(possible_title)
            try:
                parsed_datetime_iso = parser.parse(datetime_string).isoformat()
                predicted_datetimes.append(parsed_datetime_iso)
            except parser.ParserError:
                continue
        if not predicted_datetimes: continue
        mostly_predicted_date_iso = max(set(predicted_datetimes), key=predicted_datetimes.count)
        entity.entity_data['iso'] = mostly_predicted_date_iso


def _replace_common_unparseable_expressions_with_parsable_text(text: str) -> str:
    common_unparseable_expressions_to_parseable_representations = {'morning': '6:00', 'evening': '18:00', 'night': '21:00', 'noon': '12:00', 'midnight': '00:00', 'spring': 'March', 'summer': 'June', 'autumn': 'September', 'winter': 'December', }
    text = text.lower()
    for unparseable_expression, parseable_representation in common_unparseable_expressions_to_parseable_representations.items():
        text = text.replace(unparseable_expression, parseable_representation)
    return text


def _merge_mergable_datetime_entities(entities: List[DocumentEntity]):
    list_utils.merge_mergeable(entities, _check_datetime_entities_mergeagle, _merge_datetime_entities)


def _check_datetime_entities_mergeagle(entity1: DocumentEntity, entity2: DocumentEntity) -> bool:
    if entity1.entity_type != entity2.entity_type: return False
    if not entity1.entity_type in ("DATE", "TIME",): return False
    if not entity2.entity_type in ("DATE", "TIME",): return False
    iso1 = entity1.entity_data.get('iso')
    iso2 = entity2.entity_data.get('iso')
    if iso1 and iso2 and iso1 == iso2: return True
    return False


def _merge_datetime_entities(entity1: DocumentEntity, entity2: DocumentEntity) -> DocumentEntity:
    merged_entity = DocumentEntity()
    merged_entity.entity_type = entity1.entity_type
    merged_entity.entity_spans = entity1.entity_spans | entity2.entity_spans
    merged_entity.entity_data = entity1.entity_data | entity2.entity_data
    merged_entity.entity_appearances = entity1.entity_appearances | entity2.entity_appearances
    merged_entity.coreference_chains = entity1.coreference_chains | entity2.coreference_chains
    return merged_entity


def _cleanup(datetime_entities: List[DocumentEntity]):
    for entity in datetime_entities:
        entity.entity_data.pop('possible_titles', None)
