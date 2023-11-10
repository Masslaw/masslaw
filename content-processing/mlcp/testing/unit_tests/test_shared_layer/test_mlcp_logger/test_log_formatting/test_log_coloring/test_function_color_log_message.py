import unittest
from email import message

from shared_layer.mlcp_logger._log_formatting._log_coloring import _color_log_message


class TestFunctionColorLogMessage(unittest.TestCase):

    def test_function_color_log_message(self):
        colors = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
        for color in colors:
            self.assertEqual(_color_log_message(message, color), f'<{color}>{message}</{color}>')
