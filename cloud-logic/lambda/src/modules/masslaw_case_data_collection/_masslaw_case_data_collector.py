from src.modules.aws_clients.dynamodb_client import DynamoDBTableManager
from src.modules.masslaw_case_data_formatting import masslaw_case_data_formatting
from src.modules.masslaw_case_users_management import MasslawCaseUserAccessManager
from src.modules.masslaw_cases_objects import MasslawCaseCommentInstance
from src.modules.masslaw_cases_objects import MasslawCaseFileInstance
from src.modules.masslaw_cases_objects import MasslawCaseInstance


class MasslawCaseDataCollector:

    def __init__(self, case_instance: MasslawCaseInstance, access_user_id: str):
        self.__access_user_id = access_user_id
        self.__access_manager = MasslawCaseUserAccessManager(case_instance)
        self.__case_instance = self.__access_manager.get_formatted_case_instance_for_user(self.__access_user_id)

    def get_case_data(self):
        case_data = masslaw_case_data_formatting.get_case_data_full_format_from_db_item(self.__case_instance.get_data_property([], {}), self.__access_user_id or '')
        return case_data

    def get_case_content_hierarchy(self):
        case_content = self.__case_instance.get_data_property(['content'], {})
        return case_content

    def get_file_data(self, file_id):
        table_manager = DynamoDBTableManager("MasslawFiles")
        item_data = table_manager.get_item(file_id)
        file_data = masslaw_case_data_formatting.get_case_file_data_full_format_from_db_item(item_data)
        return file_data

    def get_case_file_comments_data(self, file_id: str):
        comment_instance = MasslawCaseFileInstance(file_id)
        file_comments = comment_instance.get_data_property(['comments'], [])
        files_table_manager = DynamoDBTableManager("MasslawCaseComments")
        comments_data = files_table_manager.batch_get_items(list(file_comments))
        return [masslaw_case_data_formatting.get_case_comment_base_format_from_db_item(comment_data) for comment_data in comments_data]

    def get_case_comment_data(self, comment_id: str):
        comment_instance = MasslawCaseCommentInstance(comment_id)
        comment_instance_data = comment_instance.get_data_property([], {})
        return masslaw_case_data_formatting.get_case_comment_full_format_from_db_item(comment_instance_data)
