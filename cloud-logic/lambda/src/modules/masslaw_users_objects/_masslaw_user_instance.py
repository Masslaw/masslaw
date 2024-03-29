import re

from src.modules.aws_clients.cognito_client import CognitoUserPoolManager
from src.modules.aws_clients.dynamodb_client import DynamoDBTableManager
from src.modules.aws_clients.open_search_client import OpenSearchIndexManager
from src.modules.dictionary_utils import dictionary_utils
from src.modules.masslaw_users_config import read_only_user_attributes
from src.modules.masslaw_users_objects._exceptions import MasslawUserDataUpdateException
from src.modules.remote_data_management import DataHolder
from src.modules.masslaw_users_config import opensearch_config

cognitoManager = CognitoUserPoolManager("MasslawUsers")
users_table_manager = DynamoDBTableManager('MasslawUsers')


class MasslawUserInstance(DataHolder):

    def __init__(self, user_id: str = None, access_token: str = None):
        self.__user_id = user_id or cognitoManager.get_user_id_by_access_token(access_token)
        DataHolder.__init__(self)

    def load_data(self):
        DataHolder.load_data(self)
        if not self.__user_id: return False
        user_data = {}
        user_data.update(cognitoManager.get_user_by_id(self.__user_id) or {})
        user_data.update(users_table_manager.get_item(self.__user_id) or {})
        user_data = dictionary_utils.ensure_dict(user_data)
        self._set_data(user_data)
        return True

    def save_data(self):
        DataHolder.save_data(self)
        self._save_data_to_dynamodb()
        self._save_data_to_opensearch()
        self._valid = True

    def _save_data_to_dynamodb(self):
        write_user_data = self._get_write_data_object()
        users_table_manager.update_item(self.__user_id, write_user_data)

    def _save_data_to_opensearch(self):
        opensearch_document = self._get_opensearch_document()
        users_index_manager = OpenSearchIndexManager(opensearch_config.MASSLAW_USERS_OPENSEARCH_ENDPOINT, opensearch_config.MASSLAW_USERS_OPENSEARCH_INDEX_NAME)
        users_index_manager.ensure_exists()
        users_index_manager.add_document(self.__user_id, opensearch_document)

    def get_user_id(self):
        return self.__user_id

    def _get_write_data_object(self):
        user_data = self._get_data()
        for attr in read_only_user_attributes.READ_ONLY_USER_ATTRIBUTES:
            if attr in user_data:
                del user_data[attr]
        return user_data

    def _get_opensearch_document(self):
        user_data = self._get_data()
        document = dictionary_utils.select_keys(user_data, ['User_ID', 'email', 'first_name', 'last_name'])
        return document

    def _assert_valid_data(self):
        DataHolder._assert_valid_data(self)

        provided_first_name = self.get_data_property(['first_name'], '')
        if len(provided_first_name) < 1:
            raise MasslawUserDataUpdateException('invalid first name')

        provided_last_name = self.get_data_property(['last_name'], '')
        if len(provided_last_name) < 1:
            raise MasslawUserDataUpdateException('invalid last name')

        provided_email = self.get_data_property(['email'], '')
        if len(provided_email) <= 2 or not bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', provided_email)):
            raise MasslawUserDataUpdateException('invalid email address')
