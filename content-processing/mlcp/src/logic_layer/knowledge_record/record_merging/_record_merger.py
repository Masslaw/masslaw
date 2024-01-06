from logic_layer.knowledge_record import KnowledgeRecord
from logic_layer.knowledge_record.record_merging._record_merging_logic import merge_records


class RecordMergingConfiguration:
    entity_mergeability_check_function: callable = lambda self, e1, e2: False
    connection_mergeability_check_function: callable = lambda self, c1, c2: False

    def __init__(self, entity_mergeability_check_function: callable = None, connection_mergeability_check_function: callable = None):
        self.entity_mergeability_check_function = entity_mergeability_check_function or self.entity_mergeability_check_function
        self.connection_mergeability_check_function = connection_mergeability_check_function or self.connection_mergeability_check_function


class RecordMerger:

    def __init__(self, target_record: KnowledgeRecord, merge_configuration: RecordMergingConfiguration):
        self._target_record = target_record
        self._merge_configuration = merge_configuration

    def merge_record(self, another_record: KnowledgeRecord):
        merge_records(self._target_record, another_record, self._merge_configuration.entity_mergeability_check_function, self._merge_configuration.connection_mergeability_check_function)

    def set_merge_configuration(self, merge_configuration: RecordMergingConfiguration):
        self._merge_configuration = merge_configuration
