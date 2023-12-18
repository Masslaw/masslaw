from src.modules.aws_clients.dynamodb_client import DynamoDBTableManager
from src.modules.dictionary_utils import dictionary_utils
from src.modules.lambda_base import lambda_constants
from src.modules.lambda_handler_template_http_invoked_masslaw_case_management_api import MasslawCaseManagementApiInvokedLambdaFunction
from src.modules.masslaw_case_data_formatting import masslaw_case_data_formatting


class GetMyCases(MasslawCaseManagementApiInvokedLambdaFunction):
    def __init__(self):
        MasslawCaseManagementApiInvokedLambdaFunction.__init__(self, default_response_body={'my_cases': [], })
        self.__case_id = ''

    def _reset_state(self):
        MasslawCaseManagementApiInvokedLambdaFunction._reset_state(self)
        self.__case_id = ''

    def _load_request_query_string_params(self):
        MasslawCaseManagementApiInvokedLambdaFunction._load_request_query_string_params(self)
        self.__case_id = self._request_query_string_params.get('case_id')

    def _execute(self):
        MasslawCaseManagementApiInvokedLambdaFunction._execute(self)
        user_id = self._caller_user_instance.get_user_id()
        my_cases = self._caller_user_instance.get_data_property(['cases'], {})
        table_manager = DynamoDBTableManager("MasslawCases")
        items_data = table_manager.batch_get_items(list(my_cases.keys()))
        items_data = [dictionary_utils.ensure_dict(item_data) for item_data in items_data]
        cases_data = [masslaw_case_data_formatting.get_case_data_base_format_from_db_item(item_data=item_data, user_id=user_id) for item_data in items_data]
        self._set_response_attribute([lambda_constants.EventKeys.BODY, 'my_cases'], cases_data)


handler = GetMyCases()
