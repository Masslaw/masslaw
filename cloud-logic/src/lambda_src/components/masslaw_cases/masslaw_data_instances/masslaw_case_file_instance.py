import time

from ..config.files_config import FILE_DESCRIPTION_LENGTH_HARD_LIMIT
from ...util.dynamodb_data_holder import DynamodbDataHolder


class MasslawCaseFileDataUpdateException(Exception): pass


class MasslawCaseFileInstance(DynamodbDataHolder):
    def __init__(self, file_id: str):
        DynamodbDataHolder.__init__(self, "MasslawFiles", file_id)

    def get_file_id(self):
        return DynamodbDataHolder.get_item_id(self)

    def save_data(self):
        self.update_last_updated_time()
        DynamodbDataHolder.save_data(self)

    def update_last_updated_time(self):
        self.set_data_property(['last_modified'], str(int(time.time())))

    def _assert_valid_data(self):
        DynamodbDataHolder._assert_valid_data(self)

        description = self.get_data_property(['description'], '')
        if len(description) > FILE_DESCRIPTION_LENGTH_HARD_LIMIT:
            raise MasslawCaseFileDataUpdateException(f'description length exceeds hard limit {FILE_DESCRIPTION_LENGTH_HARD_LIMIT}')
