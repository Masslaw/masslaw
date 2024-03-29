from src.modules.lambda_handler_template_masslaw_api_case_action_handler import MasslawCaseManagementApiCaseActionHandler
from src.modules.masslaw_case_users_management import MasslawCaseUserAccessManager


class PostCaseUser(MasslawCaseManagementApiCaseActionHandler):
    def __init__(self):
        MasslawCaseManagementApiCaseActionHandler.__init__(
            self,
            request_path_parameters_structure={'user_id': [str]},
            request_body_structure={'access_level': [str, None], 'access_policy': [dict, None]},
        )
        self.__user_id = ''
        self.__access_level = ''
        self.__access_policy = {}

    def _load_request_path_params(self):
        MasslawCaseManagementApiCaseActionHandler._load_request_path_params(self)
        self.__user_id = self._request_path_params.get('user_id', '')

    def _load_request_body(self):
        MasslawCaseManagementApiCaseActionHandler._load_request_body(self)
        self.__access_level = self._request_body.get('access_level', None)
        self.__access_policy = self._request_body.get('access_policy', None)

    def _execute(self):
        MasslawCaseManagementApiCaseActionHandler._execute(self)
        user_id = self._caller_user_instance.get_user_id()
        case_access_manager = MasslawCaseUserAccessManager(self._case_instance)
        case_access_manager.set_case_user_permissions_as_user(user_id, self.__user_id, self.__access_level, self.__access_policy)
        self._case_instance.save_data()


def handler(event, context):
    handler_instance = PostCaseUser()
    handler_instance.call_handler(event, context)
    return handler_instance.get_response()
