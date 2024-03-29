from typing import Set

from src.modules.aws_clients.dynamodb_client import DynamoDBTableManager
from src.modules.aws_clients.s3_client import S3BucketManager
from src.modules.dictionary_utils import dictionary_utils
from src.modules.masslaw_case_data_formatting import masslaw_case_data_formatting
from src.modules.masslaw_case_users_management import MasslawCaseUserAccessManager
from src.modules.masslaw_case_users_management import masslaw_case_users_management_exceptions
from src.modules.masslaw_cases_config import storage_config
from src.modules.masslaw_cases_objects import MasslawCaseCommentInstance
from src.modules.masslaw_cases_objects import MasslawCaseFileInstance
from src.modules.masslaw_cases_objects import MasslawCaseInstance


class MasslawCaseDataCollector:

    def __init__(self, case_instance: MasslawCaseInstance, access_user_id: str = None):
        self.__access_user_id = access_user_id
        self.__case_instance = case_instance
        if self.__access_user_id:
            access_manager = MasslawCaseUserAccessManager(case_instance)
            self.__case_instance = access_manager.get_formatted_case_instance_for_user(self.__access_user_id)

    def get_case_data(self):
        case_data = masslaw_case_data_formatting.get_case_data_full_format_from_db_item(self.__case_instance.get_data_property([], {}), self.__access_user_id or '')
        return case_data

    def get_case_content_hierarchy(self):
        case_content = self.__case_instance.get_data_property(['content'], {})
        return case_content

    def get_file_data(self, file_id):
        case_files = self.__case_instance.get_data_property(['files'], [])
        if not file_id in case_files:
            raise masslaw_case_users_management_exceptions.MasslawCaseUnauthorizedUserActionException(f"An attempt was made to get the data of a file which is not included in a user's case permissions")
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

    def get_case_knowledge(self) -> dict:
        s3_bucket_manager = S3BucketManager(storage_config.CASES_KNOWLEDGE_BUCKET_ID)
        s3_knowledge_key = f'{self.__case_instance.get_case_id()}/knowledge.json'
        knowledge_data = s3_bucket_manager.get_object(s3_knowledge_key)
        if not knowledge_data: return {
            'connections': [],
            'entities': []
        }
        knowledge = dictionary_utils.ensure_dict(knowledge_data)
        case_files = set(self.__case_instance.get_data_property(['files'], []))
        for entity in knowledge.get('entities', []):
            entity_files = set(dictionary_utils.get_from(entity, ['properties', 'files', 'list'], []))
            dictionary_utils.set_at(entity, ['files', 'list'], list(entity_files & case_files))
        for connection in knowledge.get('connections', []):
            connection_files = set(dictionary_utils.get_from(connection, ['properties', 'files', 'list'], []))
            dictionary_utils.set_at(connection, ['properties', 'files', 'list'], list(connection_files & case_files))
        knowledge['entities'] = [entity for entity in knowledge.get('entities', []) if dictionary_utils.get_from(entity, ['properties', 'files', 'list'], [])]
        knowledge['connections'] = [connection for connection in knowledge.get('connections', []) if dictionary_utils.get_from(connection, ['properties', 'files', 'list'], [])]
        return knowledge
