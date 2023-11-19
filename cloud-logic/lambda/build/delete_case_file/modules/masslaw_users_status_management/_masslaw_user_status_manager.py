from delete_case_file.modules.aws_clients.cognito_client import CognitoUserPoolManager
from delete_case_file.modules.masslaw_users_objects import MasslawUserInstance
from delete_case_file.modules.masslaw_users_config import user_statuses

cognitoManager = CognitoUserPoolManager("MasslawUsers")


class MasslawUserStatusManager:

    def __init__(self, user_instance: MasslawUserInstance):
        self.__user_instance = user_instance

    def get_user_status(self):
        if not self.__user_instance.is_valid():
            return user_statuses.UserStatuses.GUEST

        if not cognitoManager.check_user_verified(self.__user_instance.get_user_id()):
            return user_statuses.UserStatuses.UNVERIFIED

        if not self.__check_credentials():
            return user_statuses.UserStatuses.MISSING_CREDENTIALS

        return user_statuses.UserStatuses.FULLY_APPROVED

    def assert_status(self, min_status_level: int):
        user_status = self.get_user_status()
        if user_status < min_status_level:
            raise MasslawUserStatusAssertFailed(str(user_status))

    def __check_credentials(self):
        for required_credential in REQUIRED_CREDENTIALS:
            if not self.__user_instance.get_data_property(required_credential, None):
                return False
        return True