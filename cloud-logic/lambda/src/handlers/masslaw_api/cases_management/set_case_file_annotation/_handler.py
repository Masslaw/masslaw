from src.modules.lambda_handler_template_http_invoked_masslaw_case_management_api import MasslawCaseManagementApiInvokedLambdaFunction
from src.modules.masslaw_case_annotations_management import MasslawCaseAnnotationsManager
from src.modules.masslaw_case_users_management import MasslawCaseUserAccessManager
from src.modules.masslaw_case_users_management import masslaw_case_users_management_exceptions
from src.modules.masslaw_cases_objects import MasslawCaseInstance


class SetCaseFileAnnotation(MasslawCaseManagementApiInvokedLambdaFunction):
    def __init__(self):
        MasslawCaseManagementApiInvokedLambdaFunction.__init__(self, request_query_string_parameters_structure={'case_id': [str], 'file_id': [str], 'annotation_id': [str, None], },
                                                               request_body_structure={'type': [str], 'from_char': [str, int], 'to_char': [str, int], 'annotation_text': [str, None], 'annotated_text': [str, None], 'color': [str], })
        self.__case_id = ''
        self.__file_id = ''
        self.__annotation_id = ''
        self.__type = ''
        self.__from_char = 0
        self.__to_char = 0
        self.__annotation_text = ''
        self.__annotated_text = ''
        self.__color = ''

    def _reset_state(self):
        MasslawCaseManagementApiInvokedLambdaFunction._reset_state(self)
        self.__case_id = ''
        self.__file_id = ''
        self.__annotation_id = ''
        self.__type = ''
        self.__from_char = 0
        self.__to_char = 0
        self.__annotation_text = ''
        self.__annotated_text = ''
        self.__color = ''

    def _load_request_query_string_params(self):
        MasslawCaseManagementApiInvokedLambdaFunction._load_request_query_string_params(self)
        self.__case_id = self._request_query_string_params.get('case_id')
        self.__file_id = self._request_query_string_params.get('file_id')
        self.__annotation_id = self._request_query_string_params.get('annotation_id', None)

    def _load_request_body(self):
        MasslawCaseManagementApiInvokedLambdaFunction._load_request_body(self)
        self.__type = self._request_body.get('type')
        self.__from_char = int(self._request_body.get('from_char'))
        self.__to_char = int(self._request_body.get('to_char'))
        self.__annotation_text = self._request_body.get('annotation_text')
        self.__annotated_text = self._request_body.get('annotated_text')
        self.__color = self._request_body.get('color', None)

    def _execute(self):
        MasslawCaseManagementApiInvokedLambdaFunction._execute(self)
        user_id = self._caller_user_instance.get_user_id()
        case_instance = MasslawCaseInstance(case_id=self.__case_id)
        case_user_access = MasslawCaseUserAccessManager(case_instance=case_instance)
        user_access_files = case_user_access.get_user_access_files(user_id)
        if self.__file_id not in user_access_files:
            raise masslaw_case_users_management_exceptions.MasslawCaseUnauthorizedUserActionException(f"An attempt was made to create or change an annotation of a file which is not included in a user's case permissions")
        annotations_manager = MasslawCaseAnnotationsManager(case_instance=case_instance)
        annotations_manager.put_annotation(
            user_id=user_id,
            file_id=self.__file_id,
            annotation_type=self.__type,
            beginning_character=self.__from_char,
            ending_character=self.__to_char,
            annotation_text=self.__annotation_text,
            annotated_text=self.__annotated_text,
            color=self.__color,
            annotation_id=self.__annotation_id
        )


def handler(event, context):
    handler_instance = SetCaseFileAnnotation()
    handler_instance.call_handler(event, context)
    return handler_instance.get_response()
