import logging
import unittest
from io import StringIO
from unittest.mock import MagicMock
from unittest.mock import patch

from shared_layer.mlcp_logger._logger import MLCPLogger


class TestMLCPLogger(unittest.TestCase):
    def setUp(self):
        self.stream = StringIO()
        self.logger = MLCPLogger("TestMLCPLogger", log_output_stream_handler=self.stream)

    def test_start_and_end_process(self):
        process_name = "test_process"
        process_time = 10
        with patch('time.time') as mock_time:
            mock_time.side_effect = [0, 0, process_time, process_time]
            self.logger.start_process(process_name)
            self.logger.end_process()

        log_output = self.stream.getvalue()
        log_output_lines = log_output.split('\n')
        self.assertEqual(log_output_lines[0], f'01-01-1970 02:00:00  INFO       :::: ┍━ {process_name.title()}')
        self.assertEqual(log_output_lines[1], f'01-01-1970 02:00:10  INFO       :::: ┕━ took: {process_time} seconds ')

    def test_process_function_decorator(self):
        process_name = "test_process"
        process_time = 10

        @self.logger.process_function(process_name=process_name, max_memory_record=False)
        def test_func():
            return "success"

        with patch('time.time') as mock_time:
            mock_time.side_effect = [0, 0, process_time, process_time]
            res = test_func()

        self.assertEqual(res, "success")

        log_output = self.stream.getvalue()
        log_output_lines = log_output.split('\n')
        self.assertEqual(log_output_lines[0], f'01-01-1970 02:00:00  INFO       :::: ┍━ {process_name.title()}')
        self.assertEqual(log_output_lines[1], f'01-01-1970 02:00:10  INFO       :::: ┕━ took: {process_time} seconds ')

    def test_log_levels(self):
        self.logger.debug("Debug message")
        self.logger.info("Info message")
        self.logger.critical("Critical message")
        self.logger.error("Error message")

        log_output = self.stream.getvalue().split('\n')
        self.assertIn("Debug message", log_output[0])
        self.assertIn("DEBUG", log_output[0])
        self.assertIn("Info message", log_output[1])
        self.assertIn("INFO", log_output[1])
        self.assertIn("Critical message", log_output[2])
        self.assertIn("CRITICAL", log_output[2])
        self.assertIn("Error message", log_output[3])
        self.assertIn("ERROR", log_output[3])

    def test_log_levels_output(self):
        self.logger.setLevel(logging.NOTSET)
        self.logger.debug("Debug message")
        self.logger.info("Info message")
        self.logger.error("Error message")
        self.logger.critical("Critical message")
        self.logger.setLevel(logging.INFO)
        self.logger.debug("Debug message")
        self.logger.info("Info message")
        self.logger.error("Error message")
        self.logger.critical("Critical message")
        self.logger.setLevel(logging.ERROR)
        self.logger.debug("Debug message")
        self.logger.info("Info message")
        self.logger.error("Error message")
        self.logger.critical("Critical message")

        log_output = self.stream.getvalue()
        log_output_lines = log_output.split('\n')

        self.assertIn("Debug message", log_output_lines[0])
        self.assertIn("DEBUG", log_output_lines[0])
        self.assertIn("Info message", log_output_lines[1])
        self.assertIn("INFO", log_output_lines[1])
        self.assertIn("Error message", log_output_lines[2])
        self.assertIn("ERROR", log_output_lines[2])
        self.assertIn("Critical message", log_output_lines[3])
        self.assertIn("CRITICAL", log_output_lines[3])
        self.assertIn("Info message", log_output_lines[4])
        self.assertIn("INFO", log_output_lines[4])
        self.assertIn("Error message", log_output_lines[5])
        self.assertIn("ERROR", log_output_lines[5])
        self.assertIn("Critical message", log_output_lines[6])
        self.assertIn("CRITICAL", log_output_lines[6])
        self.assertIn("Error message", log_output_lines[7])
        self.assertIn("ERROR", log_output_lines[7])
        self.assertIn("Critical message", log_output_lines[8])
        self.assertIn("CRITICAL", log_output_lines[8])

    @patch('os.path.exists', return_value=True)
    def test_set_log_output_file(self, mock_exists):
        with patch('builtins.open', MagicMock()), patch('logging.FileHandler', MagicMock()):
            self.logger.set_log_output_file("test.log")
