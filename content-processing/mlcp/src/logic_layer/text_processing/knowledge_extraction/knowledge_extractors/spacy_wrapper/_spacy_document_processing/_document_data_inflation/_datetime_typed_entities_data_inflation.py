import re
from typing import List
from typing import Set

from dateutil import parser

from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy._common import get_token_dependency_chain
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._structures import DocumentEntity


def inflate_datetime_entity_data(entities: List[DocumentEntity] | Set[DocumentEntity]):
    date_typed_entities = [entity for entity in entities if entity.entity_span.label_ in ("DATE", "TIME",)]
    _load_entity_titles(date_typed_entities)
    _parse_datetimes(date_typed_entities)


def _load_entity_titles(date_entities: List[DocumentEntity]):
    for entity in date_entities:
        entity_span = entity.entity_span
        chain = get_token_dependency_chain(entity_span.root, ['compound', 'nummod', 'nmod'])
        span_tokens = entity_span.doc[min(chain[0].i, entity_span.start):max(entity_span[-1].i + 1, entity_span.end)]
        entity_title = ' '.join([token.text for token in span_tokens])
        entity.entity_data['title'] = entity_title


def _parse_datetimes(datetime_entities: List[DocumentEntity]):
    for entity in datetime_entities:
        entity_title = entity.entity_data.get('title')
        datetime_string = _replace_common_unparseable_expressions_with_parsable_text(entity_title)
        try:
            parsed_datetime_iso = _parse_datetime(datetime_string)
            entity.entity_data['datetime'] = parsed_datetime_iso
        except parser.ParserError:
            continue


def _parse_datetime(datetime_string: str) -> dict:
    parsed_datetime = parser.parse(datetime_string)
    date_time_data = {
        'Y': parsed_datetime.year,
        'M': parsed_datetime.month,
        'D': parsed_datetime.day,
        'h': parsed_datetime.hour,
        'm': parsed_datetime.minute,
        's': parsed_datetime.second,
    }
    if not _search_in_string_as_whole(str(parsed_datetime.year), datetime_string) and not _search_in_string_as_whole(str(parsed_datetime.year)[-2:], datetime_string):
        date_time_data.pop('Y')
    return date_time_data


def _search_in_string_as_whole(substring: str, string: str) -> bool:
    return re.search(r'\b' + re.escape(substring) + r'\b', string) is not None


def _replace_common_unparseable_expressions_with_parsable_text(text: str) -> str:
    common_unparseable_expressions_to_parseable_representations = {
        'morning': '6:00',
        'evening': '18:00',
        'night': '21:00',
        'noon': '12:00',
        'midnight': '00:00',
        'spring': 'March',
        'summer': 'June',
        'autumn': 'September',
        'winter': 'December',
    }
    text = text.lower()
    for unparseable_expression, parseable_representation in common_unparseable_expressions_to_parseable_representations.items():
        text = text.replace(unparseable_expression, parseable_representation)
    return text
