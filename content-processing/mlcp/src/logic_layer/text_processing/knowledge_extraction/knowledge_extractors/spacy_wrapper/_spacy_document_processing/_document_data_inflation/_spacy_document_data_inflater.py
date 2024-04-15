from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._document_data_inflation._datetime_typed_entities_data_inflation import inflate_datetime_entity_data
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._document_data_inflation._document_relations_data_inflation import inflate_relations_data
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._document_data_inflation._general_entity_data_inflation import inflate_entity_data
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._document_data_inflation._numerical_typed_entities_data_inflation import inflate_numerical_entity_data
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._document_data_inflation._person_typed_entities_data_inflation import inflate_person_entity_data
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_document_processing._structures import SpacyDocumentData


class SpacyDocumentDataInflater:

    def __init__(self, document_data: SpacyDocumentData):
        self._document_data = document_data

    def generate_titles_for_entities(self):
        for entity in self._document_data.document_entities:
            entity.entity_data['title'] = entity.entity_span.text.replace('\n', ' ')

    def inflate_entity_data(self):
        inflate_person_entity_data(self._document_data.document_entities)
        inflate_datetime_entity_data(self._document_data.document_entities)
        inflate_numerical_entity_data(self._document_data.document_entities)
        inflate_entity_data(self._document_data.document_entities)

    def inflate_relations_data(self):
        inflate_relations_data(list(self._document_data.document_relations))
