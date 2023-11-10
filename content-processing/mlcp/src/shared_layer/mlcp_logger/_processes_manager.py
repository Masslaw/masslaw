import threading

from shared_layer.mlcp_logger._log_process import LogProcess


class ProcessesManager:
    def __init__(self):
        self.__process_stack_list = {}

    def push_process_to_current_thread(self, process: LogProcess):
        process_stack = self.__get_process_stack_in_current_thread()
        process_stack.append(process)

    def pop_process_from_current_thread(self):
        process_stack = self.__get_process_stack_in_current_thread()
        return process_stack.pop()

    def get_current_process_in_thread(self):
        process_stack = self.__get_process_stack_in_current_thread()
        return process_stack[-1]

    def get_thread_process_stack_size(self):
        process_stack = self.__get_process_stack_in_current_thread()
        return len(process_stack)

    def __get_process_stack_in_current_thread(self):
        current_thread_name = threading.current_thread().name
        process_stack = self.__process_stack_list.get(current_thread_name, [])
        self.__process_stack_list[current_thread_name] = process_stack

        return process_stack
