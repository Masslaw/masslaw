from typing import List
from typing import Set

from dateutil import parser
from spacy.tokens.span import Span

from logic_layer.text_processing.named_entity_recognition.ner_processors.spacy_wrapper._spacy_document_processing._structures import DocumentEntity
from shared_layer.list_utils import list_utils


def inflate_datetime_entity_data(entities: List[DocumentEntity] | Set[DocumentEntity]):
    date_typed_entities = [entity for entity in entities if entity.entity_type in ("DATE", "TIME",)]
    _parse_datetimes(date_typed_entities)
    _merge_mergable_datetime_entities(date_typed_entities)


def _parse_datetimes(datetime_entities: List[DocumentEntity]):
    for entity in datetime_entities:
        predicted_datetimes = []
        for entity_span in entity.entity_spans:
            datetime_string = _get_parseable_datetime_string_from_span(entity_span)
            try:
                parsed_datetime_iso = parser.parse(datetime_string).isoformat()
                predicted_datetimes.append(parsed_datetime_iso)
            except parser.ParserError:
                continue
        if not predicted_datetimes: continue
        mostly_predicted_date_iso = max(set(predicted_datetimes), key=predicted_datetimes.count)
        entity.entity_data['iso'] = mostly_predicted_date_iso


def _get_parseable_datetime_string_from_span(datetime_entity_span: Span) -> str:
    span_tokens = [datetime_entity_span.doc[i] for i in range(datetime_entity_span.start, datetime_entity_span.end + 1)]
    filtered_tokens = [token for token in span_tokens if token.pos_ not in ("DET", "ADP", "PUNCT")]
    text = ' '.join([token.text for token in filtered_tokens])
    text = _replace_common_unparseable_expressions_with_parsable_text(text)
    return text


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
