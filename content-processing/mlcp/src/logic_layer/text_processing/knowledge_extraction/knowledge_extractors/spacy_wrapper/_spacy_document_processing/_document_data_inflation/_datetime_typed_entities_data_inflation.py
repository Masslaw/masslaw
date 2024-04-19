import datetime
import re
from typing import List
from typing import Set

from dateutil import parser

from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy._common import get_token_dependency_chain
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._structures import DocumentEntity
from shared_layer.mlcp_logger import logger
from shared_layer.mlcp_logger import common_formats
from shared_layer.dictionary_utils import dictionary_utils

common_unparseable_expressions_to_parseable_representations = {'morning': '6:00', 'evening': '18:00', 'night': '21:00', 'noon': '12:00', 'afternoon': '16:00', 'midnight': '00:00', 'spring': 'March', 'summer': 'June', 'autumn': 'September', 'winter': 'December', }

inferable_datetime_units = {'morning': {'h': 6}, 'evening': {'h': 18}, 'night': {'h': 21}, 'noon': {'h': 12}, 'afternoon': {'h': 16}, 'midnight': {'h': 0}, 'spring': {'M': 3}, 'summer': {'M': 6}, 'autumn': {'M': 9}, 'winter': {'M': 12}, 'jan': {'M': 1},
                            'january': {'M': 1}, 'feb': {'M': 2}, 'february': {'M': 2}, 'mar': {'M': 3}, 'march': {'M': 3}, 'apr': {'M': 4}, 'april': {'M': 4}, 'may': {'M': 5}, 'jun': {'M': 6}, 'june': {'M': 6}, 'jul': {'M': 7},
                            'july': {'M': 7}, 'aug': {'M': 8}, 'august': {'M': 8}, 'sep': {'M': 9}, 'september': {'M': 9}, 'oct': {'M': 10}, 'october': {'M': 10}, 'nov': {'M': 11}, 'november': {'M': 11}, 'dec': {'M': 12},
                            'december': {'M': 12}}


@logger.process_function("Inflating datetime typed entities data")
def inflate_datetime_entity_data(entities: List[DocumentEntity] | Set[DocumentEntity]):
    date_typed_entities = [entity for entity in entities if entity.entity_span.label_ in ("DATE", "TIME",)]
    logger.debug(f"Inflating {common_formats.value(len(date_typed_entities))} datetime typed entities data")
    _load_entity_titles(date_typed_entities)
    _parse_datetimes(date_typed_entities)


def _load_entity_titles(date_entities: List[DocumentEntity]):
    for entity in date_entities:
        entity_span = entity.entity_span
        chain = get_token_dependency_chain(entity_span.root, ['compound', 'nummod', 'nmod'])
        span_tokens = entity_span.doc[min(chain[0].i, entity_span[0].i):max(chain[-1].i + 1, entity_span[-1].i + 1)]
        entity_title = ' '.join([token.text for token in span_tokens])
        entity_title = entity_title.replace('\n', ' ')
        entity_title = re.sub(r'\s+', ' ', entity_title)
        entity.entity_data['title'] = entity_title


@logger.process_function("Parsing datetime strings")
def _parse_datetimes(datetime_entities: List[DocumentEntity]):
    datetime_entities.sort(key=lambda entity: entity.entity_span.root.i)
    last_date = {}
    for entity in datetime_entities:
        entity_title = entity.entity_data.get('title')
        logger.debug(f"datetime entity title: {common_formats.value(entity_title)}")
        parsed_datetime_data = _parse_datetime(entity_title)
        logger.debug(f"parsed datetime data: {common_formats.value(parsed_datetime_data)}")
        if not (parsed_datetime_data.keys() & {'Y', 'M', 'D'}): continue
        _attempt_to_fill_current_date_with_last(parsed_datetime_data, last_date)
        logger.debug(f"parsed datetime data after filling: {common_formats.value(parsed_datetime_data)}")
        entity.entity_data['datetime'] = parsed_datetime_data
        last_date = parsed_datetime_data


@logger.process_function("Parsing a datetime string")
def _parse_datetime(datetime_string: str) -> dict:
    logger.debug(f"original string: {common_formats.value(datetime_string)}")
    parsable_string = _construct_parsable_string(datetime_string)
    logger.debug(f"parseable string: {common_formats.value(parsable_string)}")
    date_time_data = _get_datetime_data_from_string(parsable_string)
    logger.debug(f"raw datetime data: {common_formats.value(date_time_data)}")
    _remove_nonexisting_numbers_from_date_time_data(datetime_string, date_time_data)
    logger.debug(f"datetime data after removing nonexisting numbers: {common_formats.value(date_time_data)}")
    easily_inferable_datetime_units = _get_easily_inferable_datetime_units(datetime_string)
    logger.debug(f"easily inferable datetime units: {common_formats.value(easily_inferable_datetime_units)}")
    date_time_data.update(easily_inferable_datetime_units)
    logger.debug(f"final datetime data: {common_formats.value(date_time_data)}")
    return date_time_data


@logger.process_function("Constructing a parsable datetime string")
def _construct_parsable_string(datetime_string: str) -> str:
    parsable_string = datetime_string.lower()
    parsable_string = _replace_common_unparseable_expressions_with_parsable_text(parsable_string)
    return parsable_string


@logger.process_function("Replacing common unparseable expressions with parsable text")
def _replace_common_unparseable_expressions_with_parsable_text(text: str) -> str:
    text = text.lower()
    for unparseable_expression, parseable_representation in common_unparseable_expressions_to_parseable_representations.items():
        text = re.sub(r'\b' + re.escape(unparseable_expression) + r'\b', parseable_representation, text)
    return text


@logger.process_function("Getting datetime data from a string")
def _get_datetime_data_from_string(datetime_string: str) -> dict:
    date_time_data = {}
    try:
        parsed_datetime = parser.parse(datetime_string, fuzzy=True)
        if parsed_datetime.year: date_time_data['Y'] = parsed_datetime.year
        if parsed_datetime.month: date_time_data['M'] = parsed_datetime.month
        if parsed_datetime.day: date_time_data['D'] = parsed_datetime.day
        if parsed_datetime.hour: date_time_data['h'] = parsed_datetime.hour
        if parsed_datetime.minute: date_time_data['m'] = parsed_datetime.minute
        if parsed_datetime.second: date_time_data['s'] = parsed_datetime.second
    except parser.ParserError: pass
    return date_time_data


@logger.process_function("Removing nonexisting numbers from datetime data")
def _remove_nonexisting_numbers_from_date_time_data(datetime_string: str, date_time_data: dict):
    nonexisting_keys = []
    for key, value in date_time_data.items():
        value_string = str(value)
        value_string = value_string[-2:]  # take only the last two digits
        if value_string not in datetime_string: nonexisting_keys.append([key])
    dictionary_utils.delete_keys(date_time_data, nonexisting_keys)


@logger.process_function("Getting easily inferable datetime units from a string")
def _get_easily_inferable_datetime_units(text: str):
    text = text.lower()
    datetime_data = {}
    for expression, datetime_data_update in inferable_datetime_units.items():
        if expression in text: datetime_data.update(datetime_data_update)
    return datetime_data


@logger.process_function("Attempting to fill current date with last date")
def _attempt_to_fill_current_date_with_last(date_time_data: dict, last_date: dict) -> dict:
    for key in ['Y', 'M', 'D']:
        if key in date_time_data: return;
        if key not in last_date: return;
        date_time_data[key] = last_date[key]
