from src.modules.lambda_handler_template_masslaw_api_case_file_action_handler import MasslawCaseManagementApiFileActionHandler
from src.modules.masslaw_case_data_collection import MasslawCaseDataCollector
from src.modules.lambda_base import lambda_constants


class GetCaseFileComments(MasslawCaseManagementApiFileActionHandler):
    def __init__(self):
        MasslawCaseManagementApiFileActionHandler.__init__(self, default_response_body={'comments': []},)

    def _execute(self):
        MasslawCaseManagementApiFileActionHandler._execute(self)
        user_id = self._caller_user_instance.get_user_id()
        data_collector = MasslawCaseDataCollector(case_instance=self._case_instance, access_user_id=user_id)
        comments_data = data_collector.get_case_file_comments_data(file_id=self._file_id)
        self._set_response_attribute([lambda_constants.EventKeys.BODY, 'comments'], comments_data)


def handler(event, context):
    handler_instance = GetCaseFileComments()
    handler_instance.call_handler(event, context)
    return handler_instance.get_response()
