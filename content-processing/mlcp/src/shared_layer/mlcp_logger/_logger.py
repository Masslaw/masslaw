import logging
import sys
import time

from shared_layer.file_system_utils import file_system_utils
from shared_layer.memory_utils.memory_usage_recorder._memory_usage_recorder import MemoryUsageRecorder
from shared_layer.mlcp_logger._log_formatting import common_formats
from shared_layer.mlcp_logger._log_formatting import MLCPLogFormatter
from shared_layer.mlcp_logger._log_process import LogProcess
from shared_layer.mlcp_logger._processes_manager import ProcessesManager
from shared_layer.mlcp_logger._templates import LOG_DATETIME_FORMATTING_TEMPLATE
from shared_layer.mlcp_logger._templates import LOG_MESSAGE_FORMATTING_TEMPLATE
from shared_layer.mlcp_logger._templates import log_line_with_process_stack_prefix
from shared_layer.mlcp_logger._templates import process_finished_log_string
from shared_layer.mlcp_logger._templates import process_started_log_string


class MLCPLogger(logging.Logger):

    def __init__(self, name: str, log_output_stream_handler=None, colored=False):
        super().__init__(name)

        self._process_manager = ProcessesManager()
        self._formatter = None

        self._init_formatter()
        self.set_log_output_stream(log_output_stream_handler or sys.stdout)

        self.set_colored(colored)

    def _init_formatter(self):
        self._formatter = MLCPLogFormatter(fmt=LOG_MESSAGE_FORMATTING_TEMPLATE, datefmt=LOG_DATETIME_FORMATTING_TEMPLATE, )

    def set_colored(self, colored):
        self._formatter.set_colored(colored)

    def set_styled(self, styled):
        self._formatter.set_styled(styled)

    def setLevel(self, level) -> None:
        super().setLevel(level)
        for handler in self.handlers:
            handler.setLevel(level)

    def start_process(self, process_name: str, max_memory_record=False, log_level: int = logging.INFO):
        process_name = process_name.title()
        process = LogProcess()
        process.name = process_name
        process.time_start = time.time()
        process.log_level = log_level
        if max_memory_record:
            process.memory_recorder = MemoryUsageRecorder()
            process.memory_recorder.start()
        self.log(process.log_level, process_started_log_string(process_name))
        self._process_manager.push_process_to_current_thread(process)

    def end_process(self, success: bool = True):
        process = self._process_manager.pop_process_from_current_thread()

        time_now = time.time()
        execution_time = time_now - process.time_start

        max_memory_usage = None
        if process.memory_recorder:
            process.memory_recorder.stop()
            max_memory_usage = process.memory_recorder.get_recorded_maximum_memory()

        self.log(process.log_level,
            process_finished_log_string(success=success, time_taken=execution_time, max_memory_usage=max_memory_usage and file_system_utils.get_human_readable_size(max_memory_usage)))

    def log(self, level: int, msg: object, *args: object, exc_info: any = ..., stack_info: any = ..., stacklevel: any = ..., extra: any = ..., ignore_process_stack: bool = False, ) -> None:
        to_print = str(msg)
        if not ignore_process_stack: to_print = log_line_with_process_stack_prefix(self._process_manager.get_thread_process_stack_size(), to_print)
        super().log(level, to_print)

    def debug(self, msg, *args, **kwargs):
        self.log(level=logging.DEBUG, msg=msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.log(level=logging.INFO, msg=msg, *args, **kwargs)

    def positive(self, msg, *args, **kwargs):
        self.log(level=logging.INFO, msg=common_formats.good(msg), *args, **kwargs)

    def negative(self, msg, *args, **kwargs):
        self.log(level=logging.INFO, msg=common_formats.bad(msg), *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        self.log(level=logging.WARN, msg=common_formats.important(msg), *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.log(level=logging.CRITICAL, msg=common_formats.critical(msg), *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.log(level=logging.ERROR, msg=common_formats.important(msg), *args, **kwargs)

    def set_log_output_stream(self, handler):
        stdout_handler = logging.StreamHandler(handler)
        stdout_handler.setLevel(self.level)
        stdout_handler.setFormatter(self._formatter)
        self.addHandler(stdout_handler)

    def set_log_output_file(self, log_output_file):
        log_output_file = (log_output_file or "log").replace(".log", "") + ".log"
        open(log_output_file, 'w').close()
        file_handler = logging.FileHandler(log_output_file, encoding="utf-8")
        file_handler.setLevel(self.level)
        file_handler.setFormatter(self._formatter)
        self.addHandler(file_handler)

    def process_function(self, process_name: str = None, max_memory_record=False):
        def decorator(func):
            def wrapper(*args, **kwargs):
                self.start_process(process_name or func.__name__, max_memory_record=max_memory_record)
                try:
                    result = func(*args, **kwargs)
                except Exception as e:
                    self.end_process(success=False)
                    raise e
                self.end_process(success=True)
                return result

            return wrapper

        return decorator

    def debug_io(self, output_parsing: callable = lambda x: x):
        def decorator(func):
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                function_name = func.__name__
                self.debug(f"𖢥 {common_formats.value(function_name)}{common_formats.value(args)} → {common_formats.value(output_parsing(result))}")
                return result

            return wrapper

        return decorator


logger = None

if not logger:
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logger = MLCPLogger("MLCPLogger")
    logger.setLevel(logging.NOTSET)
