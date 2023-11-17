from lambda_src.modules.lambda_base import lambda_constants
from lambda_src.modules.lambda_handler_template_http_invoked_masslaw_case_management_api import MasslawCaseManagementApiInvokedLambdaFunction
from lambda_src.modules.masslaw_case_storage_management import MasslawCaseStorageManager
from lambda_src.modules.masslaw_case_storage_management import masslaw_case_storage_management_exceptions
from lambda_src.modules.masslaw_cases_objects import MasslawCaseInstance


class StartCaseFileUpload(MasslawCaseManagementApiInvokedLambdaFunction):
    def __init__(self):
        MasslawCaseManagementApiInvokedLambdaFunction.__init__(self, default_response_body={'upload_id': '', 'upload_urls': '', 'file_id': '', }, request_body_structure={'case_id': [str], 'file_name': [str], 'num_parts': [str, int], 'languages': [list], })
        self.__case_id = ''
        self.__file_name = ''
        self.__num_parts = 0
        self.__languages = ['eng']

    def _load_request_body(self):
        MasslawCaseManagementApiInvokedLambdaFunction._load_request_body(self)
        self.__case_id = self._request_body.get('case_id')
        self.__file_name = self._request_body.get('file_name')
        self.__num_parts = self._request_body.get('num_parts')
        self.__languages = self._request_body.get('languages')

    def _execute(self):
        MasslawCaseManagementApiInvokedLambdaFunction._execute(self)
        user_id = self._caller_user_instance.get_user_id()
        case_instance = MasslawCaseInstance(case_id=self.__case_id)
        case_storage_manager = MasslawCaseStorageManager(case_instance=case_instance)
        mp_upload_data = case_storage_manager.start_uploading_file(user_id=user_id, file_name=self.__file_name, num_parts=self.__num_parts, file_languages=self.__languages)
        case_instance.save_data()
        self._set_response_attribute([lambda_constants.EventKeys.BODY, 'upload_id'], mp_upload_data['upload_id'])
        self._set_response_attribute([lambda_constants.EventKeys.BODY, 'upload_urls'], mp_upload_data['upload_urls'])
        self._set_response_attribute([lambda_constants.EventKeys.BODY, 'file_id'], mp_upload_data['file_id'])

    def _handle_exception(self, exception: Exception):
        if isinstance(exception, masslaw_case_storage_management_exceptions.MasslawFileTypeNotSupportedException):
            self._set_response_attribute([lambda_constants.EventKeys.STATUS_CODE], lambda_constants.StatusCodes.BAD_REQUEST)
            self._set_response_attribute([lambda_constants.EventKeys.BODY, lambda_constants.EventKeys.RESPONSE_MESSAGE], f'{exception}')
            return


handler = StartCaseFileUpload()
