from logic_layer.knowledge_record._record import KnowledgeRecord
from logic_layer.knowledge_record.database_sync._sync_logic import sync_record_with_graph_database
from logic_layer.knowledge_record.record_merging import RecordMergingConfiguration
from logic_layer.remote_graph_database._graph_database_manager import GraphDatabaseManager


class RecordDatabaseSyncManager:

    def __init__(self, record: KnowledgeRecord, merging_configuration: RecordMergingConfiguration):
        self._record = record
        self._merging_configuration = merging_configuration

    def sync_with_database(self, database_manager: GraphDatabaseManager):
        sync_record_with_graph_database(self._record, database_manager, self._merging_configuration)
