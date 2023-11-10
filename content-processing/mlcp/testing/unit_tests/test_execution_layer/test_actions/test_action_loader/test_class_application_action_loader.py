import unittest
from unittest.mock import MagicMock
from unittest.mock import create_autospec
from unittest.mock import patch

from execution_layer.actions import ApplicationActionLoader
from execution_layer.actions._application_action import ApplicationAction
from execution_layer.actions._exceptions import ApplicationActionImplementationNotFoundException
from execution_layer.actions._exceptions import ApplicationActionLoadingException


class TestClassApplicationActionLoader(unittest.TestCase):

    def setUp(self):
        self.loader_name = 'test_action'
        self.loader_params = {'key': 'value'}
        self.loader = ApplicationActionLoader(self.loader_name, self.loader_params)

    def test_initial_conditions(self):
        self.assertEqual(self.loader.get_name(), self.loader_name)
        self.assertFalse(self.loader.is_required())

    def test_setters_and_getters(self):
        self.loader.set_name('new_name')
        self.assertEqual(self.loader.get_name(), 'new_name')

        self.loader.set_required(True)
        self.assertTrue(self.loader.is_required())

    @patch('importlib.import_module')
    def test_execute_with_loading_exception(self, import_module_mock):
        import_module_mock.side_effect = ImportError('Module not found')

        self.loader.set_name('NonExistentAction')
        with self.assertRaises(ApplicationActionLoadingException):
            self.loader.execute()

        import_module_mock.assert_called_once()

    @patch('importlib.import_module')
    def test_execute_with_implementation_not_found_exception(self, import_module_mock):
        mock_module = MagicMock()
        mock_module._ApplicationAction__dict__ = {}
        import_module_mock.return_value = mock_module

        self.loader.set_name('NoValidActionClassesHere')
        with self.assertRaises(ApplicationActionImplementationNotFoundException):
            self.loader.execute()

        import_module_mock.assert_called_once()
