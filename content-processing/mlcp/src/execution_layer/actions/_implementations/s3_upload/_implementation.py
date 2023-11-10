from execution_layer.actions._application_action import ApplicationAction
from logic_layer.remote_storage.s3_bucket_storage_manager import S3BucketStorageManager
from shared_layer.file_system_utils import file_system_utils
from shared_layer.mlcp_logger import logger
from shared_layer.mlcp_logger import common_formats


class S3Upload(ApplicationAction):
    _required_params = ['bucket', 'files_data']

    _bucket_name = None
    _files_data = None

    def _handle_arguments(self):
        self._bucket_name = self._get_param('bucket')
        self._files_data = self._get_param('files_data')
        self._bucket_manager = S3BucketStorageManager(bucket_name=self._bucket_name)

    def _execute(self):
        logger.info(f'Uploading {common_formats.value(len(self._files_data))} files to s3')
        total_res = True
        for file_data in self._files_data:
            res = self.__handle_upload_file_data(file_data)
            total_res = total_res and res

    @logger.process_function('Uploading file')
    def __handle_upload_file_data(self, file_data):
        file_key = file_data.get('key')
        saved_as = file_data.get('saved_as', file_key)
        logger.info(f'Uploading file "{common_formats.value(saved_as)}" to bucket: "{common_formats.value(self._bucket_name)}" with key: "{common_formats.value(file_key)}"')
        local_directory = file_system_utils.get_local_directory()
        file_to_upload_location = file_system_utils.join_paths(local_directory, saved_as)
        if not file_system_utils.is_dir(file_to_upload_location) and not file_system_utils.is_file(file_to_upload_location):
            self._abort_execution(f'File: {saved_as} does not exist')
        self._bucket_manager.save_file_to_bucket(file_key=file_key, saved_as=file_to_upload_location)
