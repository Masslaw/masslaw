import unittest
from unittest.mock import MagicMock
from unittest.mock import patch, mock_open
import os
import json

from interface_layer.application._application_execution import ApplicationExecution
from interface_layer.application._exceptions import MLCPProcessConfigurationNotFoundException
from interface_layer.application._exceptions import MLCPRequiredProcessActionExecutionFailedException


class TestClassApplicationExecution(unittest.TestCase):

    @patch('os.environ.get')
    def test_load_stage(self, mock_env_get):
        mock_env_get.return_value = 'dev'
        app_exec = ApplicationExecution()
        app_exec._ApplicationExecution__load_stage()
        self.assertEqual(app_exec._ApplicationExecution__stage, 'dev')

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({"key": "value"}))
    @patch('shared_layer.file_system_utils.file_system_utils.is_file')
    def test_load_process_configuration_from_file_success(self, mock_is_file, mock_file):
        mock_is_file.return_value = True
        app_exec = ApplicationExecution()
        result = app_exec._ApplicationExecution__load_process_configuration_from_file()
        self.assertTrue(result)

    @patch('os.environ')
    def test_load_process_configuration_from_env_not_found(self, mock_env):
        mock_env.get.return_value = None
        app_exec = ApplicationExecution()
        with self.assertRaises(MLCPProcessConfigurationNotFoundException):
            app_exec._ApplicationExecution__load_process_configuration()

    @patch('execution_layer.actions.ApplicationActionLoader.execute')
    def test_execute_actions_success(self, mock_execute):
        mock_execute.return_value = True

        app_exec = ApplicationExecution()
        app_exec._ApplicationExecution__process_actions = [MagicMock(name="MockAction")]

        try:
            app_exec._ApplicationExecution__perform_main_execution()
        except Exception as e:
            self.fail(f"__execute_actions() raised {type(e).__name__} unexpectedly!")

    @patch('execution_layer.actions.ApplicationActionLoader.execute')
    def test_execute_actions_with_required_failure(self, mock_execute):
        mock_execute.return_value = False

        app_exec = ApplicationExecution()
        mock_action = MagicMock(name="MockAction")
        mock_action.is_required.return_value = True
        mock_action.execute.return_value = False
        app_exec._ApplicationExecution__process_actions = [mock_action]

        app_exec._ApplicationExecution__perform_main_execution()

        self.assertFalse(app_exec._ApplicationExecution__process_execution_result)

    @patch('execution_layer.actions.ApplicationActionLoader.execute')
    def test_execute_actions_with_required_exception(self, mock_execute):
        mock_execute.return_value = False

        app_exec = ApplicationExecution()
        mock_action = MagicMock(name="MockAction")
        mock_action.is_required.return_value = True
        def raise_exception(): raise Exception()
        mock_action.execute.side_effect = raise_exception
        app_exec._ApplicationExecution__process_actions = [mock_action]

        app_exec._ApplicationExecution__perform_main_execution()

        self.assertFalse(app_exec._ApplicationExecution__process_execution_result)

    @patch('execution_layer.actions.ApplicationActionLoader.execute')
    def test_execute_actions_with_non_required_failure(self, mock_execute):
        mock_execute.return_value = False

        app_exec = ApplicationExecution()
        mock_action = MagicMock(name="MockAction")
        mock_action.is_required.return_value = False
        mock_action.execute.return_value = False
        app_exec._ApplicationExecution__process_actions = [mock_action]

        app_exec._ApplicationExecution__perform_main_execution()

        self.assertTrue(app_exec._ApplicationExecution__process_execution_result)


    @patch('execution_layer.actions.ApplicationActionLoader.execute')
    def test_execute_actions_with_non_required_exception(self, mock_execute):
        mock_execute.return_value = False

        app_exec = ApplicationExecution()
        mock_action = MagicMock(name="MockAction")
        def raise_exception(): raise Exception()
        mock_action.is_required.return_value = False
        mock_action.execute.side_effect = raise_exception
        app_exec._ApplicationExecution__process_actions = [mock_action]

        app_exec._ApplicationExecution__perform_main_execution()

        self.assertTrue(app_exec._ApplicationExecution__process_execution_result)

    def test_execution_result_after_required_action_failed(self):
        app_exec = ApplicationExecution()

        app_exec._ApplicationExecution__on_required_action_execution_failed(action_name="TestAction")

        self.assertFalse(app_exec._ApplicationExecution__process_execution_result)
