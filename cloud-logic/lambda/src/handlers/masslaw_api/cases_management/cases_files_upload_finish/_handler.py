from src.modules.lambda_base import lambda_constants
from src.modules.lambda_handler_template_masslaw_api_case_action_handler import MasslawCaseManagementApiCaseActionHandler
from src.modules.masslaw_case_storage_management import MasslawCaseStorageManager
from src.modules.masslaw_case_storage_management import masslaw_case_storage_management_exceptions


class FinishCaseFileUpload(MasslawCaseManagementApiCaseActionHandler):
    def __init__(self):
        MasslawCaseManagementApiCaseActionHandler.__init__(self, default_response_body={'file': {}}, request_body_structure={'file_id': [str], 'parts': [dict]})
        self.__file_id = ''
        self.__parts = []

    def _load_request_body(self):
        MasslawCaseManagementApiCaseActionHandler._load_request_body(self)
        self.__file_id = self._request_body.get('file_id')
        self.__parts = self._request_body.get('parts')

    def _execute(self):
        MasslawCaseManagementApiCaseActionHandler._execute(self)
        case_storage_manager = MasslawCaseStorageManager(case_instance=self._case_instance)
        self._file_instance = case_storage_manager.complete_uploading_file(file_id=self.__file_id, parts_list=self.__parts)
        if not self._file_instance: raise Exception('Something went wrong')
        case_storage_manager.start_case_file_processing_pipeline(self._file_instance, self._stage)
        self._file_instance.save_data()
        self._case_instance.save_data()

    def _handle_exception(self, exception: Exception):
        if isinstance(exception, masslaw_case_storage_management_exceptions.MasslawFileTypeNotSupportedException):
            self._set_response_attribute([lambda_constants.EventKeys.STATUS_CODE], lambda_constants.StatusCodes.BAD_REQUEST)
            self._set_response_attribute([lambda_constants.EventKeys.BODY, lambda_constants.EventKeys.RESPONSE_MESSAGE], f'{exception}')
            return


def handler(event, context):
    handler_instance = FinishCaseFileUpload()
    handler_instance.call_handler(event, context)
    return handler_instance.get_response()
