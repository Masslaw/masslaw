from get_case_files_data.modules.remote_data_management import DataHolder
from get_case_files_data.modules.aws_clients.dynamodb_client import DynamoDBTableManager
from get_case_files_data.modules.dictionary_utils import dictionary_utils


class DynamodbDataHolder(DataHolder):
    def __init__(self, table_name: str, item_id: str, locked_attributes=None):
        self._db_manager = DynamoDBTableManager(table_name)
        self._item_id = item_id
        locked_attributes = locked_attributes or []
        locked_attributes.append(self._db_manager.get_primary_key_name())
        DataHolder.__init__(self, locked_attributes)

    def get_item_id(self):
        return self._item_id

    def load_data(self):
        DataHolder.load_data(self)
        item = self._db_manager.get_item(self._item_id, None)
        if item is None: return False
        self._set_data(item)
        return True

    def save_data(self):
        DataHolder.save_data(self)
        data = self._get_data()
        update_data = dictionary_utils.select_keys(data, self._updated_attributes)
        self._db_manager.update_item(self._item_id, update_data)
