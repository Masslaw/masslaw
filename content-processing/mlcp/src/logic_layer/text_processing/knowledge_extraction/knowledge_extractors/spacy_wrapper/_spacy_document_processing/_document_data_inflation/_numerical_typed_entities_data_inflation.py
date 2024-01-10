from typing import List
from typing import Set

from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy._common import get_token_dependency_chain
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._structures import DocumentEntity


def inflate_numerical_entity_data(entitise: List[DocumentEntity] | Set[DocumentEntity]):
    numerical_typed_entities = [entity for entity in entitise if entity.entity_span.label_ in ("QUANTITY", "CARDINAL", 'ORDINAL', 'PERCENT', "MONEY", )]
    _load_entity_titles(numerical_typed_entities)


def _load_entity_titles(numerical_entities: List[DocumentEntity]):
    for entity in numerical_entities:
        entity_span = entity.entity_span
        chain = get_token_dependency_chain(entity_span.root, ['compound', 'nummod', 'nmod'])
        span_tokens = entity_span.doc[min(chain[0].i, entity_span.start):max(entity_span[-1].i + 1, entity_span.end)]
        entity_title = ' '.join([token.text for token in span_tokens])
        entity.entity_data['title'] = entity_title.replace('\n', ' ')
