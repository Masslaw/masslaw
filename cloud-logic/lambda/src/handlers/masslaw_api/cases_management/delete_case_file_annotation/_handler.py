from src.modules.lambda_handler_template_http_invoked_masslaw_case_management_api import MasslawCaseManagementApiInvokedLambdaFunction
from src.modules.masslaw_case_annotations_management import MasslawCaseAnnotationsManager
from src.modules.masslaw_cases_objects import MasslawCaseInstance


class DeleteCaseFileAnnotation(MasslawCaseManagementApiInvokedLambdaFunction):
    def __init__(self):
        MasslawCaseManagementApiInvokedLambdaFunction.__init__(self, request_query_string_parameters_structure={'case_id': [str], 'annotation_id': [str], })
        self.__case_id = ''
        self.__annotation_id = ''

    def _reset_state(self):
        MasslawCaseManagementApiInvokedLambdaFunction._reset_state(self)
        self.__case_id = ''
        self.__annotation_id = ''

    def _load_request_query_string_params(self):
        MasslawCaseManagementApiInvokedLambdaFunction._load_request_query_string_params(self)
        self.__case_id = self._request_query_string_params.get('case_id', '')
        self.__annotation_id = self._request_query_string_params.get('annotation_id', '')

    def _execute(self):
        MasslawCaseManagementApiInvokedLambdaFunction._execute(self)
        user_id = self._caller_user_instance.get_user_id()
        case_instance = MasslawCaseInstance(self.__case_id)
        annotations_manager = MasslawCaseAnnotationsManager(case_instance)
        annotations_manager.delete_annotation(annotation_id=self.__annotation_id, user_id=user_id)


def handler(event, context):
    handler_instance = DeleteCaseFileAnnotation()
    handler_instance.call_handler(event, context)
    return handler_instance.get_response()
