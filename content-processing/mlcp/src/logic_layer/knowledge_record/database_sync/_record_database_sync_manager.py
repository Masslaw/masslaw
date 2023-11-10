from logic_layer.knowledge_record._record import KnowledgeRecord
from logic_layer.knowledge_record.database_sync._sync_logic import sync_record_with_graph_database
from logic_layer.remote_graph_database._graph_database_manager import GraphDatabaseManager


class RecordDatabaseSyncManager:

    def __init__(self, record: KnowledgeRecord):
        self._record = record

    def sync_with_database(self, database_manager: GraphDatabaseManager):
        sync_record_with_graph_database(database_manager, self._record)
