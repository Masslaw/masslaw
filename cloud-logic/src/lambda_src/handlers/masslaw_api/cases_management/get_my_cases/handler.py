from lambda_src.components.masslaw_cases.management.masslaw_case_data_formatting import *
from lambda_src.components.masslaw_cases.lambda_templates.masslaw_case_management_api_invoked_lambda_function import *


class GetMyCases(MasslawCaseManagementApiInvokedLambdaFunction):
    def __init__(self):
        MasslawCaseManagementApiInvokedLambdaFunction.__init__(
            self,
            default_response_body={
                'my_cases': [],
            }
        )

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

        items_data = [json_utils.ensure_dict(item_data) for item_data in items_data]

        cases_data = [get_case_data_base_format_from_db_item(item_data=item_data, user_id=user_id) for item_data in items_data]

        self._set_response_attribute([EventKeys.BODY, 'my_cases'], cases_data)


handler = GetMyCases()
