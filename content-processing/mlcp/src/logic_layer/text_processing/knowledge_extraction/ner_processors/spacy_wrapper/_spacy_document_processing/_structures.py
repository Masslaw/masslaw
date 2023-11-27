from contextvars import Token
from typing import List
from typing import Set

from spacy.tokens.doc import Doc
from spacy.tokens.span import Span


class CoreferenceChain:
    chain_tokens: Set[Token]
    chain_subjects: Set[Span]
    chain_entities: Set[Span]


class DocumentEntity:
    entity_spans: Set[Span] = set()
    entity_type: str = None
    entity_data: dict = {}
    entity_appearances: Set[Token]
    coreference_chains: Set[CoreferenceChain]


class DocumentEntityRelation:
    relation_type: str = 'connection'
    from_entity: DocumentEntity = None
    to_entity: DocumentEntity = None
    relating_tokens: Set[Token]
    relation_data: dict = {}
    relation_strength: float = 0.0


class SpacyDocumentData:
    spacy_document: Doc = None
    coreference_chains: Set[CoreferenceChain]
    document_entities: Set[DocumentEntity]
    document_relations: Set[DocumentEntityRelation]
    def __init__(self, spacy_document): self.spacy_document = spacy_document
