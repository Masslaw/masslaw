import boto3
from botocore.exceptions import ClientError
from get_case_data.modules.dictionary_utils import dictionary_utils

client = boto3.client('cognito-idp')


class CognitoUserPoolManager:
    def __init__(self, user_pool_name: str):
        self.user_pool_name = user_pool_name
        self.user_pool_id = self.get_user_pool_id()

    def get_user_pool_id(self):
        response = client.list_user_pools(MaxResults=60)
        user_pools = response['UserPools']
        for user_pool in user_pools:
            if user_pool['Name'] == self.user_pool_name:
                return user_pool['Id']
        raise ValueError(f'User pool {self.user_pool_name} not found')

    def get_user_by_access_token(self, access_token):
        user_id = self.get_user_id_by_access_token(access_token)
        if user_id is None: return {}
        return self.get_user_by_id(user_id)

    def get_user_id_by_access_token(self, access_token):
        try:
            response = client.get_user(
                AccessToken=access_token,
            )
            return response['Username']
        except ClientError as e:
            return None

    def get_user_by_id(self, user_id):
        try:
            response = client.admin_get_user(
                Username=user_id,
                UserPoolId=self.user_pool_id,
            )
            user_data = self.__parse_get_user_response(response)
            user_data = dictionary_utils.ensure_dict(user_data)
            return user_data
        except ClientError as e:
            return None

    def get_user_by_email(self, email):
        response = client.list_users(
            UserPoolId=self.user_pool_id,
            Filter=f"email = \"{email}\""
        )
        if len(response['Users']) == 0:
            raise ValueError(f"User with email {email} not found")
        user_data = self.__parse_get_user_response(response['Users'][0])
        return user_data

    def check_user_verified(self, user_name):
        try:
            response = client.admin_get_user(
                Username=user_name,
                UserPoolId=self.user_pool_id,
            )
            return 'UserStatus' in response and response['UserStatus'] == 'CONFIRMED'
        except ClientError as e:
            return False

    def update_user_data(self, user_id, new_data):
        dictionary_utils.ensure_flat(new_data)
        attributes = self.__format_user_data_for_write(new_data)
        response = client.admin_update_user_attributes(
            UserPoolId=self.user_pool_id,
            Username=user_id,
            UserAttributes=attributes,
        )
        return response['ResponseMetadata']['HTTPStatusCode'] == 200

    def delete_user(self, user_id):
        response = client.admin_delete_user(
            UserPoolId=self.user_pool_id,
            Username=user_id
        )
        return response

    def list_users(self):
        response = client.list_users(
            UserPoolId=self.user_pool_id,
            AttributesToGet=[
                'email'
            ]
        )
        users = [user['Attributes'][0]['Value'] for user in response['Users']]
        return users

    def __parse_get_user_response(self, response):
        user_data = {}
        user_data['User_ID'] = response['Username']
        for d in response['UserAttributes']:
            user_data[d['Name'].replace('custom:', '')] = d['Value']
        return user_data

    def __format_user_data_for_write(self, user_data):
        pool_writeable_attributes = self.__get_pool_writeable_attributes()
        attributes = []
        for key, value in user_data.items():
            if key not in pool_writeable_attributes and (key := f'custom:{key}') not in pool_writeable_attributes:
                continue
            attributes.append({'Name': key, 'Value': value})
        return attributes

    def __get_pool_attributes(self):
        attributes = self.__get_pool_attributes_data()
        return [attribute['Name'] for attribute in attributes]

    def __get_pool_writeable_attributes(self):
        attributes = self.__get_pool_attributes_data()
        writable_attributes = []
        for attribute in attributes:
            if attribute.get('Mutable', False):
                writable_attributes.append(attribute['Name'])
        return writable_attributes

    def __get_pool_attributes_data(self):
        describe_user_pool_response = client.describe_user_pool(UserPoolId=self.user_pool_id)
        attributes = describe_user_pool_response['UserPool']['SchemaAttributes']
        return attributes
