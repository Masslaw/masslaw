import importlib
import inspect

from execution_layer.actions._application_action import ApplicationAction
from execution_layer.actions._exceptions import ApplicationActionImplementationNotFoundException
from execution_layer.actions._exceptions import ApplicationActionLoadingException
from shared_layer.mlcp_logger import logger
from shared_layer.mlcp_logger import common_formats


class ApplicationActionLoader:
    def __init__(self, name="", params=None, required=False):
        self.__name = ""
        self.__params = {}
        self.__required = False

        self.__action: ApplicationAction = None

        self.set_name(name or "")
        self.set_params(params or {})
        self.set_required(required)

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def set_params(self, params):
        self.__params = params

    def set_required(self, required):
        self.__required = required

    def is_required(self):
        return self.__required

    @logger.process_function('Executing Action')
    def execute(self) -> bool:
        logger.debug(f'Executing action: {common_formats.value(self.__name)}')
        self.__load_action_implementation()
        success = self.__action()
        logger.debug(f'Action execution result: {common_formats.value(success)}')
        return success

    @logger.process_function('Loading action implementation')
    def __load_action_implementation(self):
        action_name = self.__name
        action_name = action_name.lower()
        module_name = f'execution_layer.actions._implementations.{action_name}'
        logger.debug(f'Attempting to load module {common_formats.value(module_name)}')
        try: action_module = importlib.import_module(module_name)
        except ImportError as e: raise ApplicationActionLoadingException(e)
        mlcp_action_class = None
        for name, obj in inspect.getmembers(action_module):
            if obj == ApplicationAction: continue
            if inspect.isclass(obj) and issubclass(obj, ApplicationAction):
                mlcp_action_class = obj
                break
        if mlcp_action_class is None:
            logger.error(f'Could not find an implementation for action: {common_formats.value(action_name)}')
            raise ApplicationActionImplementationNotFoundException(action_name)
        logger.positive(f'Loaded action implementation: {common_formats.value(mlcp_action_class.__name__)}')
        self.__action = mlcp_action_class(params=self.__params)
