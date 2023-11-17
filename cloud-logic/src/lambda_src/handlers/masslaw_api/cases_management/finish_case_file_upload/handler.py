from lambda_src.modules.lambda_base import lambda_constants
from lambda_src.modules.lambda_handler_template_http_invoked_masslaw_case_management_api import MasslawCaseManagementApiInvokedLambdaFunction
from lambda_src.modules.masslaw_case_storage_management import MasslawCaseStorageManager
from lambda_src.modules.masslaw_case_storage_management import masslaw_case_storage_management_exceptions
from lambda_src.modules.masslaw_cases_objects import MasslawCaseInstance


class FinishCaseFileUpload(MasslawCaseManagementApiInvokedLambdaFunction):
    def __init__(self):
        MasslawCaseManagementApiInvokedLambdaFunction.__init__(self, default_response_body={}, request_body_structure={'case_id': [str], 'file_id': [str], 'parts': [dict], })
        self.__case_id = ''
        self.__file_id = ''
        self.__parts = {}

    def _load_request_body(self):
        MasslawCaseManagementApiInvokedLambdaFunction._load_request_body(self)
        self.__case_id = self._request_body.get('case_id')
        self.__file_id = self._request_body.get('file_id')
        self.__parts = self._request_body.get('parts')

    def _execute(self):
        MasslawCaseManagementApiInvokedLambdaFunction._execute(self)
        case_instance = MasslawCaseInstance(case_id=self.__case_id)
        case_storage_manager = MasslawCaseStorageManager(case_instance=case_instance)
        file_instance = case_storage_manager.complete_uploading_file(user_id=self._caller_user_instance.get_user_id(), file_id=self.__file_id, parts_list=self.__parts)
        if not file_instance: raise Exception('Something went wrong')
        case_storage_manager.start_case_file_processing_pipeline(file_instance, self._stage)
        case_instance.save_data()

    def _handle_exception(self, exception: Exception):
        if isinstance(exception, masslaw_case_storage_management_exceptions.MasslawFileTypeNotSupportedException):
            self._set_response_attribute([lambda_constants.EventKeys.STATUS_CODE], lambda_constants.StatusCodes.BAD_REQUEST)
            self._set_response_attribute([lambda_constants.EventKeys.BODY, lambda_constants.EventKeys.RESPONSE_MESSAGE], f'{exception}')
            return


handler = FinishCaseFileUpload()
