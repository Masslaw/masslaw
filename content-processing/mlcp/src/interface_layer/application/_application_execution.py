import ctypes
import json
import logging
import os
import sys
import threading
import time
import traceback

from execution_layer.actions import ApplicationActionLoader
from interface_layer.application._exceptions import MLCPProcessConfigurationNotFoundException
from interface_layer.application._exceptions import MLCPRequiredProcessActionExecutionFailedException
from shared_layer.file_system_utils import file_system_utils
from shared_layer.mlcp_logger import logger
from shared_layer.mlcp_logger import common_formats


class ApplicationExecution:
    def __init__(self):
        logger.info("Initialized A New Application Execution")
        self.__process_configuration = None
        self.__process_actions = None
        self.__start_time = None
        self.__stage = None

    def setup(self):
        logger.info("Setting Up Application Execution")
        self.__start_time = time.time()
        self.__process_actions = []
        self.__process_configuration = {}
        self.__load_stage()
        self.__configure_logger()
        self.__handle_process_configuration()

    def __load_stage(self):
        self.__stage = os.environ.get('__mlcp_stage__', 'prod')
        logger.debug(f"Environment Stage: {common_formats.value(self.__stage)}")

    def __configure_logger(self):
        in_production = self.__stage == 'prod'
        logger.set_colored(not in_production)
        logger.set_styled(not in_production)
        logger.setLevel(logging.INFO if in_production else logging.NOTSET)

    def __handle_process_configuration(self):
        logger.info("Handling Process Configuration")
        self.__load_process_configuration()
        self.__parse_process_configuration()

    def __load_process_configuration(self):
        logger.info("Loading Process Configuration")
        if self.__load_process_configuration_from_file(): return
        if self.__load_process_configuration_from_env(): return
        logger.critical("Failed to load process configuration from file or environment variables.")
        raise MLCPProcessConfigurationNotFoundException()

    def __load_process_configuration_from_file(self):
        logger.info("Attempting To Load Configuration From File")
        local_dir = file_system_utils.get_local_directory()
        process_configuration_file_path = file_system_utils.join_paths(local_dir, "process_configuration.json")
        if file_system_utils.is_file(process_configuration_file_path):
            with open(process_configuration_file_path, 'r') as file:
                process_configuration = json.load(file)
                self.__process_configuration = process_configuration
            logger.positive("MLCP Process Configuration Found In A Local File")
            return True
        logger.info('An mlcp process configuration file was not found in the local directory.')

    def __load_process_configuration_from_env(self):
        logger.info("Attempting To Load Configuration From Environment")
        process_configuration_environment_key = "mlcp_process_configuration"
        if process_configuration_environment_key in os.environ:
            raw_process_configuration_value = os.environ.get(process_configuration_environment_key)
            if isinstance(raw_process_configuration_value, str):
                self.__process_configuration = json.loads(raw_process_configuration_value)
            elif isinstance(raw_process_configuration_value, dict):
                self.__process_configuration = raw_process_configuration_value
            else:
                self.__process_configuration = {}
            logger.positive("MLCP Process Configuration Found In Environment Variables")
            return True
        logger.info(f"An mlcp process configuration was not found in the environment variables \"{process_configuration_environment_key}\"")

    def __parse_process_configuration(self):
        logger.info("Parsing Process Configuration")
        self.__load_process_actions()

    def __load_process_actions(self):
        logger.info("Loading Process Actions")
        process_actions_data = self.__process_configuration.get("actions", [])
        for action_data in process_actions_data:
            process_action = ApplicationActionLoader()
            action_name = action_data.get("name", {})
            action_params = action_data.get("params", {})
            action_required = action_data.get("required", False)
            process_action.set_name(action_name)
            process_action.set_params(action_params)
            process_action.set_required(action_required)
            self.__process_actions.append(process_action)
        logger.positive(f"Loaded {common_formats.value(len(self.__process_actions))} process actions")

    def run(self):
        logger.info("Running Application Execution")
        self.__perform_main_execution()
        self.__kill_application()
        self.__exit()

    @logger.process_function("Performing Main Execution")
    def __perform_main_execution(self):
        try:
            self.__execute_actions()
        except MLCPRequiredProcessActionExecutionFailedException as e:
            self.__on_required_action_execution_failed(e.get_action_name())
            return

    @logger.process_function("Executing Actions")
    def __execute_actions(self):
        self.__process_execution_result = True
        for process_action in self.__process_actions:
            action_name = process_action.get_name()
            res = False
            try: res = process_action.execute()
            except Exception as e:
                logger.error(f"An error occurred trying to execute a process action \"{action_name}\" :: \"{e}\"")
                logger.debug(traceback.format_exc())
            if res: logger.positive(f"Action finished executing Successfully")
            else: logger.warn(f"Action finished executing with errors")
            if process_action.is_required() and not res:
                logger.critical(f"The required action \"{action_name}\" has failed to execute successfully, aborting execution.")
                raise MLCPRequiredProcessActionExecutionFailedException(process_action.get_name())

    def __on_required_action_execution_failed(self, action_name: str):
        logger.critical(f"The required action \"{action_name}\" has failed to execute successfully, aborting execution.")
        self.__process_execution_result = False

    @logger.process_function("Killing Application")
    def __kill_application(self):
        time.sleep(1)
        logger.info("Killing Application")
        self.__terminate_all_threads()

    @logger.process_function("Terminating all running threads")
    def __terminate_all_threads(self):
        main_thread = threading.current_thread()
        for thread in threading.enumerate():
            if thread is main_thread: continue
            logger.log(logging.INFO, f"Terminating Thread {common_formats.value(thread.name)}")
            try: thread.join(timeout=1)
            except RuntimeError: pass
            if not thread.is_alive(): continue
            if hasattr(thread, 'ident'):
                thread_id = thread.ident
                res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread_id), ctypes.py_object(SystemExit))
                if res > 1:
                    ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
                    logger.log(logging.CRITICAL, f"Failed to terminate thread {thread.name}")
        logger.positive("All threads terminated successfully")

    def __exit(self):
        suc = self.__get_execution_success()
        exit_code = self.__get_exit_code()
        logger.info(f"MLCP execution finished. Success: {common_formats.value(suc)}, Exit Code: {common_formats.value(exit_code)}, Execution time: {common_formats.value(time.time() - self.__start_time)} seconds")
        logger.info("Exiting.")
        logger.end_process(success=suc)
        logger.end_process(success=suc)
        sys.exit(exit_code)

    def __get_exit_code(self):
        suc = self.__get_execution_success()
        if suc: return 0
        else: return -1

    def __get_execution_success(self):
        return self.__process_execution_result
