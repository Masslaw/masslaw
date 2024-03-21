from src.modules.lambda_base import lambda_constants
from src.modules.lambda_handler_template_masslaw_api_case_action_handler import MasslawCaseManagementApiCaseActionHandler
from src.modules.masslaw_case_storage_management import MasslawCaseStorageManager
from src.modules.masslaw_case_storage_management import masslaw_case_storage_management_exceptions


class StartCaseFileUpload(MasslawCaseManagementApiCaseActionHandler):
    def __init__(self):
        MasslawCaseManagementApiCaseActionHandler.__init__(
            self,
            default_response_body={'upload_id': '', 'upload_urls': '', 'file_id': '', },
            request_body_structure={'file_name': [str], 'path': [list, None], 'num_parts': [str, int], }
        )
        self.__file_name = ''
        self.__num_parts = 0
        self.__path = []

    def _load_request_body(self):
        MasslawCaseManagementApiCaseActionHandler._load_request_body(self)
        self.__file_name = self._request_body.get('file_name')
        self.__num_parts = self._request_body.get('num_parts')
        self.__path = self._request_body.get('path')

    def _execute(self):
        MasslawCaseManagementApiCaseActionHandler._execute(self)
        user_id = self._caller_user_instance.get_user_id()
        case_storage_manager = MasslawCaseStorageManager(case_instance=self._case_instance)
        mp_upload_data = case_storage_manager.start_uploading_file(user_id=user_id, file_name=self.__file_name, num_parts=self.__num_parts, file_path=self.__path)
        self._case_instance.save_data()
        self._set_response_attribute([lambda_constants.EventKeys.BODY, 'upload_id'], mp_upload_data['upload_id'])
        self._set_response_attribute([lambda_constants.EventKeys.BODY, 'upload_urls'], mp_upload_data['upload_urls'])
        self._set_response_attribute([lambda_constants.EventKeys.BODY, 'file_id'], mp_upload_data['file_id'])

    def _handle_exception(self, exception: Exception):
        if isinstance(exception, masslaw_case_storage_management_exceptions.MasslawFileTypeNotSupportedException):
            self._set_response_attribute([lambda_constants.EventKeys.STATUS_CODE], lambda_constants.StatusCodes.BAD_REQUEST)
            self._set_response_attribute([lambda_constants.EventKeys.BODY, lambda_constants.EventKeys.RESPONSE_MESSAGE], f'{exception}')
            return


def handler(event, context):
    handler_instance = StartCaseFileUpload()
    handler_instance.call_handler(event, context)
    return handler_instance.get_response()
