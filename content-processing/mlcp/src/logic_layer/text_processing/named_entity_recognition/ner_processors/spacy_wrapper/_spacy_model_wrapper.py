import spacy

from logic_layer.knowledge_record import KnowledgeRecord


class SpacyModelWrapper:

    def __init__(self, spacy_model: spacy.Language):
        self._model = spacy_model
        self._knowledge_record = KnowledgeRecord()

    def load_text(self, text: str) -> KnowledgeRecord:
        ...

    def get_record(self) -> KnowledgeRecord:
        return self._knowledge_record
