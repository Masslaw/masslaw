import unittest
from abc import ABCMeta
from unittest.mock import MagicMock
from unittest.mock import call
from unittest.mock import patch

from execution_layer.actions._application_action import ApplicationAction
from execution_layer.actions._exceptions import ApplicationActionExecutionException
from execution_layer.actions._exceptions import ApplicationActionRequiredParamMissingException


class TestClassApplicationAction(unittest.TestCase):

    def setUp(self):
        self.action_name = 'name'
        self.params = {'param': 'value'}
        self.action = ApplicationAction(self.action_name, self.params)

    def test_init(self):
        self.assertEqual(self.action._action_name, self.action_name)
        self.assertEqual(self.action._params, self.params)

    @patch('execution_layer.actions._application_action.ApplicationAction._ApplicationAction__perform_execution')
    def test_call(self, mock_perform_execution):
        self.action()
        mock_perform_execution.assert_called_once()

    @patch('execution_layer.actions._application_action.ApplicationAction._ApplicationAction__handle_arguments')
    def test_handle_arguments(self, mock_handle_arguments):
        self.action._ApplicationAction__handle_arguments()
        mock_handle_arguments.assert_called_once()

    def test_missing_required_params(self):
        action_with_required_params = ApplicationAction
        action_with_required_params._required_params = ['param']
        with self.assertRaises(ApplicationActionRequiredParamMissingException):
            broken_action = action_with_required_params('name', {})

    def test_execution_exception(self):
        with patch.object(self.action, '_ApplicationAction__perform_execution', side_effect=ApplicationActionExecutionException):
            with self.assertRaises(ApplicationActionExecutionException):
                self.action()

    def test_none_action_name(self):
        custom_action_class = ApplicationAction
        custom_action_class.__name__ = 'CUTOM_ACTION_NAME'
        action = custom_action_class(None, self.params)
        self.assertEqual(action._action_name, custom_action_class.__name__)

    def test_invalid_handle_arguments(self):
        invalid_action = ApplicationAction(self.action_name, {'wrong_param': 'value'})
        with patch.object(invalid_action, '_handle_arguments', side_effect=KeyError):
            with self.assertRaises(KeyError):
                invalid_action._ApplicationAction__handle_arguments()

    def test_perform_execution_with_various_conditions(self):
        mock_perform_execution = MagicMock(name='_ApplicationAction__perform_execution')
        self.action._ApplicationAction__perform_execution = mock_perform_execution

        mock_perform_execution.return_value = None
        self.action()
        self.assertIsNone(mock_perform_execution.return_value)

        mock_perform_execution.return_value = True
        self.action()
        self.assertTrue(mock_perform_execution.return_value)

        mock_perform_execution.return_value = {'status': 'done'}
        self.action()
        self.assertEqual(mock_perform_execution.return_value, {'status': 'done'})

    def test_multiple_calls(self):
        mock_perform_execution = MagicMock(name='_ApplicationAction__perform_execution')
        self.action._ApplicationAction__perform_execution = mock_perform_execution

        self.action()
        self.action()
        self.action()

        calls = [call(), call(), call()]
        mock_perform_execution.assert_has_calls(calls)
        self.assertEqual(mock_perform_execution.call_count, 3)

    def test_get_param(self):
        action = ApplicationAction(self.action_name, {'a': 123, 'b': {'c': 234}, 'c': {'d': 98}})

        self.assertEqual(action._get_param('a'), 123)
        self.assertEqual(action._get_param(['b', 'c']), 234)
        self.assertEqual(action._get_param(['c', 'd']), 98)
        self.assertEqual(action._get_param(['c', 'd', 'e']), None)
        self.assertEqual(action._get_param(['c', 'd', 'e'], 123), 123)
