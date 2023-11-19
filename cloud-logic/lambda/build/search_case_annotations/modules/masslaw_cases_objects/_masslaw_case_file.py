import time

from search_case_annotations.modules.masslaw_cases_config import files_config
from search_case_annotations.modules.masslaw_cases_objects._exceptions import MasslawCaseFileDataUpdateException
from search_case_annotations.modules.remote_data_management_dynamodb import DynamodbDataHolder


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
        if len(description) > files_config.FILE_DESCRIPTION_LENGTH_HARD_LIMIT:
            raise MasslawCaseFileDataUpdateException(f'description length exceeds hard limit {files_config.FILE_DESCRIPTION_LENGTH_HARD_LIMIT}')
