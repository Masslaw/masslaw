import os
import unittest
from datetime import datetime

from mlcp.testing.content.content_management import content_management
from mlcp.testing.mlcp_job_tests._mlcp_job_test import MLCPJobTest
from mlcp.testing.stubs.s3_stub import S3StubTestLoader
from shared_layer.file_system_utils._file_system_utils import clear_directory
from shared_layer.file_system_utils._file_system_utils import join_paths

file_name = "A-Very-Short-Story.pdf"

bucket_name = "mlcp-test-bucket"

languages = ["eng"]

case_id = 'aH7CFNTa9stf7n8anF78anADV324gnoF'

file_id = 'ajva0SF08m8sFM09HM809fmh0CM0fhm0asF8'

parent_output_directory = 'output/text_extraction_job'


class MLCPTextExtractionJobTest(unittest.TestCase, MLCPJobTest):

    @classmethod
    def setUpClass(cls):
        cls.test_output_directory = join_paths(parent_output_directory, file_name)
        clear_directory(cls.test_output_directory)
        test_time = datetime.now()
        cls.s3_stub = S3StubTestLoader()
        with open(join_paths(cls.test_output_directory, f'{test_time}'), 'w') as file: file.write('')

    def setUp(self):
        self._open_temporary_storage()
        self.s3_stub.start_s3_stub()
        self.s3_stub.create_client()
        self.s3_stub.create_bucket(bucket_name)
        self._upload_mock_file()
        self._load_mlcp_process_configuration()
        self._set_stage("test")

    def tearDown(self):
        self.s3_stub.stop_s3_stub()
        self._close_temporary_storage()

    def _upload_mock_file(self):
        self.test_file = content_management.get_file_path("processable_files", file_name)
        self.s3_stub.upload_file(bucket_name, self.test_file, file_name)

    def _load_mlcp_process_configuration(self):
        self._set_mlcp_process_configuration({
            'actions': [{
                "name": "s3_download", "params": {
                    "bucket": bucket_name, "files_data": [{
                        "key": file_name, "save_as": self.in_temporary_storage(file_name)
                    }]
                }, "required": "True"
            }, {
                "name": "process_files", "params": {
                    "files_data": [{
                        "file_name": self.in_temporary_storage(file_name),
                        "languages": languages,
                        "case_id": case_id,
                        "file_id": file_id,
                        "file_metadata_output_dir": os.path.join(self.test_output_directory, "file_metadata"),
                        "extracted_text_output_dir": os.path.join(self.test_output_directory, "extracted_text"),
                        "assets_output_dir": os.path.join(self.test_output_directory, "processed_assets"),
                        "debug_data_dir": os.path.join(self.test_output_directory, "debug_data"),
                        "converted_file_output_dir": os.path.join(self.test_output_directory, "converted_files"),
                    }]
                }, "required": "True"
            }, {
                "name": "s3_upload", "params": {
                    "bucket": bucket_name, "files_data": [{
                        "key": f"{file_id}/client_exposed/extracted_text", "saved_as": os.path.join(self.test_output_directory, "extracted_text")
                    }, {
                        "key": f"{file_id}/client_exposed/processed_assets", "saved_as": os.path.join(self.test_output_directory, "processed_assets")
                    }]
                }, "required": "True"
            }]
        })
