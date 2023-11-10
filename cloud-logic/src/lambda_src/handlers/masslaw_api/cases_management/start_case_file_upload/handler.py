from lambda_src.components.masslaw_cases.lambda_templates.masslaw_case_management_api_invoked_lambda_function import *
from lambda_src.components.masslaw_cases.management.masslaw_case_storage_manager import *


class StartCaseFileUpload(MasslawCaseManagementApiInvokedLambdaFunction):
    def __init__(self):
        MasslawCaseManagementApiInvokedLambdaFunction.__init__(
            self,
            default_response_body={
                'upload_id': '',
                'upload_urls': '',
                'file_id': '',
            },
            request_body_structure={
                'case_id': [str],
                'file_name': [str],
                'num_parts': [str, int],
                'languages': [list],
            }
        )

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

        mp_upload_data = case_storage_manager.start_uploading_file(user_id=user_id,
                                                                   file_name=self.__file_name,
                                                                   num_parts=self.__num_parts,
                                                                   file_languages=self.__languages)

        case_instance.save_data()

        self._set_response_attribute([EventKeys.BODY, 'upload_id'], mp_upload_data['upload_id'])
        self._set_response_attribute([EventKeys.BODY, 'upload_urls'], mp_upload_data['upload_urls'])
        self._set_response_attribute([EventKeys.BODY, 'file_id'], mp_upload_data['file_id'])

    def _handle_exception(self, exception: Exception):
        if isinstance(exception, MasslawFileTypeNotSupportedException):
            self._set_response_attribute([EventKeys.STATUS_CODE], StatusCodes.BAD_REQUEST)
            self._set_response_attribute([EventKeys.BODY, EventKeys.RESPONSE_MESSAGE],
                                         f'{exception}')
            return



handler = StartCaseFileUpload()
