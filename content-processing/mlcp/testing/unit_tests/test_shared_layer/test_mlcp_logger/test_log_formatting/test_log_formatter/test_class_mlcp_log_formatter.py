import unittest

from shared_layer.mlcp_logger._log_formatting._log_formatter import MLCPLogFormatter


class TestClassMLCPLogFormatter(unittest.TestCase):

    def test_apply_colors_to_message_colored(self):
        formatter = MLCPLogFormatter()
        test_message = '<cyan>test</cyan> message <red>with</red> <green>colors</green>'
        formatter.set_colored(True)

        formatted_message = formatter.apply_colors_to_message(test_message)

        self.assertEqual(formatted_message, '\033[36mtest\033[0m message \033[31mwith\033[0m \033[32mcolors\033[0m')

    def test_apply_colors_to_message_not_colored(self):
        formatter = MLCPLogFormatter()
        test_message = '<cyan>test</cyan> message <red>with</red> <green>colors</green>'
        formatter.set_colored(False)

        formatted_message = formatter.apply_colors_to_message(test_message)

        self.assertEqual(formatted_message, 'test message with colors')

    def test_apply_styling_to_message_styled(self):
        formatter = MLCPLogFormatter()
        test_message = '<bold>test</bold> message <underline>with</underline> <blink>styles</blink>'
        formatter.set_styled(True)

        formatted_message = formatter.apply_styling_to_message(test_message)

        self.assertEqual(formatted_message, '\033[1mtest\033[0m message \033[4mwith\033[0m \033[5mstyles\033[0m')

    def test_apply_styling_to_message_not_styled(self):
        formatter = MLCPLogFormatter()
        test_message = '<bold>test</bold> message <underline>with</underline> <blink>styles</blink>'
        formatter.set_styled(False)

        formatted_message = formatter.apply_styling_to_message(test_message)

        self.assertEqual(formatted_message, 'test message with styles')
