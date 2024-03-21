from src.modules.lambda_base import lambda_constants
from src.modules.lambda_handler_template_masslaw_api_case_action_handler import MasslawCaseManagementApiCaseActionHandler
from src.modules.masslaw_case_creation import create_a_new_case
from src.modules.masslaw_case_users_management import MasslawCaseUserAccessManager
from src.modules.masslaw_case_users_management import masslaw_case_users_management_exceptions
from src.modules.masslaw_cases_config import access_config
from src.modules.dictionary_utils import dictionary_utils


class PostCase(MasslawCaseManagementApiCaseActionHandler):
    def __init__(self):
        MasslawCaseManagementApiCaseActionHandler.__init__(
            self,
            request_body_structure={'case_data': {'title': [str, None], 'description': [str, None], 'languages': [list, None]}},
            default_response_body={'case_id': ''},
        )
        self.__case_data = {}

    def _load_request_body(self):
        MasslawCaseManagementApiCaseActionHandler._load_request_body(self)
        self.__case_data = self._request_body.get('case_data')

    def _execute(self):
        MasslawCaseManagementApiCaseActionHandler._execute(self)
        user_id = self._caller_user_instance.get_user_id()
        case_user_access = MasslawCaseUserAccessManager(case_instance=self._case_instance)
        user_access_level = case_user_access.get_user_access_level_name(user_id)
        if user_access_level not in (access_config.CaseAccessEntities.OWNER_CLIENT, access_config.CaseAccessEntities.MANAGER_CLIENT):
            raise masslaw_case_users_management_exceptions.MasslawCaseUnauthorizedUserActionException(f"An attempt to change the data of a case is made by an unauthorized user.")
        update_object = {}
        if new_title := dictionary_utils.get_from(self.__case_data, ['title']): dictionary_utils.set_at(update_object, ['information', 'title'], new_title)
        if new_description := dictionary_utils.get_from(self.__case_data, ['description']): dictionary_utils.set_at(update_object, ['information', 'description'], new_description)
        if new_language_list := dictionary_utils.get_from(self.__case_data, ['languages']): dictionary_utils.set_at(update_object, ['languages'], new_language_list)
        self._case_instance.update_data(update_object, create_new_keys=False)
        self._case_instance.save_data()


def handler(event, context):
    handler_instance = PostCase()
    handler_instance.call_handler(event, context)
    return handler_instance.get_response()
