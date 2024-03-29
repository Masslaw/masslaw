from src.modules.aws_clients.s3_client import S3BucketManager
from src.modules.images import ImageManipulator
from src.modules.lambda_handler_template_http_invoked_authenticated_masslaw_user import AuthenticatedMasslawUserHttpInvokedLambdaFunction
from src.modules.masslaw_users_config import user_statuses


profile_pictures_bucket_manager = S3BucketManager('masslaw-profile-pictures')


class SetProfilePicture(AuthenticatedMasslawUserHttpInvokedLambdaFunction):

    def __init__(self):
        AuthenticatedMasslawUserHttpInvokedLambdaFunction.__init__(self, request_body_structure={'image_data': [str]}, minimum_user_status_level=user_statuses.UserStatuses.LOGGED_IN, )
        self.__image_data = ''

    def _reset_state(self):
        AuthenticatedMasslawUserHttpInvokedLambdaFunction._reset_state(self)
        self.__image_data = ''

    def _load_request_body(self):
        AuthenticatedMasslawUserHttpInvokedLambdaFunction._load_request_body(self)
        self.__image_data = self._request_body.get('image_data', {})

    def _execute(self):
        AuthenticatedMasslawUserHttpInvokedLambdaFunction._execute(self)
        large_image_data = self._generate_large_image_data()
        small_image_data = self._generate_small_image_data()
        self._log('large image data size: ' + str(len(large_image_data)))
        self._log('small image data size: ' + str(len(small_image_data)))
        user_id = self._caller_user_instance.get_user_id()
        profile_pictures_bucket_manager.put_object(f'{user_id}/large.jpg', large_image_data)
        profile_pictures_bucket_manager.put_object(f'{user_id}/small.jpg', small_image_data)

    def _generate_large_image_data(self) -> bytes:
        image_manipulator = ImageManipulator()
        image_manipulator.from_base64(self.__image_data)
        image_manipulator.resize_height(720)
        image_data = image_manipulator.to_jpeg_format(quality=85)
        return image_data

    def _generate_small_image_data(self) -> bytes:
        image_manipulator = ImageManipulator()
        image_manipulator.from_base64(self.__image_data)
        image_manipulator.resize_height(128)
        image_data = image_manipulator.to_jpeg_format(quality=50)
        return image_data


def handler(event, context):
    handler_instance = SetProfilePicture()
    handler_instance.call_handler(event, context)
    return handler_instance.get_response()
