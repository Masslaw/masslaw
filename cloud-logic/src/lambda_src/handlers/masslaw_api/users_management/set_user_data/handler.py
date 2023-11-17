from lambda_src.modules.lambda_base import lambda_constants
from lambda_src.modules.lambda_handler_template_http_invoked_authenticated_masslaw_user import AuthenticatedMasslawUserHttpInvokedLambdaFunction
from lambda_src.modules.masslaw_users_config import user_statuses
from lambda_src.modules.masslaw_users_data_access_management import MasslawUserDataAccessManager


class SetUserData(AuthenticatedMasslawUserHttpInvokedLambdaFunction):

    def __init__(self):
        AuthenticatedMasslawUserHttpInvokedLambdaFunction.__init__(self, default_response_body={'user_data': {}}, request_body_structure={'user_data': [dict]}, minimum_user_status_level=user_statuses.UserStatuses.LOGGED_IN, )
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
        self._set_response_attribute([lambda_constants.EventKeys.BODY, 'user_data'], updated_data)


handler = SetUserData()
