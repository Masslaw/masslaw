from set_user_data.modules.masslaw_users_objects import MasslawUserInstance
from set_user_data.modules.dictionary_utils import dictionary_utils
from set_user_data.modules.masslaw_users_config import user_data_access_config


class MasslawUserDataAccessManager:

    def __init__(self, user_instance: MasslawUserInstance):
        self.__user_instance = user_instance

    def update_user_data(self, update_obj):
        update_obj = dictionary_utils.select_keys(update_obj, user_data_access_config.CLIENT_WRITE_KEYS)
        self.__user_instance.update_data(update_obj)

    def get_data_formatted_for_user_client(self):
        keys = user_data_access_config.USER_OWN_CLIENT_KEYS
        return self.__user_instance.get_data_properties(keys)

    def get_data_formatted_for_other_user_client(self):
        keys = user_data_access_config.USER_OTHER_CLIENT_KEYS
        return self.__user_instance.get_data_properties(keys)

