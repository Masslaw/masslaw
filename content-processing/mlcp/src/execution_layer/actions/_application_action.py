import os
import traceback
from abc import abstractmethod

from execution_layer.actions._exceptions import ApplicationActionExecutionException
from execution_layer.actions._exceptions import ApplicationActionRequiredParamMissingException
from shared_layer.dictionary_utils import dictionary_utils
from shared_layer.mlcp_logger import logger
from shared_layer.mlcp_logger import common_formats


class ApplicationAction:
    _required_params = []

    _action_name = None

    def __init__(self, action_name=None, params=None):
        self._params = params or {}
        self._action_name = action_name or self._action_name or self.__class__.__name__
        self._execution_success = True
        self.__assert_required_params()

    def __call__(self, *args, **kwargs):
        logger.info(f'Executing action: {common_formats.value(self._action_name)}')
        self.__perform_execution()
        success = self._execution_success
        logger.positive(f'Action finished executing | result: {common_formats.value(success)}')
        return success

    @logger.process_function(f'Performing application action execution')
    def __perform_execution(self):
        logger.info('Loading arguments')
        self.__handle_arguments()
        logger.info('Executing action')
        self.__execute()

    def __handle_arguments(self):
        self._handle_arguments()

    @abstractmethod
    def _handle_arguments(self):
        pass

    @logger.process_function(f'Execution')
    def __execute(self):
        try: self._execute()
        except ApplicationActionExecutionException as e:
            self._set_execution_success(False)
            logger.error(f'An application action {common_formats.value(self._action_name)} has failed executing \n reason: {e}')
            if os.environ.get('stage', 'prod') in ('dev', 'text'):
                logger.error(traceback.format_exc())

    @abstractmethod
    def _execute(self):
        pass

    def _get_param(self, param_path: str | list, defualt_value=None):
        if isinstance(param_path, str): param_path = [param_path]
        return dictionary_utils.get_from(self._params, param_path, defualt_value)

    def _set_execution_success(self, success: bool):
        self._execution_success = success

    def __assert_required_params(self):
        for param in self._required_params:
            if param not in self._params:
                raise ApplicationActionRequiredParamMissingException(self._action_name, param)

    def _abort_execution(self, reason):
        raise ApplicationActionExecutionException(reason)
