import secrets
import time

from src.modules.aws_clients.open_search_client import OpenSearchIndexManager
from src.modules.aws_clients.s3_client import S3BucketManager
from src.modules.aws_clients.step_functions_client import StateMachineManager
from src.modules.masslaw_case_storage_management._exceptions import MasslawFileTypeNotSupportedException
from src.modules.masslaw_case_users_management import MasslawCaseUserAccessManager
from src.modules.masslaw_cases_config import opensearch_config
from src.modules.masslaw_cases_config import security_config
from src.modules.masslaw_cases_config import storage_config
from src.modules.masslaw_cases_objects import MasslawCaseFileInstance
from src.modules.masslaw_cases_objects import MasslawCaseInstance
from src.modules.masslaw_cloud_configurations import get_configuration_value
from src.modules.remote_data_management_dynamodb import DynamodbDataHolder


class MasslawCaseStorageManager:

    def __init__(self, case_instance: MasslawCaseInstance):
        self.__case_instance = case_instance

        self.__case_user_access_manager = MasslawCaseUserAccessManager(self.__case_instance)

    def get_case_file_download_url(self, user_id, file_id, content_path):
        file_data = DynamodbDataHolder("MasslawFiles", file_id)

        bucket_manager = S3BucketManager(storage_config.CASES_CONTENT_BUCKET_ID)

        access_files = self.__case_user_access_manager.get_user_access_files(user_id=user_id)
        if access_files:
            if file_id not in access_files:
                return None

        if not file_data:
            return None

        file_key = bucket_manager.get_key_for_unknown_type(f'{file_id}/client_exposed/{content_path}')
        if not file_key: return ''
        url = bucket_manager.get_object_presigned_url(file_key, security_config.FILE_DOWNLOAD_URL_EXPIRATION_SECONDS)

        return url

    def start_uploading_file(self, user_id, file_name, num_parts, file_languages):
        if not self.__case_user_access_manager.determine_can_upload_file(user_id):
            return False

        bucket_manager = S3BucketManager(storage_config.CASES_CONTENT_BUCKET_ID)

        file_type = file_name.split('.').pop()
        file_id = secrets.token_hex(16)
        file_key = f'{file_id}/raw.{file_type}'
        mp_upload_data = bucket_manager.start_multipart_upload(file_key, num_parts)
        mp_upload_data['file_id'] = file_id

        self.assert_file_type_supported(file_type)

        uploading_files = self.__case_instance.get_data_property(['uploading_files'], [])
        uploading_files.append(file_id)
        self.__case_instance.set_data_property(['uploading_files'], uploading_files)

        file_instance = MasslawCaseFileInstance(file_id)
        file_instance.update_data({'name': file_name, 'type': file_type, 'languages': file_languages, 'upload_id': mp_upload_data['upload_id'], 'case_id': self.__case_instance.get_case_id(), })
        file_instance.save_data()

        return mp_upload_data

    def complete_uploading_file(self, user_id, file_id, parts_list):
        if not self.__case_user_access_manager.determine_can_upload_file(user_id):
            return False

        file_instance = MasslawCaseFileInstance(file_id)

        bucket_manager = S3BucketManager(storage_config.CASES_CONTENT_BUCKET_ID)

        file_type = file_instance.get_data_property(['type'])
        file_s3_key = f'{file_id}/raw.{file_type}'
        upload_id = file_instance.get_data_property(['upload_id'])
        bucket_manager.complete_multipart_upload(file_s3_key, parts_list, upload_id)

        self.assert_file_type_supported(file_type)

        now = str(int(time.time()))
        file_instance.set_data_property(['upload_time'], now)
        file_instance.set_data_property(['last_modified'], now)

        uploading_files = self.__case_instance.get_data_property(['uploading_files'], [])
        uploading_files.remove(file_id)
        self.__case_instance.set_data_property(['uploading_files'], uploading_files)

        case_files = self.__case_instance.get_data_property(['files'], [])
        case_files.append(file_id)
        self.__case_instance.set_data_property(['files'], case_files)

        file_instance.save_data()

        return file_instance

    def delete_file_as_user(self, file_id, user_id):
        user_permitted_files = self.__case_user_access_manager.get_user_access_files(user_id=user_id)
        if not file_id in user_permitted_files:
            return False
        return self.delete_file(file_id)

    def delete_file(self, file_id):
        # bucket_manager = S3BucketManager(CASES_CONTENT_BUCKET_ID)
        # bucket_manager.delete_folder(f"{file_id}") -- we'll keep the files in our storage for now

        case_files = self.__case_instance.get_data_property(['files'], [])
        if file_id in case_files:
            case_files.remove(file_id)
            self.__case_instance.set_data_property(['files'], case_files)
        uploading_files = self.__case_instance.get_data_property(['uploading_files'], [])
        if file_id in uploading_files:
            uploading_files.remove(file_id)
            self.__case_instance.set_data_property(['uploading_files'], uploading_files)

        open_search_index_name = f'{self.__case_instance.get_case_id()}{opensearch_config.MASSLAW_CASE_FILES_SEARCH_INDEX_SUFFIX}'
        case_search_index_manager = OpenSearchIndexManager(opensearch_config.MASSLAW_CASES_ES_ENDPOINT, open_search_index_name)
        case_search_index_manager.remove_document(file_id)

        return True

    def start_case_file_processing_pipeline(self, file_instance: MasslawCaseFileInstance, stage='prod'):
        pipeline_state_machine_manger = StateMachineManager(f"masslaw-case-file-main-processing-pipeline-{stage}")
        pipeline_state_machine_manger.start_execution({"file_id": file_instance.get_file_id(), "stage": stage})

    def assert_file_type_supported(self, file_type):
        supported_file_types = list(get_configuration_value(key=storage_config.SUPPORTED_MLCP_FILE_TYPES))
        if not file_type in supported_file_types:
            raise MasslawFileTypeNotSupportedException("The provided file is not supported in masslaw services")
