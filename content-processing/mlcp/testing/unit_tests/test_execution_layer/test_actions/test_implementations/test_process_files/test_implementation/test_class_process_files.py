import unittest
from unittest.mock import Mock
from unittest.mock import patch

from execution_layer.actions._exceptions import ApplicationActionRequiredParamMissingException
from execution_layer.actions._implementations.process_files import ProcessFiles


class TestClassProcessFiles(unittest.TestCase):

    def test_init_with_required_params(self):
        action = ProcessFiles(params={_key: 'value' for _key in ProcessFiles._required_params})

    def test_init_with_missing_required_params(self):
        with self.assertRaises(ApplicationActionRequiredParamMissingException):
            action = ProcessFiles()

    def test_handle_arguments(self):
        action = ProcessFiles(params={'files_data': ['some_file_data']})
        action._handle_arguments()
        self.assertEqual(action._files_data, ['some_file_data'])

    @patch('execution_layer.actions._implementations.process_files._implementation.create_processor')
    def test_execution(self, mock_create_processor):

        mock_processor = Mock()
        mock_create_processor.return_value = mock_processor

        action = ProcessFiles(params={'files_data': [{'file_name': 'file1', 'languages': ['eng', 'heb']}, {'file_name': 'file2', 'languages': ['eng']}]})
        action._handle_arguments()
        action._execute()

        mock_create_processor.assert_any_call('file1', ['eng', 'heb'])
        mock_create_processor.assert_any_call('file2', ['eng'])

        mock_processor.process.assert_any_call()
        mock_processor.export_text.assert_any_call('extracted_text')
        mock_processor.export_metadata.assert_any_call('file_metadata')
        mock_processor.export_assets.assert_any_call('actioned_assets')
