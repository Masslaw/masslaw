from src.modules.lambda_handler_template_masslaw_api_case_file_action_handler import MasslawCaseManagementApiFileActionHandler


class SetCaseFileDescription(MasslawCaseManagementApiFileActionHandler):
    def __init__(self):
        MasslawCaseManagementApiFileActionHandler.__init__(self, request_body_structure={'data': [dict], })
        self.__new_data = {}

    def _load_request_body(self):
        MasslawCaseManagementApiFileActionHandler._load_request_body(self)
        self.__new_data = self._request_body.get('data')

    def _execute(self):
        MasslawCaseManagementApiFileActionHandler._execute(self)
        if 'description' in self.__new_data: self.__new_description = self.__new_data['description']
        self._file_instance.set_data_property(['description'], self.__new_description)
        self._file_instance.save_data()


def handler(event, context):
    handler_instance = SetCaseFileDescription()
    handler_instance.call_handler(event, context)
    return handler_instance.get_response()
