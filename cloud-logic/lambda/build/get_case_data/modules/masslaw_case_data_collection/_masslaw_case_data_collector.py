from get_case_data.modules.aws_clients.dynamodb_client import DynamoDBTableManager
from get_case_data.modules.masslaw_case_data_formatting import masslaw_case_data_formatting
from get_case_data.modules.masslaw_case_users_management import MasslawCaseUserAccessManager
from get_case_data.modules.masslaw_case_users_management import masslaw_case_users_management_exceptions
from get_case_data.modules.masslaw_cases_objects import MasslawCaseInstance


class MasslawCaseDataCollector:

    def __init__(self, case_instance: MasslawCaseInstance, access_user_id: str = None):
        self.__access_user_id = access_user_id
        if self.__access_user_id:
            access_manager = MasslawCaseUserAccessManager(case_instance)
            self.__case_instance = access_manager.get_formatted_case_instance_for_user(self.__access_user_id)
        else:
            self.__case_instance = case_instance

    def get_case_data(self):
        case_data = masslaw_case_data_formatting.get_case_data_full_format_from_db_item(self.__case_instance.get_data_property([], {}), self.__access_user_id or '')
        return case_data

    def get_case_base_data(self):
        case_data = masslaw_case_data_formatting.get_case_data_base_format_from_db_item(self.__case_instance.get_data_property([], {}), self.__access_user_id or '')
        return case_data

    def get_case_files_data(self):
        case_files = self.__case_instance.get_data_property(['files'], [])

        table_manager = DynamoDBTableManager("MasslawFiles")
        items_data = table_manager.batch_get_items(case_files)
        return [masslaw_case_data_formatting.get_case_file_data_base_format_from_db_item(item_data=item_data) for item_data in items_data]

    def get_file_data(self, file_id):
        case_files = self.__case_instance.get_data_property(['files'], [])
        if not file_id in case_files:
            raise masslaw_case_users_management_exceptions.MasslawCaseUnauthorizedUserActionException(f"An attempt was made to get the data of a file which is not included in a user's case permissions")

        table_manager = DynamoDBTableManager("MasslawFiles")
        item_data = table_manager.get_item(file_id)
        file_data = masslaw_case_data_formatting.get_case_file_data_full_format_from_db_item(item_data)
        return file_data

    def get_file_annotations(self, file_id):
        case_files = self.__case_instance.get_data_property(['files'], [])
        if not file_id in case_files:
            raise masslaw_case_users_management_exceptions.MasslawCaseUnauthorizedUserActionException(
                f"An attempt was made to get the data of a file which is not included in a user's case permissions")

        files_table_manager = DynamoDBTableManager("MasslawFiles")
        file_data = files_table_manager.get_item(file_id)

        annotations_table_manager = DynamoDBTableManager("MasslawFileAnnotations")
        items_data = annotations_table_manager.batch_get_items(file_data.get("annotations", []))

        return items_data
