import json
import logging
import os
from abc import abstractmethod

import time
import traceback
from src.modules.dictionary_utils import dictionary_utils
from src.modules.lambda_base._exceptions import InvalidEventLambdaException

LOGGING_FORMAT = '[%(name)s] %(asctime)s :::: [%(levelname)s] %(message)s'


class LambdaHandler:
    def __init__(
            self,
            name=None,
            default_response: dict = None,
            event_structure: dict = None
    ):
        self.name = name or str(self.__class__.__name__)
        self.__event_structure = event_structure or {}
        self.__default_response = default_response or {}
        self.__response = self.__default_response or {}
        self.__event = {}
        self.__context = None
        self._stage = os.environ.get('STAGE', 'prod')
        self._execution_exception = ''

        self.__setup()

        self._log(f'Created a lambda function "{self.name}" :: stage: {self._stage}')
        self._log(f'Expected event structure: {event_structure}', level=logging.DEBUG)
        self._log(f'Lambda environment:\n{os.environ}')

    def __reset_state(self):
        self._log(f'Resetting state')
        self._execution_exception = ''
        self.__response = self.__default_response or {}
        self.__event = {}
        self.__context = None
        self._reset_state()

    @abstractmethod
    def _reset_state(self):
        pass  # can be implemented by inheriting handler classes

    def __setup(self):
        self._setup()
        self.__write_function_name_in_environment()
        self.__init_logger()

    def _setup(self):
        pass  # can be implemented by inheriting handler classes

    def __call__(self, event, context):
        self._log(f'Calling {self.name}')
        self.__reset_state()
        _start_execution_time_milliseconds = time.time()
        res = False
        try:
            self.__response = self.__default_response
            self.__handle_event(event)
            self.__handle_context(context)
            self.__call_function()
            self._successful_execution()
            res = True
        except Exception as e:
            self._log_exception(e)
            self._handle_exception(e)
            self._execution_exception = traceback.format_exc()
        self._log(f'Finished executing.\n Success: {res}.\n Execution Time: {time.time() - _start_execution_time_milliseconds} milliseconds')
        final_response = self._prepare_final_response(self.__response)
        self._log(f'Function response: \n {final_response}', level=logging.DEBUG)
        return final_response

    def __handle_event(self, event):
        self._log("Handling event")
        self.__event = dictionary_utils.ensure_dict(event)
        self._log(f'Event: \n {self.__event}', level=logging.DEBUG)
        self._assert_event_structure()
        self._handle_event()

    def _handle_event(self):
        pass  # can be implemented by inheriting handler classes

    def __handle_context(self, context):
        self._log("Handling context")
        self.__context = context
        self._handle_context()
        self._log(f'Context: \n {self.__context}', level=logging.DEBUG)

    def _handle_context(self):
        pass  # can be implemented by inheriting handler classes

    def __call_function(self):
        self._log('Executing function...')
        self._execute()

    def _execute(self):
        pass  # can be implemented by inheriting handler classes

    def _get_request_event(self):
        return self.__event

    def _get_request_context(self):
        return self.__context

    def _set_response_attribute(self, key_path, value):
        if value is None: dictionary_utils.delete_at(self.__response, key_path)
        else: dictionary_utils.set_at(self.__response, key_path, value)

    def _prepare_final_response(self, response):
        self._log(f'Preparing final response')
        self._log(f'Raw response: {response}', level=logging.DEBUG)
        self._log(f'Response length: {len(str(response))}')
        return response

    def _assert_event_structure(self):
        if not dictionary_utils.check_structure(self.__event, self.__event_structure):
            raise InvalidEventLambdaException(f'Invalid event structure. Expected: {self.__event_structure} Got: {self.__event}')

    def __init_logger(self):
        logging.basicConfig(level=logging.DEBUG, format=LOGGING_FORMAT)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

    def _successful_execution(self):
        pass  # can be implemented by inheriting handler classes

    def _log(self, message, level=logging.INFO):
        self.logger.log(level, message)

    def _handle_exception(self, exception: Exception):
        pass  # can be implemented by inheriting handler classes

    def _log_exception(self, exception: Exception):
        self._log(f'An error occurred: [{exception.__class__.__name__}]\n \"{exception}\"\n Traceback: {traceback.format_exc()}', level=logging.ERROR)

    def __write_function_name_in_environment(self):
        os.environ['FUNCTION_NAME'] = self.name
