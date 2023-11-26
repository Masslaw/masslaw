from typing import List

from logic_layer.text_processing.named_entity_recognition.ner_processors.spacy_wrapper._spacy import common
from logic_layer.text_processing.named_entity_recognition.ner_processors.spacy_wrapper._spacy_document_processing._structures import CoreferenceChain
from logic_layer.text_processing.named_entity_recognition.ner_processors.spacy_wrapper._spacy_document_processing._structures import SpacyDocumentData


class SpacyCoreferencesResolver:

    def __init__(self, document_data: SpacyDocumentData):
        self._document_data = document_data
        self._coreference_chains: List[CoreferenceChain] = []

    def resolve_coreferences(self):
        self._load_coreference_chains()
        self._resolve_chain_subjects()
        self._resolve_chain_entities()
        self._document_data.coreference_chains = self._coreference_chains

    def _load_coreference_chains(self):
        spacy_document = self._document_data.spacy_document
        for coref_chain in spacy_document._.coref_chains:
            chain = CoreferenceChain()
            chain.chain_tokens = set([spacy_document[idx] for mention in coref_chain for idx in mention.token_indexes])
            self._coreference_chains.append(chain)

    def _resolve_chain_subjects(self):
        for chain in self._coreference_chains:
            chain.chain_subjects = set([token for token in chain.chain_tokens if token.pos_ != "PRON"])

    def _resolve_chain_entities(self):
        for chain in self._coreference_chains:
            chain.chain_entities = set()
            spacy_document = self._document_data.spacy_document
            for token in chain.chain_tokens:
                entity_span = common.get_entity_span_for_token(token)
                if not entity_span: continue
                chain.chain_entities.add(entity_span)
