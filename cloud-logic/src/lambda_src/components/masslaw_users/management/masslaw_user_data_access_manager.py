from ...masslaw_users.masslaw_user_instance import MasslawUserInstance
from ...util import json_utils
from ...masslaw_users.config.user_data_access_config import *


class MasslawUserDataAccessManager:

    def __init__(self, user_instance: MasslawUserInstance):
        self.__user_instance = user_instance

    def update_user_data(self, update_obj):
        update_obj = json_utils.select_keys(update_obj, CLIENT_WRITE_KEYS)
        self.__user_instance.update_data(update_obj)

    def get_data_formatted_for_user_client(self):
        keys = USER_OWN_CLIENT_KEYS
        return self.__user_instance.get_data_properties(keys)

    def get_data_formatted_for_other_user_client(self):
        keys = USER_OTHER_CLIENT_KEYS
        return self.__user_instance.get_data_properties(keys)

