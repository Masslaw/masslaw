from src.modules.lambda_base import lambda_constants
from src.modules.lambda_handler_template_http_invoked_authenticated_masslaw_user import AuthenticatedMasslawUserHttpInvokedLambdaFunction
from src.modules.masslaw_users_config import user_statuses
from src.modules.masslaw_users_data_collection import MasslawUserDataCollector
from src.modules.masslaw_users_objects import MasslawUserInstance


class GetUserData(AuthenticatedMasslawUserHttpInvokedLambdaFunction):

    def __init__(self):
        AuthenticatedMasslawUserHttpInvokedLambdaFunction.__init__(self, default_response_body={'user_data': {}}, minimum_user_status_level=user_statuses.UserStatuses.GUEST, )
        self.__user_id = None

    def _reset_state(self):
        AuthenticatedMasslawUserHttpInvokedLambdaFunction._reset_state(self)
        self.__user_id = None

    def _load_request_query_string_params(self):
        AuthenticatedMasslawUserHttpInvokedLambdaFunction._load_request_query_string_params(self)
        self.__user_id = self._request_query_string_params.get('user_id', None)

    def _execute(self):
        AuthenticatedMasslawUserHttpInvokedLambdaFunction._execute(self)
        if self.__user_id is not None:
            target_user_instance = MasslawUserInstance(user_id=self.__user_id)
        else:
            target_user_instance = self._caller_user_instance
        target_user_data_collector = MasslawUserDataCollector(target_user_instance)
        user_data = target_user_data_collector.get_user_data(as_user=self._caller_user_instance)
        self._set_response_attribute([lambda_constants.EventKeys.BODY, 'user_data'], user_data or {})


def handler(event, context):
    handler_instance = GetUserData()
    return handler_instance.call_handler(event, context)
