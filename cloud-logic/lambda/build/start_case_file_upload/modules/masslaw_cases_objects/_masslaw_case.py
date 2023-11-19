import time

from start_case_file_upload.modules.aws_clients.dynamodb_client import DynamoDBTableManager
from start_case_file_upload.modules.masslaw_cases_objects._exceptions import MasslawCaseDataUpdateException
from start_case_file_upload.modules.remote_data_management_dynamodb import DynamodbDataHolder

dbManager = DynamoDBTableManager("MasslawCases")


class MasslawCaseInstance(DynamodbDataHolder):
    def __init__(self, case_id: str):
        DynamodbDataHolder.__init__(self, "MasslawCases", case_id)

    def get_case_id(self):
        return DynamodbDataHolder.get_item_id(self)

    def save_data(self):
        self.update_last_updated_time()
        DynamodbDataHolder.save_data(self)

    def update_last_updated_time(self):
        self.set_data_property(['information', 'last_modified_time'], str(int(time.time())))

    def _assert_valid_data(self):
        DynamodbDataHolder._assert_valid_data(self)

        provided_title = self.get_data_property(['information', 'title'], '')
        if len(provided_title) <= 2 or len(provided_title) > 100:
            raise MasslawCaseDataUpdateException('invalid title')

        provided_description = self.get_data_property(['information', 'description'], '')
        if len(provided_description) <= 2 or len(provided_description) > 1000:
            raise MasslawCaseDataUpdateException('invalid description')
