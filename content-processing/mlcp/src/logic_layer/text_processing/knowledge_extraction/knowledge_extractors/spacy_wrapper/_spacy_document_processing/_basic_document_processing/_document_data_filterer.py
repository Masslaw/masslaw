from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._structures import DocumentEntity
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._structures import SpacyDocumentData


class DocumentDataFilterer:

    def __init__(self, document_data: SpacyDocumentData):
        self._document_data = document_data
        self._useless_entities = set()

    def filter_document_data(self):
        self._detect_useless_entities()
        self._filter_entities()
        self._filter_relations()

    def _detect_useless_entities(self):
        for entity in self._document_data.document_entities:
            if self._determine_entitiy_useless(entity):
                self._useless_entities.add(entity)
    def _determine_entitiy_useless(self, entity: DocumentEntity) -> bool:
        entity_title = entity.entity_data.get('title', '').lower()
        if not entity_title: return True
        if entity.entity_type in ('ORDINAL', ): return True
        if entity.entity_type in 'DATE' and 'old' in entity_title: return True
        if entity.entity_type in ('CARDINAL', 'QUANTITY') and sum(c.isdigit() for c in entity_title) < 4: return True
        return False

    def _filter_entities(self):
        self._document_data.document_entities = self._document_data.document_entities - self._useless_entities

    def _filter_relations(self):
        new_relations = set()
        for relation in self._document_data.document_relations:
            if relation.from_entity in self._useless_entities or relation.to_entity in self._useless_entities:
                continue
            new_relations.add(relation)
        self._document_data.document_relations = new_relations
