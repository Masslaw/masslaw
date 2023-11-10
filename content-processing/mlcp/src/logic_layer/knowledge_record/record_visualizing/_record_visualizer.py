from typing import Callable

from logic_layer.knowledge_record import KnowledgeRecordEntity
from logic_layer.knowledge_record._record import KnowledgeRecord
from logic_layer.knowledge_record.record_visualizing._mermaid_implementation import knowledge_record_to_mermaid


class KnowledgeRecordGraphVisualizer:

    def __init__(self, record: KnowledgeRecord):
        self._record = record

    def visualize_using_mermaid(self, output_mermaid_script_file: str, node_title_generator: Callable[[KnowledgeRecordEntity], str] = None):
        knowledge_record_to_mermaid(self._record, output_mermaid_script_file, node_title_generator)
