from lambda_src.components.masslaw_users.lambda_templates.authenticated_masslaw_user_http_invoked_lambda_function import *
from lambda_src.components.masslaw_users.management.masslaw_user_status_manager import *
from lambda_src.components.masslaw_users.management.masslaw_user_data_access_manager import *


class SetUserData(AuthenticatedMasslawUserHttpInvokedLambdaFunction):

    def __init__(self):
        AuthenticatedMasslawUserHttpInvokedLambdaFunction.__init__(
            self,
            default_response_body={
                'user_data': {}
            },
            request_body_structure={
                'user_data': [dict]
            },
            minimum_user_status_level=UserStatuses.LOGGED_IN,
        )

        self.__user_data = {}

    def _load_request_body(self):
        AuthenticatedMasslawUserHttpInvokedLambdaFunction._load_request_body(self)
        self.__user_data = self._request_body.get('user_data', {})

    def _execute(self):
        AuthenticatedMasslawUserHttpInvokedLambdaFunction._execute(self)

        user_data_access_manager = MasslawUserDataAccessManager(self._caller_user_instance)

        user_data_access_manager.update_user_data(self.__user_data)

        updated_data = user_data_access_manager.get_data_formatted_for_user_client()

        self._caller_user_instance.save_data()

        self._set_response_attribute([EventKeys.BODY, 'user_data'], updated_data)


handler = SetUserData()
