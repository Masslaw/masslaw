from execution_layer.actions._application_action import ApplicationAction
from logic_layer.remote_storage.s3_bucket_storage_manager import S3BucketStorageManager
from shared_layer.mlcp_logger import logger
from shared_layer.mlcp_logger import common_formats


class S3Download(ApplicationAction):
    _required_params = ['bucket', 'files_data']

    _bucket_name = None
    _files_data = None

    def _handle_arguments(self):
        self._bucket_name = self._get_param('bucket')
        self._files_data = self._get_param('files_data')
        self._bucket_manager = S3BucketStorageManager(bucket_name=self._bucket_name)

    def _execute(self):
        logger.debug(f'Downloading {common_formats.value(len(self._files_data))} files from s3')
        for file_data in self._files_data:
            self.__handle_download_file_data(file_data)

    @logger.process_function('Downloading file')
    def __handle_download_file_data(self, file_data):
        file_key = file_data.get('key')
        save_as = file_data.get('save_as')
        if (not file_key) or (not save_as):
            self._abort_execution(common_formats.important('File data is missing file_key and save_as'))
        logger.debug(f'Downloading file with key: "{common_formats.value(file_key)}" to: "{common_formats.value(save_as)}"')
        self._bucket_manager.get_file_from_bucket(file_key=file_key, save_as=save_as)
