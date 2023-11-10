import unittest
from email import message

from shared_layer.mlcp_logger._log_formatting._log_styling import _style_log_message


class TestFunctionStyleLogMessage(unittest.TestCase):

    def test_function_style_log_message(self):
        styles = ['italic', 'bold', 'underline', 'blink', 'reverse', 'concealed', 'strike']
        for style in styles:
            self.assertEqual(_style_log_message(message, style), f'<{style}>{message}</{style}>')
