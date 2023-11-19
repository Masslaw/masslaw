import re

from src.modules.aws_clients.cognito_client import CognitoUserPoolManager
from src.modules.masslaw_users_objects._exceptions import MasslawUserDataUpdateException
from src.modules.remote_data_management import DataHolder
from src.modules.dictionary_utils import dictionary_utils
from src.modules.masslaw_users_config import read_only_user_attributes


cognitoManager = CognitoUserPoolManager("MasslawUsers")


class MasslawUserInstance(DataHolder):

    def __init__(self, user_id: str = None, access_token: str = None):
        self.__user_id = user_id or cognitoManager.get_user_id_by_access_token(access_token)

        DataHolder.__init__(self)

    def load_data(self):
        if not self.__user_id:
            return False
        DataHolder.load_data(self)
        user_data = cognitoManager.get_user_by_id(self.__user_id)
        if not user_data:
            return False
        user_data = dictionary_utils.ensure_dict(user_data)
        self._set_data(user_data)
        return True

    def save_data(self):
        DataHolder.save_data(self)
        write_user_data = self._get_write_data_object()
        dictionary_utils.ensure_flat(write_user_data)
        cognitoManager.update_user_data(self.__user_id, write_user_data)
        self._valid = True

    def get_user_id(self):
        return self.__user_id

    def _get_write_data_object(self):
        user_data = self._get_data()
        for attr in read_only_user_attributes.READ_ONLY_USER_ATTRIBUTES:
            if attr in user_data:
                del user_data[attr]
        return user_data

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

        # provided_phone = data.get('phone', '')
        # if len(provided_phone) <= 2 or not bool(re.match(r'^\+?\d{1,3}[-.\s]?\(?\d{2,3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$', provided_phone)):
        #     raise MasslawUserDataUpdateException('invalid phone number')
