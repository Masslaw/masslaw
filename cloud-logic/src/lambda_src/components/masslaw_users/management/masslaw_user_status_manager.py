from ...masslaw_users.masslaw_user_instance import MasslawUserInstance
from ...cognito_manager.cognito_manager import CognitoManager
from ...masslaw_users.config.user_statuses import *

cognitoManager = CognitoManager("MasslawUsers")


class MasslawUserStatusAssertFailed(Exception): pass


class MasslawUserStatusManager:

    def __init__(self, user_instance: MasslawUserInstance):
        self.__user_instance = user_instance

    def get_user_status(self):
        if not self.__user_instance.is_valid():
            return UserStatuses.GUEST

        if not cognitoManager.check_user_verified(self.__user_instance.get_user_id()):
            return UserStatuses.UNVERIFIED

        if not self.__check_credentials():
            return UserStatuses.MISSING_CREDENTIALS

        return UserStatuses.FULLY_APPROVED

    def assert_status(self, min_status_level: int):
        user_status = self.get_user_status()
        if user_status < min_status_level:
            raise MasslawUserStatusAssertFailed(str(user_status))

    def __check_credentials(self):
        for required_credential in REQUIRED_CREDENTIALS:
            if not self.__user_instance.get_data_property(required_credential, None):
                return False
        return True