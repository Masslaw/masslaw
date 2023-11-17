from ...masslaw_users_objects.masslaw_user_instance import MasslawUserInstance
from lambda_src.modules.masslaw_users_data_access_management._masslaw_user_data_access_manager import MasslawUserDataAccessManager


class MasslawUserDataCollector:

    def __init__(self, user_instance: MasslawUserInstance):
        self.__user_instance = user_instance

        self.__user_data_access_manager = MasslawUserDataAccessManager(self.__user_instance)

    def get_user_data(self, as_user: MasslawUserInstance):
        if as_user.get_user_id() == self.__user_instance.get_user_id():
            return self.__user_data_access_manager.get_data_formatted_for_user_client()
        else:
            return self.__user_data_access_manager.get_data_formatted_for_other_user_client()
