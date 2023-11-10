import threading
import unittest
from unittest.mock import MagicMock

from shared_layer.mlcp_logger._log_process import LogProcess
from shared_layer.mlcp_logger._processes_manager import ProcessesManager


class TestClassProcessesManager(unittest.TestCase):

    def setUp(self):
        self.manager = ProcessesManager()

    def test_push_process(self):
        process = MagicMock(spec=LogProcess)
        self.manager.push_process_to_current_thread(process)

        self.assertEqual(process, self.manager.get_current_process_in_thread())

    def test_pop_process(self):
        process = MagicMock(spec=LogProcess)
        self.manager.push_process_to_current_thread(process)

        popped_process = self.manager.pop_process_from_current_thread()

        self.assertEqual(process, popped_process)

    def test_get_current_process(self):
        process1 = MagicMock(spec=LogProcess)
        process2 = MagicMock(spec=LogProcess)
        self.manager.push_process_to_current_thread(process1)
        self.manager.push_process_to_current_thread(process2)

        self.assertEqual(process2, self.manager.get_current_process_in_thread())

    def test_get_thread_process_stack_size(self):
        self.assertEqual(0, self.manager.get_thread_process_stack_size())

        process1 = MagicMock(spec=LogProcess)
        process2 = MagicMock(spec=LogProcess)
        self.manager.push_process_to_current_thread(process1)
        self.manager.push_process_to_current_thread(process2)

        self.assertEqual(2, self.manager.get_thread_process_stack_size())

    def test_multithreading_support(self):
        process1 = MagicMock(spec=LogProcess)
        process2 = MagicMock(spec=LogProcess)

        def thread_fn():
            self.manager.push_process_to_current_thread(process2)
            self.assertEqual(process2, self.manager.get_current_process_in_thread())
            self.assertEqual(1, self.manager.get_thread_process_stack_size())

        thread = threading.Thread(target=thread_fn)
        thread.start()
        thread.join()

        self.manager.push_process_to_current_thread(process1)

        self.assertEqual(process1, self.manager.get_current_process_in_thread())
        self.assertEqual(1, self.manager.get_thread_process_stack_size())
